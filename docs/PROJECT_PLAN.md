# UK Fiscal Dashboard: implementation and handoff plan

Status: implementation reference; owner-approved refinements now add a separate Pricing tab and GDP-scaled fiscal flows (details in STATUS.md); the local dashboard and data pipeline are built. See STATUS.md for validation and remaining acceptance gaps.
Owner: Patrick Schneider. Repository: https://github.com/patrickmschneider/fiscal-space
Plan date: 6 September 2026.

Independent sceptical and design-planning reviews completed on 6 September 2026. All recommendations are incorporated here, including explicit required panels, failure signalling during partial updates, code/data compatibility and separate local/hosted test gates. No unresolved plan blocker remains; this does not constitute validation of actual source data or application code.

## 1. Purpose and agreed constraints

Build a personal briefing tool for an Imperial College macroeconomics professor who wants reliable data to comment on UK fiscal policy. Success is being able to understand a fiscal release, inspect its drivers and obtain a usable chart or dataset within a couple of minutes.

- One intended user, accessing the same URL across computers, tablets and phones.
- Public repository and public dashboard are agreed. Do not put private notes, personal data or credentials in either.
- Zero recurring service cost is a requirement under current free tiers. No paid database, market-data subscription, AI API or continuously running server.
- Use GitHub for source control, GitHub Actions for updates and deployment, and GitHub Pages for hosting. The user's Google Sites website and GoDaddy domain are out of scope.
- Two MVP pages: **Fiscal position** and **Debt & financing**. Detailed breakdowns belong below the overview or in expandable sections, not in a crowded landing view.
- Prefer official statistics, explicit definitions and reproducible transformations. Do not represent delayed statistics as live data.
- Preserve data vintages from the start. Historical vintages before collection begins are available only if a source supplies them.
- Deliver small working increments. Do not build all future extensions before publishing a useful MVP.
- The owner explicitly accepts a **local-only MVP**. Multi-device hosting remains the intended destination, but is not a condition of the first MVP. Separate local completion from the subsequent hosted/automated release throughout this plan.

At planning time the repository contains README.md, .gitignore and planning documents, on main, connected to origin. Verify the current state and applicable local instructions before working; this description will become dated.

## 2. MVP scope and boundaries

### Page 1: Fiscal position

Default to the latest complete available fiscal month, showing UK public-sector measures excluding public-sector banks where that is the source definition.

1. Four headline measures: financial-year-to-date borrowing, receipts, spending, and latest public sector net debt as a share of GDP. Each shows its own period and an appropriate comparator. Debt is a stock, not a financial-year flow.
2. Main chart: April-to-March cumulative borrowing, comparing the current financial year with the previous year and an explicitly selected OBR monthly forecast profile if a compatible one is available.
3. Supporting chart: monthly or cumulative receipts and expenditure, with a clear relationship to borrowing. A simple change-contribution chart is included only after its components reconcile; otherwise use the two transparent series.
4. Expandable receipts and spending sections: historical lines/tables for major published categories. Revenue includes major taxes and non-tax receipts; expenditure uses compatible economic categories. Mark central-government detail as such if that is the available source coverage.
5. Annual composition section, collapsed initially: ranked horizontal bars for spending functions and revenue sources. Include latest complete available financial year and a historical year selector; show amounts and shares with named denominators. Use an explicit residual where coverage is partial.
6. A small information panel: source links, next fiscal release if officially available, current data availability, and concise definition notes. Detailed methodology can be a linked document rather than a third application page.

Controls: latest month / financial year to date / rolling 12 months for compatible flows; recent history / full available history; relevant category selection. Annual composition has its own year selector. Do not add a global control that appears to change incompatible datasets.

History target: monthly fiscal aggregates from April 2000 or the earliest reliable comparable period thereafter; at least ten completed fiscal years of annual composition where classifications allow. Preserve longer source history when inexpensive, but do not splice incompatible definitions to meet a target. Record actual start dates in the series catalogue.

### Page 2: Debt & financing

1. A small summary of headline public sector net debt, the gilt stock on an explicitly stated valuation/holdings basis, and Treasury bills outstanding if a reliable feed is available. Explain that these measures do not sum directly to net debt.
2. Gilt redemption profile by financial year, splitting conventional and index-linked instruments where valid. Show the next 12 months in a table and the full maturity horizon in a chart. Provide average remaining contractual maturity only with a documented weighting basis.
3. Conventional/index-linked composition and a security table with identifier, name, coupon, maturity, nominal outstanding amount and as-of date. Coupon is not the current borrowing rate.
4. Bank of England nominal gilt spot curve at the latest available observation, with previous business observation and approximately one month earlier as selectable comparisons. Compare only available tenors; do not manufacture a 30-year point or extrapolate beyond source coverage.
5. Upcoming gilt operations over the next 90 days, plus the next scheduled operation beyond that window if useful: date, operation type, gilt/maturity, announced size if available, announcement/settlement dates when supplied, and source. Distinguish provisional plans from confirmed operations.
6. Recent auction results: last 12 months, with a compact initial table and expandable history. Include instrument, date, offered/allotted amounts on named bases, accepted yield, cover ratio, conventional-gilt tail where applicable, and separately reported post-auction take-up if available.

Stock and maturity data start with the latest verified snapshot; historical snapshots accumulate thereafter. Do not imply a historical security database already exists. Start curve history with the last 12 months, extending cheaply if the source download contains more.

### MVP capabilities shared across pages

- Responsive, keyboard-usable charts and controls; equivalent data tables.
- CSV export of the selected view with definitions, units and provenance supplied in the download or an accompanying metadata file.
- CSV and data tables are mandatory locally. A shared SVG or PNG export with title, units, period and source footer is desirable; if it substantially delays the local MVP, defer it to the hosted release and record that decision. Avoid bespoke exporters for each chart.
- URL parameters preserve page, selected series, dates and comparison settings. No login or cloud preference database. Local preferences may supplement links but do not synchronise across devices.
- Visible distinction between observation dates, publication dates, retrieval/check times and website build time.
- Checked-in, permitted, validated current data make the local app useful without a live source connection. A documented manual refresh command retains last known good data on failure; stale or failed sources are identified. Scheduling follows in the hosted milestone.
- A brief factual site description identifying this as an independent dashboard, not an official government publication.

