"""对账:目标股数 vs 实际股数 → 差额订单。补差/清掉榜/持平不动。"""

def diff_orders(target_sh, actual_sh, tol=0.01):
    out = []
    for sym in sorted(set(target_sh) | set(actual_sh)):
        diff = round(target_sh.get(sym, 0) - actual_sh.get(sym, 0), 6)
        if abs(diff) < tol:
            continue
        out.append({"sym": sym, "qty": diff})
    return out
