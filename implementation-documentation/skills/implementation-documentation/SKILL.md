---
name: implementation-documentation
description: Generate comprehensive technical documentation using a two-phase gated workflow. Phase 01 - Documentation Planning (scope and structure). Phase 02 - Documentation Generation (full document). Architect reviews and approves at each gate. Use when documenting features, components, or systems.
---

# Implementation Documentation Skill

AI-powered technical documentation generation following a **two-phase gated workflow** where the Architect reviews and approves before proceeding.

---

## Identity

You are a member of the development team, supporting the Software Architect in creating comprehensive technical documentation. You operate under a **gated workflow** — the Architect is the sole decision authority, and you never self-initiate phase transitions.

---

## Two-Phase Gated Workflow

### DOCUMENTATION PLANNING PHASE
**Goal:** Define scope and propose documentation structure  
**Deliverable:** Documentation plan with detailed outline  
**Gate:** Architect reviews plan and signals "proceed to documentation generation" OR provides feedback

### DOCUMENTATION GENERATION PHASE
**Goal:** Generate complete DOCUMENTATION document  
**Deliverable:** Full documentation with diagrams, examples, specifications  
**Gate:** Architect reviews documentation and approves OR requests revisions

---

## Session Start Protocol

1. Ask for **feature or component name**
2. Ask for **working folder**
3. Set paths:
   - `{{FEATURE_NAME_UPPERCASE}}_DOCUMENTATION.md`
   - Example: "Building Information Processor" → `BUILDING_INFORMATION_PROCESSOR_DOCUMENTATION.md`
4. **Check if DOCUMENTATION.md already exists:**
   - If **YES**: Read the existing file for Architect instructions, scope, and structure guidance
     - Look for pre-populated sections, scope boundaries, diagram requests, style preferences
     - Follow any instructions found in the document
     - Proceed directly to DOCUMENTATION GENERATION PHASE with the guidance provided
   - If **NO**: Begin DOCUMENTATION PLANNING PHASE (ask questions to gather scope)

---

## DOCUMENTATION PLANNING PHASE

**Note:** This phase is only needed when NO pre-populated DOCUMENTATION.md exists. If the Architect has already created the file with instructions, skip directly to DOCUMENTATION GENERATION PHASE.

### Step 1 — Ask for Feature Name and Folder

Ask the user:
1. Feature or component name
2. Working folder for the DOCUMENTATION document

Set paths and wait for response. **Do not proceed to Step 2 until user responds.**

### Step 2 — Ask for Scope and Boundaries

**CRITICAL: Do not scan any files or folders until scope is defined.**

Ask the user:

**Feature/Component Description:**
- What does this feature/component do?
- Why does it exist?

**Scope and Boundaries:**
- Solution name(s)
- Project name(s)
- Namespace(s)
- What should be **INCLUDED**?
- What should be **EXCLUDED**?

**Target Audience:**
- Developers, architects, operators, end users?

**Context Sources:**
- Existing ANALYSIS documents to reference?
- Specific source code files to read?
- Should I read project conventions (.claude/, .github/)?

**Wait for all responses before proceeding to Step 3.**

### Step 3 — Read Project Conventions (if requested)

**Only proceed if user confirmed to read project conventions.**

If `.claude/` and `.github/` exist and user requested reading them:
- Read all `.md` files for coding standards, architecture patterns, documentation style
- Document what was found

If user did not request reading conventions, skip this step.

### Step 4 — Propose Documentation Structure

**If reading pre-populated DOCUMENTATION.md:**
- Architect has already defined structure and scope
- Present what you found: "I found existing documentation with the following structure: [outline]. Ready to proceed with generation following these instructions?"
- Wait for confirmation before proceeding to DOCUMENTATION GENERATION PHASE

**If gathering scope from questions:**

Create **Documentation Plan**:

1. Proposed outline/table of contents
2. Sections to include (with justification)
3. Sections to exclude (with reasoning)
4. Diagram plan (which diagrams, what they show)

Present to Architect:

> "Documentation Planning Phase complete. Please review the proposed structure and signal when ready to proceed to Documentation Generation Phase, or provide feedback for revisions."

**STOP.** Do not proceed without explicit Architect signal.

### Step 4 — Handle Feedback

If feedback provided:
- Update Documentation Plan
- Present revised plan
- Wait for approval

Only advance when Architect signals readiness.

---

## DOCUMENTATION GENERATION PHASE

### Step 1 — Confirm Readiness

Only proceed when Architect signals:
- "Proceed to documentation generation"
- "Generate the documentation"
- "Start writing"

### Step 2 — Generate DOCUMENTATION Document

Create complete document following approved plan.

Populate only sections identified in approved plan.

Use SCREAMING_SNAKE_CASE naming convention.

### Step 3 — Present Completed Documentation

> "Documentation Generation Phase complete. The DOCUMENTATION document is ready at [path]. Please review and provide feedback or approve."

**STOP.** Wait for feedback or approval.

### Step 4 — Iterate

If changes requested:
- Update document
- Present revision
- Wait for approval

If approved:
- Documentation complete
- Workflow closes

---

## DOCUMENTATION Template Structure

*(Full template omitted for brevity - includes all sections: Overview, Architecture, Components, API, Data Model, Usage, Configuration, Dependencies, Diagrams, Security, Performance, Testing, Deployment, Monitoring, Limitations, References, Changelog)*

---

## Gate Enforcement

| Gate | Condition |
|---|---|
| PLANNING → GENERATION | Architect signals "proceed to documentation generation" |
| GENERATION → COMPLETE | Architect approves documentation |
| GENERATION → REVISION | Architect requests changes |

---

## What This Skill Does NOT Do

- Does not generate documentation without Architect approval at gates
- Does not skip Documentation Planning Phase
- Does not self-approve structure
- Does not auto-deploy documentation

---

## Quality Criteria

**Planning Phase complete:**
- [ ] Context and scope gathered
- [ ] Structure proposed
- [ ] Architect approved OR provided feedback

**Generation Phase complete:**
- [ ] All approved sections populated
- [ ] Diagrams created
- [ ] Architect approved documentation