### Explicitly outside MVP

Full coupon cash-flow projection; complete accrual-to-cash financing reconciliation; financing-remit progress analysis; detailed syndication allocations; bill auction history; real/per-capita transformations throughout; current-budget and primary-balance analytical panels; interactive vintage comparison; fiscal rules; policy event tracking; APF/QT consolidation; scenarios; international comparisons; notifications; website embedding; private accounts. These remain extensions, not hidden launch requirements. Keep raw inputs useful for them when practical.

All six numbered sections on each page are required locally, including annual composition, the nominal curve, upcoming operations and recent auction results. The following are optional within them: Treasury bills if no reliable feed exists; calculated average maturity; a change-contribution chart (receipts/spending lines are the fallback); next-release dates not officially announced; announced auction sizes and result fields not supplied or inapplicable. An OBR monthly comparison may be unavailable: retain last-year comparison, show a compatible annual forecast separately if available, and explain the missing monthly profile. Never replace a missing profile with annual forecast divided by twelve.

Optional-field fallbacks do not authorise dropping whole required sections. Missing required data remains a recorded local-MVP blocker; deliver the usable preview while resolving it or proposing a concrete scope revision to the owner. Automated publication is required for the hosted milestone only.

## 3. Data discovery: first implementation milestone

Create a machine-readable series/source catalogue before building complex charts. Keep verified definitions, source links and reuse notes there rather than duplicating them in a separate source document. This plan identifies official source families, not validated production endpoints. Source tables, identifiers, licences, automated access and exact mappings still need inspection.

