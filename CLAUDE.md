# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **Claude Code plugin marketplace** that delivers specialized skills through a structured marketplace system. Each skill extends Claude's capabilities with specialized knowledge, workflows, or tool integrations.

**Key architecture**: The marketplace uses a **progressive disclosure loading system** where skills load in three tiers:
1. **Metadata** (frontmatter) - Always in context (~100 words)
2. **SKILL.md body** - When skill triggers (<5k words)
3. **Bundled resources** - As needed (unlimited, scripts can execute without loading into context)

## Project Structure

```
skills/
├── .claude-plugin/
│   └── marketplace.json          # Central plugin configuration
├── skills/
│   ├── prompt-optimizer/         # 57 AI prompt engineering frameworks
│   ├── skill-creator/            # Custom skill creation toolkit
│   ├── mcp-builder/              # MCP server development framework
│   ├── docx/                     # Word document processing
│   ├── pptx/                     # PowerPoint processing
│   ├── xlsx/                     # Excel spreadsheet handling
│   └── pdf/                      # PDF form manipulation
└── CLAUDE.md
```

### Relationship: marketplace.json → SKILL.md

- **marketplace.json**: Index/catalog that defines logical groupings of skills
- **SKILL.md files**: Actual skill implementation with detailed instructions

## Skill Creation Commands

When creating new skills, use the scripts in `skill-creator/`:

```bash
# Initialize a new skill template
python3 skills/skill-creator/scripts/init_skill.py <skill-name> --path <output-directory>

# Package and validate a skill into distributable .skill file
python3 skills/skill-creator/scripts/package_skill.py <path/to/skill-folder> [output-dir]

# Quick validation during development
python3 skills/skill-creator/scripts/quick_validate.py <path/to/skill-folder>
```

## Skill Structure

Every skill must follow this pattern:

```
skill-name/
├── SKILL.md (required)
│   ├── YAML frontmatter (name, description only)
│   └── Markdown body (imperative/infinitive form)
├── scripts/          # Executable code (optional)
├── references/       # Documentation for context (optional)
└── assets/           # Files for output (optional)
```

**Do NOT create** in skill directories: README.md, INSTALLATION_GUIDE.md, QUICK_REFERENCE.md, CHANGELOG.md, or other auxiliary documentation.

### SKILL.md Frontmatter (Critical)

The `description` field is the **primary triggering mechanism** for skills:

```yaml
---
name: skill-name
description: What the skill does AND when to use it. Include all "when to use" information here—not in the body.
---
```

The body is only loaded AFTER triggering, so "When to Use This Skill" sections in the body are not helpful.

### Progressive Disclosure Patterns

Keep SKILL.md under 500 lines. Split content using these patterns:

1. **High-level guide with references**: Link advanced features to separate files
2. **Domain-specific organization**: Separate by domain/framework to avoid loading irrelevant context
3. **Conditional details**: Show basics, link to advanced

Example for multi-domain skills:
```
skill/
├── SKILL.md          # Overview and navigation
└── reference/
    ├── finance.md    # Loaded only for finance tasks
    ├── sales.md      # Loaded only for sales tasks
    └── marketing.md  # Loaded only for marketing tasks
```

## Writing Conventions

- **Use imperative/infinitive form**: "Create a skill" not "You should create a skill"
- **Be concise**: Context window is a shared resource. Challenge each sentence for necessity.
- **Avoid duplication**: Information lives in SKILL.md OR references, not both
- **Reference clearly**: When splitting content, explicitly state when to read reference files

## Adding New Skills

1. Create skill using `init_skill.py`
2. Implement scripts, references, or assets as needed
3. Write SKILL.md with clear frontmatter description
4. Validate and package with `package_skill.py`
5. Add entry to `.claude-plugin/marketplace.json`:

```json
{
  "name": "skill-group-name",
  "description": "Human-readable description",
  "source": "./",
  "strict": false,
  "skills": ["./skills/skill-name"]
}
```

## Key Design Principles

1. **Context Efficiency**: Progressive disclosure keeps context usage minimal
2. **Modularity**: Each skill is self-contained and independently loadable
3. **Degrees of Freedom**: Match specificity to task fragility—low freedom for error-prone operations, high freedom for creative tasks
4. **No Build Process**: This is a documentation/plugin marketplace—no compilation needed

## Important Context

- **License**: MIT License for main project; individual skills may have their own licenses
- **Installation**: Users install via `/plugin marketplace add samlaudev/skills`
- **No tests/build**: This is a skill collection, not a traditional software project
