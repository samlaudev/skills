# samlau-skills

Agent skills for real engineering work, packaged as a Claude Code plugin (and installable as plain Agent Skills for Codex and other compatible harnesses).

## Install

As a Claude Code plugin, from this repo as a local marketplace:

```bash
claude plugin marketplace add /Users/samlau/Repository/AI/skills
claude plugin install samlau-skills
```

Or, to symlink every skill straight into your local harness skill directories (`~/.claude/skills`, `~/.agents/skills`) without going through the plugin system:

```bash
./scripts/link-skills.sh
```

Each symlink points back into this repo, so a `git pull` keeps installed skills current. Re-run the script after adding, removing, or renaming a skill.

## Skills

Skills are organized into bucket folders under `skills/`, each with its own index:

- **[engineering](./skills/engineering/README.md)**: daily code work.
- **[productivity](./skills/productivity/README.md)**: daily non-code workflow tools.

## User-invoked

- **[architect-from-spec](./skills/engineering/architect-from-spec/SKILL.md)**: Turn an approved spec into an implementation-ready codebase architecture: modules, seams, dependency rules, project structure, coding and testing rules, then scaffold and verify the skeleton.
- **[prompt-optimizer](./skills/productivity/prompt-optimizer/SKILL.md)**: Optimize a prompt by matching it to one of 57 prompt engineering frameworks, then writing the prompt in that framework's structure.

## Model-invoked

_None yet._

## Conventions

See [AGENTS.md](./AGENTS.md) for how skills are organized, how invocation mode works, and the repo's writing conventions.
