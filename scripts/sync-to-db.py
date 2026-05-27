"""
Sync all JSON history files into data/trading.db (SQLite).
Run manually or called from GitHub Actions after each workflow.

Tables:
  morning_notes   — daily market metrics + narrative
  stock_picks     — 10 picks per morning note
  trading_signals — deep TradingAgents analysis (2/day)
  signal_outcomes — accuracy tracking (filled next day)
"""
import json
import os
import sqlite3
import glob
from datetime import datetime, timezone, timedelta

DB_PATH = "data/trading.db"
MN_DIR  = "dashboard/morning-note-history"
TS_DIR  = "dashboard/trading-signals-history"

os.makedirs("data", exist_ok=True)
conn = sqlite3.connect(DB_PATH)
conn.row_factory = sqlite3.Row
cur = conn.cursor()

# ── Schema ────────────────────────────────────────────────────────────────────

cur.executescript("""
CREATE TABLE IF NOT EXISTS morning_notes (
    date                    TEXT PRIMARY KEY,
    generated_at            TEXT,
    sp500_futures_pct       REAL,
    treasury_10y            REAL,
    treasury_10y_change_bps REAL,
    eps_beat_rate           REAL,
    market_overview         TEXT,
    macro                   TEXT,
    earnings                TEXT,
    trade_ideas             TEXT,
    api_cost_usd            REAL,
    cumulative_cost_usd     REAL,
    avg_daily_cost_usd      REAL,
    balance_warning         INTEGER
);

CREATE TABLE IF NOT EXISTS stock_picks (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    date        TEXT NOT NULL,
    ticker      TEXT NOT NULL,
    name        TEXT,
    sector      TEXT,
    direction   TEXT,
    buy_zone    TEXT,
    target      TEXT,
    stop_loss   TEXT,
    reason      TEXT,
    UNIQUE(date, ticker)
);

CREATE TABLE IF NOT EXISTS trading_signals (
    id             INTEGER PRIMARY KEY AUTOINCREMENT,
    date           TEXT NOT NULL,
    generated_at   TEXT,
    ticker         TEXT NOT NULL,
    name           TEXT,
    sector         TEXT,
    action         TEXT,
    current_price  REAL,
    target_price   REAL,
    stop_loss      REAL,
    summary        TEXT,
    api_cost_usd   REAL,
    UNIQUE(date, ticker)
);

CREATE TABLE IF NOT EXISTS signal_outcomes (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    date         TEXT NOT NULL,
    ticker       TEXT NOT NULL,
    action       TEXT,
    entry_price  REAL,
    actual_price REAL,
    pct_change   REAL,
    correct      INTEGER,
    UNIQUE(date, ticker)
);
""")
conn.commit()

# ── Sync helpers ──────────────────────────────────────────────────────────────

def upsert_morning_note(d):
    m = d.get("market", {})
    n = d.get("note", {})
    cur.execute("""
        INSERT INTO morning_notes
            (date, generated_at, sp500_futures_pct, treasury_10y, treasury_10y_change_bps,
             eps_beat_rate, market_overview, macro, earnings, trade_ideas,
             api_cost_usd, cumulative_cost_usd, avg_daily_cost_usd, balance_warning)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        ON CONFLICT(date) DO UPDATE SET
            sp500_futures_pct=excluded.sp500_futures_pct,
            treasury_10y=excluded.treasury_10y,
            treasury_10y_change_bps=excluded.treasury_10y_change_bps,
            eps_beat_rate=excluded.eps_beat_rate,
            market_overview=excluded.market_overview,
            macro=excluded.macro,
            earnings=excluded.earnings,
            trade_ideas=excluded.trade_ideas,
            api_cost_usd=excluded.api_cost_usd,
            cumulative_cost_usd=excluded.cumulative_cost_usd,
            avg_daily_cost_usd=excluded.avg_daily_cost_usd,
            balance_warning=excluded.balance_warning
    """, (
        d.get("date"), d.get("generated_at"),
        m.get("sp500_futures_pct"), m.get("treasury_10y"),
        m.get("treasury_10y_change_bps"), m.get("eps_beat_rate"),
        n.get("market_overview"), n.get("macro"),
        n.get("earnings"), n.get("trade_ideas"),
        d.get("api_cost_usd"), d.get("cumulative_cost_usd"),
        d.get("avg_daily_cost_usd"), int(bool(d.get("balance_warning")))
    ))
    for p in d.get("stock_picks", []):
        cur.execute("""
            INSERT INTO stock_picks (date, ticker, name, sector, direction, buy_zone, target, stop_loss, reason)
            VALUES (?,?,?,?,?,?,?,?,?)
            ON CONFLICT(date, ticker) DO UPDATE SET
                name=excluded.name, sector=excluded.sector, direction=excluded.direction,
                buy_zone=excluded.buy_zone, target=excluded.target,
                stop_loss=excluded.stop_loss, reason=excluded.reason
        """, (
            d.get("date"), p.get("ticker"), p.get("name"), p.get("sector"),
            p.get("direction"), p.get("buy_zone"), p.get("target"),
            p.get("stop_loss"), p.get("reason")
        ))


