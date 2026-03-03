---
name: implementation-documentation
description: Generate comprehensive technical documentation using a two-phase gated workflow with state tracking and prompt logging. Phase 01 - Documentation Planning. Phase 02 - Documentation Generation. Architect reviews at each gate. Commits to git at phase transitions.
---

# Implementation Documentation Skill

AI-powered technical documentation generation following a **two-phase gated workflow** with workflow state tracking, prompt logging, and automatic git commits at phase transitions.

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
   - If **YES**: Read the existing file for:
     - Workflow State (current phase)
     - Architect instructions, scope, structure guidance
     - Existing Prompt Log
     - Resume from current phase or proceed based on state
   - If **NO**: Create new DOCUMENTATION.md with Workflow State block, begin DOCUMENTATION PLANNING PHASE

---

## DOCUMENTATION PLANNING PHASE

**Note:** This phase is only needed when NO pre-populated DOCUMENTATION.md exists. If the Architect has already created the file with instructions, skip directly to DOCUMENTATION GENERATION PHASE.

### Step 1 — Create DOCUMENTATION.md with Workflow State

Create the file with this initial structure:

```markdown
# [FEATURE_NAME] Implementation Documentation

---
## WORKFLOW STATE

**Current Phase:** DOCUMENTATION PLANNING PHASE — IN PROGRESS  
**Last Updated:** YYYY-MM-DD HH:MM

### Phase History
- DOCUMENTATION PLANNING PHASE — Started: YYYY-MM-DD HH:MM
---

[Rest of document structure...]

---

## PROMPT LOG

### [YYYY-MM-DD HH:MM] — Session Start

**Prompt:**
```
[Initial user request]
```

**AI Response Summary:**
Created DOCUMENTATION document, beginning Planning Phase.

---
```

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

**Diagram Format Preference:**
- PlantUML, Mermaid, or both?
- If both: which diagram types should use which format?
- Note: ASCII art will be generated for ALL diagrams regardless of markup format

**Context Sources:**
- Existing ANALYSIS documents to reference?
- Specific source code files to read?
- Should I read project conventions (.claude/, .github/)?

**Log this prompt in PROMPT LOG section.**

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

### Step 5 — Handle Feedback or Complete Phase

**If feedback provided:**
- Log feedback in PROMPT LOG
- Update Documentation Plan
- Present revised plan
- Wait for approval

**When Architect signals to proceed:**
1. Update Workflow State to: `DOCUMENTATION PLANNING PHASE — COMPLETE`
2. Add completion timestamp to Phase History
3. Add new phase: `DOCUMENTATION GENERATION PHASE — Started: [timestamp]`
4. Log the proceed signal in PROMPT LOG
5. **Git commit**: Check if in git repo, if yes: `git commit -m "chore: complete DOCUMENTATION PLANNING PHASE [skip ci]"`
6. Advance to DOCUMENTATION GENERATION PHASE

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

**For all diagrams, generate BOTH formats:**
1. PlantUML/Mermaid markup (for rendering in tools that support it)
2. ASCII art representation (for plain text viewing)

Present both formats for each diagram so the Architect can choose which to keep.

**Update Workflow State:**
- Current Phase remains: `DOCUMENTATION GENERATION PHASE — IN PROGRESS`
- Update Last Updated timestamp

### Step 3 — Present Completed Documentation

> "Documentation Generation Phase complete. The DOCUMENTATION document is ready at [path]. Please review and provide feedback or approve."

**STOP.** Wait for feedback or approval.

### Step 4 — Iterate or Complete

**If changes requested:**
- Log change request in PROMPT LOG
- Update document
- Present revision
- Wait for approval

**If approved:**
1. Update Workflow State to: `DOCUMENTATION GENERATION PHASE — COMPLETE`
2. Add completion timestamp to Phase History
3. Log approval in PROMPT LOG
4. **Git commit**: `git commit -m "chore: complete DOCUMENTATION GENERATION PHASE [skip ci]"`
5. Documentation workflow complete

---

## DOCUMENTATION Template Structure

