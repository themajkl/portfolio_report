# Zadání denního reportu

Tento soubor čte Claude při každém ranním spuštění. Novou funkci přidáš tak, že sem dopíšeš další bod.

## Data
- Kurzy: `data/prices.json` (stahuje GitHub Actions každé ráno). Zkontroluj `generated_at_utc` a `date` u pozic – pokud jsou data starší než poslední obchodní den, napiš to na začátek reportu.
- Pozice a nákupní ceny: `portfolio.csv`, hotovost: `cash.json`.
- Zprávy a důvody pohybů: finance.yahoo.com (články).
- Cílové ceny analytiků a valuace: stockanalysis.com (stránka `/stocks/<ticker>/forecast/`).

## Pravidla
- Rozebírej jen akcie, které se za poslední obchodní den pohnuly o **±3 % a více**.
- U každé takové akcie: pohyb a cena, důvod (zpráva), cílová cena analytiků a potenciál, P/E pokud je k dispozici, stav pozice vůči průměrné nákupní ceně.
- Pokud se nic nepohnulo o 3 %, pošli jen krátké shrnutí: hodnota portfolia a denní změna.
- Na začátek: celková hodnota portfolia, denní změna v USD a %, celkový zisk/ztráta.
- Přilož koláčový graf rozložení portfolia včetně hotovosti (top 8 pozic barevně, zbytek jako „Ostatní“, hotovost zvlášť).
- Upozorni na výsledky hospodaření, které firmy z portfolia zveřejní v příštích 7 dnech.
- Piš česky, stručně, bez investičních doporučení.
