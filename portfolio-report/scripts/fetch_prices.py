"""Stáhne poslední závěrečné ceny všech pozic z portfolio.csv a uloží je do data/prices.json.

Spouští se automaticky přes GitHub Actions (viz .github/workflows/fetch-prices.yml).
"""

import csv
import json
import time
from datetime import datetime, timezone
from pathlib import Path

import yfinance as yf

ROOT = Path(__file__).resolve().parent.parent
PORTFOLIO = ROOT / "portfolio.csv"
CASH = ROOT / "cash.json"
OUT = ROOT / "data" / "prices.json"


def last_two_closes(symbol: str, retries: int = 3):
    """Vrátí (datum, close, předchozí close) pro poslední dva obchodní dny."""
    for attempt in range(retries):
        try:
            hist = yf.Ticker(symbol).history(period="10d", interval="1d", auto_adjust=False)
            hist = hist.dropna(subset=["Close"])
            if len(hist) >= 2:
                last, prev = hist.iloc[-1], hist.iloc[-2]
                return hist.index[-1].strftime("%Y-%m-%d"), float(last["Close"]), float(prev["Close"])
        except Exception as e:  # síťová chyba, rate limit apod.
            print(f"{symbol}: pokus {attempt + 1} selhal: {e}")
        time.sleep(3 * (attempt + 1))
    return None


def main():
    with open(PORTFOLIO, newline="", encoding="utf-8") as f:
        positions = list(csv.DictReader(f))
    cash = json.loads(CASH.read_text(encoding="utf-8"))

    fx = last_two_closes("EURUSD=X")
    eurusd = fx[1] if fx else None

    rows, total_now, total_prev, total_cost = [], 0.0, 0.0, 0.0
    for p in positions:
        qty = float(p["quantity"])
        avg = float(p["avg_buy_price"]) if p["avg_buy_price"] else None
        to_usd = eurusd if p["currency"] == "EUR" and eurusd else 1.0
        data = last_two_closes(p["yahoo_symbol"])
        row = {"ticker": p["ticker"], "company": p["company"], "currency": p["currency"], "quantity": qty}
        if data:
            date, close, prev = data
            value_usd = qty * close * to_usd
            row.update({
                "date": date,
                "close": round(close, 4),
                "prev_close": round(prev, 4),
                "change_pct": round((close / prev - 1) * 100, 2),
                "value_usd": round(value_usd, 2),
                "avg_buy_price": avg,
                "pl_pct": round((close / avg - 1) * 100, 2) if avg else None,
            })
            total_now += value_usd
            total_prev += qty * prev * to_usd
            if avg:
                total_cost += qty * avg * to_usd
        else:
            row["error"] = "cena nedostupná"
        rows.append(row)

    cash_usd = cash.get("USD", 0) + cash.get("EUR", 0) * (eurusd or 1.0)
    for r in rows:
        if "value_usd" in r:
            r["weight_pct"] = round(r["value_usd"] / (total_now + cash_usd) * 100, 2)

    out = {
        "generated_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "eurusd": round(eurusd, 4) if eurusd else None,
        "cash_usd_total": round(cash_usd, 2),
        "positions_value_usd": round(total_now, 2),
        "portfolio_total_usd": round(total_now + cash_usd, 2),
        "day_change_usd": round(total_now - total_prev, 2),
        "day_change_pct": round((total_now / total_prev - 1) * 100, 2) if total_prev else None,
        "total_pl_pct": round((total_now / total_cost - 1) * 100, 2) if total_cost else None,
        "positions": sorted(rows, key=lambda r: -abs(r.get("change_pct", 0))),
    }
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
