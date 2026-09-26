# Experiments

## Select a representative benchmark

Start with the user's real task class and claimed improvement. Prefer recoverable project artifacts from before the relevant correction and the original outcome-level request. Do not replace a complex task with a toy whose brief already enumerates the solution. Preserve the representative sources of difficulty: dependencies, ambiguity, branches, state, audience constraints or factual synthesis. Match difficulty to the claim, not to project size; a focused real edit can be sufficient. Keep small synthetic checks for smoke tests and negative controls, not as the sole support for broad improvement.

Separate two experiments: replay the known defect to validate a regression test; independently produce or repair the deliverable from the earlier snapshot to measure instruction effectiveness. Replaying a historical fix does not establish that candidate instructions caused it. Both creator packets get the same starting bytes, original brief, tools, relevant baseline skills, budgets and permitted self-review. Only the candidate instruction differs. Record any reconstructed brief, adapted baseline or missing original artifact; never call a reduced instruction excerpt a full installed-skill comparison.

Do not leak later corrections, preferred outputs, fixed source, private tests, judge criteria or author rationale into creator inputs, including through version history, comments, inherited chat context or neighboring files. Keep legitimate user requirements; do not create difficulty by hiding information needed to solve the task. Record what each worker actually could access. Freeze output hashes before judging; preserve first-pass defects. If testing revisions, predeclare the same feedback and repair budget for both conditions and retain every version.

Keep a small benchmark catalog in the existing external learning ledger, not a parallel archive or client-specific skill. For each selected case record: stable ID, project/family, task class, source/permission scope, original request and starting artifact version/hash, reference outcome provenance, difficulty factors, metric, role (development/regression/held-out transfer/control), exposure history, and artifact locations. Capture only relevant authorized material; accepted outcomes are reference evidence, not necessarily the only valid solution.

When meaningful future project feedback is captured, consider adding a representative case or replacing a redundant one; do not turn every project into a benchmark or trigger an expensive rebuild automatically. Select a bounded suite before the run, covering the target behavior and already-good behavior across independent project families. For a cross-project improvement claim, require a separate, comparably demanding transfer family, preferably a real task; label synthetic transfer honestly. Renamed versions of one incident are not independent families. Once seen by the editor, transfer cases become development/regression cases; rotate in fresh cases rather than tuning indefinitely on the same project. Missing representative transfer evidence means hold the broad claim, not invent a win.

## Include the completed project as a reference

When an authorized completed project artifact is available, freeze its exact version/hash and evaluate three outputs for each benchmark project:

| Output | Comparison role |
|---|---|
| Fresh baseline | Existing instructions applied to the selected earlier starting artifact and original request. |
| Fresh candidate | Same starting artifact, request, tools and budget, with only the proposed instruction changed. |
| Completed project | Reference quality reached through prior iterations and user guidance; not an equal-effort experimental condition or an infallible answer key. |

Keep the completed artifact and later feedback out of both creator packets. First lock the blind baseline-versus-candidate judgment; then let the independent evaluator inspect the completed reference. Apply the same predeclared, task-relevant checks to all three, recording scope differences and unavailable checks. Do not penalize fresh outputs for features or requirements introduced only after the original request. Preserve the reference snapshot and live project unchanged.

Report instruction gain (candidate versus baseline) separately from each fresh output's gap to the completed reference, including preserved strengths and new regressions. Accept alternative designs that meet the goal better; do not reward imitation, visual similarity or extra features by default. Claim fewer corrections, lower effort or faster delivery only when comparable intervention/effort records were actually measured; closing a quality gap alone does not prove those savings. A completed reference from the same project does not create another independent task family or replace transfer evidence. If unavailable, run the paired comparison with an explicit missing-reference limitation rather than reconstructing a supposedly exact final artifact.

## Evaluate the produced artifact

Use the task's requested output as the evaluation unit:

