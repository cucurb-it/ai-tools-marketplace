---
name: implementation-review
description: Review code implementations against ANALYSIS documents, project conventions, and security standards. Use when reviewing PRs, validating implementations, or auditing code quality. Produces structured Review Reports for human and AI review.
---

# Implementation Review Skill

AI-augmented code review that validates implementations against blueprints, conventions, and best practices. Works standalone or integrated with Analysis-Gated Workflow.

---

## When to Use This Skill

- Reviewing pull requests, human or AI-authored
- Validating implementations against ANALYSIS documents
- Auditing code for security issues and convention compliance
- Final review gate before merging to main
- Post-implementation quality checks

---

## How It Works

This skill performs **state-based review** — it reviews the current codebase state, not authorship. The code may have been written by AI, human, or both. The review assesses whether the current state meets requirements and quality standards.

### Skill Invocation Protocol

At the start of every review session:

1. Ask the user for the **feature or refactoring name** (same as used in ANALYSIS document, if present)
2. Ask for the **working folder** where the Review Report should be stored
3. Set:
   - `{{FEATURE_NAME}}` = the name provided (use as-is, no normalisation)
   - `{{FOLDER_NAME}}` = the folder provided
   - `{{FEATURE_NAME_UPPERCASE}}` = feature name converted to SCREAMING_SNAKE_CASE
   - Review Report path = `{{FOLDER_NAME}}/{{FEATURE_NAME_UPPERCASE}}_REVIEW_{{ISO_TIMESTAMP}}.md`
     where `{{ISO_TIMESTAMP}}` is the current date and time in ISO 8601 format: `YYYYMMDD_HHMMSS`
   - Example: "Building Information Processor" → `BUILDING_INFORMATION_PROCESSOR_REVIEW_20260218_143022.md`
4. Check if an ANALYSIS document exists at `{{FOLDER_NAME}}/{{FEATURE_NAME_UPPERCASE}}_ANALYSIS.md`
   - If present, use it as the review blueprint
   - If absent, review against project conventions only

### Review Process

1. **Gather Context**
   - Locate ANALYSIS document (if present)
   - Read project conventions (.claude/, .github/)
   - Identify git changes since implementation started
   
2. **Perform Review**
   - Cross-reference code against ANALYSIS document
   - Check compliance with project conventions
   - Scan for security issues, such as null checks, input validation, error handling
   - Identify deviations from Implementation Plan
   - Flag code quality issues
   
3. **Produce Review Report**
   - Categorize findings by severity (CRITICAL, HIGH, MEDIUM, LOW, INFO)
   - Document what changed between implementation and current state
   - Provide actionable recommendations
   
4. **Human Decision**
   - Architect reviews findings
   - Approves, requests changes, or rejects

---

## Inputs (Flexible)

### Required
- **Current codebase** — the working directory being reviewed

### Optional (Auto-detected)
- **ANALYSIS document** — blueprint for the implementation (searches common paths)
- **Implementation Plan** — within ANALYSIS document
- **Project conventions** — .claude/ and .github/ folders
- **Git history** — to identify delta between implementation commit and current HEAD
- **Feature branch** — to compare against base branch

### User-Specified
- Path to ANALYSIS document if not in standard location
- Base commit SHA for comparison
- Specific files/folders to review (or review entire working directory)

---

## Invocation

### Standalone Usage

The skill will prompt you for:
1. Feature or refactoring name
2. Folder for storing the Review Report

Then it will:
- Check for an ANALYSIS document at the standard path
- Review the current codebase state
- Produce a Review Report

```bash
# Review current working directory
/implementation-review

# The skill will ask for feature name and folder
```

### Integrated with Analysis-Gated Workflow

When invoked from Phase 06 of the workflow, the skill automatically uses:
- Feature name from the ANALYSIS document
- Same folder as the ANALYSIS document
- Existing ANALYSIS document as the review blueprint

---

## Review Checklist

The skill evaluates the current codebase against these criteria:

### Functional Requirements
- [ ] Does the implementation satisfy the original feature request?
- [ ] Are all acceptance criteria met?
- [ ] Does it align with the Implementation Plan intent (if ANALYSIS document exists)?

### Project Conventions Compliance
- [ ] CRITICAL/MANDATORY rules from .claude/ and .github/ followed?
- [ ] Naming conventions respected?
- [ ] Architecture boundaries respected?
- [ ] Technology constraints followed (e.g., .NET version restrictions)?
- [ ] Critical workflows followed (migrations, code generation)?

### Code Quality
- [ ] **Simplicity First** — is the solution as simple as possible?
- [ ] **Minimal Impact** — only necessary code changed?
- [ ] **No Temporary Fixes** — no TODOs, placeholders, or "fix later" code?
- [ ] **Senior Developer Standards** — production-ready quality?
- [ ] No unnecessary comments or over-documentation?

### Security & Safety
- [ ] Input validation present and correct?
- [ ] Null safety — all code paths checked for null dereference?
- [ ] Error handling appropriate?
- [ ] No hardcoded secrets or sensitive data?
- [ ] Authentication/authorization checks in place where needed?

### Deviations & Scope
- [ ] Were there unauthorized deviations from the Implementation Plan?
- [ ] Was scope creep introduced (unrelated refactoring, style changes)?
- [ ] Were new dependencies added without approval?

