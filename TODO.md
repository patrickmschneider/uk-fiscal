# The Fiscal Space — Master Redesign & Implementation Brief

You are redesigning and extending the existing UK fiscal dashboard at:

https://patrickmschneider.github.io/uk-fiscal/?page=fiscal

The product is being renamed:

# The Fiscal Space

The objective is not simply to add more charts. The existing dashboard should be restructured into a coherent, narrative-driven tool for understanding and monitoring UK fiscal policy.

The target user is an economist who understands macroeconomics but may not have followed UK fiscal developments closely over the past several months.

Imagine briefing a smart new member of an economics team.

The dashboard should answer, in sequence:

1. Where are we?
2. How did we get here?
3. What is driving the fiscal position?
4. What is fiscal policy actually doing to the economy?
5. What does the official forecast say happens next?
6. What assumptions does that forecast depend on?
7. Is incoming data consistent with that forecast?
8. How much room does the Chancellor have?
9. What could change the picture?
10. What has changed recently, and what should we watch next?

The core product philosophy is:

> **Brief me first. Let me investigate second.**

The landing experience should therefore be curated and opinionated. Comprehensive datasets and less-important charts should remain accessible through deeper pages and a Data Explorer rather than competing for attention on the main page.

---

# A. PRODUCT / BRAND

Rename the product everywhere:

# The Fiscal Space

Suggested subtitle:

**Understanding the UK fiscal position, outlook and risks.**

Alternative shorter subtitle where space is limited:

**A guide to the UK public finances.**

The design should feel like a serious economics/policy research product rather than a generic BI dashboard.

Prioritise:

* editorial hierarchy;
* typography;
* whitespace;
* excellent charts;
* restrained use of colour;
* clear distinction between actuals and forecasts;
* clear distinction between official data and derived calculations;
* excellent source/provenance information.

Avoid excessive cards, borders, widgets, decorative UI, gauges and dashboard clutter.

---

# B. TOP-LEVEL INFORMATION ARCHITECTURE

Use approximately:

**Briefing | Outlook | Fiscal Rules | Tax Reliefs | Data**

The default destination should be **Briefing**.

The main Briefing page tells the fiscal story.

The deeper pages provide analytical detail.

The Data section acts as the investigation/data-explorer layer.

Do not organise the primary user experience simply around datasets or government institutions.

---

# C. THE BRIEFING — COMPLETE STRUCTURAL OVERHAUL

Reorganise the current fiscal material into the following narrative.

---

## 1. THE FISCAL POSITION IN 60 SECONDS

Purpose:

Allow a knowledgeable user to understand the current UK fiscal position within approximately 15–30 seconds.

At the top provide a dynamically generated summary sentence along the lines of:

> The UK is running a deficit of X% of GDP, with debt at Y% and debt-interest spending elevated. The OBR expects borrowing to fall over the forecast, leaving £Zbn of headroom against the fiscal rule.

Generate this deterministically from underlying data/templates rather than using an LLM.

Below it show only four primary headline indicators:

### Borrowing

£bn and/or % GDP

Question answered:
**How much is government currently borrowing?**

### Debt

% GDP

Question answered:
**What debt stock has accumulated?**

### Debt interest

£bn, % GDP and/or % revenue

Question answered:
**How costly is servicing the debt?**

### Fiscal headroom

£bn

Question answered:
**How much room remains against the binding fiscal rule?**

Each indicator should include the most economically useful comparison, such as:

* previous year;
* previous OBR forecast;
* historical average;
* previous fiscal event.

Do not fill the opening screen with secondary metrics.

---

# 2. HOW DID WE GET HERE?

Purpose:

Give the historical context necessary to understand today's fiscal position.

Hero chart:

## UK borrowing — history and OBR forecast

Show borrowing as % GDP over a sufficiently long period, ideally approximately 1990-present plus OBR forecast.

Clearly distinguish:

* outturn;
* forecast.

Annotate only major episodes:

* Global Financial Crisis;
* post-2010 consolidation/austerity;
* COVID;
* energy shock;
* major recent fiscal events where relevant.

