"""杠杆指数模拟核心(纯函数,被回测+paper腿共用)。见 spec 2026-07-07-leverage-index-leg。"""
import numpy as np


def simulate_leverage(prices, base_lev=1.5, ma_window=200, vol_window=20,
                      vol_cap=0.30, rebal_tol=0.2, borrow_annual=0.06,
                      confirm_days=5, start=2000.0):
    """prices: pandas Series 日线收盘(日期升序索引)。
    规则:价>200MA **连续confirm_days天** 且 波动不高 → base_lev,否则1x(前一日信号,防前视)。
    confirm_days=1=只要当日在线上(原始行为);>1=跌破后要连站N天才重新加杠(防whipsaw假反弹被割)。
    降杠即时(下跌快躲)、加杠要确认(上涨慢追)。融资按(L-1)扣;再平衡偏离>rebal_tol才重置。
    返回 dict: curve=[(date,equity,lev)], cagr, maxdd, final, ruined, days。"""
    px = prices.dropna()
    ret = px.pct_change()
    ma = px.rolling(ma_window).mean()
    vol = ret.rolling(vol_window).std() * np.sqrt(252)
    # 连续站上200MA的天数(跌破归零)——加杠确认用
    streak = []; s = 0
    for pi, mi in zip(px.values, ma.values):
        s = s + 1 if (mi == mi and pi > mi) else 0
        streak.append(s)
    borrow_daily = borrow_annual / 252.0
    idx = list(px.index)
    equity = start; peak = start; maxdd = 0.0; ruined = False; actual = None
    curve = []
    need = max(confirm_days, 1)
    for i in range(1, len(idx)):
        v = vol.iloc[i - 1]                                    # 前一日信号
        above = streak[i - 1] >= need                         # 连续站线上need天才算加杠信号
        highv = (v == v) and (v > vol_cap)
        target = base_lev if (above and not highv) else 1.0
        if actual is None or abs(actual - target) > rebal_tol:  # 再平衡带宽
            actual = target
        r = ret.iloc[i]
        daily = actual * r - max(actual - 1.0, 0.0) * borrow_daily
        equity *= (1 + daily)
        if equity <= 0:
            equity = 0.0; ruined = True
            curve.append((str(idx[i].date()), 0.0, round(actual, 3))); break
        actual = actual * (1 + r) / (1 + daily)                 # 价格变动后杠杆漂移
        peak = max(peak, equity); maxdd = max(maxdd, (peak - equity) / peak)
        curve.append((str(idx[i].date()), round(equity, 2), round(actual, 3)))
    yrs = len(curve) / 252.0 if curve else 1.0
    cagr = (equity / start) ** (1 / yrs) - 1 if (equity > 0 and yrs > 0) else -1.0
    return {"curve": curve, "cagr": cagr, "maxdd": maxdd,
            "final": equity, "ruined": ruined, "days": len(curve)}
