# UK Fiscal Dashboard

A personal UK fiscal briefing dashboard for Patrick Schneider. The first local version has two pages: fiscal balances and breakdowns; and debt, yields, financing operations and redemptions. Charts include source notes, tables, CSV and SVG downloads.

## Run locally

Requires Node.js 22.12+ (tested on 24) and npm.

```sh
npm ci
npm run dev
```

Open the local address printed by Vite. The included official-data snapshots let the app run immediately. This local address is available on the computer running it; public hosting and scheduled updates are a subsequent milestone.

## Refresh data

Requires Python 3.11+ (tested on 3.13).

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m pipeline.refresh
```

Use `--group fiscal`, `--group composition`, `--group debt`, `--group forecast` or `--group curve` for an individual source group. `--offline` replays locally archived downloads; `--validate` checks saved data. A failed group keeps its last good dataset, records the failure and returns a nonzero exit code. Downloads and release vintages are retained in ignored `data/archive/`; back up that directory if you need those vintages. Remote durable archives are planned with hosting.

Bank of England curve downloads are used locally under personal/internal-use terms. Their derived payload and original workbook are deliberately excluded from GitHub until public redistribution is cleared. On a fresh checkout, run `python -m pipeline.refresh --group curve` to populate the curve panel. Other panels work without it.

## Current coverage

- ONS public sector finances through July 2026, with reconciled receipts, expenditure and borrowing; March 2026 OBR monthly borrowing forecast via ONS.
- HM Treasury PESA annual functional spending composition, five financial years. Its TES denominator differs from the fiscal page's TME measure.
- DMO gilt stock dated 4 September 2026. Auction results include July 2025–June 2026 and selected later notices; July–August 2026 coverage is incomplete. The July–December financing calendar uses curated official notices and still needs source discovery when schedules change.
- Local Bank of England nominal spot curves through 3 September 2026. These are fitted spot yields, not auction yields or borrowing-cost forecasts.

The app labels definitions, observation dates and partial coverage. Refreshing a curated DMO notice does not discover newly published notices. Machine-readable source mappings and reuse notes live in `catalogue/`.

## Checks

```sh
npm run build
npm test
source .venv/bin/activate
npm run test:data
npx playwright install chromium webkit
APP_URL=http://127.0.0.1:5173 npm run test:browser
```

Run the development server first and set `APP_URL` to its printed address. Browser checks cover both pages, mobile overflow, keyboard access, accessibility, URL state and exports.

## Project references

- [Implementation plan and future extensions](docs/PROJECT_PLAN.md)
- [Progress, limitations and next task](docs/STATUS.md)

The intended hosted version uses GitHub Pages and GitHub Actions with no recurring paid services. Personal website integration remains outside scope.
