# Oakheart skills for Claude — portability preview v0.1.1

[Download the complete package](./Oakheart_Claude_Skills.zip) · Individual skill ZIPs are in [dist/chat-uploads](./dist/chat-uploads).

This package exports five personal skills from the 2026-09-26 snapshot. It includes complete original skill folders, reproducible adaptations, individual Claude chat/Cowork ZIPs, and Claude Code plugins. Your existing ChatGPT skills have not been changed.

The package has not been installed or behaviorally tested in Claude. It is not a claim of equivalent performance, automatic synchronization, or a running background service.

## Start in Claude chat / Cowork

1. Extract the outer archive using Files on iPhone or an archive tool on your computer.
2. In Claude on the web, open **Customize → Skills → + → Create skill → Upload a skill**.
3. Upload the individual ZIPs under `dist/chat-uploads/main/`. Do not upload this entire outer archive as one skill.
4. Start with `copy-reviewer.zip` and `learning-loop.zip`, then add the remaining main skills. Enable code execution/file creation if required by your account and task.
5. Start a fresh conversation and ask Claude to use a skill by name. Verify that it can read its referenced files. No separate Claude Code installation is required for this path.

For Cowork, use the same account's enabled skills. Verify availability in the session rather than assuming account synchronization succeeded. Configure connectors separately when a task needs them.

## Start in Claude Code

With Claude Code installed and signed in, open a terminal in this extracted folder:

```bash
claude plugin validate ./dist/oakheart
claude --plugin-dir ./dist/oakheart
```

This loads the local plugin for that launch; it is not a permanent account installation. In that session, check `/skills` and `/agents`. Try `/oakheart:copy-reviewer` with a real draft. The plugin includes a read-only artifact-reviewer; browser and rendering checks require separate available tools.

Use either an account-synced copy or this local plugin for the same workflow; avoid enabling duplicate versions. This package does not configure permissions, MCP servers, credentials, hooks, or deployment services.

## Included skills

| Skill | Package | Dependency or status note |
| --- | --- | --- |
| copy-reviewer | Main | Includes medium guidance, voice preferences and review rubric. Sales plugin not included. |
| sales-pitch-reviewer | Main | Works with copy-reviewer; original Sales workflow not included. |
| business-strategy-copilot | Main | Research and document tools depend on the Claude environment. |
| software-delivery-agency | Main | Current source and learning ledger identify it as active. Sites/analytics/vendor connections need separate access. |
| learning-loop | Main | Python checker included. Existing external ledger retained by reference; no schedules or history migrated. |

No `uninstalled/` skills were present in the inspected personal-skills checkout. Held and archived learning candidates live separately in the existing evidence repository and have not been copied into active packages. The archived broader agency proposal is distinct from the current active agency skill.

## What transfers and what does not

All 44 original files across the five custom skill folders are preserved under `source/`, with SHA-256 hashes in `source-manifest.json`. Generated packages omit OpenAI UI metadata and add runtime instructions; exact replacements are defined in `build.py`, with a generated diff under `dist/`.

Provider/plugin skills—including Sites, Library, Sales, native artifact tools, browser tooling, and Skill Creator—are not exported as if they were your custom implementations. Their dependencies have explicit mappings or limitations. ChatGPT memory, transcripts, project artifacts, credentials, external ledger contents, and scheduled jobs are not included. Historical evaluation results embedded in references remain historical, not evidence of Claude performance.

The existing learning ledger remains `yilunzh/personal-os`, branch `feature/skill-learning-loop`. Its current policy controls learned-change promotion. Claude needs separately authorized access. Missing access does not justify creating a second ledger or loosening its gates.

## Maintain one source

Treat `source/` as the exact imported baseline. Update it deliberately and refresh its manifest when adopting an approved upstream version. Keep platform adaptations in `build.py` and `adapters/`; regenerate packages rather than editing each ZIP. The build fails on unexpected baseline drift.

```bash
python3 build.py
python3 validate.py
```

Clone the current repository to work with its version history:

```bash
git clone https://github.com/yilunzh/oakheart-skills.git
```

This dedicated private repository, yilunzh/oakheart-skills, is the home for the skill source and Claude distribution packages on main. It contains no personal-os application code or inherited repository hooks. The accompanying ZIP contains the current five-skill package; version history is retained in this repository. Review bounded changes and keep generated versions tied to the source version. Account uploads are distribution copies, not an automatic two-way sync.

## First validation in Claude

1. **Copy:** Use the same real draft, brief, facts, and constraints in both platforms. Compare finished drafts blind; check voice, invented claims, and preservation.
2. **Learning loop:** Ask Claude to evaluate an incomplete experiment packet. It should report missing evidence and hold promotion while still completing useful analysis.
3. **Code reviewer:** Verify the reviewer runs as a separate execution and cannot edit files. Check its findings against the artifact. This is not proof of filesystem-isolated holdouts.
4. **Real-project parity:** Freeze equivalent starting artifacts and original briefs for PTC, AutoNation, and Oakheart. Run matched tasks with comparable tools and budgets; withhold completed references until blind comparison. Add a fresh transfer case. Record corrections and actual outputs, not prompt quality alone.

The real-project artifacts are not part of this export, so those comparisons remain pending. Do not infer success from package validation or the existing Python tests.

## Documentation checked

- https://support.claude.com/en/articles/12512180-use-skills-in-claude
- https://support.claude.com/en/articles/12512198-how-to-create-custom-skills
- https://code.claude.com/docs/en/skills
- https://code.claude.com/docs/en/plugins-reference
- https://code.claude.com/docs/en/sub-agents

