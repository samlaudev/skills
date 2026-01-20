# Sam Lau's Agent Skills

A collection of [Claude Code](https://claude.com/claude-code) skills and plugins designed to extend Claude's capabilities with specialized workflows, prompt engineering frameworks, document processing, and Model Context Protocol (MCP) server development.

## Overview

This plugin marketplace provides ready-to-use skills that enhance Claude Code's functionality across multiple domains:

- **Prompt Engineering** - 57 proven frameworks for crafting optimized AI prompts
- **Skill Development** - Tools for creating custom Claude Code skills
- **MCP Building** - Framework for building Model Context Protocol servers
- **Document Processing** - Excel, Word, PowerPoint, and PDF manipulation capabilities

## Included Skills

### 1. Prompt Optimizer
57 proven prompt engineering frameworks including:
- RACEF, CRISPE, BAB frameworks
- Tree of Thought, Chain of Thought
- RICE, RELIC, SCAMPER
- And 50+ more for marketing, education, decision analysis, and creative work

### 2. Skill Creator
A tool for creating new custom skills that extend Claude's capabilities with specialized knowledge, workflows, or tool integrations.

### 3. MCP Builder
Framework for building Model Context Protocol (MCP) servers - the standard protocol for connecting AI assistants to external tools and data sources.

### 4. Document Skills Suite
Complete document processing capabilities:
- **xlsx** - Excel spreadsheet manipulation
- **docx** - Word document processing
- **pptx** - PowerPoint presentation handling
- **pdf** - PDF form filling and manipulation

## Installation

### Prerequisites
- [Claude Code](https://claude.com/claude-code) installed

### Install via Marketplace

Run the following command in Claude Code:

```bash
/plugin marketplace add samlaudev/skills
```

### Manual Installation (Alternative)

If you prefer to install from source:

1. Clone this repository:
```bash
git clone https://github.com/samlaudev/skills.git
```

2. Add the plugin to your Claude Code configuration:
```bash
claude plugin add /path/to/skills
```

## Usage

Once installed, skills are automatically available in Claude Code. Simply invoke them by name:

- **Prompt optimization**: "Use the prompt-optimizer skill to improve this prompt..."
- **Create a skill**: "Use the skill-creator to make a new skill for..."
- **Build an MCP**: "Use the mcp-builder to create a server for..."
- **Process documents**: "Use the xlsx skill to analyze this spreadsheet..."

### Example Conversations

```
You: I need to create a better prompt for code review
Claude: I'll use the prompt-optimizer skill with the RACEF framework...

You: Help me build an MCP server for my API
Claude: I'll use the mcp-builder skill to design and implement...
```

## Project Structure

```
skills/
├── .claude-plugin/
│   └── marketplace.json      # Plugin marketplace configuration
├── skills/
│   ├── prompt-optimizer/     # 57 prompt engineering frameworks
│   ├── skill-creator/        # Custom skill creation toolkit
│   ├── mcp-builder/          # MCP server development framework
│   ├── docx/                 # Word document processing
│   ├── pptx/                 # PowerPoint processing
│   ├── xlsx/                 # Excel spreadsheet handling
│   └── pdf/                  # PDF form manipulation
└── README.md
```

## Contributing

Contributions are welcome! Feel free to:
- Report issues
- Suggest new skill ideas
- Submit pull requests

## License

See [LICENSE](LICENSE) file for details.

## Author

**Sam Lau** - [GitHub](https://github.com/samlaudev)

## Acknowledgments

Built for [Claude Code](https://claude.com/claude-code) by Anthropic.
