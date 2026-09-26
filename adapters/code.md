
## Claude Code execution

When a skill calls for independent editorial review, delegate a fresh execution to the plugin's `artifact-reviewer` (namespaced `oakheart:artifact-reviewer` in the main plugin). Provide only the task brief, permitted changes, relevant source evidence, artifact paths, and applicable rubric. Do not include creator self-ratings, expected verdicts, or target scores. The reviewer returns findings; the creator makes edits. A reviewer must not spawn another reviewer.

The reviewer is limited to reading files and cannot run a browser, render files, or execute tests. Provide actual visual/behavioral evidence separately or use a separately authorized QA execution; never claim these checks from text inspection. Read-only tools do not enforce filesystem isolation: a separate reviewer context is not an access-separated holdout. Learning-loop release gates still require their stated evidence and isolation.
