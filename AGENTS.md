# AGENTS.md

Skills are organized into bucket folders under `skills/`:

- `engineering/`: daily code work
- `productivity/`: daily non-code workflow tools

Both buckets are **promoted**: every skill in them must have a reference in the top-level `README.md`, an entry in its bucket's `README.md`, and an entry in `.claude-plugin/plugin.json`'s `skills` array (the Claude Code plugin ships exactly the promoted set). A skill added, renamed, or removed here must be reflected in all three places at once.

Each skill lives at `skills/<bucket>/<skill-name>/SKILL.md`, with a matching `skills/<bucket>/<skill-name>/agents/openai.yaml` alongside it for Codex UI metadata.

Each skill also has a human-facing docs page at `docs/<bucket>/<skill-name>.md` (the docs tree mirrors the bucket tree under `skills/`). When you add, rename, or change the behavior of a skill, create or re-sync its docs page. See [.agents/writing-docs.md](./.agents/writing-docs.md) for the template and section order.

Every `SKILL.md` is either user-invoked (`disable-model-invocation: true` plus `policy.allow_implicit_invocation: false` in `agents/openai.yaml`, reachable only by the human typing its name) or model-invoked (model- or user-reachable, with rich trigger phrasing in its description). A skill is user-invoked in both harnesses or neither. See [.agents/invocation.md](./.agents/invocation.md) for the full convention, including how one skill calls another.

To (re)link every skill into the local harness skill directories (`~/.claude/skills`, `~/.agents/skills`), run `scripts/link-skills.sh`. Each entry is a symlink into this repo, so a `git pull` keeps installed skills current; re-run the script after adding, removing, or renaming a skill. The script refuses to overwrite a destination that already exists and is not a symlink, so a name collision with a skill from elsewhere is something you resolve by hand rather than something the script silently deletes.

No em dashes anywhere in this repo's prose (`SKILL.md` files, docs, `README.md`, code comments). Where a sentence reaches for one, rewrite it with a comma, colon, period, parentheses, or a conjunction, whichever the sentence actually wants; never do a blind character substitution.
