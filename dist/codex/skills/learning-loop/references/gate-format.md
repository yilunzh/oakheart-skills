# Read-only experiment gate format (schema version 1)

Run from the skill directory:

```sh
python -B scripts/gate.py validate /path/to/experiment/experiment.json --current-baseline-sha256 ACTUAL_CURRENT_SNAPSHOT_SHA256
python -B scripts/gate.py monitor /path/to/observations.json
python -B -m unittest discover -s scripts -p 'test_gate.py' -v
```

The commands only read inputs and print JSON. They never edit a skill, promote a candidate, record approval, or mutate monitoring state. Exit 1 means `hold`; exit 0 means a recommendation or monitoring report, never authorization. Supply the current live skill snapshot digest before any promotion; omitting it supports offline review only and does not establish that the live baseline is current. Use the same deterministic snapshot format for baseline, candidate, and current skill, covering every relevant file, path, and byte.

Every artifact is a nonempty raw file beneath the experiment directory, including the frozen protocol, full baseline/candidate snapshots, case inputs, complete paired outputs, raw judge outputs, source evidence, and exact patch. Symlinks escaping this directory are rejected. Record SHA-256 of actual bytes. Never invent missing runs, raw artifacts, timestamps, or judgments to satisfy this format.

## Experiment object

Required fields:

| Field | Value |
| --- | --- |
| `schema_version` | `1` |
| `artifacts` | Object mapping unique reference IDs to `{ "path": "relative/path", "sha256": "64 lowercase hex characters" }` |
| `protocol_ref`, `baseline_ref`, `candidate_ref` | IDs in `artifacts` |
| `started_at` | ISO 8601 timestamp with timezone |
| `creator_execution_id` | Actual nonempty creator execution ID |
| `thresholds` | Exact copy of frozen protocol thresholds |
| `diff_category` | Exact copy of frozen protocol category |
| `user_protected`, `behavioral_change` | Explicit booleans; uncertain classifications must not be reported as false |
| `hypothesis`, `patch`, `dependencies`, `risks`, `rollback`, `diff_attestation` | Each `{ "rationale": "concrete description of at least 12 characters", "evidence_refs": ["artifact-id"] }` |
| `provenance` | `{ "source": "concrete source description", "captured_at": "dated ISO timestamp", "evidence_refs": ["source-id"] }` |
| `cases` | One paired case record for every frozen protocol case, with no duplicates or extras |

The exact patch artifact and its attestation must establish the category; a declaration alone is not evidence of safety. `nonbehavioral_reference_addition` and `test_addition` can yield `eligible_for_human_review` only when both protection/behavior flags are false. Every other category, any behavioral change, and any protected behavior yields `eligible_requires_approval` after passing evidence checks. Neither status permits writing on its own. Every result has `release_ready:false`; human calibration, blinded human preference labels, access-separated holdout enforcement, and fresh-session activation remain mandatory release gates in the existing workflow. A structural pass cannot replace or waive them. Dependencies and risks with none identified still need a concrete assessment and evidence references; do not use empty values or vague placeholders.

## Frozen protocol artifact

Store this separate JSON artifact before executing either version. Record its hash in the experiment manifest and retain a trustworthy external freeze receipt or history.

```json
{
  "frozen": true,
  "frozen_at": "2026-09-20T11:00:00Z",
  "baseline_sha256": "<actual baseline artifact SHA-256>",
  "candidate_sha256": "<actual candidate artifact SHA-256>",
  "thresholds": {"target_wins": 1, "transfer_wins": 1},
  "diff_category": "behavioral_change",
  "edge_required": false,
  "edge_rationale": "Explain concretely whether boundary behavior is touched.",
  "cases": [
    {
      "id": "failure-1",
      "category": "historical_failure",
      "bucket": "target",
      "input_ref": "failure-1-input",
      "conditions": {
        "model": "actual pinned model/version",
        "tools": [],
        "budget": 2000,
        "environment": "actual environment snapshot"
      },
      "label_to_version": {"A": "candidate", "B": "baseline"},
      "presentation_order": ["B", "A"]
    }
  ]
}
```

This excerpt is not a passing protocol: add independent cases covering `historical_success`, `variant`, `transfer`, and `negative_control`; add `edge` if applicable. Historical successes and negative controls use `guard`; only transfer-category cases use `transfer`. Historical failures, variants, and edges may use `target` or `guard`. Set both thresholds to integers of at least one before execution. Freeze assignment and presentation order per case, preferably counterbalancing across cases. Preserve identical inputs, model, tools, budget, environment, and other relevant conditions between the two runs. Declare random seeds and sampling policy in `conditions` when relevant.

## Paired case record

