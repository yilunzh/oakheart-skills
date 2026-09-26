# Runtime and dependency adaptation

This is a portability adaptation of a shared personal skill, not proof of equivalent behavior across platforms. Follow the host's tool, permission, and instruction rules. Historical test results in bundled references describe the source workflow, not tests performed in Claude.

Read supporting paths relative to this skill's directory. Run bundled scripts from that directory, with Python 3, after inspecting their inputs. Only use metadata supported by the current host.

Resolve companion skills by their frontmatter name among installed skills; plugin names may be namespaced. Load each needed companion once and avoid circular handoffs. The main pack includes copy-reviewer, sales-pitch-reviewer, business-strategy-copilot, software-delivery-agency, and learning-loop.

## Capability mapping

- **Commercial work:** Use supplied evidence and the bundled sales-pitch-reviewer for buyer logic. Discover an available CRM or account-research integration only when the task needs it; no particular vendor plugin is required. Never fabricate account data.
- **Artifact production:** Discover the host's document, presentation, spreadsheet, PDF, browser, and image tools when needed. Use actual rendering and behavioral inspection when required. If a required capability is absent, complete supported work and identify the precise missing validation. Text review is not visual QA.
- **Sites:** No ChatGPT Sites credentials, project tools, or hosting are transferred. Use the existing project's actual repository/build/release workflow. An existing Sites deployment must be handled in its authorized environment until migration is explicitly requested. Do not create a replacement deployment implicitly.
- **Library and context:** ChatGPT Library, memories, previous chats, and project files do not transfer with a skill. Use supplied artifacts and authorized connected storage. Ask for a missing authoritative artifact only when it controls the task. Never invent prior decisions.
- **Scheduling:** Importing skills creates no recurring jobs. Existing ChatGPT automations stay separate. Scheduling in another host requires an available scheduler and a verified creation result; do not create duplicate jobs merely to mirror this pack.

## Skill maintenance

For an authorized change, read the current source, relevant evidence, dependencies, and existing promotion policy. Preserve an exact baseline and a bounded diff. The canonical source is `yilunzh/oakheart-skills`, `source/`; host differences belong in `adapters/`. Read that repository's AGENTS.md and CONTRIBUTING.md before a change. Edit shared source or adapters on a branch, not generated ZIPs or installed caches. If work began in an installed copy, preserve its diff and reconcile it into the canonical source before updating that installation. Run relevant checks, rebuild distributions, record the version and content hashes, and save through the established version-control workflow. Keep unapproved candidates outside installed skill paths. Only report activation after checking the installed version in a fresh session.

A package update does not prove native activation. Learning-loop evidence can remain task-local or be saved with the current project; no external repository is required.

## Claude Code execution

When a skill calls for independent editorial review, delegate a fresh execution to the plugin's `artifact-reviewer` (namespaced `oakheart:artifact-reviewer` in the main plugin). Provide only the task brief, permitted changes, relevant source evidence, artifact paths, and applicable rubric. Do not include creator self-ratings, expected verdicts, or target scores. The reviewer returns findings; the creator makes edits. A reviewer must not spawn another reviewer.

The reviewer is limited to reading files and cannot run a browser, render files, or execute tests. Provide actual visual/behavioral evidence separately or use a separately authorized QA execution; never claim these checks from text inspection. Read-only tools do not enforce filesystem isolation: a separate reviewer context is not an access-separated holdout. Learning-loop release gates still require their stated evidence and isolation.
