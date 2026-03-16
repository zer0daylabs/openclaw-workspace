#!/usr/bin/env python3
"""Freqtrade bot status checker — run anytime to see current activity.
Usage: python3 check_status.py"""

import json
import urllib.request
import base64
from collections import Counter
from datetime import datetime, timezone

API_BASE = "http://localhost:8080/api/v1"
USERNAME = "freqtrade"
PASSWORD = "freqtrade"

# Day boundaries by trade ID (update as needed)
DAY_BOUNDARIES = {
    "Day 1": (1, 29),      # id 1-29
    "Day 2": (30, 39),     # id 30-39
    "Day 3": (40, 999),    # id 40+
}


def api_call(path, method="GET", auth_token=None):
    url = f"{API_BASE}/{path}"
    req = urllib.request.Request(url, method=method)
    if auth_token:
        req.add_header("Authorization", f"Bearer {auth_token}")
    elif method == "POST":
        creds = base64.b64encode(f"{USERNAME}:{PASSWORD}".encode()).decode()
        req.add_header("Authorization", f"Basic {creds}")
    req.add_header("Content-Type", "application/json")
    if method == "POST" and not auth_token:
        req.data = b""
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode())


def get_token():
    data = api_call("token/login", method="POST")
    return data.get("access_token", "")


def main():
    token = get_token()
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    print(f"\n{'='*60}")
    print(f"  FREQTRADE STATUS CHECK — {now}")
    print(f"{'='*60}\n")

    # Open trades
    open_trades = api_call("status", auth_token=token)
    print("📊 OPEN TRADES")
    print("-" * 50)
    if not open_trades:
        print("  No open trades — book is flat\n")
    else:
        for t in open_trades:
            pr = (t.get("profit_ratio", 0) or 0) * 100
            pabs = t.get("profit_abs", 0) or 0
            pair = t["pair"]
            tid = t["trade_id"]
            entry = t.get("open_rate", 0)
            cur = t.get("current_rate", 0)
            od = t.get("open_date", "")
            # Duration
            try:
                ot = datetime.fromisoformat(od.replace("Z", "+00:00"))
                dur = (datetime.now(timezone.utc) - ot).total_seconds() / 3600
                dur_str = f"{dur:.1f}h"
            except:
                dur_str = "?"
            flag = " ⚠️" if dur_str != "?" and float(dur_str[:-1]) > 4 else ""
            print(f"  #{tid:>3}  {pair:12s}  ${entry:<12}  now ${cur:<12}  {pr:+.2f}% (${pabs:+.4f})  {dur_str}{flag}")
        print(f"  {len(open_trades)} open\n")

    # All trades
    all_data = api_call("trades", auth_token=token)
    trades = all_data.get("trades", [])
    closed = [t for t in trades if not t.get("is_open", True)]
    closed.sort(key=lambda t: t.get("close_date", ""), reverse=True)

    print("📈 RECENT CLOSED (last 8)")
    print("-" * 50)
    for t in closed[:8]:
        pr = (t.get("profit_ratio", 0) or 0) * 100
        reason = t.get("exit_reason", "")
        icon = "✅" if pr > 0 else "❌"
        print(f"  {icon} #{t['trade_id']:>3}  {t['pair']:12s}  {pr:+.2f}%  via {reason:18s}  {t.get('close_date', '')[:16]}")
    print()

    # Exit reason breakdown
    reasons = Counter(t.get("exit_reason", "") for t in closed)
    print("🔍 EXIT REASONS")
    print("-" * 50)
    for reason, count in reasons.most_common():
        wins = len([t for t in closed if t.get("exit_reason") == reason and (t.get("profit_ratio", 0) or 0) > 0])
        wr = wins / count * 100 if count else 0
        avg_pnl = sum((t.get("profit_ratio", 0) or 0) * 100 for t in closed if t.get("exit_reason") == reason) / count
        print(f"  {reason:20s}  {count:>3} trades  {wins}W/{count-wins}L  ({wr:.0f}% WR)  avg {avg_pnl:+.2f}%")
    print()

    # Day breakdown
    print("📅 DAILY BREAKDOWN")
    print("-" * 50)
    for label, (lo, hi) in DAY_BOUNDARIES.items():
        day_trades = [t for t in trades if lo <= t.get("trade_id", 0) <= hi]
        day_closed = [t for t in day_trades if not t.get("is_open", True)]
        day_open = [t for t in day_trades if t.get("is_open", True)]
        wins = len([t for t in day_closed if (t.get("profit_ratio", 0) or 0) > 0])
        losses = len(day_closed) - wins
        pnl = sum((t.get("profit_abs", 0) or 0) for t in day_closed)
        wr = wins / len(day_closed) * 100 if day_closed else 0
        status = f"{wins}W/{losses}L ({wr:.0f}%)" if day_closed else "no closed"
        open_str = f", {len(day_open)} open" if day_open else ""
        print(f"  {label:8s}  {len(day_trades):>2} trades  {status:16s}  P&L: ${pnl:+.4f}{open_str}")
    print()

    # Profit summary
    profit = api_call("profit", auth_token=token)
    total_wins = profit.get("winning_trades", 0)
    total_losses = profit.get("losing_trades", 0)
    total_count = max(total_wins + total_losses, 1)

    print("💰 OVERALL")
    print("-" * 50)
    print(f"  Closed P&L:  {profit.get('profit_closed_coin', 0):+.4f} USDT")
    print(f"  Total P&L:   {profit.get('profit_all_coin', 0):+.4f} USDT")
    print(f"  Win rate:    {total_wins}W / {total_losses}L = {total_wins/total_count*100:.0f}%")
    print(f"  Avg duration: {profit.get('avg_duration', '?')}")
    print(f"\n{'='*60}\n")


if __name__ == "__main__":
    main()
