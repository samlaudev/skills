---
name: architect-from-spec
description: "Turn an approved spec into an implementation-ready codebase architecture: modules, seams, dependency rules, project structure, coding and testing rules, then scaffold and verify the skeleton."
disable-model-invocation: true
---

Turn an approved spec into an implementation-ready engineering foundation.

This is the architecture gate between `/to-spec` and `/to-tickets`.

The output is not feature implementation. The output is a codebase whose shape, module seams, dependency rules, engineering conventions, test strategy, and basic tooling are settled enough that future agents can implement vertical slices without inventing the architecture as they go.

## Scope

Own:

- architecture
- module boundaries
- public interfaces and seams
- dependency direction
- external adapters
- directory structure
- project/tooling scaffold
- project-specific coding rules
- project-specific testing rules
- agent-facing architecture pointers
- architecture verification

Do not own:

- business feature implementation
- ticket decomposition
- speculative future abstractions
- exhaustive documentation
- implementation details that belong inside future tickets

After this skill completes, `/to-tickets` or `/implement` owns the next step.

## Inputs

Start from the spec provided by the user.

The spec may be:

- a local Markdown file
- an issue produced by `/to-spec`
- the current conversation
- another authoritative project specification

Read the complete source before designing anything.

Also read, when they exist:

- `CONTEXT.md`
- `CONTEXT-MAP.md`
- relevant ADRs
- `AGENTS.md`
- `CLAUDE.md`
- existing manifests and build configuration
- existing source layout

Respect existing domain terminology and architectural decisions.

Call the Skill tool with "codebase-design" before designing modules. Use its vocabulary and principles for modules, interfaces, seams, adapters, depth, leverage, and locality.

If architectural work resolves new domain vocabulary or a genuinely hard-to-reverse architectural decision, call the Skill tool with "domain-modeling" rather than inventing a separate glossary or ADR convention.

Do not create `CONTEXT.md` or ADRs merely because they do not exist.

## Preconditions

This skill is primarily for a greenfield project or a repository whose application architecture has not yet been established.

If substantial application code already exists, do not silently replace its structure.

Instead:

1. understand the existing architecture;
2. preserve compatible decisions;
3. call out conflicts between the spec and the existing system;
4. scaffold only new architecture explicitly requested by the user.

If the task is fundamentally a redesign of an existing codebase, recommend `/improve-codebase-architecture` instead of pretending the repository is greenfield.

## Architecture Gate

Do not create source files immediately.

First make the architectural decisions that determine the repository shape.

Work in this order:

1. extract constraints
2. design modules
3. define dependency direction
4. define runtime and data flow
5. design the project structure
6. define coding rules
7. define testing rules
8. record architecture
9. record agent rules
10. ADRs
11. scaffold the repository
12. verify the architecture gate

A later step may refine an earlier decision, but do not scaffold the repository while foundational decisions are still unresolved.

## 1. Extract Constraints

Derive architecture-driving constraints from the spec.

Look for:

- target platforms
- language and runtime
- framework
- deployment model
- persistence requirements
- network/API dependencies
- offline requirements
- concurrency requirements
- security/privacy requirements
- performance constraints
- compatibility constraints
- observability requirements
- expected scale
- team or repository constraints

Separate:

- explicit constraints from the spec
- existing repository constraints
- assumptions introduced during architecture design

Do not invent product requirements.

### Missing decisions

For reversible choices, choose a conventional default that matches the stack and record the assumption.

Examples:

- test file naming
- formatter choice
- internal directory naming
- local lint configuration

For foundational choices that materially change the entire project shape, do not guess unless the spec explicitly delegates that choice to you.

Examples:

- programming language
- primary framework
- database category
- deployment target
- client/server ownership split

If one of these is missing and cannot be derived from existing project context, stop before scaffolding and report it as an architecture blocker.

## 2. Design Modules

Design the smallest set of modules needed by the current spec.

For every module identify:

- responsibility
- complexity it hides
- public interface
- owned state/data
- dependencies
- dependants
- external dependencies
- test seam

Prefer deep modules: substantial complexity behind a small interface.

Avoid pass-through modules whose abstraction merely renames another abstraction.

