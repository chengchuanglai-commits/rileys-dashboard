"""IBKR 连接测试 —— 网关登录+开API后,验证能连上、读到 paper 账户、取到行情。
用法: python3 scripts/ibkr_connect_test.py
端口: 7497=TWS paper / 4002=Gateway paper(脚本两个都试)。只读,不下单。
"""
from ib_insync import IB, Stock

def try_connect():
    for port in (7497, 4002, 4001, 7496):
        ib = IB()
        try:
            ib.connect("127.0.0.1", port, clientId=99, timeout=8)
            return ib, port
        except Exception as e:
            print(f"  端口 {port}: 连不上 ({str(e)[:50]})")
    return None, None

def main():
    print("尝试连接 IB 网关…")
    ib, port = try_connect()
    if not ib:
        print("\n❌ 没连上。检查清单:")
        print("  1. IB Gateway/TWS 登录了吗(paper 账户)?")
        print("  2. 配置 → API → Settings 勾了 'Enable ActiveX and Socket Clients'?")
        print("  3. Socket port 是 7497(TWS) 或 4002(Gateway)?")
        print("  4. 'Allow connections from localhost' 勾上,127.0.0.1 在信任列表?")
        return
    print(f"\n✅ 连上了! 端口 {port}")
    acct = ib.managedAccounts()
    print(f"  账户: {acct}  {'(paper ✅ DU开头)' if acct and acct[0].startswith('DU') else '(注意:非DU=可能是实盘!)'}")
    summ = {v.tag: v.value for v in ib.accountSummary() if v.tag in ("NetLiquidation", "TotalCashValue", "BuyingPower")}
    print(f"  净值 NetLiquidation: {summ.get('NetLiquidation','?')}  现金: {summ.get('TotalCashValue','?')}")
    # 取一个行情验证数据通
    try:
        spy = Stock("SPY", "SMART", "USD")
        ib.qualifyContracts(spy)
        t = ib.reqMktData(spy); ib.sleep(2)
        px = t.marketPrice() or t.close
        print(f"  SPY 行情: {px}  {'✅ 数据通' if px==px and px else '(无行情权限?paper常无实时,延迟数据也行)'}")
    except Exception as e:
        print(f"  行情取用失败(不致命): {str(e)[:60]}")
    ib.disconnect()
    print("\n✅ 测试完成,连接正常。下一步我写正式执行层(下单+对账+安全闸)。")

if __name__ == "__main__":
    main()