Second major chart:

## UK public debt — history and OBR forecast

% GDP, same broad historical horizon.

The intended narrative is:

**persistent deficits + large shocks → accumulated debt → current fiscal constraints.**

Avoid excessive annotation.

---

# 3. WHAT DRIVES THE DEFICIT?

Before showing detailed revenue and expenditure charts, establish the accounting relationship.

Create a visual decomposition:

**Receipts**

minus

**Primary spending**

minus

**Debt interest**

=

**Borrowing**

Use current/latest fiscal-year values.

Then allow the user to investigate each side.

### Where does the money come from?

Show major receipts:

* Income Tax;
* National Insurance contributions;
* VAT;
* Corporation Tax;
* other major receipts.

Prefer a ranked bar / composition chart over a pie chart.

### Where does the money go?

Show major expenditure categories such as:

* health;
* pensions;
* welfare;
* education;
* defence;
* public investment;
* other departmental spending;
* debt interest.

Use the most coherent official classification available and document it.

The user should understand the aggregate before seeing detailed components.

---

# 4. WHAT IS FISCAL POLICY ACTUALLY DOING?

Purpose:

Separate the **level of borrowing** from the **fiscal stance**.

Explain briefly:

> The deficit tells us the fiscal position. Changes in the structural primary balance tell us more about whether fiscal policy is becoming expansionary or contractionary.

Include where robust official data allow:

### Primary balance

### Structural / cyclically adjusted primary balance

### Fiscal impulse

Define fiscal impulse explicitly and document the sign convention.

Preferred calculation:

change in the cyclically adjusted/structural primary balance, with the visualization transformed so that the interpretation of positive/negative expansion/contraction is immediately clear.

Show:

* history;
* current estimate;
* OBR forecast.

Also provide supporting measures such as:

* real government spending growth;
* tax/revenue changes;
* discretionary policy measures where official decomposition exists.

Do not create false precision where the OBR does not provide enough information.

---

# 5. WHAT HAPPENS NEXT?

Visually transition from observed fiscal data into the **OBR forecast world**.

Make the distinction between actual and forecast unmistakable.

Start with:

## The OBR expects borrowing to...

Show borrowing actuals + forecast.

Then explain **why borrowing changes over the forecast**.

Build a decomposition / waterfall where official data permit:

**Current borrowing → forecast-end borrowing**

with contributions from:

* receipts;
* primary current spending;
* investment;
* debt interest.

Then:

## Debt trajectory

Show actual + OBR forecast debt/GDP.

The section should explain the official fiscal strategy rather than merely reproduce OBR charts.

---

# 6. WHAT DOES THE FORECAST ASSUME?

Purpose:

Expose the macro assumptions underneath the fiscal forecast.

The fiscal outlook depends particularly on:

### Real GDP growth

### Nominal GDP growth

### Inflation

### Wages / earnings

### Bank Rate

### Gilt yields / interest-rate assumptions

Where possible compare:

**OBR forecast | latest outturn | current consensus/market information**

The objective is to let users identify cases where incoming macroeconomic information is moving away from the assumptions embedded in the fiscal forecast.

This should become an important bridge between macro news and fiscal implications.

Use official or high-quality sources and clearly identify non-official consensus/market data if introduced.

---

# 7. IS THE PLAN ON TRACK?

This should eventually become one of The Fiscal Space's signature features.

Incoming fiscal data should be interpreted relative to the latest OBR forecast/profile.

Create:

## Receipts vs OBR profile

## Spending vs OBR profile

## Debt interest vs OBR profile

## Borrowing vs OBR profile

Most importantly create:

# Cumulative borrowing surprise

Conceptually:

actual borrowing year-to-date minus borrowing implied by the contemporaneous/latest appropriate OBR profile.

Where feasible decompose into:

* receipts surprise;
* primary spending surprise;
* debt-interest surprise;
* other;
* resulting borrowing surprise.

Use cumulative fiscal-year values where appropriate.

Make the sign convention extremely obvious.