```json
{
  "id": "failure-1",
  "baseline": {
    "output_ref": "failure-1-baseline-output",
    "full_output": true,
    "conditions": {"model": "actual pinned model/version", "tools": [], "budget": 2000, "environment": "actual environment snapshot"},
    "started_at": "2026-09-20T12:00:00Z",
    "execution_id": "actual-baseline-execution-id"
  },
  "candidate": {
    "output_ref": "failure-1-candidate-output",
    "full_output": true,
    "conditions": {"model": "actual pinned model/version", "tools": [], "budget": 2000, "environment": "actual environment snapshot"},
    "started_at": "2026-09-20T12:00:00Z",
    "execution_id": "actual-candidate-execution-id",
    "objective_pass": true,
    "critical_failures": []
  },
  "judge": {
    "execution_id": "actual-separate-judge-execution-id",
    "presentation_order": ["B", "A"],
    "seen_labels": ["A", "B"],
    "identity_hidden": true,
    "raw_ref": "failure-1-raw-blind-judgment",
    "rationale": "Specific observed difference, with exact evidence in the two outputs.",
    "evidence_refs": ["failure-1-baseline-output", "failure-1-candidate-output"],
    "outcome": "win",
    "regression": "none"
  }
}
```

The judge receives only blinded outputs and the scoring rubric, not the identity mapping, creator's preferred answer, or expected winner. Keep the raw blinded judgment before decoding `outcome` relative to candidate (`win`, `tie`, `loss`). The case IDs link runs to the frozen inputs. The full protocol may contain additional rubric, expected invariants, freeze receipt, and tool receipts; these are necessary review evidence even where the script does not interpret their contents.

Any unknown or ambiguous outcome holds. Any loss or regression classification other than `none` holds. Ties do not count toward target or transfer wins. Missing pair, required category, concrete references, independence IDs, matched conditions, or complete artifacts holds. Each candidate run requires explicit `objective_pass:true` and `critical_failures:[]`; missing, unknown, failed, or nonempty values hold. All baseline/candidate generator execution IDs must differ from the editor (`creator_execution_id`). All judge execution IDs must differ from the editor and every generator across the entire experiment, including other cases. Unknown model provenance holds as exploratory-only evidence.

Example passing behavioral recommendation:

```json
{"status":"eligible_requires_approval","wins":{"target":1,"transfer":1},"authorization":false,"release_ready":false,"pending_release_gates":["human_calibration","blind_human_preference_labels","access_separated_holdout","fresh_session_activation"],"limitation":"Hashes and execution IDs cannot authenticate self-attested provenance, independence, blinding, or diff classification."}
```

## Monitoring object

```json
{
  "promotions": [
    {"correction_id":"correction-17","skill":"skill-name","version_id":"promoted-v2","promoted_at":"2026-09-21T12:00:00Z"}
  ],
  "observations": [
    {
      "observation_id":"actual-unique-observation-id",
      "correction_id":"correction-17",
      "skill":"skill-name",
      "task_class":"editing",
      "eligible":true,
      "observed":true,
      "result":"correction",
      "version_id":"actual-observed-active-version-or-unknown",
      "observed_at":"2026-09-22T12:00:00Z",
      "evidence":"Specific transcript location and observed recurrence."
    }
  ]
}
```

Use `success`, `correction`, or `unknown`. An eligible opportunity is a task where this particular correction could be tested. An observed opportunity has an inspected outcome; absence of feedback is not success. Unknown observed outcomes remain in the opportunity denominator and have their own count. Unobserved or ineligible tasks do not enter the denominator. Identical observation IDs deduplicate; conflicting copies hold. Invocation counts never enter this metric.

`counts` is an array grouped by correction ID, skill, task class, and observed version; `aggregate` separately totals those observed opportunities. `observed_correction_rate_lower_bound` divides corrections by all eligible observed opportunities (including unknowns); it must not be read as a success rate. `confirmed_outcomes_correction_rate` divides corrections only by corrections plus explicit successes. A zero denominator yields null.

Promotions require known `skill` and `version_id` as well as correction ID and date. Recurrence matches the correction and skill, then compares the observed version with the latest preceding promotion. A matching version returns `reopen`; missing, unknown, or mismatched/old versions return `attribution_pending` while retaining a contextual reopened event. Each event contains correction, skill, task class, observed version, promoted version, and observation ID. An unrelated skill cannot reopen or blame another skill's promotion. Old-version observations can reopen the investigation but cannot establish regression in the promoted version. These reports request investigation and do not change any record automatically.

## Trust boundary

This gate validates local byte integrity and declared relationships. It cannot authenticate an LLM's self-attested freeze timestamp, authorship, independence, complete-output claim, semantic evidence, blind execution, or diff classification. A fabricated but internally consistent record can pass. Inspect raw execution receipts, independent judge context, source provenance, exact diff, scoring rationale, and external freeze history before treating eligibility as meaningful. Missing or unverifiable evidence requires hold even if structural validation passes. Editing the frozen protocol and recalculating every hash cannot be detected without a separately trusted freeze record. This limitation is not a reason to fabricate an external receipt or to treat structural validation as authorization.
