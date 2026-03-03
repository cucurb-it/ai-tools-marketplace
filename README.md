# AI Tools Marketplace

Production-ready skills, agents, and workflows for AI-augmented software development by Cucurb IT BV.

---

## Available Tools

### Implementation Review
**Status:** Available  
**Version:** 26.303.2

AI-augmented code review skill that validates implementations against ANALYSIS documents, project conventions, and security best practices. Produces structured Review Reports for human and AI consumption.

**Use cases:**
- Review pull requests (human or AI-authored)
- Validate implementations against blueprints
- Audit code for security and quality issues
- Final review gate before merging

[Documentation →](./implementation-review/)

---

## Installation

### Install the Marketplace

```bash
/plugin marketplace add cucurb-it/ai-tools-marketplace
```

### Install Individual Tools

```bash
# Implementation Review
/plugin install implementation-review@ai-tools-marketplace
```

### Install via VS Code Extension

1. Install the [Agent Plugins extension](https://github.com/timheuer/vscode-agent-plugins)
2. Command Palette → `Agent Plugins: Add Marketplace`
3. Enter: `cucurb-it/ai-tools-marketplace`
4. Browse and install tools

---

## For GitHub Copilot CLI Users

```bash
# Add marketplace
gh copilot skill marketplace add cucurb-it/ai-tools-marketplace

# Install tools
gh copilot skill install implementation-review
```

---

## Repository Structure

```
ai-tools-marketplace/
├── .claude-plugin/
│   └── marketplace.json          ← Catalog of all tools
├── implementation-review/         ← Individual tool
│   ├── .claude-plugin/
│   │   └── plugin.json
│   ├── skills/
│   │   └── implementation-review/
│   │       └── SKILL.md
│   └── README.md
└── [future-tool]/
```

Each tool is independently versioned and installable.

---

## Versioning

All tools in this marketplace use **date-based versioning**: `YY.MDD.N`

- `YY` = two-digit year
- `M` = month without leading zero (2, not 02)
- `DD` = day with leading zero (01, 18)
- `N` = increment (resets daily)

Example: `26.218.1` = February 18, 2026, first release

---

## Contributing

These tools are developed and maintained by Cucurb IT BV based on real-world software development experience. 

If you have feedback or suggestions, please open an issue.

---

## License

MIT License - see individual tool directories for details.

---

## Related Projects

- [Analysis-Gated Workflow](https://github.com/cucurb-it/analysis-gated-workflow-skills) - Structured phase-gated workflow for software development and refactoring
