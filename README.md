# Oakheart Skills

Five reusable workflows for writing, business strategy, sales, software delivery, and improving how you work with AI. One shared source for Codex, Claude Code, Claude chat, and Cowork.

**Version 0.2.1 · Ready to try.** Package and installer checks pass. Native activation and task quality still need testing in each environment.

[Download the package](./Oakheart_Claude_Skills.zip?raw=true)

## What’s included

| Skill | Use it to… |
| --- | --- |
| **Copy reviewer** | Draft or improve writing for its audience and format while preserving your meaning and voice. |
| **Sales pitch reviewer** | Sharpen a pitch’s business case, credibility, offer, and next step. |
| **Business strategy copilot** | Research a business problem, weigh options, and develop a recommendation. |
| **Software delivery agency** | Coordinate client discovery, software delivery, integrations, verification, and support. |
| **Learning loop** | Turn feedback into proposed skill improvements, test them, and track whether they help. |

Each skill includes instructions and supporting references. Some also include Python tools for checking evidence or planning experiments.

## Start with the shared repository

```bash
git clone https://github.com/yilunzh/oakheart-skills.git
cd oakheart-skills
```

This private repository requires GitHub access. Both agents contribute here. Shared instructions live in `source/`; platform differences live in `adapters/`. Read [the contribution guide](./CONTRIBUTING.md) before making improvements.

## Use in Codex CLI or IDE

With Python 3 installed, run these commands from this repository:

```bash
python3 sync.py status --platform codex --target ~/.agents/skills
python3 sync.py install --platform codex --target ~/.agents/skills
```

Check that the skills are available and try `$copy-reviewer`. For one project's installation, use `/path/to/project/.agents/skills` as the target instead. Avoid installing a second copy of a skill already supplied by another source.

These commands manage local Codex files. ChatGPT Work's account skills use a separate installation process through Skill Creator; this repository cannot update those automatically.

## Use in Claude chat or Cowork

1. Download and extract the package above.
2. In Claude on the web, open **Customize → Skills → + → Create skill → Upload a skill**.
3. Upload individual ZIPs from `dist/chat-uploads/main/`. Start with `copy-reviewer.zip`; add the others as you need them.
4. Enable the uploaded skills and start a new conversation. For Cowork, use the same account and check that the skills are available in your session.

Try it with a real draft:

> Use copy-reviewer to improve this draft for [audience]. The goal is [purpose]. Preserve my meaning and voice, and flag any claims that need evidence.

Upload each skill ZIP separately. The complete package contains multiple skills and cannot be installed as one skill. Some tasks also require code execution, file creation, or a connected service.

## Use in Claude Code

With Git and Claude Code installed, and Claude signed in:

```bash
python3 sync.py install --platform code --target ~/oakheart-plugin
claude plugin validate ~/oakheart-plugin
claude --plugin-dir ~/oakheart-plugin
```

Run these commands from the repository or the extracted download. `~/oakheart-plugin` is a dedicated installation folder; choose another unused folder if needed.

The plugin loads for that session. Check `/skills` and `/agents`, then invoke a skill such as `/oakheart:copy-reviewer`.

Claude Code also gets a separate, read-only reviewer. It can inspect supplied files; browser testing and visual checks need additional tools. Avoid loading both a local and an account-synced copy of the same skill.

## What you’ll need to connect

Skills carry the workflow instructions. Connectors, credentials, ChatGPT memories, project files, hosting, and scheduled jobs need separate setup. The original Sales, Sites, and Library plugins are not included; each skill’s `references/runtime.md` explains the available fallback and its limits.

The learning loop’s evidence and experiment history remain in [`personal-os`, on `feature/skill-learning-loop`](https://github.com/yilunzh/personal-os/tree/feature/skill-learning-loop/learning-loop). Connect that repository before using the loop to record or promote changes.

## Keep installations in sync

After an approved change merges, pull the new release and rerun the installation command for each environment:

```bash
git pull --ff-only
python3 sync.py status --platform codex --target ~/.agents/skills
python3 sync.py install --platform codex --target ~/.agents/skills
python3 sync.py install --platform code --target ~/oakheart-plugin
```

The installer records the version and exact file hashes. It preserves unrelated skills and stops if a managed copy has local edits. Reconcile those improvements into the shared source before updating. Claude chat and Cowork uploads still need to be replaced explicitly. Check the skill in a fresh session before calling it activated.

`status` compares against your checkout, so pull first. There is no background watcher or automatic account-to-account sync.

## Improve or add a skill

Make a branch, edit `source/` or `adapters/`, and run:

```bash
python3 sync.py manifest
python3 build.py
python3 check.py
```

Submit the source and generated changes together for review. For releases, increment `VERSION` before building. Both agents read the same contribution rules through `AGENTS.md` and `CLAUDE.md`.

GitHub Actions verifies reproducible packages and helper tests on pushes and pull requests, and provides downloadable build artifacts. Meaningful behavior changes also need actual output comparisons under the [evaluation process](./evaluations/README.md). Passing code checks does not approve a learned change.

| Location | Purpose |
| --- | --- |
| `source/` | Canonical skill instructions and supporting files |
| `adapters/` | Host-specific tools, storage and review instructions |
| `dist/` | Generated Codex skills, Claude plugin and chat ZIPs |
| `dist/release.json` | Shared version, build identity and package hashes |
| `evaluations/` | Evaluation procedure; private evidence stays in its existing ledger |

## Testing status

The package passed file-integrity and reference checks. The learning-loop and agency helpers passed 34 unit tests; 12 infrastructure tests cover conflicts, file preservation and failed-update recovery. See [the verification record](./SCRIPT_CHECKS.md) for scope and details.

Next, run the skills on real tasks in Claude. Compare the finished work with a known baseline, checking factual accuracy, voice, missed requirements, and corrections needed. Independent review requires a separate execution; if the session cannot provide one, label the result as self-reviewed. Existing checks do not yet establish equivalent performance across platforms.

Installation references: [Codex skills](https://learn.chatgpt.com/docs/build-skills) · [Claude plugins](https://code.claude.com/docs/en/plugins).