Do not introduce a seam merely because an implementation could hypothetically change someday.

A seam must earn its existence through one of:

- an actual external boundary
- multiple real adapters
- independent lifecycle
- independently meaningful behavior
- meaningful complexity hidden from callers
- isolation required for testing or platform integration

Use the deletion test:

If deleting the module merely spreads the same complexity across its callers, the module is probably earning its keep.

If deleting it makes complexity disappear, reconsider whether the module should exist.

## 3. Define Dependency Direction

For each module, make the allowed dependency direction explicit.

The dependency graph must be acyclic unless the technology makes a cycle unavoidable and the reason is documented.

Prefer dependencies to point toward stable domain behavior rather than toward delivery mechanisms or infrastructure.

Keep external systems behind adapters when the external dependency represents a real seam.

Examples include:

- network services
- databases
- filesystem
- operating-system APIs
- clock
- randomness
- analytics SDKs
- payment providers
- platform services

Do not wrap every library merely to create an interface.

## 4. Define Runtime And Data Flow

Describe the important end-to-end flows required by the spec.

Cover the flows the spec actually depends on, usually two to four. Do not diagram every call path.

Give each flow a diagram, not prose alone. Choose the form the flow calls for:

- a Mermaid `sequenceDiagram` when the flow crosses several modules or external systems and the ordering of calls is the point;
- a Mermaid `flowchart` when the flow branches on a result, retries, or fans out into follow-up work;
- a Mermaid `stateDiagram-v2` when the flow is a state machine;
- a plain `text` chain when the flow is genuinely linear:

```text
input
-> module/interface
-> domain behavior
-> persistence/external boundary
-> observable result
```

If the project's documentation toolchain does not render Mermaid, draw the same diagram in ASCII inside a `text` block.

Quote every Mermaid node and edge label that contains punctuation: colons beyond the first, semicolons, parentheses, commas, or question marks. Use `id["label text"]` for nodes and `-->|"label text"|` for edges. An unquoted semicolon inside a flowchart node label ends the statement early and breaks the parser; quoting the whole label avoids that and every similar surprise. Render every Mermaid block before treating it as done.

When drawing an ASCII diagram, use box-drawing characters (`┌ ┐ └ ┘ │ ─ ├ ┬ ┴ ┼ ▼`), not `|`, `-`, `+`, `v`, or `/` `\`. Compute the column of every connector, vertical, and arrow instead of eyeballing the spacing: pick the parent line's connector column, then place every `│` and `▼` beneath it at that exact column, and a branch node's own children at columns computed the same way from its branch point. A vertical that drifts off its parent's column by even one space is as broken as bad Mermaid syntax; it just fails silently instead of refusing to render.

Name every participant and node after a real module, entry point, or external system from the module map. Generic labels such as `Service`, `Handler`, or `Manager` mean the diagram is not describing this system.

Add one line under each diagram stating what it establishes, such as an ownership rule or a failure path. A diagram with no claim attached is decoration.

Keep this at architecture level.

Do not write implementation pseudocode unless a specific algorithm or state machine is itself an architectural decision.

Identify:

- ownership of mutable state
- synchronization points
- transaction boundaries
- asynchronous boundaries
- error propagation
- retry responsibility
- persistence ownership

## 5. Design The Project Structure

Map architecture to directories.

The directory structure should expose the architecture rather than hide it.

Prefer names based on real domain modules and architectural responsibilities.

Avoid generic dumping grounds such as:

- `utils`
- `helpers`
- `common`
- `misc`
- `services`

unless the contents genuinely form one coherent module.

A module that has a public interface and private implementation should make that distinction obvious from the chosen language's normal conventions.

Design the structure from the module graph, not from a generic framework template.

Describe directory rules, not an exhaustive snapshot of every future file.

Example shape:

```text
src/
  <module-a>/
  <module-b>/
  platform/
  app/

tests/
  ...

docs/
  architecture/
  agents/
  adr/
