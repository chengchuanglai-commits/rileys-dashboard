# launchd 安装(本地Mac跑IBKR执行)

四个 batch 定时(北京时间近似):
- `preflight` 21:00 开盘前自检
- `trade_open` 21:30 开盘下单
- `trade_close` 04:00(次日)收盘出场
- `review` 04:30(次日)复盘推飞书

安装:
```bash
chmod +x launchd/run.sh
cp launchd/*.plist ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/com.riley.ibkr-*.plist
```

卸载:
```bash
launchctl unload ~/Library/LaunchAgents/com.riley.ibkr-*.plist
```

前提:
- IB Gateway 登录 + API 端口 4002 开(且勾选允许 API 连接)。
- Mac 接电源不睡眠(系统设置→电池→电源适配器→防止自动进入睡眠)。
- 真钱开关:`scripts/ibkr/config.py` 的 `LIVE`(默认 False=paper)。

注意:
- 时间为北京时间近似;美股夏令时切换时各 plist 的 `Hour` 需 ±1 调整。
- 运行日志在 `data/exec-log/launchd.log`;每个 batch 的 stderr 在 `data/exec-log/launchd-*.err`。
- `run.sh` 已设 `NO_PROXY=127.0.0.1,localhost`(IBKR走本地不走代理)+ 代理(yfinance/飞书走代理)+ `NOTIFY_WEBHOOK`。

## ⚠️ 重要补充
- **防睡眠(必须)**:盖盖子凌晨 batch 才能跑。运行:
  `sudo pmset -c disablesleep 1`  (插电时完全不睡眠;-c=接电源)
  恢复默认:`sudo pmset -c disablesleep 0`
- **夏令时/冬令时**:plist 时间按美东夏令时(EDT)设。冬令时(11月初-3月初)美东开盘晚1小时,
  4个plist的 Hour 各 +1(preflight22/open22:30/close05:00/review05:30 北京),换季时改并重新 load。
- **caffeinate**:run.sh 已用 caffeinate -i 在跑期间防睡眠(配合 pmset 双保险)。
