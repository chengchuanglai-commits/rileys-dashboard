"""每晚市场情报 · 第一段:纯 Python 数据快照(无 AI)。
QQQ:IBKR 日线为主、yfinance 交叉验证;账户(只读);大盘股异动(IBKR 免费扫描器)。
用法: python3 -m scripts.market_intel.snapshot   退出码 0=已写快照 3=没有新交易日(跳过) 2=QQQ 两源都取不到"""
import math
from datetime import time as dtime

import pandas as pd

from scripts.lev_engine import gate_signal
from scripts.market_intel.config import BACKSTOP, XCHECK_TOL

SESSION_CLOSE = dtime(16, 15)   # 美东 16:15 前,当天那根日线视为未收盘


def complete_bars(df, now_et):
    """盘中手动运行/补跑时,IBKR 会给当天未收盘的半根K线——丢掉它。"""
    if len(df) and pd.Timestamp(df.index[-1]).date() == now_et.date() and now_et.time() < SESSION_CLOSE:
        return df.iloc[:-1]
    return df


def should_run(last_bar_date, last_done):
    """有比上次成功处理更新的交易日才跑:同时覆盖休市日、补跑、重复运行。"""
    return last_done is None or last_bar_date > last_done


def _pct(x):
    return round(float(x) * 100, 2)


def qqq_section(primary, primary_src, secondary):
    if primary is None or len(primary) < 210:
        raise ValueError(f"QQQ 日线太短({0 if primary is None else len(primary)} 根,需 ≥210)")
    c = primary["close"].astype(float)
    last = primary.index[-1]
    close = float(c.iloc[-1])
    high_52w = float(primary["high"].astype(float).iloc[-252:].max())
    vol = c.pct_change().rolling(20).std().iloc[-1] * math.sqrt(252)

    xcheck = {"status": "single_source", "other_close": None, "diff_pct": None}
    if secondary is not None and len(secondary):
        other = secondary["close"]
        hit = other[[pd.Timestamp(i).date() == pd.Timestamp(last).date() for i in other.index]]
        if len(hit):
            oc = float(hit.iloc[-1])
            diff = oc / close - 1
            xcheck = {"status": "ok" if abs(diff) <= XCHECK_TOL + 1e-12 else "mismatch",
                      "other_close": round(oc, 2), "diff_pct": _pct(diff)}

    return {
        "source": primary_src,
        "date": pd.Timestamp(last).date().isoformat(),
        "close": round(close, 2),
        "high": round(float(primary["high"].iloc[-1]), 2),
        "low": round(float(primary["low"].iloc[-1]), 2),
        "ma20": round(float(c.iloc[-20:].mean()), 2),
        "ma50": round(float(c.iloc[-50:].mean()), 2),
        "ma200": round(float(c.iloc[-200:].mean()), 2),
        "vol20_ann": _pct(vol) if vol == vol else None,      # 单位 %
        "high_52w": round(high_52w, 2),
        "dd_from_high_pct": _pct(close / high_52w - 1),
        "gate": gate_signal(c),
        "backstop": BACKSTOP,
        "backstop_dist_pct": _pct(close / BACKSTOP - 1),
        "xcheck": xcheck,
    }