For example:

> Borrowing is £Xbn higher than implied by the OBR profile so far this fiscal year.

or:

> Borrowing is £Xbn lower than implied by the OBR profile.

Preserve forecast vintages so this comparison is historically reproducible.

Do not compare historical actuals against a forecast that was published after those actuals became known.

---

# 8. HOW MUCH ROOM DOES THE CHANCELLOR HAVE?

Only after explaining the fiscal position and forecast should the dashboard introduce the fiscal rules.

Provide:

# Current fiscal rules

For each rule show:

1. plain-English description;
2. formal definition;
3. target year;
4. current OBR margin/headroom;
5. whether the rule is met.

Then make the binding-rule headroom prominent:

# £Xbn headroom

Contextualise it.

Show:

## Headroom at successive fiscal events

Budget / Autumn Statement / Spending Review / other relevant OBR forecast events.

Preserve historical forecast vintages.

Then, where robustly implementable using official OBR sensitivities, add:

## How sensitive is the headroom?

Possible shocks:

* gilt yields;
* nominal GDP;
* productivity;
* inflation;
* other OBR-published sensitivities.

Do not invent elasticities.

Use OBR sensitivities/scenarios wherever possible.

The point is to communicate that fiscal headroom is a forecast residual and can be small relative to normal forecast errors.

---

# 9. WHAT COULD CHANGE THE PICTURE?

Create a compact:

# Risks to the outlook

Organise around:

### Growth risk

latest information relative to OBR assumptions.

### Interest-rate risk

market rates/yields relative to forecast assumptions.

### Inflation risk

including implications for indexed debt and spending where relevant.

### Receipts risk

recent receipts performance relative to profile.

### Spending risk

recent spending/debt-interest performance relative to profile.

If directional indicators such as:

**UPSIDE | NEUTRAL | DOWNSIDE**

are used, they must be generated by explicit transparent rules.

Do not have an LLM subjectively classify fiscal risk.

---

# 10. WHAT CHANGED — AND WHAT SHOULD I WATCH NEXT?

Finish the briefing by turning it into a live policy-monitoring tool.

## Since the last OBR forecast

Maintain a chronological ledger of important developments.

Possible categories:

* macro data;
* fiscal outturn;
* interest rates;
* policy announcements;
* tax changes;
* spending announcements;
* OBR/HMT changes.

Suggested schema:

`date`
`event`
`category`
`description`
`likely_fiscal_channel`
`source`

Where a quantified official policy costing exists, include it.

Do not create unofficial numerical fiscal impacts unless explicitly labelled as our own estimates.

Then:

## Next things to watch

Fiscal/macro calendar including:

* ONS Public Sector Finances;
* CPI;
* labour-market releases;
* GDP;
* Bank of England decisions;
* OBR forecasts;
* Budget / fiscal events;
* relevant HMRC releases.

The conceptual endpoint of the briefing should be:

**Here is the fiscal position → here is what could change it → here is what to watch next.**

---

# D. UX PATTERN THROUGHOUT THE BRIEFING

Every major section should follow:

### 1. Takeaway

One sentence explaining the economic point.

### 2. Evidence

One principal visualization.

### 3. Explanation

Short supporting text / secondary visualization.

### 4. Investigation

Optional deeper material / link to Data Explorer.

Example:

> ## Debt interest is consuming a larger share of government resources.
>
> [principal chart]
>
> **Why it matters:** higher financing costs reduce the resources available for other spending and can reduce headroom against the fiscal rules.
>
> Explore debt interest →

Design for three users simultaneously:

**5-minute user:** headlines only.

**15-minute user:** headlines + charts.

**Expert user:** can drill into series, definitions, vintages and source data.

---

# E. FORECAST VINTAGES — IMPORTANT CROSS-CUTTING FEATURE

Do not overwrite historical forecasts.

Build the data architecture around vintages.

For major variables retain successive OBR forecasts for:

* borrowing;
* debt;
* receipts;
* spending;
* debt interest;
* GDP;
* nominal GDP;
* inflation;
* wages;
* interest rates;
* fiscal-rule headroom.

