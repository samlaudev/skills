## What it does

`prompt-optimizer` turns a rough requirement or an existing draft into a well-structured prompt. It matches your task against a library of 57 prompt engineering frameworks, picks the one that fits, asks a few targeted questions if your input is vague, and writes the prompt in that framework's structure.

It delivers the prompt itself, never the answer to the task the prompt is for, and the structure is never improvised: it always comes from a named framework, with the reason that framework was chosen.

## When to reach for it

You invoke this by typing `/prompt-optimizer`; the agent won't reach for it on its own.

| Where you are | What to do |
| --- | --- |
| A rough idea and no prompt yet | `/prompt-optimizer` with the requirement in plain words |
| A draft prompt that underperforms | `/prompt-optimizer` with the draft pasted in |
| You want the task done, not a prompt for it | Just ask the agent directly |
| You already know the framework you want | `/prompt-optimizer` and name it (or name several to combine) |

## Framework choice is a complexity trade-off

The library is sorted by how many elements a framework asks you to fill in, and the skill's leading idea is to match that weight to the task.

| Complexity | Examples | Reach for it when |
| --- | --- | --- |
| Simple (3 elements) | APE, ERA, TAG, RTF | A quick, low-stakes request where overhead would outweigh the gain |
| Medium (4-5 elements) | RACE, CIDI, SPEAR, GRADE | Most everyday work with a clear audience and output |
| Complex (6+ elements) | RACEF, CRISPE, PROMPT, RISEN | Multi-faceted tasks where a missed dimension would hurt |

## How the 57 frameworks are organized

`Frameworks_Summary.md` is the lookup table mapping each framework to its use cases. `frameworks/01..57_*.md` holds one file per framework with its components, strengths, weaknesses, and examples. You can ask the skill to explore them ("which frameworks suit content creation?"), to compare two, or to chain them (for example RICE to prioritize, then Chain of Thought to analyze).

## Common questions

**Will it just do the task for me?**
No. The output is a prompt you paste into whatever model or tool you are using.

**Can I choose the framework myself?**
Yes. Name one, or ask for a combination, and the skill uses it instead of choosing.

**Are the framework docs in English?**
No. `Frameworks_Summary.md` and the 57 files under `frameworks/` are in Chinese. `SKILL.md` and this page are in English.

## It's working if

- You get a prompt you can paste as-is, not a finished piece of work.
- The skill names the framework it chose and says why.
- Vague input gets a few targeted questions before any prompt is written.
- The prompt's sections visibly follow the chosen framework's components.

## Where it fits

`prompt-optimizer` is a standalone tool and the first skill in the `productivity/` bucket. It is not a step in the engineering build chain, so it neither depends on nor feeds skills like [architect-from-spec](../engineering/architect-from-spec.md); use it whenever you need a better prompt, for any tool, at any point.
