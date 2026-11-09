# Portfolio report

Každé ráno stáhne GitHub Actions závěrečné kurzy pozic do `data/prices.json`. Claude z nich v 7:00 sestaví report.

- `portfolio.csv` – pozice (po nákupu/prodeji uprav počet kusů a průměrnou cenu)
- `cash.json` – hotovost na účtu
- `INSTRUCTIONS.md` – co má report obsahovat (sem přidávej nové funkce)
- `scripts/fetch_prices.py` – stahování kurzů (yfinance)
- `.github/workflows/fetch-prices.yml` – plán spouštění (út–so 4:30 UTC), ručně přes Actions → Fetch prices → Run workflow
