# UK Fiscal Dashboard

A personal UK fiscal policy dashboard for Patrick Schneider, designed for use across desktop and mobile browsers.

## Initial scope

- **Fiscal position:** borrowing, receipts and spending; financial-year comparisons and available OBR forecast profiles; spending and revenue breakdowns and annual composition.
- **Debt and financing:** debt stock, maturity profile, yield curves, upcoming auctions and redemptions, and recent auction results.

Each chart will identify its source, observation period and release date, and offer a CSV download. Data vintages will be retained to support later revision analysis.

## Hosting and data

The project targets zero recurring cost using a public GitHub repository, GitHub Actions for scheduled data updates, and GitHub Pages for the dashboard. Official sources will include ONS, OBR, HM Treasury, HMRC, the UK Debt Management Office and the Bank of England, subject to source-specific reuse terms.

Website embedding is outside the initial scope.

## Status

Planning and independent review are complete; recommendations are incorporated into the plan. The app and update workflows are not yet implemented or deployed. The first MVP may run locally; GitHub Pages and scheduled updates are a subsequent milestone.

## Implementation handoff

- [Detailed project plan](docs/PROJECT_PLAN.md): local MVP, data and accounting contracts, architecture, milestones, proportionate independent reviews, design standards and future extensions.
- [Current status and next task](docs/STATUS.md).

Next: validate a small set of fiscal series and forecast comparisons, then build the first fiscal page using real data. Follow the plan's local MVP acceptance criteria before adding hosting and scheduled updates.