Enable charts such as:

## How has the borrowing forecast changed?

Budget A → Autumn Statement → Budget B → latest → actual.

This allows decomposition of changes into:

* economic/forecast changes;
* policy changes;
* classification changes;
* outturn surprises,

where OBR data provide those decompositions.

The key analytical principle is:

> Preserve what policymakers knew and forecast at each point in time.

---

# F. DERIVED ANALYTICAL SERIES

Where underlying official data support them, calculate and document:

### Fiscal impulse

Change in structural/cyclically adjusted primary balance.

### Revenue buoyancy

Revenue growth relative to nominal GDP growth.

### Real spending growth

### Real per-capita spending growth

### Interest burden

Debt interest / government revenue.

### Debt snowball

Conceptually:

(r − g) × lagged debt ratio

with precise implementation documented.

### Fiscal forecast surprise

Actual minus contemporaneous official forecast/profile.

### Revenue surprise

### Spending surprise

### Debt-interest surprise

### Policy vs economic decomposition

Only where official OBR forecast-change decompositions allow this robustly.

Every derived series must have:

* formula;
* source series;
* frequency;
* transformation;
* sign convention;
* update logic.

Never make a derived estimate appear to be an official OBR/ONS/HMRC statistic.

---

# G. DEBT / FINANCING ANALYTICS

Expand the existing debt treatment beyond debt/GDP.

Where official data are available include:

* gross/public-sector debt measure used in fiscal analysis;
* relevant net debt measure;
* debt/GDP;
* debt interest;
* debt interest/GDP;
* debt interest/revenue;
* effective interest rate on debt stock if robustly derivable;
* average maturity;
* refinancing profile;
* index-linked share;
* relevant government cash/liquid-asset position;
* 2y/5y/10y/long gilt yields;
* real gilt yields where useful.

Create a debt-dynamics explainer around:

Δd ≈ ((r − g)/(1+g))dₜ₋₁ − pb

where:

d = debt/GDP
r = effective nominal interest rate
g = nominal GDP growth
pb = primary balance/GDP

If implemented numerically, document exact definitions and approximations.

Do not present this as the official OBR debt identity unless it exactly matches their accounting.

---

# H. TAX RELIEFS — NEW FIRST-CLASS MODULE

Add:

# Tax Reliefs

This module should demonstrate that fiscal policy operates through the tax system as well as through explicit expenditure.

Use official HMRC estimates.

Do not construct our own counterfactual tax-expenditure model.

Canonical source:

**HMRC Tax Relief Statistics**

Also use:

**HMRC Private Pension Statistics**

for richer pension analysis.

---

# I. TAX RELIEFS — CONCEPTUAL RULES

Maintain strict distinction between:

### Official expenditure

### Estimated cost of tax relief

### Potential revenue from reform

These are not interchangeable.

Never:

* add tax reliefs to official expenditure;
* add them to PSNB;
* describe them as additional borrowing;
* imply that abolishing a £10bn relief raises £10bn.

Persistent caveat:

> **Tax relief cost ≠ revenue available**
>
> HMRC's estimates measure tax relieved under its methodology. They generally do not represent the Exchequer gain from abolition because behavioural responses, interactions and wider economic effects may differ.

If an actual reform has an official HMT/HMRC/OBR policy costing, that may be shown separately as:

**Official policy costing**

with policy specification and forecast vintage.

---

# J. TAX RELIEFS — DATA MODEL

Preserve HMRC's classifications.

HMRC distinguishes:

### Non-structural reliefs

Reliefs designed to advance economic or social objectives.

### Structural reliefs

Features integral to the tax system or definition/calculation of the tax base.

Do not create our own classification.

Import where available:

`relief_id`
`relief_name`
`tax_head`
`classification`
`tax_year`
`estimated_cost`
`estimate_status`
`claimant_count`
`objective`
`notes`
`methodology_quality`
`publication_vintage`
`source`
`retrieval_date`

Missing/withheld/unavailable estimates must remain missing/withheld/unavailable.

