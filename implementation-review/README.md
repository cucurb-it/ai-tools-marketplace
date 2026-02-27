# Implementation Review

AI-augmented code review skill that validates implementations against ANALYSIS documents, project conventions, and security best practices.

---

## Overview

This skill performs **state-based review** — it reviews the current codebase state, regardless of authorship (AI, human, or mixed). It validates against:

- ANALYSIS documents (if present)
- Project conventions (.claude/, .github/)
- Security best practices
- Code quality standards
- Implementation plans

Produces structured **Review Reports** for human and AI consumption.

---

## Features

✅ **Context-aware** — adapts to available documentation  
✅ **Flexible** — works standalone or with Analysis-Gated Workflow  
✅ **Security-focused** — scans for null safety, input validation, error handling  
✅ **Convention-compliant** — validates against project-specific rules  
✅ **Change-aware** — identifies what changed since implementation  
✅ **Actionable** — categorizes findings by severity with clear recommendations  

---

## Installation

### Via Claude Code CLI

```bash
/plugin marketplace add cucurb-it/ai-tools-marketplace
/plugin install implementation-review@ai-tools-marketplace
```

### Via GitHub Copilot CLI

```bash
gh copilot skill marketplace add cucurb-it/ai-tools-marketplace
gh copilot skill install implementation-review
```

### Via VS Code Extension

Install the [Agent Plugins extension](https://github.com/timheuer/vscode-agent-plugins) and add the marketplace through the UI.

---

## Usage

### Standalone Review

```bash
# Review current working directory
/implementation-review

# Review with specific ANALYSIS document
Review the implementation against docs/FEATURE_ANALYSIS.md

# Review specific folder
Review the src/Platform/VrvSelection implementation
```

### With Analysis-Gated Workflow

The skill can be invoked automatically at Phase 06 or manually by the Architect before final commit.

---

## What Gets Reviewed

### Functional Requirements
- Does implementation satisfy the feature request?
- Are acceptance criteria met?
- Does it align with Implementation Plan?

### Project Conventions
- CRITICAL/MANDATORY rules followed?
- Naming conventions respected?
- Architecture boundaries maintained?
- Technology constraints followed?

### Code Quality
- Simplicity First — simple as possible?
- Minimal Impact — only necessary changes?
- No Temporary Fixes — production-ready?
- Senior Developer Standards — high quality?

### Security & Safety
- Input validation present?
- Null safety — no null dereference risks?
- Error handling appropriate?
- No hardcoded secrets?

### Deviations & Scope
- Unauthorized deviations from plan?
- Scope creep (unrelated changes)?
- New dependencies without approval?

---

## Review Report

The skill produces `IMPLEMENTATION_REVIEW_REPORT_[TIMESTAMP].md` with:

- **Overall assessment** (APPROVED / CHANGES REQUESTED / REJECTED)
- **Findings by severity** (CRITICAL → INFO)
- **Compliance assessment** against conventions
- **Change delta analysis** (what changed since implementation)
- **Actionable recommendations** (must fix / should fix / consider)
- **Approval status and next steps**

---

## Configuration (Optional)

Create `.claude/review-config.json`:

```json
{
  "severity_thresholds": {
    "null_safety_violations": "CRITICAL",
    "missing_input_validation": "HIGH",
    "style_violations": "LOW"
  },
  "auto_detect_analysis_document": true,
  "analysis_document_paths": [
    "docs/*_ANALYSIS.md",
    "*_ANALYSIS.md"
  ],
  "exclude_patterns": [
    "**/node_modules/**",
    "**/bin/**",
    "**/obj/**"
  ]
}
```

---

## Use Cases

**PR Review** — validate pull requests before merge  
**Quality Gates** — automated review before deployment  
**Compliance Audits** — verify convention adherence  
**Security Scans** — identify safety issues  
**Post-Implementation Validation** — confirm requirements met  

---

## Integration

### Works With
- Analysis-Gated Workflow (optional)
- Standard git/PR workflows
- Any codebase (with or without ANALYSIS documents)
- Human review processes
- AI review agents (structured output)

### Supports
- Multiple programming languages
- Multiple project conventions
- Custom severity thresholds
- Flexible input paths

---

## Version

Current version: **26.218.1**  
Versioning scheme: `YY.MDD.N` (date-based)

---

## License

MIT License

Copyright (c) 2026 Cucurb IT BV

---

## Related Tools

- [Analysis-Gated Workflow](https://github.com/cucurb-it/analysis-gated-workflow-skills) - Structured workflow this skill integrates with
