# Improving and releasing skills

`source/` is the shared source for all five skills. Change the workflow there when it should apply everywhere. Put host tools, storage and reviewer execution differences in `adapters/`. Generated packages are delivery copies.

## Make a change

1. Fetch current `main`, preserve any local work, and start a branch for one change. Record the baseline commit and installed version if the feedback came from a running skill.
2. Read the affected skill, its dependencies and the learning-loop policy. Explain the problem, expected improvement, counterexample and possible regressions. For learned changes, retain the candidate and evidence with the current task or authorized project.
3. Edit source or adapters. For a new skill, add a folder whose name matches its SKILL.md frontmatter. Add a representative trigger case and a non-trigger case to the evaluation plan.
4. Run `python3 sync.py manifest` after reviewing intentional source edits. This updates the inventory, including added or removed skills. It is a bookkeeping command, not approval.
5. Run `python3 build.py` and `python3 check.py`. Review the generated adaptation diff. Compare actual baseline and candidate outputs when behavior changes; record each platform tested and any gaps.
6. Open a pull request with scope, evidence, authorization, test results and rollback reference. Resolve overlapping edits against the newest source and rerun affected checks. Never use a force push to discard another contributor's work.

For a release, increment `VERSION`, rebuild and check, then merge the reviewed change. Source hashes, adapter hashes and build-tool hashes determine the release identity in `dist/release.json`. Version labels alone are insufficient to prove identical content. The GitHub workflow checks committed packages and uploads artifacts; it does not merge, promote skills or install them on devices.

The workflow is not an enforced merge restriction unless a repository administrator configures its status check as required. Do not describe branch protection as enabled without verifying it.

## Update installations

Pull the approved release with `git pull --ff-only`. If your checkout has changes, preserve and reconcile them first. Then use the README's status/install commands. The installer records exact managed file hashes, preserves unrelated skills, and refuses updates when it detects local edits, missing managed files or name collisions. There is no force-overwrite option.

If you improved an installed copy, save the diff against its recorded release, apply the intended change to shared source or the appropriate adapter on a branch, and complete the same review. Preserve that local work before restoring the managed installation to its recorded bytes. Then update. Installed copies never silently become a second source of truth.

`current` means installed files match this checkout's generated release. Fetch first to learn whether GitHub has a newer release. A file receipt does not prove the model invoked that version: verify the version, trigger and non-trigger behavior in a fresh session and record the result with the current task or authorized project.

## ChatGPT Work and learning history

ChatGPT Work personal skills are managed separately from local Codex installations. Apply an authorized release through Skill Creator, one skill at a time, preserving host metadata and concurrent edits. Verify saved bytes and activation. The local installer deliberately rejects managed personal-skill paths. GitHub updates do not update this account automatically.

Learning-loop works with task-local evidence and optional project records. No external repository or ledger configuration is required. Preserve its bundled evidence, authorization and promotion requirements. Existing scheduled jobs and historical records are separate; this package neither changes nor provisions them.

For rollback, revert the affected source/adapter change through review, publish a new patch version and update the affected installation. Preserve unrelated later improvements and all failed-candidate evidence.

After final documentation and generated-file changes, run `python3 bundle.py` and `python3 bundle.py --check` to refresh and verify the complete download before committing.