**All diagrams generated in both PlantUML/Mermaid and ASCII art formats.**

### Diagram Format Example

```markdown
### Architecture Diagram

**PlantUML:**
```plantuml
@startuml
[Component A] --> [Component B]
[Component B] --> [Database]
@enduml
```

**ASCII Art:**
```
     ,-----------.          ,-----------.
     |Component A|          |Component B|
     `-----------'          `-----------'
           |                      |
           |--------------------->|
           |                      |
           |                      v
           |                 ,--------.
           |                 |Database|
           |                 `--------'
```
```

### Documentation Sections (In Order)

1. **Workflow State** — Current phase, phase history (at top of document)
2. **Overview** — Purpose, scope, audience
3. **Architecture** — High-level design, architecture diagrams, patterns
4. **Service Contracts** — Business capabilities, interfaces, behavioral contracts (CRITICAL SECTION)
5. **Components** — Detailed component breakdown
6. **API / Interfaces** — Public APIs with examples
7. **Data Model** — Entities, relationships, ERDs
8. **Usage Examples** — Basic and advanced scenarios
9. **Configuration** — Settings, environment variables
10. **Dependencies** — Packages, libraries, external services
11. **Sequence Diagrams** — Interaction flows
12. **State Diagrams** — State machines and transitions
13. **Error Handling** — Exceptions, error codes
14. **Performance** — Characteristics, bottlenecks
15. **Security** — Authentication, authorization, data protection
16. **Testing** — Unit tests, integration tests, coverage
17. **Deployment** — Steps, configuration, rollback
18. **Monitoring** — Metrics, alerts, logging
19. **Known Limitations** — Current constraints
20. **Future Enhancements** — Planned improvements
21. **Related Features** — Dependencies and relationships
22. **References** — Links to related docs
23. **Changelog** — Version history
24. **Prompt Log** — All prompts and AI responses (at bottom of document)

---

## Service Contracts Section (Critical)

This section documents the business capabilities and behavioral contracts that drive implementation.

**Include:**

**Business Capabilities:**
- What business capabilities does this component/service expose?
- What business problems does it solve?
- Who are the consumers of these capabilities?

**Service Contract Definition:**
- Interface definitions (C# interfaces, API contracts, message contracts)
- Operations exposed by the service
- Expected behavior for each operation

**Contract Diagrams (PlantUML + ASCII):**
- Service contract overview showing consumers and providers
- Contract dependencies between services

**Data Contracts:**
- Request/response message structures
- DTOs and their fields
- Validation rules

**Behavioral Contracts:**
- **Preconditions:** What must be true before calling
- **Postconditions:** What will be true after calling
- **Invariants:** What remains true throughout
- **Behavioral guarantees:** Idempotency, timeout constraints, error handling

**Contract Versioning:**
- How contracts evolve over time
- Backward compatibility strategy
- Deprecation policy

**Quality of Service:**
- SLA requirements (response time, availability)
- Throughput expectations
- Error handling guarantees

**Example:**

```markdown
## Service Contracts

### Business Capabilities

This component exposes:

1. **Building Processing**
   - **Purpose:** Process building information and generate structural analysis
   - **Consumers:** Building Management UI, Import Service, Mobile App
   - **Business Rules:** Must validate building data before processing

### Service Contract Overview

**PlantUML:**
```plantuml
@startuml
interface IBuildingProcessor {
  + ProcessBuilding(request: BuildingRequest): BuildingResponse
  + ValidateBuilding(buildingId: Guid): ValidationResult
}

component BuildingProcessor implements IBuildingProcessor
component Client1 --> IBuildingProcessor
component Client2 --> IBuildingProcessor
@enduml
```

**ASCII Art:**
```
┌─────────────────────────────┐
│   IBuildingProcessor        │
│ ─────────────────────────── │
│ + ProcessBuilding()         │
│ + ValidateBuilding()        │
└──────────▲──────────────────┘
           │ implements
┌──────────┴──────────────────┐
│  BuildingProcessor          │
└─────────────────────────────┘
     ▲              ▲
     │              │
  Client1        Client2
```

