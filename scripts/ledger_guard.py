"""台账写盘守卫 —— 平仓数单调递增校验(2026-08-04 优化#2,"假恢复"事件的推广修复)。

背景:2026-08-03 网络故障期行情拉不到,hds 回填把 27 笔已平仓误标回"在手"并写盘,
残缺台账骗过 tripwire 自动开闸(gate 播报也被污染)。tripwire 已装单调守卫,
本模块把同一守卫下沉到回填写盘层,保护整条证据链(gate/edge/tripwire/dashboard)。

规则:累计平仓数只会单调增;新算出的平仓数 < 现有文件 → 拒写保留旧版 + 告警。
用法: from ledger_guard import safe_write_ledger
      if not safe_write_ledger(path, out): return   # 拒写时跳过后续衍生写盘(如dashboard js)
"""
import json, os


def safe_write_ledger(path, out):
    """平仓数不回退才写盘。返回 True=已写, False=拒写(保留旧版)。"""
    try:
        old = json.load(open(path))
        n_old = len(old.get("closed_positions", []))
    except Exception:
        n_old = 0
    n_new = len(out.get("closed_positions", []))
    if n_new < n_old:
        print(f"[ledger-guard] ⚠️ {os.path.basename(path)} 平仓数回退({n_new}<{n_old}),"
              f"疑似行情缺失,拒写保留旧版(证据链保护)")
        return False
    json.dump(out, open(path, "w"), ensure_ascii=False, indent=2)
    return True
