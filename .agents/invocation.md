# Model-invoked vs user-invoked

Every `SKILL.md` in this repo is a skill. The one axis that splits them is **invocation**, who can reach it:

- **User-invoked**: reachable **only by the human typing its name**. Set `disable-model-invocation: true` in the frontmatter (Claude Code) and `policy.allow_implicit_invocation: false` in `agents/openai.yaml` (Codex). The `description` is **human-facing**: a one-line summary read by a person browsing slash commands. Strip trigger lists ("Use when the user says...").
- **Model-invoked**: reachable by **model or user**. The default: omit `disable-model-invocation` and the `policy` block from `agents/openai.yaml`. The `description` is **model-facing** and keeps rich trigger phrasing ("Use when the user wants..., mentions..., asks for...") so auto-invocation fires.

Each harness excludes a user-invoked skill from the model's reach in its own way, so nothing but the human can fire it: no other skill can. A user-invoked skill may invoke model-invoked skills, but it can never reach another user-invoked skill.

## Dependencies between them

Dependencies are expressed as an explicit instruction to **call the Skill tool** with the named skill (`Call the Skill tool with "codebase-design"`), not a bare `/skill`-style mention left for the model to interpret. Naming the tool is what gets it fired.

This is about **operative** instructions: a skill's own steps telling the agent to go run another skill right now. Prose that just names a skill for a human to pick from is not invoking anything, so it keeps `/skill`-style names as plain labels.

This whole convention only holds when the named skill is **model-invoked**. A user-invoked skill can never be reached this way, full stop: no other skill can call it, including by naming it to the Skill tool. When a step's precondition is a user-invoked skill, phrase it as an instruction for the human to act on ("tell the user to run `/some-skill`"), never as a Skill tool call.