```

Adapt this to the language and framework rather than copying it literally.

If the repository already has some of this structure in place, verify each directory in the module map actually exists on disk before writing it into the architecture document as though it does. A module that exists only as a target, with its code still sitting in unmigrated legacy files, is a fact worth recording, not a detail to gloss over: name those files and point to whatever tracks their migration (a checker script, a checklist, an issue), rather than presenting the target layout as the current one.

## 6. Define Coding Rules

Create project-specific coding rules.

Prefer executable enforcement over prose: compiler > formatter > linter > static analysis > documentation.

If a rule can be reliably enforced by a tool, configure the tool instead of restating the complete rule in prose.

Document only conventions an agent cannot reliably discover from configuration.

Consider:

- naming rules not enforced by tooling
- module import/dependency rules
- visibility rules
- error handling
- concurrency conventions
- dependency injection
- configuration management
- logging
- generated code
- comments/documentation expectations
- prohibited patterns
- ownership rules

Keep the document short.

Do not turn it into a language style guide.

## 7. Define Testing Rules

Base testing decisions on the seams defined by the architecture.

Tests verify observable behavior through public interfaces.

Do not test private implementation details.

Do not mock internal modules merely to make tests easier.

Use fakes, stubs, mocks, or test adapters primarily at true external boundaries.

For the project, define:

- which module seams are test surfaces
- where tests live
- test naming convention
- unit/integration/end-to-end responsibilities
- which external boundaries receive test adapters
- fixture strategy
- test data ownership
- commands used for focused tests
- command used for the complete test suite

Prefer the smallest test pyramid that adequately protects the behaviors in the spec.

Do not introduce arbitrary coverage percentages unless the spec requires them.

Do not create tests whose only purpose is asserting that scaffolding exists.

## 8. Record Architecture

Write:

```
docs/architecture/architecture.md
```

It should contain:

<architecture-template>

# Architecture

## Constraints

Only architecture-driving constraints.

## System Overview

The whole system on one screen, for a reader who has not opened the repository.

One short paragraph saying what the system does and how it is deployed, then a diagram of the top-level components with the external systems they talk to, drawn so the dependency or call direction is visible. Use an ASCII diagram or a Mermaid `flowchart`, whichever the project's documentation renders. Where the repository layout *is* the architecture, label the boxes with the real top-level directories. If drawn in ASCII, follow the box-drawing and column-alignment rule from step 4; a diagram whose arrows do not line up under their boxes fails the same reader it was meant to orient.

When the system runs as more than one process, service, or deployable, follow the diagram with a table of those runtime units:

| Unit | Entry point | Responsibility |

Do not restate the module table or the directory tree here. This section orients; the sections below carry the detail.

## Module Map

For each module:

- purpose
- public interface
- dependencies
- owned state/data
- test seam

## Dependency Rules

State allowed dependency directions and forbidden dependencies.

## External Boundaries

List real external systems and their adapters.

## Runtime / Data Flow

The important system flows, each with its diagram from step 4 and the claim that diagram establishes.

## Project Structure

Describe directory conventions and show the actual current skeleton, verified against the repository, not an aspirational one. If a module from the module map does not yet have its own directory, say so and name where its logic currently lives.

## Assumptions

Only assumptions introduced because the spec did not decide them.

## Open Architecture Questions

This section must be empty before scaffolding begins.

</architecture-template>

Keep this document about decisions and rules that are not obvious from inspecting the repository.

Do not duplicate information that package manifests, compiler configuration, formatter configuration, or the directory tree already express clearly.

## 9. Record Agent Rules

Create or update:

```
docs/agents/coding-standards.md
```

and:

```
docs/agents/testing.md
```

These documents contain only project-specific rules.

If the project already uses another documented location for these concerns, use that instead.

Update the instruction file the current harness actually reads, such as `AGENTS.md` or `CLAUDE.md`.

Add short pointers rather than copying the documents.

For example:

```markdown
## Architecture

Before changing module structure or dependencies, read
`docs/architecture/architecture.md`.

## Coding standards

Follow `docs/agents/coding-standards.md`.

## Testing

