import sys, os, tempfile
from datetime import date, datetime, timedelta
from pathlib import Path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))
import pandas as pd
from scripts.market_intel.snapshot import complete_bars, should_run, qqq_section


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


if __name__ == "__main__":
    for n, f in list(globals().items()):
        if n.startswith("test_"): f(); print(f"  ok {n}")
    print("ALL PASS")
