# Working on Oakheart Skills

Read CONTRIBUTING.md before changing skills or adapters. `source/` is the canonical skill source; `adapters/` holds host-specific instructions. `dist/` is generated. Keep learned candidates outside installed paths.

Start from current main and use a branch for a bounded change. Read current source and preserve concurrent edits. For an improvement discovered in an installed copy, capture its diff and reconcile it into source; never overwrite local edits to force a sync.

For behavioral changes, use learning-loop, read the existing ledger policy and attach actual baseline/candidate output evidence. Infrastructure checks do not establish skill quality. Preserve promotion gates, authorization and rollback requirements. Changes to triggers, dependencies and adapters can change behavior too.

After approved source edits: `python3 sync.py manifest`, `python3 build.py`, `python3 check.py`. Bump VERSION for a release and regenerate packages. Include source, adapter, manifest and generated changes together. Do not claim installation or native activation from a successful build.

Keep private project evidence and holdouts out of this reusable repository. Use the existing learning ledger; do not duplicate schedules or provision model APIs. Do not edit provider-owned skills.

After final documentation and generated-file changes, run `python3 bundle.py` and `python3 bundle.py --check` to refresh and verify the complete download before committing.
