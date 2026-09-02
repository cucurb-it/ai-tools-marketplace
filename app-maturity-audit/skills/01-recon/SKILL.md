---
name: audit-recon
description: RECON stage of the Application Maturity Audit. Loaded by the app-maturity-audit governing skill at the start of a new audit to scaffold the analysis bundle and orient on the codebase. Not a standalone entry point — the governing skill invokes it.
---

# Audit — RECON Stage

Scaffold the bundle and build the shared orientation that every dimension pass will use.
Read `skills/00-governing-audit/references/bundle-conventions.md` first — it defines the
folder layout and frontmatter for every file created here.

## Procedure

### Step 1 — Scaffold the bundle
Create the skeleton in `{{AUDIT_FOLDER}}` per bundle-conventions:
- `STATE.md` (`type: State`, Stage: `RECON`)
- `log.md` (`type: Log`) with today's date heading and a "audit started" entry
- `index.md` (`type: Index`, regenerable — will fill as files appear)
- `recon.md` (`type: Recon`)
- empty `dimensions/`, `docs/`, `adrs/`

### Step 2 — Orient
A fast pass, not a deep analysis. Determine and record in `recon.md`:
- Languages and framework(s); **software type** (service / library / CLI / frontend / monorepo)
- Entry points; build files; CI configuration; test directories; any `docs/`
- Repository size; large vendored or generated areas to **skip** during scoring
- Anything that will cap confidence (huge monorepo, no runtime access, generated code)

Keep it to a paragraph or two. Its only job is to let each dimension pass search efficiently
and calibrate to the software type.

### Step 2b — System Profile
Record the system's composition under a `## System Profile` heading in `recon.md`. These are
**descriptors, not scores** — a well-run monolith is not inherently below a microservices
sprawl. The profile calibrates the rubrics (a distributed system and a monolith have different
reasonable ceilings for reliability, observability, performance, deployment) and anchors the
TCO narrative. Capture what the code actually shows:
- **Decomposition style** — monolith / modular monolith / layered n-tier / functional
  decomposition / DDD / volatility-based / microservices / event-driven (name the closest).
- **Topology & tiers** — physical/logical tiers; process and deployment units.
- **Runtime & concurrency model** — sync/async; threads/workers/event loop; batch vs online.
- **Integration & coupling style** — in-process calls / shared DB / synchronous HTTP /
  asynchronous messaging.
- **Data architecture** — single DB / DB-per-service / CQRS / event-sourced; migration approach.
- **State & scaling model** — stateful vs stateless; vertical vs horizontal scaling story.

Note whether the decomposition looks aligned to **axes of change (volatility)** or to
**functional axes** — that observation feeds the Adaptability dimension directly.

### Step 3 — Hand back
Set `STATE.md` Stage to `SCORING`. Append the transition to `log.md`. Regenerate `index.md`.
Return control to the governing skill, which loads `skills/02-dimension-analysis/SKILL.md`.
