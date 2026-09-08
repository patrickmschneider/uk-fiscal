# Project status

Updated: 6 September 2026.

## Current state

A usable two-page local MVP is implemented with real official data, manual refresh, local vintage capture and downloadable charts/data. It has not been deployed. See the README for startup and refresh commands.

## Milestones

- [x] M0: planning and independent review.
- [x] M1: representative official-source validation and accounting reconciliation, with limitations below.
- [x] M2: fiscal page working locally with real data.
- [ ] M3: local implementation is usable and reviewed; full recent-auction coverage and reliable calendar discovery remain acceptance gaps.
- [ ] M4: hosted release, automated refresh and durable remote archives.
- [ ] M5: owner feedback and refinement; can begin now.

## Validation and review

Independent sceptical plan review was incorporated into PROJECT_PLAN.md. Bounded independent code/data and visual-design reviews were also completed. Fixes include stable historical gilt identities, numeric curve tenors and missing-value handling, calendar-year redemption windows, week-based syndication dates, fiscal-history comparisons, export legends, mobile table cues, contrast and copy-link feedback. Reviews are recorded here rather than retained as separate documents.

Final checks: production build; seven frontend unit tests; 29 Python adapter/pipeline tests; four Chromium/WebKit browser tests, including mobile layouts, keyboard navigation, CSV/SVG downloads and automated accessibility scans. Browser resize checks wait for responsive charts to settle. Real-source checks reconcile monthly spending less receipts to borrowing and annual composition totals within published rounding.

## Known limitations and next task

- DMO auction results have a July–August 2026 gap, with selected subsequent notices. Complete aggregate result discovery and replace curated calendar notice discovery before calling M3 fully accepted. Repeated downloads alone do not make calendar discovery current.
- Annual functional spending has five consistent years; longer history needs classification-aware extension.
- Bank of England curves work locally, but their public redistribution is not cleared. Payload and actual workbook are gitignored. Resolve terms or select a permissible equivalent before M4; do not publish the local payload by accident.
- Vintages currently live only in the local ignored archive. M4 must add durable remote preservation, CI refresh, failure monitoring and hosted-path testing.
- Production build flags a large chart-library bundle; acceptable for this local version, revisit if hosted performance warrants it.

Next: obtain owner feedback on the running local version, close the DMO coverage/discovery gaps, then implement the separate hosting milestone. Do not add scenarios, policy tracking, embedding or elaborate design infrastructure yet.

## Owner feedback queued for later

Requested after the first MVP preview; record only for now, implementation deferred:

- Yield curve: make changes over time easy to compare, including a change-in-yield view in basis points between selected dates.
- Add comparisons with the other G7 countries (US, Canada, Japan, Germany, France and Italy). Before implementation, check official source availability, reuse terms and comparability of curve definitions, maturities and observation dates; clearly label national currencies and any methodological differences.
- Add a horizontal-axis label to the yield curve: “Maturity (years)”, including in exported charts.
- Maturity profile: add a histogram or distribution curve showing each maturity bucket as a percentage of the total debt stock, rather than only amounts. State the stock denominator, weighting basis and bucket widths; retain amounts as an optional view.
- Add a rate-distribution graph combining the maturity profile with the yield curve, weighted by the debt share at each maturity. Clarify the intended measure before implementation: current yields mapped to maturities describe a market-yield distribution / refinancing-cost proxy, whereas rates actually payable on existing debt require contractual coupons and index-linked treatment. Label the measure explicitly and avoid presenting current yields as existing debt-service costs.

- Requested 8 September: add implied RPI inflation from conventional nominal and index-linked real gilt yields. Consider a separate **Pricing** tab grouping nominal/real yield curves, their changes, G7 comparisons and inflation pricing; tab structure remains a design option, not a settled decision.
- Implement as an **RPI breakeven inflation term structure**, using matched dates, maturities, compounding conventions and comparable fitted spot curves; do not subtract unmatched individual gilt redemption yields. Show changes between selected dates, underlying nominal/real curves and source/observation metadata. Validate source methodology, inflation indexation lags, relevant RPI reform effects and reuse rights before implementation. Explain that breakevens embed inflation risk and liquidity premia and are not pure expected inflation or CPI forecasts. Forward inflation rates can be a later extension.

## Decisions

Public GitHub repository; intended GitHub Pages and Actions; no recurring paid services. One user, two pages, progressively disclosed detail. Local-first delivery is approved. No duplicate review or source documents: definitions live in the catalogue, plan in PROJECT_PLAN.md, progress here.