def upsert_trading_signals(d):
    cost = d.get("api_cost_usd", 0)
    for s in d.get("signals", []):
        cur.execute("""
            INSERT INTO trading_signals
                (date, generated_at, ticker, name, sector, action,
                 current_price, target_price, stop_loss, summary, api_cost_usd)
            VALUES (?,?,?,?,?,?,?,?,?,?,?)
            ON CONFLICT(date, ticker) DO UPDATE SET
                action=excluded.action, current_price=excluded.current_price,
                target_price=excluded.target_price, stop_loss=excluded.stop_loss,
                summary=excluded.summary, api_cost_usd=excluded.api_cost_usd
        """, (
            d.get("date"), d.get("generated_at"),
            s.get("ticker"), s.get("name"), s.get("sector"), s.get("action"),
            s.get("current_price"), s.get("target_price"), s.get("stop_loss"),
            s.get("summary"), cost
        ))
        if "correct" in s:
            cur.execute("""
                INSERT INTO signal_outcomes (date, ticker, action, entry_price, actual_price, pct_change, correct)
                VALUES (?,?,?,?,?,?,?)
                ON CONFLICT(date, ticker) DO UPDATE SET
                    actual_price=excluded.actual_price, pct_change=excluded.pct_change, correct=excluded.correct
            """, (
                d.get("date"), s.get("ticker"), s.get("action"),
                s.get("current_price"), s.get("actual_price"),
                s.get("pct_change"), int(bool(s.get("correct")))
            ))


# ── Run sync ──────────────────────────────────────────────────────────────────

mn_count = ts_count = 0

for fpath in sorted(glob.glob(f"{MN_DIR}/*.json")):
    try:
        d = json.load(open(fpath))
        upsert_morning_note(d)
        mn_count += 1
    except Exception as e:
        print(f"[warn] {fpath}: {e}")

for fpath in sorted(glob.glob(f"{TS_DIR}/*.json")):
    try:
        d = json.load(open(fpath))
        upsert_trading_signals(d)
        ts_count += 1
    except Exception as e:
        print(f"[warn] {fpath}: {e}")

conn.commit()
conn.close()
print(f"✅ Synced {mn_count} morning notes + {ts_count} signal files → {DB_PATH}")

# ── Quick summary ─────────────────────────────────────────────────────────────

conn2 = sqlite3.connect(DB_PATH)
cur2  = conn2.cursor()
print("\n── 数据库概览 ──────────────────────────")
for tbl in ["morning_notes", "stock_picks", "trading_signals", "signal_outcomes"]:
    n = cur2.execute(f"SELECT COUNT(*) FROM {tbl}").fetchone()[0]
    print(f"  {tbl:<22} {n} 行")

print("\n── 信号准确率 ───────────────────────────")
row = cur2.execute("""
    SELECT COUNT(*) total,
           SUM(correct) correct,
           ROUND(AVG(correct)*100,1) pct
    FROM signal_outcomes
""").fetchone()
if row[0]:
    print(f"  共 {row[0]} 条已验证信号，正确 {row[1]} 条，准确率 {row[2]}%")
else:
    print("  暂无已验证信号（需隔日才能验证）")

print("\n── API 总成本 ────────────────────────────")
mn_cost = cur2.execute("SELECT SUM(api_cost_usd) FROM morning_notes").fetchone()[0] or 0
ts_cost = cur2.execute("SELECT SUM(api_cost_usd) FROM trading_signals").fetchone()[0] or 0
print(f"  晨报:   ${mn_cost:.4f}")
print(f"  信号:   ${ts_cost:.4f}")
print(f"  合计:   ${mn_cost+ts_cost:.4f}")
conn2.close()