Never turn them into zero.

---

# K. TAX RELIEFS — PAGE STORY

The Tax Reliefs page should answer:

**How big?**

↓

**Which reliefs?**

↓

**Which taxes?**

↓

**How has the cost changed?**

↓

**Who benefits?**

↓

**Why has it changed?**

↓

**What does the number actually mean?**

Do not begin with the full HMRC table.

---

# L. TAX RELIEFS — HEADLINE

Show the latest HMRC aggregate for costed non-structural reliefs, but label the coverage precisely.

Do not write:

> Total cost of UK tax reliefs: £Xbn

unless HMRC actually defines the statistic that way.

Use something like:

> **£Xbn**
>
> Estimated cost of non-structural reliefs with available multi-year estimates, 20XX/XX

Explain that other reliefs may have:

* single-year estimates;
* no reliable estimate;
* estimates withheld for disclosure reasons.

The aggregate is therefore not necessarily the cost of every UK tax relief.

---

# M. TAX RELIEFS — MAIN VISUALIZATIONS

## Largest tax reliefs

Ranked horizontal bar chart.

Default:

* latest appropriate year;
* non-structural;
* top 15–20;
* £bn.

Controls:

**£bn | % GDP**

Filters:

**All | Income Tax | NICs | VAT | Corporation Tax | Capital taxes | Other**

Calculate ranking dynamically from imported HMRC data.

---

## Reliefs by tax head

Aggregate cost by tax head.

Prefer horizontal/stacked bars to pie charts.

---

## Evolution through time

For reliefs with comparable multi-year estimates:

**£bn | % GDP**

Make clear when aggregate coverage changes because HMRC's available estimates change.

Do not interpret coverage changes as economic changes.

---

# N. TAX RELIEF DETAIL PAGES

Clicking a relief should show:

# [Relief]

**Estimated cost**
**% GDP**
**Tax head**
**HMRC classification**
**Latest year**
**Estimate status**

Then:

### What is it?

HMRC description/objective.

### How large is it?

Historical £bn / % GDP.

### Who benefits?

HMRC distributional information where available.

### Why has it changed?

HMRC commentary where available.

### How reliable is the estimate?

HMRC methodology/quality metadata.

### Could abolishing it raise this amount?

Explain why cost-of-relief estimates are not policy costings.

Always source the data.

---

# O. FEATURED TAX-RELIEF STORY — ISAs

Create a particularly good detail experience for:

# Individual Savings Accounts

Import HMRC's official annual estimated tax-relief cost.

Show:

## Estimated cost of ISA tax relief

**£bn | % GDP**

Where official data permit, separately show:

* number of ISA holders;
* subscriptions;
* ISA wealth;
* income distribution;
* age distribution.

Surface HMRC's explanation for changes in the estimated cost.

Do not independently estimate the tax cost.

---

# P. FEATURED TAX-RELIEF STORY — PENSIONS

Pensions require special handling.

Use:

1. HMRC Tax Relief Statistics for consistency with the cross-relief comparison;
2. HMRC Private Pension Statistics for detailed Income Tax/NIC analysis.

Do not treat differently defined pension estimates as interchangeable.

Explicitly label each measure.

Where HMRC supplies data, show:

* Income Tax relief;
* NIC relief;
* tax on pension income where relevant to the stated net measure;
* contribution mechanism;
* DB/DC;
* public/private sector;
* marginal Income Tax rate.

Do not construct our own lifetime present-value estimate.

---

# Q. “BEYOND THE BUDGET” EXPLAINER

After the receipts/expenditure section of the main Briefing, add a bridge:

# The Budget isn't the whole story

Explain:

> Government can pursue policy objectives through the tax system as well as through explicit expenditure. HMRC estimates the cost of hundreds of tax reliefs, including pension, ISA, VAT and capital-tax reliefs.

CTA:

**Explore tax reliefs →**

Optionally create:

## Spending through the Budget — and through the tax system

Two clearly separated columns:

**PUBLIC EXPENDITURE**

