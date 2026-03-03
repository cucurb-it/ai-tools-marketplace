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

**For all diagrams, generate BOTH formats:**
1. PlantUML/Mermaid markup (for rendering in tools that support it)
2. ASCII art representation (for plain text viewing)

Present both formats for each diagram so the Architect can choose which to keep.

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

All diagrams should be generated in **both PlantUML/Mermaid and ASCII art formats**.

Example:

```markdown
### Architecture Diagram

**PlantUML:**
\```plantuml
@startuml
[Component A] --> [Component B]
[Component B] --> [Database]
@enduml
\```

**ASCII Art:**
\```
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
\```
```

Or using Mermaid:

```markdown
**Mermaid:**
\```mermaid
graph TD
    A[Component A] --> B[Component B]
    B --> C[Database]
\```

**ASCII Art:**
\```
    ┌───────────┐
    │Component A│
    └─────┬─────┘
          │
          ▼
    ┌───────────┐
    │Component B│
    └─────┬─────┘
          │
          ▼
    ┌─────────┐
    │ Database│
    └─────────┘
\```
```

**Apply this dual-format approach to all diagrams:**
- Architecture diagrams
- Service contract diagrams
- Component diagrams
- Sequence diagrams
- State diagrams
- Entity relationship diagrams

**Documentation sections (in order):**

1. **Overview** — Purpose, scope, audience
2. **Architecture** — High-level design, architecture diagrams, patterns
3. **Service Contracts** — Business capabilities, interfaces, behavioral contracts (CRITICAL SECTION)
4. **Components** — Detailed component breakdown
5. **API / Interfaces** — Public APIs with examples
6. **Data Model** — Entities, relationships, ERDs
7. **Usage Examples** — Basic and advanced scenarios
8. **Configuration** — Settings, environment variables
9. **Dependencies** — Packages, libraries, external services
10. **Sequence Diagrams** — Interaction flows
11. **State Diagrams** — State machines and transitions
12. **Error Handling** — Exceptions, error codes
13. **Performance** — Characteristics, bottlenecks
14. **Security** — Authentication, authorization, data protection
15. **Testing** — Unit tests, integration tests, coverage
16. **Deployment** — Steps, configuration, rollback
17. **Monitoring** — Metrics, alerts, logging
18. **Known Limitations** — Current constraints
19. **Future Enhancements** — Planned improvements
20. **Related Features** — Dependencies and relationships
21. **References** — Links to related docs
22. **Changelog** — Version history

### Service Contracts Section Template

The Service Contracts section should thoroughly document:

**Business Capabilities:**
- What business capabilities does this component/service expose?
- What business problems does it solve?
- Who are the consumers of these capabilities?

**Service Contract Definition:**
- Interface definitions (C# interfaces, API contracts, message contracts)
- Operations exposed by the service
- Expected behavior for each operation

**Contract Diagrams (both PlantUML/Mermaid and ASCII):**
- Service contract overview showing consumers and providers
- Contract dependencies between services

**Data Contracts:**
- Request/response message structures
- DTOs and their fields
- Validation rules

**Behavioral Contracts:**
- Preconditions (what must be true before calling)
- Postconditions (what will be true after calling)
- Invariants (what remains true throughout)

**Contract Versioning:**
- How contracts evolve over time
- Backward compatibility strategy
- Deprecation policy

**Quality of Service:**
- SLA requirements (response time, availability)
- Throughput expectations
- Error handling guarantees

**Example structure:**

```markdown
## Service Contracts

### Business Capabilities

This component exposes the following business capabilities:

1. **[Capability Name]**
   - **Purpose:** [What business need it addresses]
   - **Consumers:** [Who uses this capability]
   - **Business Rules:** [Key business rules enforced]

### Service Contract Overview

**PlantUML:**
\```plantuml
@startuml
interface IBuildingProcessor {
  + ProcessBuilding(request: BuildingRequest): BuildingResponse
  + ValidateBuilding(buildingId: Guid): ValidationResult
}

component BuildingProcessor implements IBuildingProcessor
component Client1 --> IBuildingProcessor
component Client2 --> IBuildingProcessor
@enduml
\```

**ASCII Art:**
\```
┌─────────────────────────────┐
│   IBuildingProcessor        │
│ ─────────────────────────── │
│ + ProcessBuilding()         │
│ + ValidateBuilding()        │
└──────────▲──────────────────┘
           │
           │ implements
           │
┌──────────┴──────────────────┐
│  BuildingProcessor          │
└─────────────────────────────┘
           ▲
           │
           │ consumes
   ┌───────┴────────┐
   │                │
┌──┴───┐      ┌────┴──┐
│Client│      │Client2│
│  1   │      │       │
└──────┘      └───────┘
\```

### Contract Operations

#### ProcessBuilding

**Signature:**
\```csharp
BuildingResponse ProcessBuilding(BuildingRequest request)
\```

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
\```csharp
public class BuildingRequest
{
    public Guid BuildingId { get; init; }
    public string BuildingType { get; init; }
    public BuildingData Data { get; init; }
}
\```

**Data Contract (Response):**
\```csharp
public class BuildingResponse
{
    public Guid ProcessingId { get; init; }
    public ProcessingStatus Status { get; init; }
    public ValidationResult[] Validations { get; init; }
}
\```

**Exceptions:**
- `ArgumentNullException` — Request is null
- `InvalidBuildingException` — Building data is invalid
- `TimeoutException` — Processing exceeded 5 seconds
- `UnauthorizedException` — User lacks permission

### Contract Dependencies

**This service consumes:**
- `IValidationService` — For building validation
- `IBuildingRepository` — For building persistence

**This service is consumed by:**
- Building Management UI
- Import Service
- Mobile App

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

**Guarantees:**
- At-least-once processing (may retry on failure)
- Results cached for 5 minutes
- Audit trail for all operations
```


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