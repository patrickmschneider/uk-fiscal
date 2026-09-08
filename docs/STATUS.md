# Project status

Updated: 9 September 2026.

## Current state

A usable three-tab local MVP is implemented with real official data, manual refresh, local vintage capture and downloadable charts/data. It has not been deployed. See the README for startup and refresh commands.

## Milestones

- [x] M0: planning and independent review.
- [x] M1: representative official-source validation and accounting reconciliation, with limitations below.
- [x] M2: fiscal page working locally with real data.
- [ ] M3: local implementation is usable and reviewed; full recent-auction coverage and reliable calendar discovery remain acceptance gaps.
- [ ] M4: hosted release, automated refresh and durable remote archives.
- [ ] M5: owner feedback and refinement; can begin now.

## Validation and review

Independent sceptical plan review was incorporated into PROJECT_PLAN.md. Bounded independent code/data and visual-design reviews were also completed. Fixes include stable historical gilt identities, numeric curve tenors and missing-value handling, calendar-year redemption windows, week-based syndication dates, fiscal-history comparisons, export legends, mobile table cues, contrast and copy-link feedback. Reviews are recorded here rather than retained as separate documents.

Final checks: production build; 10 frontend unit tests; 39 Python adapter/pipeline tests; 12 Chromium/WebKit browser tests, including mobile layouts, keyboard navigation, CSV/SVG downloads and automated accessibility scans. Browser resize checks wait for responsive charts to settle. Real-source checks reconcile monthly spending less receipts to borrowing and annual composition totals within published rounding.

## Known limitations and next task

- DMO auction results have a July–August 2026 gap, with selected subsequent notices. Complete aggregate result discovery and replace curated calendar notice discovery before calling M3 fully accepted. Repeated downloads alone do not make calendar discovery current.
- Annual functional spending has five consistent years; longer history needs classification-aware extension.
- Bank of England curves work locally, but their public redistribution is not cleared. Payload and actual workbook are gitignored. Resolve terms or select a permissible equivalent before M4; do not publish the local payload by accident.
- Vintages currently live only in the local ignored archive. M4 must add durable remote preservation, CI refresh, failure monitoring and hosted-path testing.
- Production build flags a large chart-library bundle; acceptable for this local version, revisit if hosted performance warrants it.

Next: obtain owner feedback on the running local version, close the DMO coverage/discovery gaps, then implement the separate hosting milestone. Do not add scenarios, policy tracking, embedding or elaborate design infrastructure yet.

## Owner refinements delivered, 9 September

- Pricing is now a separate tab with nominal and real gilt spot curves, matched RPI breakevens, arbitrary saved-date comparisons and expandable changes in basis points. Maturity axes are labelled in years, including exports. Local data extend through 7 September 2026; real/breakeven coverage starts at 2.5 years. Exact matched nominal-minus-real calculations agree with the official BoE inflation workbook to ten decimal places in the test fixture.
- Fiscal headline and time-series flows now toggle between £bn and % of GDP, including narrative, tables and exports. GDP is published BKTL nominal NSA GDP over four quarters, at the latest quarter end on/before each endpoint (maximum two months carry-forward); monthly/YTD numerators are not annualised. This is dashboard scaling, not an official ONS fiscal ratio. Latest denominator ends June 2026 (£3,103.024bn). CSV/table exports include denominator dates and values. Forecast percentages stop at the latest fiscal outturn month, with no GDP forecast assumed. Composition remains its separately labelled share-of-total view.
- Independent code/data review found no blocker; its narrative/denominator-export suggestions were incorporated. Mobile views and SVG export were visually checked, including the populated GDP view, alongside browser accessibility checks. A non-blocking resilience limitation remains: GDP fetch failure retains the whole previous fiscal bundle rather than promoting only fresh fiscal numerators.

## Rendering and date-picker follow-up, 9 September

- The saved payload contains all three curves. A stale nominal-only in-memory snapshot was identified as a reproducible cause of missing real/breakeven panels: the original app loaded JSON only once. Data reads now bypass the browser cache and reload on focus/visibility return; Pricing also offers Reload saved data and explains incomplete snapshots. This mechanism is verified in headless regression tests; the user's original screen state was not inspected.
- An independent static review identified optional-source reload failures discarding last-good curves. Reload now retains prior curve/forecast datasets and shows the failed-read warning; a 503 regression verifies this.
- Replaced date lists with year/month calendar controls and previous/next-month arrows. Only published observation days are selectable. Shared controls are also available inside every change panel, with selected dates retained in the URL. Keyboard Escape, mobile sizing and accessibility are covered in Chromium/WebKit tests. No screen or microphone access is needed for these checks.

## Owner feedback queued for later

- Add comparisons with the other G7 countries (US, Canada, Japan, Germany, France and Italy). Before implementation, check official source availability, reuse terms and comparability of curve definitions, maturities and observation dates; clearly label national currencies and any methodological differences.
- Maturity profile: add a histogram or distribution curve showing each maturity bucket as a percentage of the total debt stock, rather than only amounts. State the stock denominator, weighting basis and bucket widths; retain amounts as an optional view.
- Add a rate-distribution graph combining the maturity profile with the yield curve, weighted by the debt share at each maturity. Clarify the intended measure before implementation: current yields mapped to maturities describe a market-yield distribution / refinancing-cost proxy, whereas rates actually payable on existing debt require contractual coupons and index-linked treatment. Label the measure explicitly and avoid presenting current yields as existing debt-service costs.
- Forward inflation curves and model-based inflation-expectations decompositions remain possible later extensions.

## Decisions

Public GitHub repository; intended GitHub Pages and Actions; no recurring paid services. One user, three tabs, progressively disclosed detail. Local-first delivery is approved. No duplicate review or source documents: definitions live in the catalogue, plan in PROJECT_PLAN.md, progress here.