vs

**TAX RELIEFS**

Allow magnitude comparisons between selected programmes and reliefs.

Never sum the columns.

Explicitly explain that these are different accounting concepts.

---

# R. DATA EXPLORER

Build/retain a comprehensive investigation layer.

Every chart on the briefing should be backed by inspectable data.

Data Explorer should allow:

* series search;
* category browsing;
* charting;
* transformations;
* source metadata;
* CSV download where appropriate.

Useful transformations:

* level;
* YoY;
* % GDP;
* real;
* real per capita;
* fiscal-year cumulative;
* difference vs OBR forecast;
* share of receipts/expenditure where meaningful.

Only enable transformations that are economically coherent for the series.

Suggested hierarchy includes:

Fiscal Accounts
→ Receipts
→ Spending
→ Borrowing

Debt & Financing

OBR Forecasts

Fiscal Rules

Macro Assumptions

Tax Reliefs
→ Structural / Non-structural
→ Tax head
→ Individual relief

---

# S. SOURCE AND PROVENANCE

Every chart must clearly identify its source.

Prioritise official sources:

* OBR;
* ONS;
* HM Treasury;
* HMRC;
* DMO;
* Bank of England.

Where market/consensus/private data are used, identify them explicitly.

Every series should store:

`source`
`source_url`
`release/publication`
`publication_date`
`data_vintage`
`last_retrieved`
`units`
`frequency`
`seasonal_adjustment`
`forecast/outturn status`
`notes`

Do not conflate:

**publication date**

with:

**data last checked by The Fiscal Space**.

---

# T. DATA PIPELINES

Prefer machine-readable official sources over scraping HTML.

General pipeline:

**fetch → validate → normalise → compare with previous vintage → store → derive → build**

Validation should detect:

* schema changes;
* renamed series;
* missing observations;
* revised history;
* forecast-vintage changes;
* unexpected frequency changes;
* large revisions;
* newly added/deleted tax reliefs;
* classification changes.

Do not silently accept broken source schemas.

Store raw source files/vintages where practical so results remain reproducible.

---

# U. FISCAL CALENDAR / POLICY LEDGER

Create reusable structured datasets for:

## Fiscal calendar

Schema approximately:

`date`
`event`
`institution`
`type`
`url`
`importance`

and:

## Policy ledger

`announcement_date`
`measure`
`tax_or_spending`
`description`
`fiscal_cost`
`cost_period`
`temporary_permanent`
`start_date`
`legislative_status`
`official_source`
`forecast_vintage`

Only include quantified costs when an official costing is available, unless clearly labelled otherwise.

Eventually allow:

**Announced but not yet implemented measures**

to be aggregated separately from fiscal outturn.

---

# V. CHART DESIGN RULES

The dashboard should have a consistent visual grammar.

### Actual vs forecast

Use the same convention everywhere.

### £bn vs % GDP

Where both are economically useful, offer a simple toggle.

### Fiscal years

Label consistently.

### Recessions/shocks

Use sparingly and consistently.

### Annotations

Only annotate economically important episodes.

### Tooltips

Include:

* exact value;
* period;
* units;
* actual/forecast;
* source where appropriate.

### Titles

Prefer analytical/question titles:

**Is borrowing falling?**

or:

**Borrowing is forecast to fall sharply**

over generic titles such as:

**PSNB**

Series names can appear as subtitles/metadata.

Charts should answer questions.

---

# W. EDITORIAL RULES

Use plain English without dumbing down the economics.

Define specialist concepts on first use:

* primary balance;
* structural balance;
* fiscal impulse;
* headroom;
* tax expenditure/relief;
* debt snowball.

Distinguish clearly between:

**fact**

**official forecast**

**derived calculation**

**interpretation**

Do not use AI-generated prose to create untraceable factual claims.

Dynamic takeaways should preferably be deterministic templates based on data.

---

# X. MOBILE / RESPONSIVE UX

The narrative briefing must work on mobile.

On narrow screens:

