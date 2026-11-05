import sys, os, tempfile
from datetime import date, datetime, timedelta
from pathlib import Path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))
import pandas as pd
from scripts.market_intel.snapshot import (complete_bars, should_run, qqq_section, select_movers,
                                           enrich_mover, build_snapshot, need_fundamentals)
from scripts.market_intel.config import paths


def _bars(n, end="2026-11-05", growth=1.001):
    idx = pd.bdate_range(end=end, periods=n)
    c = pd.Series([100.0 * growth ** i for i in range(n)], index=idx)
    return pd.DataFrame({"close": c, "high": c * 1.005, "low": c * 0.995, "volume": 1000.0})


def test_qqq_section_basic():
    df = _bars(300)
    q = qqq_section(df, "ibkr", None)
    close = float(df["close"].iloc[-1])
    assert q["source"] == "ibkr" and q["date"] == "2026-11-05"
    assert abs(q["close"] - round(close, 2)) < 1e-9
    assert q["gate"]["target"] == 1.5                      # 稳升+低波动 → 1.5x
    assert q["backstop"] == 648.43
    assert q["backstop_dist_pct"] == round((close / 648.43 - 1) * 100, 2)
    assert q["xcheck"]["status"] == "single_source" and q["xcheck"]["other_close"] is None
    assert abs(q["ma200"] - round(float(df["close"].iloc[-200:].mean()), 2)) < 1e-9
    assert abs(q["high_52w"] - round(float(df["high"].iloc[-252:].max()), 2)) < 1e-9


def test_xcheck_ok_and_mismatch():
    df = _bars(300)
    ok = df.copy(); ok.loc[ok.index[-1], "close"] *= 1.001
    bad = df.copy(); bad.loc[bad.index[-1], "close"] *= 1.005
    assert qqq_section(df, "ibkr", ok)["xcheck"]["status"] == "ok"
    x = qqq_section(df, "ibkr", bad)["xcheck"]
    assert x["status"] == "mismatch" and x["diff_pct"] == 0.5


def test_xcheck_date_missing_is_single_source():
    # yfinance 偶尔晚一天:第二源没有同一天的收盘 → 不能拿前一天的价去比
    df = _bars(300)
    lag = df.iloc[:-1]
    assert qqq_section(df, "ibkr", lag)["xcheck"]["status"] == "single_source"


def test_too_short_raises():
    try:
        qqq_section(_bars(150), "ibkr", None)
    except ValueError:
        return
    raise AssertionError("150 根 K 线应抛 ValueError")


def test_complete_bars_drops_partial():
    df = _bars(30, end="2026-11-05")
    midday = datetime(2026, 11, 5, 11, 0)
    after = datetime(2026, 11, 5, 17, 0)
    assert len(complete_bars(df, midday)) == 29            # 盘中:当天半根K线丢掉
    assert len(complete_bars(df, after)) == 30             # 收盘后:保留
    assert len(complete_bars(df, datetime(2026, 11, 6, 11, 0))) == 30   # 次日盘中:昨天那根是完整的


def test_should_run():
    d = date(2026, 11, 5)
    assert should_run(d, None) is True
    assert should_run(d, d) is False                       # 休市日/重复运行:没有新K线
    assert should_run(d, d - timedelta(days=1)) is True


def test_select_movers():
    rows = [{"symbol": "AAA", "scan": "TOP_PERC_GAIN", "rank": 0},
            {"symbol": "BBB", "scan": "TOP_PERC_GAIN", "rank": 1},
            {"symbol": "SPY", "scan": "TOP_PERC_GAIN", "rank": 2},
            {"symbol": "AAA", "scan": "HOT_BY_VOLUME", "rank": 3},
            {"symbol": "CCC", "scan": "TOP_PERC_LOSE", "rank": 4}]
    m = select_movers(rows, {"AAA": False, "BBB": False, "SPY": True, "CCC": False}, 2)
    assert [x["symbol"] for x in m] == ["AAA", "BBB"]
    assert m[0]["scans"] == ["TOP_PERC_GAIN", "HOT_BY_VOLUME"] and m[0]["rank"] == 0
    assert "SPY" not in [x["symbol"] for x in select_movers(rows, {"SPY": True}, 10)]   # ETF 剔除


