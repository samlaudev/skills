# Writing docs pages

Every skill in `engineering/` and `productivity/` has a human-facing docs page at `docs/<bucket>/<skill-name>.md`. The docs tree mirrors those two bucket folders under `skills/`. The page is not the skill and not a copy of `SKILL.md`.

Most of these skills are user-invoked: the agent will never fire them for you, so *you* are the index that has to remember they exist and when to reach for them. The job of a docs page is to relieve that: to orient one reader around one skill so they can hold it in their head and know when to reach for it.

Act whenever a skill is added, renamed, or has its behavior changed: create or re-sync its docs page. A rename moves the file too (`docs/<bucket>/<old>.md` -> `docs/<bucket>/<new>.md`). A skill that moves between `engineering/` and `productivity/` moves its docs file to the matching folder.

There is no H1. Links are repo-relative, not absolute.

## Page structure

<page-template>

## What it does

One or two plain-language paragraphs. Lead with the skill's one-sentence job, then state the **defining constraint**: the single fact that makes this skill behave differently from the obvious default. Write it as a plain declarative sentence, never a labelled aside like "The defining constraint:". This line is the most valuable on the page; never omit it.

## When to reach for it

How and when you reach for the skill, in two beats:

- **Invocation mode.** State whether you type it or the agent fires it.
- **Trigger boundary.** "Reach for this when...". Where the skill is confusable with a sibling, add the other half: "for X instead, use [sibling](../bucket/sibling.md)."

## Prerequisites

Optional: include only when the skill needs something in place to be functional; omit the heading entirely otherwise.

## <free-form middle>

One to three short sections, in the skill's own vocabulary, that make it click. The single non-negotiable: surface the skill's leading word or defining idea.

## Common questions

The questions readers really ask about this skill, each in bold with the answer beneath it. Sized to what is actually known; padding a thin skill's section to match a richer one teaches the reader nothing. Omit the heading where there is nothing worth answering yet.

## It's working if

A few bullets naming what the reader sees when the skill is doing its job, each checkable without opening `SKILL.md`.

## Where it fits

Always present. Situate the skill in the system: its role (chain step, run-once setup, periodic maintenance, or standalone), and the one or two siblings that matter, each with a because-clause.

</page-template>

## Conventions

- Explain the **why**, not the process. The page orients; it never reproduces the `SKILL.md` steps.
- Use the skill's leading words so the page and the skill speak one language.
- Branches go in a table or a list, never in a paragraph.
- No em dashes.
