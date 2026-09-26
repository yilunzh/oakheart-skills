# Agency operations

Use one client record with source references. Save runtime records and deliverables through Library unless they belong to an existing externally synced project. Keep client personal data and secrets out of this reusable skill; store secret references rather than credentials. Inspect live records before updates and preserve unrelated edits.

| Stage | Owner | Output and exit evidence |
| --- | --- | --- |
| Qualify | Prospecting + measurement | Buyer, fit, capacity, economics, actual baseline or explicit gap; distinguish prospect fit from guarantee eligibility |
| Research | Customer/niche researcher | Sourced buyer brief, offer facts, objections, incumbent strengths and friction |
| Design | Conversion strategist | Scoped journey, complete content, visual direction, hypotheses and measurement specification |
| Build | Product/integration engineer | Working scoped artifact, implementation notes and functional evidence |
| Release | Independent QA | Current-version acceptance evidence, migration/recovery plan, authorized release |
| Measure | Experiment owner | Reconciled outcomes, agreed decision rule, uncertainty and guardrails |
| Operate | Client success + revenue operations | Support record, outcome report, maintained workflows and prioritized improvement |

Agency operator owns dependencies, deadlines, scope, capacity, invoice preparation and founder attention. Demand generation owns acquisition. Evaluation owner maintains tested improvements. These are execution roles, not eleven always-on services.

Handoffs contain client ID, task, stage, sources, output reference, version, acceptance evidence, unknowns, action authorization and next owner. Mark blocked work explicitly and proceed with independent ready work. Document existence alone is not completion.

The JSON dossier is a starter shape, not a substitute for the actual brief or agreement. Add evidence under the check ID used by `agency_checks.py`, with `status: verified`, `artifact` (accessible evidence reference), `observed_at` (ISO date/time), `reviewer`, and `release_id` for build/release checks. Preserve failed/unknown records as such. The qualify checker covers performance-offer evidence; its failure does not forbid ordinary prospect research or an authorized prototype. Inspect the referenced evidence before assigning verified status.

## Onboarding and economics

### Resolve consequential decisions before expanding

For substantial new work or a material change in direction, form a compact working brief from available evidence: buyer/user, current process and strengths, specific gap, offer or intended outcome, differentiation and proof where relevant, next action, and approved constraints. Separate confirmed decisions from assumptions and open choices. Reuse the client record; do not create a second brief or ask the user to repeat known facts.

Resolve consequential uncertainty with a recommendation and a small concrete example. When competing directions would materially change the result, explain their tradeoff and recommend one. Ask only when the choice needs the user's judgment or missing facts; proceed autonomously on routine, reversible choices. Do not invent facts to avoid a question or require approval for every brief.

When direction is uncertain and expansion would create substantial rework, produce a representative slice first: for example, a headline, substantive section and next action, or one end-to-end software workflow. Check the riskiest assumption before extending it. Share the slice for a consequential user choice when needed; otherwise evaluate it and continue. Skip this step for settled direction, bounded edits or explicitly requested complete drafts. A slice is an intermediate artifact, not a reason to leave the authorized task unfinished.

Before building, challenge the proposal from the user's perspective: why does this matter, what do they already do, why is the proposed improvement worthwhile, and what effort must they spend before receiving value? Include existing software, capable staff and workarounds when supported. Distinguish ordinary rules or integration work from any incremental AI contribution. Preserve necessary eligibility, safety and fulfillment inputs; do not assume fewer steps is always better.

After meaningful feedback, record the accepted decision, its scope and rationale, what it supersedes, and strengths to preserve in the existing client record. Apply it to affected work in the same pass. Distinguish a changed user preference from an implementation miss; do not turn project-specific feedback into a universal skill rule. Keep isolated edits local unless they change a shared decision or promise.

Assemble available facts before asking questions. Collect only what changes the next deliverable:
- Business/site identity, owner, region, target buyers and priority programs/rentals.
- Actual prices, dates, seat/car/instructor capacity, eligibility, policies, approved proof and media rights.
- Analytics/booking/CRM access, baseline, conversion definitions, sales cycle and qualification rules.
- Platform/domain/code ownership, integration access, staff routing, support owner and release authority.
- Scope, covered fees, success agreement, third-party costs, maximum test duration, handoff and support terms.

Defaults are proposals: one niche, two concurrent builds, reusable web components and bounded revisions/support. Honor user changes. Determine whether the project replaces booking, improves its front end or captures leads; never silently change this choice.

Track founder hours, costs, rework, unpaid pilot exposure, collectible fees, acquisition effort and support load. Distinguish booked from collected fees. Model contribution with explicit assumptions including founder time; do not invent prices or win rates. Give the founder decisions with recommended actions and consequences.

Apply existing authorization to communications, spending and publishing. Use recipient resolution before person-directed actions. Client promises and production actions need actual authorization, not an inferred permission from this workflow’s existence.

## Continuation and scheduling

Read latest durable state each run. Use client/task IDs, expected input version, completion evidence and stop conditions. Re-read before conflicting writes; merge or stop. Reconcile uncertain side effects against their external IDs before retrying.

For an explicitly authorized schedule, demonstrate a live read and useful manual run using the required tools, then verify a scheduled run before calling it operational. Cloud tasks need durable connected inputs, not scratch paths. Limit transient read retries to two; mutation retries require idempotency or readback. Report access failures as blocked; do not replace live evidence with memory. Keep production transactions in reliable application workflows and use agents for bounded tasks and exceptions.
