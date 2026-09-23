## What it does

`architect-from-spec` turns an approved spec into an implementation-ready codebase architecture: module boundaries, seams and interfaces, dependency direction, project structure, coding rules, and testing rules, then scaffolds the repository skeleton and verifies it. It produces no product feature behavior; any feature code in its diff is a defect, not a bonus.

## When to reach for it

You invoke this by typing `/architect-from-spec`; the agent won't reach for it on its own.

| Where you are | What to run |
| --- | --- |
| Greenfield project, spec approved, no architecture yet | `/architect-from-spec` |
| Substantial application code already exists and needs a redesign | `/improve-codebase-architecture` instead |
| Architecture already settled, need to cut work into steps | `/to-tickets` or `/implement` |

## Prerequisites

Needs an approved spec: a local Markdown file, an issue produced by `/to-spec`, the current conversation, or another authoritative project specification. It also reads `CONTEXT.md`, `CONTEXT-MAP.md`, relevant ADRs, `AGENTS.md`/`CLAUDE.md`, and any existing manifests or source layout, when they exist.

## The architecture gate

The skill will not create source files until the foundational decisions (constraints, modules, dependency direction, runtime and data flow, project structure, coding rules, testing rules) are settled. Only after that does it write `docs/architecture/architecture.md`, update agent-facing pointers, record any justified ADRs, and scaffold the repository. That document opens with a system overview (a component diagram plus, for a multi-process system, its runtime units) and carries a diagram for each important flow, not prose alone. A later step may refine an earlier decision, but the repository is never scaffolded while foundational decisions are still open.

## Deep modules, not generic layers

The module design step leans on the same vocabulary as `codebase-design`: prefer deep modules (substantial complexity behind a small interface), and use the deletion test on every proposed seam. If deleting a module would just spread its complexity across its callers, it earns its keep; if deleting it makes the complexity disappear, it probably should not exist.

## Common questions

**Why doesn't it write any application code?**
Because that is `/implement`'s job, not this skill's. A placeholder is allowed only when required for the project to build, typecheck, launch, or expose the intended module structure. Anything beyond that is scope creep the skill's own verification step is meant to catch.

**What if the repository already has application code?**
The skill will not silently replace an existing structure. It understands the existing architecture first, preserves compatible decisions, calls out conflicts between the spec and the existing system, and scaffolds only new architecture explicitly requested. If the real task is a redesign, it recommends `/improve-codebase-architecture` instead.

## It's working if

- No source files appear before the architecture decisions (constraints, modules, dependency direction) are made explicit.
- `docs/architecture/architecture.md` opens with a diagram you could hand to someone who has never seen the repository, and its flow section has diagrams rather than only paragraphs.
- `docs/architecture/architecture.md` has an empty "Open Architecture Questions" section by the time scaffolding starts.
- The directory structure you get maps to real modules, not to generic buckets like `utils/` or `services/`.
- Build, typecheck, lint, and the test command all run clean on the scaffold, even with an empty test suite.
- The diff contains no meaningful product behavior.

## Where it fits

`architect-from-spec` is the architecture gate in the build chain, between the spec and the ticket/implementation steps:

```txt
grill-with-docs -> to-spec -> architect-from-spec -> to-tickets -> implement -> code-review
```

Its upstream neighbor is `/to-spec`, which produces the spec this skill reads. Downstream, `/to-tickets` cuts the now-architected work into tracer-bullet tickets for `/implement` to build. For an existing codebase that needs re-architecting rather than a foundation built from scratch, use `/improve-codebase-architecture` instead.
