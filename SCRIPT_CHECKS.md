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
- Existing learning-loop ledger, scheduled jobs and promotion policy were read but not modified. This is authorized infrastructure bootstrap, not evidence of a learned behavior improvement.

Independent infrastructure review found and verified fixes for unregistered source additions, failed rollback cleanup, interruption recovery, and concurrent edits during staging. Its final bounded verification passed all 12 regression tests with no remaining blocker in that scope.