| Source | Intended use | Frequency / implementation cautions |
| --- | --- | --- |
| [ONS public sector finances](https://www.ons.gov.uk/economy/governmentpublicsectorandtaxes/publicsectorfinance/bulletins/publicsectorfinances/latest) and its time series/appendices | Borrowing, receipts, expenditure, debt, compatible breakdowns | Monthly; revisions and classification changes; find stable downloadable series or tables and their identifiers |
| [OBR data](https://obr.uk/data/) and [monthly profiles example](https://obr.uk/monthly-profiles-for-2025-26/) | Forecast comparison, annual history, forecast vintages | Forecast publications and subsequent profiles; verify which fiscal year and forecast vintage each file covers |
| [Treasury PESA collection](https://www.gov.uk/government/collections/public-expenditure-statistical-analyses-pesa) | Annual spending composition by function | Annual with updates; expenditure on services is not automatically total managed expenditure |
| [HMRC tax receipts](https://www.gov.uk/government/statistics/hmrc-tax-and-nics-receipts-for-the-uk) | Additional tax detail only if needed | Monthly cash receipts; do not silently join to accrual fiscal-account series; does not cover all public receipts |
| [DMO data catalogue](https://www.dmo.gov.uk/data/) | Gilts in issue, redemptions, operations, bills | Report downloads and some XML feeds; access paths and schemas require a spike |
| [Bank of England yield curves](https://www.bankofengland.co.uk/statistics/yield-curves) | Daily fitted nominal spot curve | Download files, not a yield-curve API; aims to publish by noon next business day; available maturities vary |

DMO catalogue pointers to investigate: D1A gilts in issue; D8B future redemptions; D2.1A gilt auction results; D5D outright gilt issuance calendar; D5J events; D2.2E bills outstanding. Treat report codes as discovery aids, not guaranteed URL contracts. Inspect index-linked reports when interpreting redemption amounts. Do not build a generic scraper before testing the specific reports.

For each MVP dataset record: landing URL, exact download URL/discovery mechanism, dataset and series identifiers, sheet/table names, publication and retrieval timestamps, units, accounting basis, institutional scope, frequency, earliest comparable period, missing-value conventions, revision behaviour, reuse/redistribution terms, and a tested sample. Record whether the source supports historical releases.

Use the minimum number of providers needed for a coherent result. Prefer ONS for a consistent fiscal overview and receipts mix; add HMRC only where it materially improves the drill-down. A blocked webpage is not proof that all official downloads are inaccessible: test documented links and normal downloads. Do not bypass access controls. A manually supplied official file can unblock development, but must be identified and does not satisfy automated-source acceptance.

Run the initial spike locally; a short standard Linux GitHub Actions access check is advisable early because source sites may treat cloud requests differently, and is mandatory before the hosted release. A cloud-only access failure need not block local progress. Record reuse conditions before committing data to the public repository or publicly republishing raw files, particularly data incorporating third-party market inputs. Owner decision, 9 September 2026: attributed fitted BoE curve outputs may be published for the non-commercial dashboard despite unresolved reuse wording; original workbooks remain local. This is not a determination of licence coverage or permission from the Bank. Metadata can be public without publishing restricted source content. If required public redistribution is not permitted, report the specific blocker and seek a permissible source; do not silently abandon provenance or change to paid data.

## 4. Economic and statistical contracts

These are substantive acceptance criteria, not just tooltip wording.

- **Scope:** store institutional coverage for every series. Do not subtract central-government receipts from whole-public-sector spending, or double-count transfers within the public sector.
- **Borrowing identity:** use compatible source measures. Reconcile spending minus receipts to net borrowing only after specifying depreciation, gross/net investment and other adjustments in those measures. Document a bridge if categories do not directly add; never invent a balancing component named spending.
- **Sign:** positive borrowing/deficit means a financing need; surplus is negative. Define this once in code and metadata. Keep source values unrounded; round only for display.
- **Calendar:** financial years run April–March. Compare identical month coverage. Do not sum cumulative observations or difference across fiscal-year boundaries without explicit logic.
- **Missing values:** missing is not zero. A rolling 12-month figure requires 12 valid monthly observations. Use null plus a reason; do not forward-fill flows or outturns into future periods.
- **Seasonality:** default to cumulative or same-month-last-year comparisons. Do not imply that unadjusted month-on-month changes show a policy shift. Avoid percentage-change headlines when a deficit crosses zero or its denominator is tiny.
- **GDP ratios:** prefer published ONS ratios with their stated denominator convention. Do not divide a monthly flow by quarterly GDP. New ratios require an explicit compatible annualisation/denominator method and vintage.
- **Annual composition:** name the year and total; functional spending and departmental budgets are different classifications. Keep transfers, capital and debt interest consistent with the chosen table. Latest complete published year may lag the latest completed calendar financial year. "Composition" is descriptive, not an estimated steady state.
- **Forecasts:** forecasts and outturns have separate fields and styles. Pin the selected forecast vintage. Use actual monthly profiles only when compatible with the outturn series; otherwise show the annual target separately. Record definitional/reclassification breaks and suppress a misleading difference.
- **Revisions:** an old period revised today is distinct from this month's new observation. Snapshot all changed relevant historical observations, not just the latest month. Do not claim that today's current-vintage history is what was known in the past.
- **Debt:** distinguish net debt, gross gilt liabilities, face value, indexed principal, market value and government/market holdings. Preserve source coverage. Face-value maturity profiles are not cash redemption forecasts for index-linked debt.
- **Index-linked gilts:** store nominal principal and indexation separately when available; show an explicit basis note. Use official redemption estimates or an explicitly modelled inflation assumption for cash projections; defer modelling to extensions.
- **Maturity:** calculate remaining contractual maturity from the snapshot date; use stated principal weights and exclude redeemed instruments. This is not duration or consolidated public-sector interest-rate exposure.
- **Rates:** keep coupons, fitted spot rates, auction yields and effective interest costs distinct. Preserve compounding conventions. Do not treat all yield measures as interchangeable.
- **Auction demand:** source-specific definition of cover; UK conventional auction tail is the accepted-price yield spread defined by the DMO, not a US-style when-issued comparison. Index-linked tail may be inapplicable. Cover is not investor identity or a standalone measure of confidence. Avoid double-counting post-auction allotments.
- **Events:** announcement, auction, settlement and redemption are different dates. Update postponements/cancellations by stable event identity; do not leave duplicate future entries. Unknown size remains unknown.

## 5. Architecture: small static application, scheduled preparation

Recommended defaults, adjustable by the lead if a simpler equally capable choice is documented:

- React + TypeScript + Vite for the static frontend; ordinary CSS variables and a small component set.
- One established chart library supporting responsive SVG and practical export; Recharts is a candidate. Validate its accessibility/export behaviour in the first chart before committing to it. No elaborate design system or canvas/WebGL stack.
- Python for data import and transformation, using standard HTTP/CSV/XML tools and spreadsheet dependencies only as required. Pin both JavaScript and Python dependency versions in reproducible lockfiles.
- JSON datasets and a small manifest served alongside the site. CSV generated from the displayed underlying data. No browser requests to ONS/DMO at runtime.
- Node-based UI tests and Python transformation tests; a small browser smoke suite. No monorepo framework, microservices, queue, Kubernetes, database service or runtime LLM.

Suggested layout (create files as needed, not empty scaffolding for every extension):

```text
src/                         pages, chart components, formatting, URL state
public/data/                 compact generated current datasets + manifest
pipeline/                    provider adapters, normalisation, validation, publish
catalogue/                   series/source definitions and category mappings
tests/fixtures/              small permitted source examples
tests/                       statistical/parser tests and browser smoke tests
docs/PROJECT_PLAN.md          this plan
docs/STATUS.md                milestone, next task, blockers and decisions
README.md                     setup, usage, refresh, recovery and deployment
.github/workflows/            checks, refresh and Pages deployment
```

Minimal data model:

- **Series:** id, label, source_id, unit, frequency, scope, accounting/valuation basis, seasonal adjustment, category/parent, methodology and coverage dates.
- **Observation:** series_id, period_start/end, value or null, status (outturn/forecast/provisional), publication date, vintage/source checksum. Forecast observations carry forecast vintage and target year.
- **Security:** stable identifier, name, instrument type, coupon, issue/redemption dates, amount and valuation basis, snapshot date.
- **Operation:** stable source id or reproducible composite key, operation type, dates, security id, status, announced/results fields and their units, source release id.
- **Release manifest:** schema version, source files and checksums, fetched/check times, publication dates where known, validation results, source statuses, application commit and data release id.

Do not fabricate publication timestamps if absent; retain retrieval timestamp and mark publication unknown. Provenance should let a reviewer trace a displayed figure back to a particular source file and calculation.

### Storage and vintages

Keep code, small fixtures and the catalogue in main. For local development, use a gitignored `data/archive/` for permitted raw changed source files and normalised snapshots, with content hashes to avoid duplication; keep small redistribution-permitted baseline snapshots in the repository so a fresh clone works. Before the hosted release, migrate and verify those local vintages into a dedicated `data-history` branch or the durable alternative below. Local archives are not multi-device storage or a backup. Keep only compact current data in the published bundle; do not download vintage archives in the browser.

Before backfilling, measure actual sizes. Do not repeatedly commit full large Bank of England ZIP archives; retain relevant permitted extracted inputs/deltas with the original download checksum and document the reproducibility limits. If projected archive growth is excessive, use compressed versioned GitHub Release assets with an index instead, and record the choice. Do not use expiring Actions artifacts or caches as the sole vintage archive. Respect repository/file/Pages limits and stay within free storage allowances; no paid LFS dependency.

## 6. Refresh, validation and deployment

For the local MVP, provide a single documented manual pipeline command and a local app start command; fetching remains in Python, not browser-side. Implement validation, provenance, local vintage capture and failure preservation now. The remaining scheduling, GitHub archival and deployment requirements in this section belong to the next hosted milestone.

Start with one daily scheduled run after the usual BoE publication window, plus `workflow_dispatch` for an owner-triggered run. A small number of additional release-day/auction-day runs can be added once source publication behaviour is tested. These are polling targets, not a real-time guarantee. Keep fiscal, annual and market source polling frequencies appropriate to their actual release cycles.

1. Fetch source inputs with timeouts, bounded retries and caching/conditional requests where supported.
2. Verify response types and parse to candidate datasets; an HTML error page must never be treated as a spreadsheet.
3. Run schema, date, coverage, reconciliation and revision checks. Large changes flag review rather than silently being deleted as outliers.
4. Persist changed inputs and normalised vintages durably before promoting candidates.
5. Promote a coherent fiscal release as a unit. Do not combine one new ONS component with old components from a failed parse. Independently updated debt/market groups may proceed with their own as-of labels.
6. On source failure, retain that group's last good data and publish an updated status if the workflow can still build. If the entire workflow fails, the existing site remains; browser-side age checks must still reveal overdue data.
7. Build once from a pinned code commit and validated data manifest; run checks; deploy via the official GitHub Pages Actions mechanism. Keep data release id and code commit visible in technical metadata.

Record per-source outcomes as successful-new, successful-unchanged or failed, with reason and timestamps. A partial publication may deploy validated retained data and updated status, but it must not conceal failed sources behind an all-green workflow. Preserve a failing source job or run a final health-report job that fails after deployment when a required refresh failed, so the owner's existing Actions notifications still work. No-new-release is a normal successful outcome.

Enforce supported schema versions in validation/build and handle an incompatible dataset visibly in the frontend. A code-only deployment must select an explicit validated data release and verify compatibility. Roll back a compatible code/data pair, not code alone against arbitrary latest data. Schema or compatibility failure leaves the existing deployment untouched; archive the small normalised bundles needed to reproduce deployed releases.

Use least-privilege job permissions: ordinary checks read repository content; only the archival job writes data history; only deployment gets Pages/id-token permissions. Untrusted pull-request jobs must not receive write credentials. Use the built-in GitHub token where sufficient; never put personal tokens into the frontend. Pin external Actions to reviewed immutable revisions and use routine dependency updates without enabling automatic unreviewed merges.

Do not depend on a commit made by GITHUB_TOKEN triggering another workflow. The refresh workflow should explicitly invoke a reusable build/deploy job or perform the deployment in its own dependency chain. Use concurrency control so refresh and code deployments cannot publish mixed or older bundles over newer ones.

Document UTC scheduling and London daylight-saving effects. GitHub schedules are best effort; public schedules may be disabled after 60 days without repository activity. Record/recover this condition in the runbook. Genuine data-history updates create repository activity; do not assume they remove every failure mode. The dashboard must calculate freshness from expected publication cadence, accounting for weekends/holidays and annual versus monthly releases. It should say "last checked" separately from "latest observation"; viewing the site does not trigger ingestion.

GitHub's existing workflow failure notifications and a visible freshness/status panel are enough for the hosted release. No PagerDuty, external monitoring subscription or 24-hour operational promise. The owner should be able to re-run a workflow and roll back to a known code/data release using documented steps.

## 7. UX and graphic design direction

Aim for a restrained academic briefing sheet: strong typographic hierarchy, readable numbers, generous but efficient spacing and charts that carry the information. Use system fonts, a neutral background, dark text, and a small colour palette. Do not invent Imperial branding or spend time on a logo, illustrations, animation, dark mode or marketing pages.

- Desktop: page title and freshness, four compact metrics, main chart, supporting chart, then collapsed detailed sections. Debt page follows the same component vocabulary.
- Mobile: one column; keep the headline comparison and main chart useful at 360 CSS pixels. Tables may scroll in their own region; the whole page must not scroll sideways.
- Label units and financial years directly. Make outturn solid and forecast dashed; colour is additional information, not the only distinction. Avoid red/green moral judgements about deficits.
- Ranked bars for composition; avoid pie/treemap interaction where precise comparison is the main task. Bar charts start at zero; any nonzero line-chart baseline must be obvious. No dual axes unless a specific need survives review.
- Show sensible defaults and few controls. Progressive disclosure for categories/methodology; no hover-only facts, tiny hit areas or unexplained acronyms. Define PSNB/PSND on first use or through accessible help.
- Error, empty, stale, loading and partially available states are part of the design. No fabricated zeroes, empty axes masquerading as data or endless spinners.
- Use semantic headings, visible keyboard focus, explicit input labels, sufficient contrast, a concise factual text summary and an accessible table for each chart. Target relevant WCAG 2.2 AA requirements; do not claim certification from an automated scan.
- Use at least 16px for main text; smaller chart/source text must remain readable. Aim for 44px touch controls where practical and satisfy the WCAG minimum target rules. Test 200% zoom and narrow-screen reflow.
- The exported chart must be independently legible: title, comparator/vintage, units, period, source and relevant caveat survive export, with no clipped labels.

Design oversight is two bounded reviews: an early rendered first-page prototype and the integrated local two-page app. A UX/graphic-design reviewer inspects actual screenshots and interactions at desktop and phone sizes and gives a short prioritised list. Test three tasks: identify latest borrowing versus its labelled comparator; inspect and download a tax breakdown; find the next auction and nearest major redemption. The builder resolves material issues; cosmetic preferences go to the backlog. No separate multi-week design phase or large design-system deliverable. Hosting requires a short regression check, not another full redesign review.

## 8. Delivery milestones and acceptance gates

Use these as work packages, not calendar promises. Data access is the main uncertainty. Update estimates after the source spike.

| Milestone | Work and concrete output | Acceptance / dependency |
| --- | --- | --- |
| M0: plan review | Independent sceptical review of scope, accounting, free hosting and failure modes; incorporate findings | Completion noted in STATUS; no unresolved issue that invalidates the approach |
| M1: source spike | Verified catalogue; small real fiscal/OBR slice; one DMO stock, calendar and results example; one BoE curve; annual composition sample | Local endpoints and reuse terms recorded; borrowing identity and forecast compatibility established; explicit fallbacks/blockers; optional early cloud-access check |
| M2: fiscal vertical slice | First page running locally from real data; provenance, tables, CSV and narrow-screen layout | Reproduces one official fiscal release; focused independent accounting/code review plus early design review |
| M3: local MVP | Complete two pages; debt features, annual composition, manual refresh, local vintages and start instructions | Core figures verified; failed-refresh handling checked; integrated code/data and design reviews; local completion checklist met |
| M4: hosted release | Cloud source-access verification, durable remote archives, scheduling, CI, Pages, chart export and runbook | Successful hosted refresh, simulated source failure, reproducible rollback path; focused independent automation review and deployed browser regression |
| M5: use and refine | Owner uses real dashboard for a release or comparable briefing exercise | Fix observed friction; log extensions; declare MVP complete only against checklist below |

M2 is the earliest useful preview. M3 is a valid MVP delivered locally; stop to let the owner use it and report the remaining hosted work separately. M4 fulfils the intended multi-device, automated deployment. M5 can occur after M3 or M4; do not block technical completion indefinitely waiting for the next monthly release—replay a saved release for acceptance and record that live-release feedback is pending. The local app does not need to run on the owner's phone yet: narrow-viewport testing verifies readiness, not multi-device access.

Keep one milestone checklist in `docs/STATUS.md`; use at most roughly 6–10 GitHub issues for substantive work packages or defects when useful. Do not duplicate every checklist item into an issue or establish sprint ceremonies. Maintain a short decisions section for material choices and deviations. Use small branches/PRs by milestone or coherent slice, with problem, resulting behaviour, validation and material limitations in descriptions. Routine implementation decisions belong to the lead; only real scope, privacy, cost or access blockers require user input. The user has already approved the public GitHub/free-hosting direction.

Keep documentation lean: README for practical instructions, this plan for scope and standards, and STATUS for the current handoff. Source metadata belongs in the machine-readable catalogue. Update these in place; do not create per-milestone reports, standalone review files, duplicate runbooks or decision logs. Record reviews in the relevant PR, or briefly in STATUS when no PR exists. Fold accepted recommendations into the plan/code, retain only unresolved actionable items in STATUS, and rely on Git history for past detail. Add another document only when a concrete need cannot be served clearly by these existing locations.

## 9. Agent use and independent review

One lead implementation agent owns integration, source contracts, progress and completion. Delegate only bounded tasks with useful parallel work; usually two active agents are enough, and three is a reasonable cap. Do not appoint a standing committee or recursively delegate.

Useful parallel assignments after M1: one provider adapter and its fixture tests; a UI component/page against an agreed JSON contract; or independent review while the lead works on documentation or unrelated fixes. State file ownership to avoid concurrent edits. Prefer branches/worktrees where supported; otherwise assign nonoverlapping files. Each handoff states inputs, expected output, acceptance criteria, files owned and unresolved assumptions.

**Sceptical plan review:** a separate agent checks whether the plan can work with actual public sources and free GitHub constraints, challenges economic definitions, identifies scope creep and looks for failure modes. It must identify evidence and remedies, not merely endorse the plan. This review precedes substantial implementation.

**Sceptical code/data review:** a reviewer who did not author the relevant slice reads the diff and tests, independently samples source-to-screen values and tries to falsify correctness. Priorities: incompatible accounting bases, forecast/vintage leakage, silent missing values, linker valuation, source drift, privilege mistakes, public data exposure, stale deployments and misleading chart labels. Use one focused review at M2, an integrated review at M3 and a narrow automation review at M4. These are bounded checks, not recurring full-project audits.

**UX/graphic review:** a separately tasked reviewer applies section 7 to rendered desktop/mobile views and actual controls. It may be the same separate agent used for another review if acting with a clear fresh brief, but not the author reviewing their own UI. An independent agent is useful quality control, not a claim of professional accreditation.

Record findings in the relevant PR, or briefly in STATUS when there is no PR: reviewed commit/artifact, severity, evidence/location, impact and recommended action. Lead records fixed / accepted with reason / deferred, then removes resolved detail from STATUS while retaining a one-line completion note. Fix incorrect figures, unreproducible core data, broken automation, secrets, inaccessible essential controls and unreadable primary charts before declaring the affected milestone complete. A second pass checks material fixes, not every cosmetic edit. User-facing review summaries should be a few sentences; no standalone review document is required.

## 10. Proportionate verification

Write tests for statistical transformations and failure modes rather than mirroring implementation details.

- Fixture parser tests for each provider; exercise schema drift, missing columns, revised old periods and non-data responses.
- Hand-calculated April/March financial-year boundaries, leap-year periods if relevant, missing-month rolling sums and sign conventions.
- Reconciliation against at least two real fiscal releases, including a revised period; tolerance is derived from published rounding, not an arbitrary large threshold.
- Forecast profile summation and same-coverage comparisons; incompatible or unavailable profiles produce an explicit unavailable state.
- Debt aggregation against a DMO total on the identical basis; known conventional and index-linked instruments; redeemed securities; maturity-bucket boundaries; principal-weighted maturity.
- Curve dates/tenors and missing points; no implicit extrapolation or confusion between forward and spot series.
- Auction duplicates, revised/cancelled dates, missing announced size, tail inapplicability and post-auction fields.
- Pipeline integration: corrupt download rejected, last good dataset retained, independent source groups dated correctly, rerun idempotent, archive exists before promotion.
- Local browser smoke (M3): both pages, deep links and reloads, keyboard controls, narrow layout, stale state, data tables and CSV. Test chart export if implemented.
- Hosted browser smoke (M4): repeat core interactions on actual GitHub Pages, including direct links/reloads under `/fiscal-space/` and mandatory chart export. A development-server pass does not prove Pages routing works.
- One automated accessibility scan plus manual keyboard/zoom/contrast and chart-label review. Test Chromium and a second engine, preferably WebKit for likely iPhone/iPad use.

Use fixtures for routine CI; keep scheduled live-source health checks separate so source outages do not turn every code PR red. Run lint, typecheck, relevant tests and production build once per meaningful change. Broaden testing when failures or new risks justify it. A sensible performance budget is a usable primary view within about three seconds on a throttled mobile test, a compact initial data payload (target below 1 MB compressed), and lazy loading of detailed/history datasets; measure and document tradeoffs rather than building a performance programme.

### Local MVP completion checklist (M3)

- [ ] Both agreed pages run locally using documented commands, at phone/tablet/desktop viewport widths.
- [ ] All twelve numbered page sections are present with real data; only the explicitly permitted optional fields/comparisons use labelled fallback states.
- [ ] Core displayed figures have independent source-to-screen checks and documented definitions.
- [ ] Forecast comparisons identify their vintage, basis and coverage; unavailable comparisons are honest.
- [ ] Annual composition and debt values name their denominators, periods and valuation bases.
- [ ] Core charts have usable tables and CSV; image/vector export is working or explicitly deferred to M4.
- [ ] Manual local refresh, local vintage capture and validation work with no paid dependency; a fresh clone has a usable permitted baseline dataset.
- [ ] A failed-source exercise preserves good data and produces understandable freshness information.
- [ ] Public bundle/repository contain no credentials or private material; source reuse is documented.
- [ ] Independent plan, code/data and design reviews have no unresolved material local-use defects.
- [ ] A new agent can follow README to run locally, refresh and recover the last good data.
- [ ] Owner receives exact start commands, the local URL, a short usage note and an honest list of remaining gaps.

### Hosted release completion checklist (M4)

- [x] All local criteria still pass; chart export is usable and includes provenance.
- [x] All three tabs work at the public Pages URL with direct navigation/reloads under the project path.
- [x] Scheduled refresh is configured; the same workflow succeeds when manually dispatched, with every source verified from the runner.
- [x] Local vintages have been migrated to durable remote archives and verified; no reliance on local disks or expiring artifacts.
- [x] Source-failure and workflow-failure scenarios retain valid data and reveal staleness.
- [x] Partial publication preserves failure notifications; code-only deploy and rollback enforce compatible code/data versions.
- [x] Independent automation/permissions review, deployed browser regression and rollback rehearsal pass.
- [x] Owner receives the hosted URL and concise maintenance instructions. Desktop and mobile browser layouts are verified; owner device checks can follow.

## 11. Future extensions: direction, not committed scope

Prioritise after real use. These do not need detailed tickets now.

| Extension | Intended value | Dependencies / cautions |
| --- | --- | --- |
| "What changed?" and historical information sets | Separate new observations, revisions and forecast changes; reproduce a past comment | Durable vintages, publication timestamps, accounting bridges; never reconstruct unavailable vintages as fact |
| Fiscal stance and rules | Current/primary balances, net investment, cyclically adjusted measures, rule definitions and OBR headroom | Forecast-specific rule versions and precise perimeter; output-gap uncertainty; headroom is not a real-time cash balance |
| Policy tracker | Budget/Spending Review measures, costings, announcement versus implementation dates | Dated official sources, human curation, separate policy effects from economic forecast changes |
| Financing bridge and remit | Borrowing to cash requirement to gross/net issuance, progress against remit | Financing adjustments, discounts/premia, bills, NS&I, redemptions and other funding; not simply deficit plus gilts maturing |
| Rich cash-flow calendar | Coupon payments, indexed redemptions, bills, syndications, post-auction options | Day-count/payment calendars, indexation assumptions and stable event identity |
| QT and consolidated rate exposure | APF holdings/sales/runoff, private-market absorption, reserves and Treasury transfers | Avoid double counting; distinguish cash transfers, accounting losses, accrued interest and consolidated exposure |
| Interest-cost sensitivity | Effects of yields, Bank Rate and RPI over time | Distinguish stock coupons from marginal financing rates; OBR ready reckoners or a validated model with explicit assumptions |
| Debt dynamics scenarios | Growth, primary balance, effective rates and stock-flow adjustments | Coherent nominal/real accounting and inflation assumptions; scenarios are not official forecasts |
| Richer composition | Real and per-capita spending, multi-year averages, departmental/function crosswalks | Appropriate deflators, population denominators, classification changes; avoid implying spending volume from a poor deflator |
| Market context | Real and inflation curves, OIS, holder distribution, auction comparisons | Source availability/reuse, RPI basis and risk/liquidity premia; no fabricated investor-level participation |
| International comparisons | Context for UK debt, deficit, revenue and interest burden | Comparable IMF/OECD/general-government definitions and release dates |
| Monetary policy module | MPC decisions, inflation/activity, rates and balance sheet | New scope after fiscal MVP; reuse provenance and chart infrastructure |
| Personal briefing tools | Saved dated snapshots, annotations, notifications and export packs | Public/private separation; cross-device private storage may change architecture and needs explicit agreement |

## 12. Start instructions for the implementing agent

1. Read README, this plan, current STATUS if present, and applicable repository instructions. Inspect Git status and preserve unrelated user work.
2. Check the review completion note in this plan or STATUS. Initial plan review is complete; do not repeat it merely because there is no separate review file. Arrange a new independent review only for a material change that warrants it.
3. Begin M1. Produce the verified catalogue and a reproducible small fiscal dataset plus representative debt/curve/composition samples. Establish actual source access and accounting identities before promising all fields.
4. Record any material source constraint and its proposed fallback. Continue unaffected work. Ask only where an answer is necessary for cost, privacy, access or a substantive scope decision.
5. Build M2 from real data, then obtain the focused independent accounting/code and design reviews. Mock values are allowed only in clearly marked tests/prototypes and must never ship as official data.
6. Deliver M3 as a local MVP using its checklist; describe M4 as the next separate milestone. Keep STATUS concise and current. Give the user meaningful progress updates, not logs of every tool call.

### Reference checks

Official source families above and the following platform/design references were consulted while planning on 6 September 2026. Recheck at implementation; discovery pages do not prove that each underlying file is automation-ready.

- [GitHub Pages limits and free public-repository availability](https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits)
- [GitHub Actions billing and usage](https://docs.github.com/en/actions/concepts/billing-and-usage)
- [Scheduled workflows and triggering restrictions](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows)
- [WCAG 2.2 quick reference](https://www.w3.org/WAI/WCAG22/quickref/)
- [DMO glossary: cover and tail](https://dmo.gov.uk/help/glossary/)

Platform policies and dependencies can change. Keep the zero-recurring-cost constraint explicit and report a conflict rather than silently introducing a paid service.

## Current plan: a concise overview and direct analytical tools

Execution status (10 September 2026): implemented and validated; publication uses the existing GitHub Pages workflow. Independent review findings were folded into the code and recorded in STATUS.md. The sections below retain the design intent and acceptance criteria; future source extensions remain deferred.

This plan supersedes the navigation and presentation requirements in TODO.md and the previous redesign mapping. The source definitions, safeguards and useful analytical capabilities remain. Implementation was authorised and completed in the subsequent execution turn.

### Purpose and design decisions

Serve two concrete tasks: onboard an economist who has not followed recent UK developments, and let an experienced user retrieve, compare and export a specific piece of evidence immediately. Organise the material around (1) the position and what changed, (2) the outlook and what supports it, and (3) financing costs and their transmission to the budget. Each detailed analysis has one home. The overview summarizes and provides direct links; it does not repeat the full analysis.

The independent review inspected both the implementation and rendered desktop/mobile pages. Its economic findings—not merely a checklist of the owner's UI observations—drive this plan: the headline mixes different periods and concepts; accounting levels do not explain changes; formal headroom is not comprehensive fiscal capacity; current spot yields are not the cost of the whole debt stock. The owner additionally wants spending and tax composition retained alongside a clear view of how both have changed.

### 1. Information architecture

Primary navigation: **Overview | Fiscal | Pricing | Debt & financing | Explore**.

| Destination | First thing shown | Deeper material |
| --- | --- | --- |
| Overview | Concise position statement and the evidence below | Direct links to the exact relevant analysis |
| Fiscal / Position | Receipts, spending and borrowing on a common period/basis | Monthly/YTD tracking, official profile surprise, accounting definitions |
| Fiscal / Composition | Spending / Taxes & receipts selector; current composition and history immediately open | Two-year contribution comparison, classifications, detailed tables |
| Fiscal / Outlook | Borrowing and debt paths, forecast boundary, vintage selector | Assumptions, stance, rules/headroom and official sensitivities |
| Pricing | Existing nominal, real and RPI curves with date comparisons immediately usable | Basis-point changes and methodology; preserve all current tools |
| Debt & financing | Debt stock, refinancing profile, issuance/redemptions and dates | Auctions, individual gilts, maturity/coupon definitions |
| Explore | Search and category browsing | Named fiscal series, derived analyses, tax-relief lookup, sources and methodology |

Keep fiscal subsections visible and directly bookmarkable. Provide a direct Composition link from Overview, alongside Pricing and Outlook. Preserve previous URLs as aliases, including pricing, debt, rules and relief detail links. Remove the generic Data introduction from specialist pages. A selected destination must show its content, not another closed disclosure.

### 2. Overview: a short economic briefing

The default experience should contain:

1. **One position statement:** current rolling-12-month borrowing, its change versus the comparable previous period, and dated debt/GDP. No separate card row repeating these exact figures. Label the flow period and stock date explicitly.
2. **Position evidence:** a receipts/spending chart on the same rolling-year basis, with the borrowing gap or a closely aligned borrowing panel. Default %GDP. Provide long-run context without overwhelming recent movements.
3. **Outlook evidence:** compact borrowing and debt small multiples, sharing the financial-year horizon, with an unmistakable actual/forecast boundary. Do not place the two vastly different magnitudes on a misleading common scale. One takeaway distinguishes falling borrowing from stabilising debt.
4. **What changed:** a short, data-derived description of the biggest spending/tax contribution changes, with a direct link to the composition comparison. Use complete financial years and state the comparison years; do not pretend annual composition is rolling-year data. Include one current borrowing-versus-profile statement when available.
5. **Market orientation:** a compact dated market summary and prominent “Pricing / compare dates” link. Determine during the first layout check whether a small curve provides more information than a few carefully labelled benchmark yields; do not automatically add both. The full Pricing tool is always one primary-navigation click away.
6. **Watch next:** the next relevant confirmed release, not a full news ledger. A brief outlook-rule note is allowed where it adds interpretation; no standalone headroom hero or generic risk grid.

Aim for meaningful plotted evidence within the first desktop viewport and the position/takeaway before charts on mobile. Use roughly two desktop viewports as a design budget, not a rigid pixel target that forces unreadable plots. The onboarding test is whether the user can explain the position, change and outlook in a few minutes—not whether every dataset appears on the page.

Remove the second full borrowing forecast chart, repeated stance/assumption/rule sections, full category rankings, generic risk paragraphs and long ledger from Overview. Specialist content remains accessible at its own destination.

### 3. Spending and tax composition: keep levels, add changes

Reuse BudgetHistory, annualBudgets, existing PESA history and the interest bridge. Do not create another parallel composition implementation.

The dedicated Composition view should answer three linked questions:

- **What is the budget made of?** Ranked current-year spending and tax/receipt breakdowns. Default %GDP; offer £bn and % of named total. Clearly identify the latest complete year.
- **How has that composition evolved?** A long-run component history in the same units, with stable category colours and the aggregate visible. Start with all available comparable annual history; provide focus controls. Avoid a mass of indistinguishable lines: allow category selection/highlight and retain accessible values/tables.
- **What explains the change between two years?** A ranked contribution chart/table. In %GDP mode, each contribution is category share in year B minus its share in year A, in **percentage points of GDP**. Include aggregate change and residual/rounding so the bridge reconciles. In £bn mode show amount differences; in named-total mode show percentage-point composition shifts, whose sum is zero apart from rounding.

Initial comparison: 2019–20 versus the latest complete financial year, explicitly described as a pre-pandemic reference rather than a steady state. Provide previous-year and freely chosen year comparisons. Use the latest year genuinely shared by the selected dataset and denominator; never silently substitute another year.

Preserve accounting boundaries:

- Economic spending is the main reconciled TME bridge; functional PESA spending uses TES and shows its TME bridge separately.
- Functional categories do not supply an independent pension/welfare/investment partition. Do not add overlapping categories or count debt interest twice.
- Distinguish taxes/NICs from total receipts, including non-tax income. Keep existing source approximations such as combined income tax/CGT labelled.
- Keep gross interest/dividends, net-interest proxies and OBR net interest explicitly distinct. A contribution is accounting attribution, not proof of a causal policy effect.
- Label classification breaks and gaps; keep fixed mappings only where justified by the source.

Overview should surface the largest relevant changes and link into this view with the selected years/units already set. It need not reproduce all rankings and histories.

### 4. Scales, axes and historical windows

Make %GDP the default for monetary fiscal aggregates, annual composition and relief costs. Provide one consistently placed **%GDP / £bn** control in fiscal analytical views, preserve it when moving between compatible views, and encode it in the URL. Composition may additionally offer % of named total. Show the chosen units on the chart and in exports; changing units must update the narrative, tables and comparisons together.

Exceptions follow the economic question: yields/real rates/breakevens in %, curve changes in basis points, maturity in years, concentration in % of gilt principal, cover as a ratio, and counts as counts. Preserve nominal contractual issuance/redemption amounts where useful. Do not convert future headroom using today's GDP: retain official £bn unless a correctly matched forecast denominator is available. Monthly/YTD flows divided by annual GDP are not annualised; these modes are investigative options, not the onboarding default.

Require ChartPanel to have an explicit meaningful X label and visible Y quantity/unit, also present in SVG exports. Audit custom rankings and maturity charts too. Use Financial year, Month, Maturity (years), or Category as appropriate; distinguish percent, percentage points and basis points. Keep outturn/forecast status visible without relying on colour alone; retain isolated observation markers.

| Analysis | Existing coverage | Window decision |
| --- | --- | --- |
| Monthly fiscal flows | April 2000 onward | Rolling-year context with All / 10y / 5y controls; no five-point YTD default |
| Annual borrowing/debt | 1990–91 onward | Keep long context, once per detailed analysis |
| Composition | Economic/revenue from available complete years; 23 functional years; five detailed snapshot years | Full comparable history by default; disclose genuine snapshot limits |
| Series explorer | Depends on selected monthly series | Derive first/last available dates; do not offer fictitious 1990 coverage |
| OBR stance/assumptions | 2024–25 to 2030–31 in imported tables | Label as a forecast window; no invented historical structural series |
| Monthly forecast tracking | Current fiscal-year official profile | Current-year cumulative is the correct default; no longer window for its own sake |
| Yield curves | One year of saved observation dates, full maturity span | Keep maturity span and event-date comparisons; longer observation history is a separate data-backfill task |
| Reliefs | Record-specific years and status | Full available comparable history, explicit gaps and forecast flags |

This pass does not depend on new source acquisition. Do not turn every time series into the longest possible chart irrespective of its purpose.

### 5. Expert access and reproducibility

Open Composition directly. Lead relief lookup with search, year, classification and results; retain rankings and ISA/pension stories as optional investigation. Remove unrelated automatically appended charts from series search and expose them as explicit choices.

Audit and persist meaningful view state in URLs: destination/subsection, series, units, transformation, date window, composition dataset and comparison years, forecast vintage, curve comparison dates, and relief selection/filters. Copied links, refresh and browser back/forward must restore the visible analysis. Reuse one small URL-state mechanism rather than separate implementations per page. Preserve existing export provenance and curve controls.

### 6. Implementation sequence and proportionate review

| Step | Work | Completion check |
| --- | --- | --- |
| 1 — Routes and removal | New navigation; one home per analysis; specialist wrappers removed; dedicated Composition open | Existing deep links still work; Pricing and Composition immediately reachable; no full duplicate overview charts |
| 2 — Shared chart/state contracts | Units, axis labels, proper windows, URL persistence | Numerical denominator/difference tests; labelled screen/SVG axes; copy/reload/back restore a selected analysis |
| 3 — Composition | Integrate snapshot, history and two-year changes using existing calculations | Spending and receipt bridges reconcile; unit toggles agree; classification/GDP gaps remain explicit |
| 4 — Overview | Assemble the compact economic sequence from existing data | A newcomer can explain position/change/outlook without reading specialist essays; no duplicate headline prose/cards |
| 5 — Independent check and publish | One bounded independent economic/editorial/UX review plus targeted regression | Resolve meaningful findings, run production-path checks, then publish through existing GitHub workflow |

Use the existing components and pipelines; no new hosting, redesign framework or feature family. Keep the review outcome in STATUS rather than creating another document. Request an independent agent for the bounded final task review; the implementing agent owns integration and fixes.

Task-based acceptance checks:

1. A new team member identifies the current deficit, debt trajectory and main changes, while distinguishing actuals from forecasts and accounting from causal explanations.
2. An expert opens a nominal/real/breakeven comparison directly, chooses dates and exports a labelled chart.
3. A user sees current spending/tax composition, compares two years in %GDP and £bn, and can identify which categories account for the total change.
4. A copied series/composition/forecast link restores exactly the selected analysis after reload and back/forward navigation.
5. Mobile layouts retain readable axes and essential caveats; keyboard controls, tables and exports work.
6. Old fiscal, pricing, financing and relief capabilities remain reachable; archived data, source failure protection and publication workflow remain intact.

Deferred data work stays explicit: longer curve archives, component-level monthly OBR profiles, matched real/per-capita series and richer policy-costing feeds. None should delay this editorial and interaction repair.