### Change Delta (if git available)
- [ ] What changed between implementation commit and current HEAD?
- [ ] Were changes made by humans after AI implementation?
- [ ] Do human changes introduce issues?

---

## Review Report Format

The skill produces a structured **Review Report** saved as:
`{{FOLDER_NAME}}/{{FEATURE_NAME_UPPERCASE}}_REVIEW_{{ISO_TIMESTAMP}}.md`

Example: `BUILDING_INFORMATION_PROCESSOR_REVIEW_20260218_143022.md`

This naming convention:
- Matches the ANALYSIS document convention (if present)
- Uses SCREAMING_SNAKE_CASE for feature name
- Includes ISO 8601 timestamp for multiple reviews of the same feature
- Makes Review Reports easy to locate alongside ANALYSIS documents

### Report Structure

Filename: `{{FEATURE_NAME_UPPERCASE}}_REVIEW_{{ISO_TIMESTAMP}}.md`

```markdown
# Implementation Review Report
# [FEATURE_NAME]

**Date:** YYYY-MM-DD HH:MM  
**Reviewer:** AI Model (with optional human co-review)  
**Branch/Commit:** [branch name or commit SHA]  
**ANALYSIS Document:** [path or "None"]

---

## Summary

**Overall Assessment:** [APPROVED / CHANGES REQUESTED / REJECTED]  
**Critical Issues:** [count]  
**High Priority Issues:** [count]  
**Medium Priority Issues:** [count]  
**Low Priority Issues:** [count]  

**Key Findings:**
- [Brief summary of most important findings]

---

## Findings by Category

### CRITICAL Issues

#### [Issue Title]
**Severity:** CRITICAL  
**File:** path/to/file.cs:line  
**Description:** [What the issue is]  
**Evidence:** [Code snippet or reference]  
**Recommendation:** [How to fix]  
**Reference:** [ANALYSIS doc section or convention rule that was violated]

---

### HIGH Priority Issues
[Same format as CRITICAL]

---

### MEDIUM Priority Issues
[Same format]

---

### LOW Priority Issues
[Same format]

---

### INFO / Observations
[Same format, for non-issues worth noting]

---

## Compliance Assessment

### Project Conventions
- ✓ CRITICAL/MANDATORY rules followed
- ✓ Naming conventions respected
- ⚠ [Any violations]

### Implementation Plan Alignment
- ✓ All planned phases completed
- ✓ No unauthorized deviations
- ⚠ [Any deviations documented]

### Code Quality Standards
- ✓ Simplicity First principle followed
- ✓ Minimal Impact maintained
- ⚠ [Any violations]

---

## Change Delta Analysis

**Implementation Commit:** [SHA]  
**Current HEAD:** [SHA]  
**Changes Since Implementation:** [file count]

### Modified by Humans Post-Implementation
| File | Lines Changed | Type of Change | Issues Introduced? |
|---|---|---|---|
| path/to/file.cs | +25 / -10 | Refactoring | None |
| path/to/other.cs | +5 / -0 | Bug fix | ⚠ Missing null check |

---

## Recommendations

### Must Fix (Blocking)
1. [Issue that must be resolved before merge]
2. [Another blocking issue]

### Should Fix (Non-blocking but important)
1. [Issue that should be addressed]
2. [Another important issue]

### Consider (Optional improvements)
1. [Suggestion for improvement]
2. [Another suggestion]

---

## Approval Status

**Status:** [APPROVED / CHANGES REQUESTED / REJECTED]

**Rationale:**
[Why this status was assigned]

**Next Steps:**
[What should happen next]
```

---

## What This Skill Does

- **Scans the current codebase state** (not just AI-written code)
- **Cross-references against ANALYSIS document** (if present)
- **Validates project conventions** from .claude/ and .github/
- **Identifies security issues** (null safety, input validation, error handling)
- **Flags deviations** from Implementation Plan
- **Documents change delta** (what changed since implementation)
- **Produces actionable Review Report** for human and AI consumption
- **Categorizes findings by severity** (CRITICAL → INFO)

---

## What This Skill Does NOT Do

- Does not auto-approve implementations
- Does not fix issues automatically (reports only)
- Does not assume AI authorship (reviews all code equally)
- Does not replace human judgment (augments it)
- Does not gate workflow without human decision

---

## Integration Points

### With Analysis-Gated Workflow
- Can be invoked automatically at Phase 06
- Uses ANALYSIS document as review blueprint
- Respects Implementation Plan structure

### With Standard PR Review
- Works on any branch without ANALYSIS document
- Reviews against project conventions only
- Produces same Review Report format

### With AI Review Agents
- Review Report is structured for AI consumption
- Another AI model (e.g., Opus) can analyze findings
- AI can categorize, summarize, or deep-dive on specific issues

---

## Configuration (Optional)

Create `.claude/review-config.json` to customize review behavior:

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
  ],
  "require_human_approval": true
}
```

---

## Quality Criteria

A review is complete when:

- [ ] All configured checks have been performed
- [ ] Review Report is generated and saved
- [ ] Findings are categorized by severity
- [ ] Recommendations are actionable
- [ ] Human reviewer has visibility into findings
- [ ] Approval status is clearly stated