* four-column KPI layouts become stacked/two-column;
* charts retain readable axes;
* tables become horizontally scrollable or transform into cards;
* chart annotations should reduce automatically;
* navigation should remain simple;
* primary takeaway must appear before visualization.

Do not require hover to understand essential information.

---

# Y. METHODOLOGY

Create a proper Methodology/Data Notes destination.

For every derived metric document:

* definition;
* formula;
* official input series;
* transformations;
* frequency conversion;
* GDP denominator where applicable;
* treatment of forecast years;
* vintage selection;
* known limitations.

Particularly document:

* fiscal impulse;
* structural balance;
* debt snowball;
* cumulative OBR surprise;
* tax-relief aggregates;
* % GDP conversions.

The dashboard should be suitable for academic/policy use, so reproducibility matters.

---

# Z. IMPLEMENTATION PRIORITIES

Do not attempt to build every new feature simultaneously.

## Phase 1 — Information architecture

1. Rename to The Fiscal Space.
2. Create new navigation.
3. Reorganise existing charts into the Briefing narrative.
4. Remove/relegate redundant charts.
5. Implement section takeaway → evidence → detail pattern.
6. Standardise chart styles, actual/forecast treatment and source presentation.

The product should already feel dramatically better after this phase.

## Phase 2 — Core fiscal analytics

Implement:

1. 60-second snapshot.
2. historical borrowing/debt narrative.
3. receipts/spending decomposition.
4. primary/structural balance and fiscal impulse.
5. OBR outlook.
6. macro assumptions.
7. fiscal rules/headroom.
8. expanded debt-interest analytics.

## Phase 3 — Real-time OBR tracking

Implement:

1. forecast vintages;
2. receipts vs profile;
3. spending vs profile;
4. interest vs profile;
5. borrowing vs profile;
6. cumulative borrowing surprise;
7. forecast-revision history.

Treat this as a high-priority differentiating feature.

## Phase 4 — Tax Reliefs

Implement:

1. HMRC ingestion;
2. overview/rankings;
3. tax-head composition;
4. historical series;
5. ISA detail;
6. pension detail;
7. Beyond the Budget bridge;
8. Data Explorer integration.

## Phase 5 — Live policy monitoring

Implement:

1. fiscal calendar;
2. policy ledger;
3. since-last-OBR timeline;
4. risks dashboard;
5. upcoming-events module.

---

# AA. DEFINITION OF SUCCESS

Do not judge the redesign primarily by the number of charts or datasets.

A successful version should allow a new economist to visit The Fiscal Space and, within approximately five minutes, answer:

1. How large is UK borrowing?
2. How high is debt?
3. Why is the government borrowing?
4. Is fiscal policy tightening or loosening?
5. What does the OBR expect to happen?
6. What macro assumptions underpin that forecast?
7. Is the latest data running ahead of or behind the OBR forecast?
8. How much fiscal-rule headroom remains?
9. How fragile is that headroom?
10. What developments could change it?
11. What are the major fiscal choices embedded in the tax system?
12. What data/releases should I watch next?

An expert should then be able to drill down and inspect:

* underlying series;
* transformations;
* forecast vintages;
* methodologies;
* official sources;
* downloadable data.

The finished product should feel less like:

> **“Here is a collection of UK fiscal data.”**

and more like:

> **“Here is the current UK fiscal story, why it looks this way, what the official forecast expects, whether that forecast is on track, how much room policymakers have, and what could change next.”**

That is the central product idea behind **The Fiscal Space**.

---

# FINAL INSTRUCTION

Before implementing, audit the existing repository and current deployed dashboard against this specification.

Do not blindly rebuild components that already work.

Produce an implementation plan mapping:

**existing component/chart/data source → retain / modify / move / replace / remove**

and:

**new requirement → required data → proposed component → implementation complexity**

Then implement incrementally, preserving working functionality and existing useful data pipelines wherever possible.

When a requested metric cannot be produced robustly from available official data, flag it rather than inventing a methodology or silently substituting a different concept.

Accuracy, provenance, interpretability and narrative hierarchy take priority over feature count.
