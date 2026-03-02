---
name: documentation
description: Generate comprehensive technical documentation using a two-phase gated workflow. Phase 01 - Documentation Planning (scope and structure). Phase 02 - Documentation Generation (full document). Architect reviews and approves at each gate. Use when documenting features, components, or systems.
---

# Documentation Skill

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
4. Begin DOCUMENTATION PLANNING PHASE

---

## DOCUMENTATION PLANNING PHASE

### Step 1 — Gather Context & Scope

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
- Existing ANALYSIS documents?
- Source code files to read?
- Project conventions (.claude/, .github/)?

Wait for responses.

### Step 2 — Read Project Conventions

If `.claude/` and `.github/` exist, read all `.md` files for:
- Coding standards
- Architecture patterns
- Documentation style

### Step 3 — Propose Documentation Structure

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
