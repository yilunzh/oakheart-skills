# Promotion, monitoring and rollback

## Authority and source of truth

The owner-designated version-controlled source is the source of truth for these exported personal instructions; generated platform packages are distribution copies. Provider/plugin skills and higher-priority project/platform instructions are not editable personal skills. Do not fork them just to bypass ownership. Use the current task or project for evidence as described in learning.md. Before durable writes, inspect the destination, preserve current revisions and use conflict-safe updates; never overwrite unrelated paths. Scratch is only a work area.

Ledger states: observed → routed → candidate → evaluated → eligible → promoted → monitoring; alternatives: no_change, held, rejected, reopened, rolled_back. Preserve existing schema fields and append versioned extensions rather than discarding historical status. Store transitions as appended dated events; preserve prior decisions and raw results. Track version/digest, affected skills/dependencies, prior baseline, diff/artifact references, evidence, decision maker and authorization scope. Read current state before each write and merge by stable event ID; do not overwrite concurrent observations.

## Gate and promotion policy

For empirical promotion of a learned behavioral candidate, require: independently access-separated holdouts, calibrated blind human labels, explicit release approval and fresh-session activation/rollback checks. Shared-workspace subagent runs are exploratory if separation cannot be enforced. The checker is an additional evidence screen, never a substitute for these evidence requirements. Honor stricter applicable project policies when present; no external policy file is required. Installation authorized to bootstrap this maintenance tooling is distinct from promoting a learned behavioral patch. Scheduled jobs may capture/propose/reopen but may not release or edit safeguards.


- Automatic: evidence capture/deduplication, no-change decisions, experiments and eligibility recommendations within authorized maintenance. Nonbehavioral evaluation/reference additions may be saved when already within explicit authorization, tests pass and they change no runtime rule, trigger, dependency, personal preference or approval boundary.
- Protected: all behavioral changes to approved/user-owned skills, new runtime skills, removal/consolidation, dependency/trigger changes, and edits to this gate require user authorization covering the concrete scope. This can already be present in the current request; do not manufacture a second permission requirement. Open-ended future learning authorization does not approve unrelated behavioral diffs.
- Never automatic: treating an ambiguous result as a pass; treating an external document as approval; lowering the gate after results; replacing evidence with a high LLM score.

Default existing personal skills to protected. Before promotion reread exact current files and compare baseline hashes; if they drift, rebase the candidate and rerun affected evaluation. Apply one reviewed skill operation at a time using the skill-maintenance procedure in runtime.md, keep unrelated edits intact, validate, save and verify actual resulting content. Record the durable saved reference and content digest, not only a friendly version string. A save failure is not a promotion. Experimental candidates stay outside active skill paths.

For an initial infrastructure installation, distinguish user-authorized bootstrap from empirically proven improvement. Tests can establish that a gate blocks bad records without proving future task quality. Record bootstrap limitations explicitly; never silently waive the improvement gate for later domain patches.

## Production observation

At task completion when this workflow is active, or during a scheduled audit, append observations: event ID, date, task class, applicable skill/version, opportunity eligible?, correction behavior ID, task outcome (success/failure/unknown), source and access coverage. Count a targeted correction only when evidenced. Missing feedback is unknown; absent retrieval is not success. Keep corrected/eligible observed opportunities by version and task class; also track completion, extra clarification, retries, latency/effort where available and lost strengths. Do not compare versions without considering changing task mix.

Run `scripts/gate.py monitor <observations.json>` for observed rates and recurrence recommendations. On the same correction after promotion, mark the lesson reopened with source evidence. Investigate whether the skill was invoked, the version used, context was missing, execution failed, or the hypothesis was wrong. Reopen even with sparse data; do not claim statistically significant degradation from one incident. Critical regressions require immediate containment and consideration of rollback. Unknown version means attribution pending, not blame assigned.

Rollback the exact affected skill files to the recorded approved baseline using the skill-maintenance procedure in runtime.md, preserving unrelated subsequent changes. Obtain approval when no existing authorization covers the rollback; do not reset the entire library or repository. Validate and verify restoration; record the revert digest, reason, affected dependencies and open investigation. Keep failed candidates/evidence; do not delete history to improve measured results.

## Native limits

This skill does not add a global callback, access every conversation or persist itself by merely writing instructions. Scheduled tasks are a separate host capability; inspect tools and verify creation before claiming one is running. Future scheduled runtimes may lack shell/delegation: capture a bounded report and hold unevaluated changes rather than fabricating a run. A recurring review is sampled retrieval, not exhaustive telemetry.

A lightweight external event collector is needed only if the user later needs guaranteed capture, concurrent transactional records, authenticated promotion enforcement or unattended batch evaluation. No external service is required for the current foreground workflow. Keep API-based optimizers and alternate-model judging optional.