### Contract Operations

#### ProcessBuilding

**Signature:**
```csharp
BuildingResponse ProcessBuilding(BuildingRequest request)
```

**Business Capability:** Process building information and generate structural analysis

**Preconditions:**
- Request must not be null
- Building ID must be valid GUID
- User must have ProcessBuilding permission

**Postconditions:**
- BuildingResponse returned with processing status
- Building marked as processed in database
- Audit log entry created

**Behavioral Contract:**
- **Must** validate all input before processing
- **Must** be idempotent (same input = same output)
- **Must** complete within 5 seconds or throw TimeoutException
- **Must** rollback changes if processing fails

**Data Contract (Request):**
```csharp
public class BuildingRequest
{
    public Guid BuildingId { get; init; }
    public string BuildingType { get; init; }
    public BuildingData Data { get; init; }
}
```

**Data Contract (Response):**
```csharp
public class BuildingResponse
{
    public Guid ProcessingId { get; init; }
    public ProcessingStatus Status { get; init; }
    public ValidationResult[] Validations { get; init; }
}
```

**Exceptions:**
- `ArgumentNullException` — Request is null
- `InvalidBuildingException` — Building data is invalid
- `TimeoutException` — Processing exceeded 5 seconds
- `UnauthorizedException` — User lacks permission

### Contract Versioning

**Current Version:** v2.0

**Version History:**
- v2.0 (2025-01): Added idempotency requirement
- v1.5 (2024-06): Added timeout constraint
- v1.0 (2023-12): Initial contract

**Backward Compatibility:**
- v1.x clients supported until 2026-12
- Deprecated: `ProcessBuildingLegacy` operation (remove in v3.0)

### Quality of Service

**SLA Requirements:**
- **Availability:** 99.9% uptime
- **Response Time:** P95 < 2 seconds, P99 < 5 seconds
- **Throughput:** Support 1000 requests/minute
- **Error Rate:** < 0.1% for valid requests
```

---

## Git Commit Protocol

At each phase transition, after updating Workflow State:

1. Check if DOCUMENTATION document is in a git repository
2. Check if git is configured (user.name, user.email)
3. If both pass: `git commit -m "chore: complete [PHASE_NAME] [skip ci]"`
4. If fails: continue silently (no error)

**Commit messages:**
- Planning complete: `chore: complete DOCUMENTATION PLANNING PHASE [skip ci]`
- Generation complete: `chore: complete DOCUMENTATION GENERATION PHASE [skip ci]`

This creates automatic checkpoints at phase boundaries for audit trail.

---

## Gate Enforcement

| Gate | Condition |
|---|---|
| PLANNING → GENERATION | Architect signals "proceed to documentation generation" |
| GENERATION → COMPLETE | Architect approves documentation |
| GENERATION → REVISION | Architect requests changes |

---

## What This Skill Does

- **Tracks workflow state** (current phase, phase history)
- **Logs all prompts** and AI responses for audit trail
- **Commits to git** at phase transitions
- **Reads pre-populated DOCUMENTATION.md** if Architect created it
- **Generates comprehensive documentation** with dual-format diagrams
- **Emphasizes Service Contracts** as critical business capability layer

---

## What This Skill Does NOT Do

- Does not generate documentation without Architect approval at gates
- Does not skip Documentation Planning Phase (unless pre-populated)
- Does not self-approve structure
- Does not auto-deploy documentation
- Does not modify Workflow State without explicit phase completion

---

## Quality Criteria

**Planning Phase complete:**
- [ ] Workflow State updated to COMPLETE
- [ ] Context and scope gathered
- [ ] Structure proposed
- [ ] Architect approved OR provided feedback
- [ ] Git commit created (if in repo)

**Generation Phase complete:**
- [ ] Workflow State updated to COMPLETE
- [ ] All approved sections populated
- [ ] Service Contracts thoroughly documented
- [ ] Diagrams created (both PlantUML and ASCII)
- [ ] Prompt Log maintained throughout
- [ ] Architect approved documentation
- [ ] Git commit created (if in repo)