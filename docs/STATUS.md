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

Final checks: production build; 14 frontend unit tests; 43 Python adapter/pipeline tests; 14 Chromium/WebKit browser tests, including mobile layouts, keyboard navigation, CSV/SVG downloads and automated accessibility scans. Browser resize checks wait for responsive charts to settle. Real-source checks reconcile monthly spending less receipts to borrowing and annual composition totals within published rounding.

## Known limitations and next task

- DMO auction results have a July–August 2026 gap, with selected subsequent notices. Complete aggregate result discovery and replace curated calendar notice discovery before calling M3 fully accepted. Repeated downloads alone do not make calendar discovery current.
- Annual functional history now spans 2003-04–2025-26 on the PESA 2026 vintage. Published classification breaks are labelled; the exact five-year functional snapshot remains available separately.
- Owner authorised public non-commercial use of the fitted BoE curve outputs on 9 September, accepting the reuse uncertainty with attribution. The former project publication hold is removed; this is not specific permission from the Bank. Curve outputs are tracked, original workbooks remain local. Attribution is shown in-app and in CSV/SVG exports; details in catalogue/boe.json.
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

## Budget history and interest bridge, 9 September

- Added Compare budgets over time on Fiscal position: full-year economic spending, functional spending and revenue composition, in % GDP, % of total or £bn. Two selected years produce a ranked percentage-point contribution table and CSV. Functional history covers 23 years from PESA 2026 chapter 4 (official rounded amounts and GDP shares), keeping TES/TME and accounting adjustments distinct. Debt interest is identified as an of-which within general public services, never counted twice.
- Added taxes/NICs versus total receipts (ONS AHHY/JW2O), council tax and interest/dividend receipts (JW2L). Economic/revenue history uses matched financial-year nominal GDP. Explicit residuals preserve totals; rounding is present in every functional year, including zeros. Independent review suggestions on rounding and denominator notes were incorporated.
- Current-vintage annual TME: 39.1% GDP in 2019-20, 44.3% in 2025-26. PESA debt interest +1.8pp, health +1.1pp, social protection +1.1pp; social protection includes pensions and services. Dashboard broad net interest/dividends is 1.45%→2.87%; subtracting it yields spending of 37.6%→41.4%. This analytical bridge includes dividends and is not an official primary-spending measure. A plateau is not evidence of a steady state.
- Automated tests check annual boundaries, residual reconciliation, functional changes, the interest bridge and mobile accessibility without accessing the user's screen or microphone. Fixed tooltip text contrast revealed by the new open-history test.

## Owner feedback queued for later

- Add comparisons with the other G7 countries (US, Canada, Japan, Germany, France and Italy). Before implementation, check official source availability, reuse terms and comparability of curve definitions, maturities and observation dates; clearly label national currencies and any methodological differences.
- Maturity profile: add a histogram or distribution curve showing each maturity bucket as a percentage of the total debt stock, rather than only amounts. State the stock denominator, weighting basis and bucket widths; retain amounts as an optional view.
- Add a rate-distribution graph combining the maturity profile with the yield curve, weighted by the debt share at each maturity. Clarify the intended measure before implementation: current yields mapped to maturities describe a market-yield distribution / refinancing-cost proxy, whereas rates actually payable on existing debt require contractual coupons and index-linked treatment. Label the measure explicitly and avoid presenting current yields as existing debt-service costs.
- Forward inflation curves and model-based inflation-expectations decompositions remain possible later extensions.

## Decisions

Public GitHub repository; intended GitHub Pages and Actions; no recurring paid services. One user, three tabs, progressively disclosed detail. Local-first delivery is approved. No duplicate review or source documents: definitions live in the catalogue, plan in PROJECT_PLAN.md, progress here.

RPI control refinement: comparison and observation calendars now also appear directly on the RPI breakeven level chart. They share the selected dates with the pricing/change panels; a browser regression checks that the selected historical curve appears in the data table.

State composition refinement: added % of named total / % of GDP selector for both functional spending and revenue sources. Named totals are TES and public-sector current receipts; GDP uses the selected full financial year (BKTL), explicitly distinguished from Treasury published GDP shares. Bars use a common 0–100% denominator scale; CSV includes the chosen denominator. Selection persists in the URL. Production build and two focused Chromium/WebKit tests pass, covering year changes, exports and accessibility.

Stacked-chart design refinement: replaced the muddy palette with stable name-based categorical colours adapted from Tableau 10; navy replaces its grey substantive category, while residuals, EU transactions and rounding use neutrals. Debt stacks use blue/orange. Thin white segment boundaries and matching filled-square legends also apply to SVG exports. Independent static design advice incorporated; rendered functional chart and export inspected in an isolated headless browser. Production build and four focused Chromium/WebKit checks passed. No user-screen or microphone access.
