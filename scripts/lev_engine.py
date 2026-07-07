"""杠杆指数模拟核心(纯函数,被回测+paper腿共用)。见 spec 2026-07-07-leverage-index-leg。"""
import numpy as np


def simulate_leverage(prices, base_lev=1.5, ma_window=200, vol_window=20,
                      vol_cap=0.30, rebal_tol=0.2, borrow_annual=0.06, start=2000.0):
    """prices: pandas Series 日线收盘(日期升序索引)。
    规则:>200MA且波动不高→base_lev,否则1x(前一日信号,防前视)。融资成本按(L-1)扣。
    再平衡:实际杠杆偏离目标>rebal_tol(=0.2,即1.5x的[1.3,1.7]带)才重置。
    返回 dict: curve=[(date,equity,lev)], cagr, maxdd, final, ruined, days。"""
    px = prices.dropna()
    ret = px.pct_change()
    ma = px.rolling(ma_window).mean()
    vol = ret.rolling(vol_window).std() * np.sqrt(252)
    borrow_daily = borrow_annual / 252.0
    idx = list(px.index)
    equity = start; peak = start; maxdd = 0.0; ruined = False; actual = None
    curve = []
    for i in range(1, len(idx)):
        m = ma.iloc[i - 1]; v = vol.iloc[i - 1]                 # 前一日信号
        above = (m == m) and (px.iloc[i - 1] > m)              # NaN-safe
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