Follow `docs/agents/testing.md`.
```

Preserve existing instructions.

Do not overwrite unrelated content.

## 10. ADRs

Do not write an ADR for every architecture choice.

An ADR is justified when a decision is:

- expensive to reverse
- non-obvious without context
- the result of a real trade-off

Use the project's existing ADR convention.

If `domain-modeling` owns ADR creation in this repository, use it.

Typical ADR candidates include:

- architecture style
- persistence technology
- major state-management strategy
- cross-module communication model
- offline synchronization strategy
- deployment topology

Typical non-ADR decisions include:

- directory names
- formatter selection
- test file suffix
- trivial library choices

## 11. Scaffold The Repository

Only after the architecture is settled, create the minimum repository skeleton required to make the architecture real.

Create as applicable:

- directories
- package/project manifests
- compiler configuration
- formatter configuration
- linter configuration
- test runner configuration
- source/module roots
- application entry point
- minimal module entry points
- external adapter locations
- test directories
- CI configuration if explicitly required by the spec
- agent-facing documentation

Use official project generators when they are the conventional source of truth for the chosen framework.

Avoid manually reconstructing files that an official generator should own.

Do not implement business behavior.

A placeholder is allowed only when required for the project to build, typecheck, launch, or expose the intended module structure.

Keep placeholders minimal.

Do not create speculative repositories, abstractions, entities, DTOs, or interfaces just to fill the tree.

## 12. Verify The Architecture Gate

Before declaring the architecture ready, verify all applicable conditions.

### Traceability

Every module exists because of a requirement, constraint, or real architectural responsibility.

Every external adapter corresponds to an actual external boundary.

Every documented test seam corresponds to a public module interface or true system boundary.

### Structure

The repository structure matches the module map.

Dependency direction is representable by the chosen directory/package/module structure.

No generic dumping-ground directory was introduced without a coherent responsibility.

### Tooling

Run the project's applicable commands:

- dependency/install validation
- build or compile
- typecheck
- lint
- formatter check
- focused test command
- full test command

Fix scaffold problems until these commands pass.

An empty test suite is acceptable at this stage if no business behavior has been implemented, but the test command itself must be valid.

### Documentation

Verify that:

- architecture pointers resolve to real files
- coding-standard pointers resolve
- testing-rule pointers resolve
- ADR links resolve
- documentation does not contradict configuration
- documentation does not duplicate trivially discoverable configuration
- the system overview diagram exists and shows dependency or call direction
- every diagram names only modules, entry points, and external systems that exist in the module map and in the scaffold
- no diagram has drifted below architecture level into private functions
- every Mermaid diagram renders without a syntax error; punctuation-bearing labels are quoted
- every ASCII diagram's verticals and arrows sit exactly under their parent connector's column
- the project structure section's directory tree matches the repository as it exists right now; a module without its own directory yet is called out, not shown as if already scaffolded

### Scope

Inspect the diff.

There must be no meaningful product behavior implemented by this skill.

If feature behavior has appeared, remove it unless it is strictly required to prove that the generated application skeleton can start.

## Completion Criteria

Do not stop at "architecture document written."

This skill is complete only when:

1. the spec has been fully read;
2. architecture-driving constraints are identified;
3. there are no unresolved architecture blockers;
4. the module map is explicit;
5. the architecture document opens with a system overview and a diagram of the important flows;
6. module interfaces and test seams are identified;
7. dependency direction is explicit;
8. external boundaries are identified;
9. the initial project structure exists;
10. project-specific coding rules exist;
11. project-specific testing rules exist;
12. agent instruction files point to those rules;
13. required ADRs have been recorded;
14. the scaffold builds/typechecks as applicable;
15. lint/format validation passes as applicable;
16. the test command runs successfully;
17. no product feature has been prematurely implemented.

If any applicable criterion fails, continue working until it passes or report a concrete blocking dependency that cannot be resolved from the spec or repository.

## Final Report

At completion report:

**Architecture**

One paragraph describing the architecture and its dependency direction.

**Modules**

The module names and their public responsibilities.

**Scaffold**

The important directories/configuration created.

**Rules**

Where coding and testing rules were written.

**ADRs**

ADRs created, or `None`.

**Verification**

Commands run and their results.

**Assumptions**

Only assumptions introduced during architecture work.

**Next**

Recommend `/to-tickets` for work spanning multiple implementation sessions, or `/implement` when the complete feature comfortably fits in one fresh context window.