| Task | Required evidence |
|---|---|
| Interactive product | Operate the built interface through ordinary visible controls; test end-to-end completion, branch/recovery behavior, state preservation and prerequisite boundaries. Model/unit tests supplement but do not establish browser usability. |
| Code or data workflow | Run the produced code on representative inputs; check outputs, invariants and failure/recovery behavior. |
| Writing, strategy or presentation | Compare actual drafts, sourced analysis or rendered artifacts against purpose, audience, factual support and preservation constraints—not outlines of what would be written. |
| Planning or evaluation design | Inspect the actual plan/protocol and its fitness for execution; a plan is valid evidence when it is itself the requested deliverable. Do not claim it proves downstream execution quality. |

Use an independent operator/judge who has the task facts but not condition identities. Record observed completion, intervention, errors, regressions and effort using predeclared measures; track actions/time only if actually measured. Distinguish executed, failed, blocked, not applicable and not tested. If the required browser/runtime/source is unavailable, report the missing evidence and hold relevant claims rather than substituting a plan and calling it an end-to-end test. Give the user the actual paired outputs and traceable result summary, not only scores; publishing or sharing artifacts requires its own task authorization and must not modify the live source project.

## Freeze before generation

Write a protocol specifying hypothesis, task class, target measure, baseline/current file hashes, candidate hash/diff, dependencies, fixed case IDs/categories, critical failures, tolerated regressions, model/effort (unknown if unobservable), facts, attempts and budgets. Record date and execution IDs. Freeze meaningful thresholds before results; do not tune them to a desired verdict.

Default small pilot: at least one historical failure, historical success, variant, unseen transfer and negative control; add an adversarial/edge case when relevant. Predeclare a meaningful target and transfer improvement in completion, preservation, quality or workload; require those concrete wins with no material regression. This minimum is a screening gate, not statistical proof. For consequential or variable behavior, predeclare repeat runs and confirmation on fresh transfer cases. Record all runs, including failed generation and bad outcomes. No selective reruns.

An independent test designer should create holdouts and acceptance criteria without the editor's patch rationale. In a shared workspace, minimal-context instructions provide procedural isolation, not a security sandbox. Workers must read only their assigned packets and not shared rationale, mappings, other outputs or criteria. If contamination occurs, discard the claimed holdout status and create new cases. Where the project requires enforced holdout isolation, procedural shared-workspace isolation is insufficient for release; label results exploratory.

## Run and blind

Use fresh minimal-context creator executions with identical raw requests and runtime constraints. Only instructions under comparison differ. Evaluation actions must be local-only: no publication, messaging, purchases or live system edits. Do not invoke a workflow whose mandatory external action conflicts with isolation; use its supplied instructions as data in a controlled task instead. Label that as instruction-content simulation, not actual skill invocation/composition. Require separate trigger and dependency checks when those behaviors change.

The blind judge receives requests, source facts, acceptance criteria, inspected raw outputs and anonymized A/B order randomized per case. Do not reveal version mapping, patch rationale, creator scores or promotion target. Require exact evidence locations and a tie/uncertain option. Check word limits, arithmetic, links, state transitions or rendered output objectively where applicable. Calibrate with a known defective output and an equivalent-output control; for consequential close decisions reverse order or use a second fresh judge. Disagreement holds or triggers a predefined tie-break; never average away a critical failure.

Same-model separation reduces context bias, not correlated model error. Human preference is still needed for authentic personal voice. Model identity and hidden system instructions may be unobservable; report that limit. Prefer artifacts and measured task outcomes over numeric fluency ratings.

## Interpret

List every case, pairwise outcome, objective pass/fail, regression, source and limitations. Ties are no measured gain. A failed baseline and successful candidate on the original case is insufficient without transfer. If both already succeed, consider no patch, a smaller resource change, or a new measurement—not an invented superiority claim. Changes after final testing invalidate that version's result.

Keep run artifacts and protocol in the external experiment bundle. The gate validates declared records and hashes; a trusted coordinator must corroborate provenance, order isolation, source truth, and whether the metrics represent the user's goal. Do not treat self-authored JSON as independent evidence.
