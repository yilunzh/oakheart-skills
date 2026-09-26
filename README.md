# Oakheart Skills

Five reusable workflows for writing, business strategy, sales, software delivery, and improving how you work with AI. Adapted from Yilun’s ChatGPT skills for use in Claude chat, Cowork, and Claude Code.

**Version 0.1.1 · Ready to try.** Package checks pass; installation and task performance in Claude still need testing.

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
git clone https://github.com/yilunzh/oakheart-skills.git
cd oakheart-skills
claude plugin validate ./dist/oakheart
claude --plugin-dir ./dist/oakheart
```

This private repository requires GitHub access. If you downloaded the ZIP instead, open its extracted folder and run the last two commands.

The plugin loads for that session. Check `/skills` and `/agents`, then invoke a skill such as `/oakheart:copy-reviewer`.

Claude Code also gets a separate, read-only reviewer. It can inspect supplied files; browser testing and visual checks need additional tools. Avoid loading both a local and an account-synced copy of the same skill.

## What you’ll need to connect

Skills carry the workflow instructions. Connectors, credentials, ChatGPT memories, project files, hosting, and scheduled jobs need separate setup. The original Sales, Sites, and Library plugins are not included; each skill’s `references/runtime.md` explains the available fallback and its limits.

The learning loop’s evidence and experiment history remain in [`personal-os`, on `feature/skill-learning-loop`](https://github.com/yilunzh/personal-os/tree/feature/skill-learning-loop/learning-loop). Connect that repository before using the loop to record or promote changes.

## Updating the skills

| Location | Purpose |
| --- | --- |
| `source/` | Original instructions and supporting files for the five skills |
| `build.py` and `adapters/` | Changes needed to run them in Claude |
| `dist/` | Generated plugin, upload ZIPs, and a diff of the adaptations |
| `source-manifest.json` | File hashes that detect unexpected source changes |

Make reviewed changes in the source or adapters. Update the manifest when intentionally changing source files, then rebuild and check the packages:

```bash
python3 build.py
python3 validate.py
```

Upload the new skill ZIPs to Claude or load the rebuilt Code plugin. Updates do not sync automatically between ChatGPT, this repository, and Claude.

## Testing status

The package passed file-integrity and reference checks. The learning-loop and agency helpers passed 34 unit tests. See [the verification record](./SCRIPT_CHECKS.md) for scope and details.

Next, run the skills on real tasks in Claude. Compare the finished work with a known baseline, checking factual accuracy, voice, missed requirements, and corrections needed. Independent review requires a separate execution; if the session cannot provide one, label the result as self-reviewed. Existing checks do not yet establish equivalent performance across platforms.
