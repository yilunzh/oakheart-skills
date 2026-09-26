# Claude task evaluations

This harness measures answer quality and skill routing on supplied tasks. It does not certify production deployment, rendered artifacts, protected holdouts or native chat installations.

The initial 11 tasks are synthetic development cases adapted from the earlier evaluation branch. They are not facts about the user's business and are not unseen transfer evidence. Add authorized original briefs and starting artifacts for real-task testing; keep private inputs and outputs outside this repository.

## Run a new experiment

Use an already authenticated Claude Code installation with `--restricted` support (v2.1.248 or later), Python 3, and explicit model choices. The harness does not configure authentication or call a model API directly.

```bash
python3 evals/run.py --model YOUR_MODEL --output-root /private/path/oakheart-evals
python3 evals/judge.py --experiment /private/path/oakheart-evals/RUN_ID --model YOUR_JUDGE_MODEL
python3 evals/analyze.py --batch /private/path/oakheart-evals/RUN_ID/judgments/BATCH_ID
```

Each run creates a unique directory, snapshots the plugin and tasks, records hashes, CLI version and requested/observed models, and randomizes execution order. Existing runs and judgments are never silently reused. Each judging command creates a fresh batch. To compare an earlier skill version directly, pass `--baseline-plugin /path/to/previous/plugin`; otherwise the baseline has no Oakheart plugin.

Only read, search, skill and agent tools are enabled for generation. The temporary working directory and frozen plugin are added to the restricted read scope. User/project settings and MCP connections are excluded; managed host policies may still affect execution and must be inspected in raw traces. No permission bypass is used. Missing tool access, errors, timeouts and empty outputs remain visible and are excluded from answer-quality scoring. This controlled setup differs from full production tooling.

Raw stream events, commands, read/tool errors, model identity, costs, timing and tool calls are retained in each run. A requested slash command alone is not proof a skill executed. Inspect command expansion and reference reads in the raw trace; an absent Skill event is inconclusive for a direct invocation. Check whether the required reviewer actually ran rather than inferring it from the final answer.

## Interpret results

The judge sees task-local answers with their order swapped, without the condition label. It separately flags unsupported numeric and nonnumeric claims, critical failures and unavailable evidence. It has no tools; manually verify consequential facts and calculations and calibrate a sample with the user.

Analysis combines the two orders into one pair-level result. Disagreement is reported as order-sensitive; missing grades stay incomplete. Repeats and shared baselines are correlated. Report automatic-routing results separately from explicit-invocation results. Do not filter only successful invocation runs and present that as the experience of loading the plugin.

Use actual deliverables, objective requirements, task-family coverage and blind human preferences before promoting learned changes. A judge's lack of findings does not establish zero failures. Native Claude execution has not been run in the build environment; local tests exercise harness logic with synthetic event fixtures only.

CLI reference: https://code.claude.com/docs/en/cli-reference
