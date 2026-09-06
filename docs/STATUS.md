# Project status

Updated: 6 September 2026.

## Current state

- Public repository created and connected to the local project folder.
- Detailed implementation plan written in [PROJECT_PLAN.md](PROJECT_PLAN.md).
- Independent design-planning advice and four sceptical plan-review findings incorporated; see [review record](reviews/PLAN_REVIEW.md).
- No application, source adapters, data snapshots, workflows or deployment yet.

## Milestones

- [x] M0: planning and independent review complete.
- [ ] M1: source discovery, definitions and representative real-data validation.
- [ ] M2: first fiscal page working locally with real data.
- [ ] M3: reviewed two-page local MVP with manual refresh and vintage capture.
- [ ] M4: hosted release with automated refresh and durable remote archives.
- [ ] M5: owner feedback and refinement (can begin after M3).

## Next bounded task

Begin M1 after checking the plan review record. Produce `docs/DATA_SOURCES.md`, a small machine-readable catalogue, a reproducible fiscal/forecast sample and representative debt, curve and annual composition samples. Verify actual official downloads and redistribution terms; reconcile the fiscal measures on a common accounting basis. Report specific blockers and feasible fallbacks without stopping unaffected work.

Do not start scenarios, policy tracking, website embedding or elaborate design infrastructure.

## Decisions

- Hosting destination: public GitHub Pages; automation: GitHub Actions; no recurring paid services.
- Local-only MVP is acceptable and is the first completion gate. Hosting is the next separate milestone.
- Existing personal website and domain are outside scope.
- Two local pages, with detailed breakdowns progressively disclosed.
- Preserve vintages from the first real-data collection, initially locally with a documented remote migration at M4.
- Independent reviews are bounded milestone checks; one lead remains responsible for integration.

## Unknowns requiring implementation evidence

- Exact fiscal series mappings, source schemas, comparability and history.
- Current-year OBR monthly profile availability and compatibility.
- Reliable DMO automated downloads and permitted redistribution.
- Market-data source reuse terms and cloud-runner access.
- Actual data size and the simplest durable remote vintage storage choice.

No user input is currently needed to start source discovery.
