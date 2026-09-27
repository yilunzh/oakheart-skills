# Local verification — 2026-09-26

- Source preservation: 44 files matched recorded SHA-256 hashes.
- Package structure: 10 generated skill folders, 5 individual chat ZIPs, and 1 JSON plugin manifest passed local checks.
- Relative Markdown references: 62 checked, no missing files.
- Learning-loop checker: 26 existing unit tests passed on the generated Code package.
- Agency checker: 8 existing unit tests passed on the generated Code package.
- No Claude CLI is installed here. Claude import, native plugin validation, automatic invocation, connector access, and behavioral parity have not been tested.
- No PTC, AutoNation, or Oakheart task comparisons were run during this export.

These checks establish file preservation and limited local executable compatibility. They do not demonstrate improved or equivalent model behavior.

Independent static review inspected source preservation, generated packages, dependencies, and installation instructions. It found no blocker in the generated Linux packages. Findings about source inventory checks, manifest counts, optional reviewer namespace, portable path formatting, full adaptation diffs, archive fidelity, and failed-rebuild preservation were addressed. A deliberate source-inventory failure confirmed that the previous distribution remains intact. Windows rebuilds have not been executed on Windows.

Follow-up independent static review verified all four final fixes on current bytes with no remaining findings in that scope. It did not rerun failure injection or execute Claude.

Version 0.1.1: removed the optional skill and regenerated distributions. Structure, exact ZIP contents, 44 retained source hashes, and 62 relative links verified. The 34 helper test results above are from the previous run; retained helper source bytes are unchanged.

## Shared-source infrastructure — version 0.2.0

- One shared source now generates 15 skill folders across three targets, five individual chat ZIPs and one Claude plugin.
- All 44 shared source files and 93 relative links verified. The source normalization moves the existing platform adaptation into shared instructions; original snapshots remain in Git history.
- Two successive builds produced identical file hashes. Release receipts cover source, adapter and build-tool identity plus every generated file.
- Reran all 34 learning-loop and agency helper tests on the Codex distribution: passed.
- Twelve new infrastructure tests passed: initial install/idempotence, local edit refusal and unrelated preservation, unmanaged name collision, Claude plugin installation, missing-file refusal, failed-update rollback, symlink/managed-host refusal malformed receipt paths, unregistered source additions, interrupted updates, edits during staging and concurrent installers (some tests cover multiple cases).
- No model benchmark or native Codex/Claude activation was executed. Local temporary installation tests are not account installation.
- At version 0.2.0, existing learning records, scheduled jobs and promotion policy were read but not modified. This is authorized infrastructure bootstrap, not evidence of a learned behavior improvement.

Independent infrastructure review found and verified fixes for unregistered source additions, failed rollback cleanup, interruption recovery, and concurrent edits during staging. Its final bounded verification passed all 12 regression tests with no remaining blocker in that scope.

## Project-context cleanup — version 0.2.1

Removed AutoNation-specific strategy/application context and PTC prospect/booking constraints from reusable references. Preserved the removed text as separate private project notes outside the package. General working preferences and motorsport research guidance remain. Client context is retrieved only for the relevant task. This is a user-directed content correction, not a claimed learned behavioral improvement or native runtime benchmark.

## Portable runtime and evaluation repairs — version 0.3.0

- Removed the fixed external-repository/ledger dependency from learning-loop, all generated runtime references and contribution documentation. Retained the skill, historical records and explicit evidence/promotion safeguards. Existing schedules were not modified.
- Made runtime loading conditional; clarified copy and strategy triggers; replaced vendor-specific commercial dependencies with available capabilities; aligned strategy review to task size and two defect-driven cycles.
- Added fresh experiment and grading IDs, frozen plugin/task/harness snapshots, model and CLI provenance, raw traces and error retention, invalid-run exclusion, expected-pair accounting, order-sensitive verdicts and unsupported-claim checks.
- All 56 local tests passed: 34 existing helper, 12 installer, 10 evaluation-harness tests. The harness integration test used a mock CLI, not a model.
- Independent static review verified fixes for missing judgments, malformed streams and judging implementation identity. No remaining blocker within that review's scope.
- One fresh-agent exercise produced correct six-month pricing economics and a plain email without unsupported customer claims. This was a bounded exploratory check, not a matched benchmark or evidence of Claude performance.
- No Claude executable is available in this build environment. Native routing, reference access, reviewer execution, output quality and current performance remain untested.

## Agency claim and default rules — version 0.3.1

- software-delivery-agency now defaults pending money, terms or legal decisions to the narrower reversible option, and states founder experience, clients or capabilities only when supplied (PR #4).
- Claude Code 2.1.283, restricted headless, 3 runs per condition against v0.3.0: candidate preferred in 6 of 12 blind order-combined pairs, baseline in 1, 5 order-sensitive, no critical failures. Candidate defaulted to new bookings only in 6 of 6 refund-change runs. Synthetic tasks, model-graded, no human calibration.
- Claude chat, Cowork and Codex behavior untested.