def test_enrich_mover():
    idx = pd.bdate_range(end="2026-11-05", periods=22)
    close = [100.0] * 21 + [105.0]
    vol = [100.0] * 21 + [300.0]
    e = enrich_mover(pd.DataFrame({"close": close, "high": close, "low": close, "volume": vol}, index=idx))
    assert e == {"close": 105.0, "chg_pct": 5.0, "vol_ratio": 3.0}


def test_build_snapshot_gateway_offline():
    p = paths(Path(tempfile.mkdtemp()))
    snap = build_snapshot(datetime(2026, 11, 5, 17, 0), None, None, p=p,
                          fetch_yf=lambda sym: _bars(300))
    assert snap["session_date"] == "2026-11-05" and snap["mode"] == "full"
    assert snap["qqq"]["source"] == "yfinance"
    assert snap["qqq"]["xcheck"]["status"] == "single_source"
    assert snap["account"] == {"missing": "网关离线"}
    assert snap["movers"] == []
    assert any("网关离线" in s for s in snap["data_issues"])
    assert snap["run_fundamentals"] is True                 # 还没有任何基本面结论 → 必须跑


def test_build_snapshot_no_new_session():
    p = paths(Path(tempfile.mkdtemp()))
    assert build_snapshot(datetime(2026, 11, 5, 17, 0), None, date(2026, 11, 5), p=p,
                          fetch_yf=lambda sym: _bars(300)) is None


def test_build_snapshot_both_sources_fail():
    p = paths(Path(tempfile.mkdtemp()))
    try:
        build_snapshot(datetime(2026, 11, 5, 17, 0), None, None, p=p, fetch_yf=lambda sym: None)
    except RuntimeError:
        return
    raise AssertionError("两源都没有 QQQ 应抛 RuntimeError")


def test_build_snapshot_skips_movers_when_session_stale():
    # 补跑撞上次日盘中:扫描器反映的是进行中的交易日,和快照交易日(前一天)对不上 → 异动股不取
    import scripts.market_intel.snapshot as S
    def boom(ib):
        raise AssertionError("交易日对不上时不该扫描")
    orig = (S.scan_movers, S.account_section)
    S.scan_movers, S.account_section = boom, lambda ib: {"nav": 1.0}
    try:
        p = paths(Path(tempfile.mkdtemp()))
        snap = build_snapshot(datetime(2026, 11, 5, 10, 46), object(), None, p=p,
                              fetch_yf=lambda sym: _bars(300, end="2026-11-05"),
                              fetch_ib=lambda ib, sym, duration="2 Y": _bars(300, end="2026-11-05"))
    finally:
        S.scan_movers, S.account_section = orig
    assert snap["session_date"] == "2026-11-04"           # 当天半根丢掉
    assert snap["movers"] == [] and snap["account"] == {"nav": 1.0}
    assert any("盘中" in s for s in snap["data_issues"])


def test_need_fundamentals():
    tmp = Path(tempfile.mkdtemp()); f = tmp / "fundamentals_latest.md"
    mon, thu = date(2026, 11, 2), date(2026, 11, 5)
    assert need_fundamentals(thu, f, "full", today=thu) is True        # 没有旧结论
    f.write_text("x")
    assert need_fundamentals(mon, f, "full", today=thu) is True        # 周一照跑
    assert need_fundamentals(thu, f, "full", today=thu) is False       # 平日沿用
    assert need_fundamentals(thu, f, "full", today=thu + timedelta(days=9)) is True   # 旧结论超过 8 天
    assert need_fundamentals(mon, f, "lite", today=thu) is False       # 降级模式不跑


if __name__ == "__main__":
    for n, f in list(globals().items()):
        if n.startswith("test_"): f(); print(f"  ok {n}")
    print("ALL PASS")
