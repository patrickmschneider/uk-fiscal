# Planning review record

Date: 6 September 2026.
Artifact: `docs/PROJECT_PLAN.md`, initial handoff plan. No application code exists yet.

## Independent UX / graphic-design planning advice

Reviewer: separately tasked `design_review` agent, independent of the plan author.
Scope: proportionate design process and acceptance criteria; no rendered application was available or reviewed.

Recommendations incorporated:

- Two bounded design reviews: early real-data layout and integrated local app; a short regression check after hosting.
- Restrained typography/colour/spacing conventions instead of a separate design-system project.
- Visible reference periods and comparison labels; consistent line styles; ranked composition bars and an auction table.
- Accessible data tables, text summaries, keyboard/touch controls, contrast and narrow-screen/zoom checks.
- Three task-based checks: inspect borrowing versus a labelled comparator; open and download a tax breakdown; find the next auction and nearest major redemption.
- CSV mandatory locally; shared image/vector export may move to the hosted milestone if it would delay useful local delivery.
- Misleading economic comparisons and unusable core controls block completion; cosmetic improvements go to the backlog.

Design advice does not constitute visual approval or accessibility certification. Actual app reviews remain required at M2 and M3.

## Independent sceptical plan review

Reviewer: separately tasked `sceptical_plan_review` agent, independent of the plan author.
Status: completed; four actionable findings incorporated. The reviewer found no approach-invalidating accounting or architecture error. This is a plan review, not verification of actual source series or working code.

| Severity | Finding | Disposition |
| --- | --- | --- |
| Medium | Required page sections versus optional source fields were ambiguous | Fixed: section 2 explicitly requires every numbered page section, lists permitted field/comparison fallbacks, and mirrors this in M3 acceptance |
| Medium | A successful partial deployment could mask a source failure and suppress workflow failure notifications | Fixed: section 6 separates per-source outcomes and requires a failing source/health job even when valid retained data can be deployed |
| Medium | Code-only deployment and rollback lacked enforced code/data schema compatibility | Fixed: section 6 requires explicit data release selection, schema checks and rollback of a compatible pair; failed checks preserve the existing deployment |
| Low | General browser/export requirements conflicted with a local MVP | Fixed: section 10 explicitly assigns local checks to M3 and deployed project-path/export checks to M4 |

The lead checked that these changes were reflected in scope, milestones and completion checklists. No unresolved plan blocker remains. M1 must still establish exact source availability, accounting mappings and reuse permissions.
