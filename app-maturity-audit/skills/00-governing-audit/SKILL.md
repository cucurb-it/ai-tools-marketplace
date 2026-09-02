---
name: app-maturity-audit
description: Governs the Application Maturity Audit — a gated workflow that assesses a codebase's production maturity and modernization needs, then emits a sliced analysis bundle (a folder of markdown files, not one document). Orchestrates the recon, dimension-analysis, scorecard-review, and synthesis stage skills, enforces a human review gate on the scores, and manages bundle state. Use when starting or resuming an audit — including "maturity audit", "production readiness review", "application health check", "tech debt assessment", "legacy modernization assessment", "is this repo slow / insecure / hard to maintain", or "is this ready to ship or scale" — even if the exact words "maturity audit" are not used.
---

# Application Maturity Audit — Governing Skill

## Identity

You support a maturity audit of a single codebase. You are not an independent agent: you
score against explicit rubrics, back every score with evidence, and **stop at the review
gate** for human validation before writing any budget-owner document.

**CRITICAL**: You confirm you have read the current stage's skill before executing it.
**CRITICAL**: You never write an audience document before the Architect has reviewed the scores.
**CRITICAL**: You follow the bundle conventions exactly (paths, frontmatter, templates).

The audit answers two questions and keeps them separate:
1. **Can you responsibly keep running this as-is?** — the production-readiness gate.
2. **How much is it holding you back, and how urgently should you act?** — modernization pressure.

## Output: a sliced analysis bundle

The audit emits a **bundle** — a folder of small markdown files, not one document — sliced on
two axes:
- **Vertical = the ten dimensions.** Each is a self-contained folder under `dimensions/` with
  a full `detail.md` and a bounded `summary.md`.
- **Horizontal = layers across all dimensions.** Depth (`index.md` → per-dimension
  `summary.md` → `scorecard.md` → `detail.md`) and audience (`docs/doc-executive.md`,
  `doc-business.md`, `doc-technical.md`).

`references/bundle-conventions.md` (in this skill's folder) is the **single source of truth**
for the folder layout, per-file frontmatter, navigation bars, stable anchors, the regenerable
`index.md` rules, STE writing style, and the audience-document templates. Every stage skill
refers back to it. Read it before creating or writing any bundle file.

## The maturity model

| Level | Label | Meaning |
|-------|-------|---------|
| 0 | Absent | Not present at all. |
| 1 | Initial | Ad-hoc, inconsistent, undocumented. |
| 2 | Emerging | Basic version exists but has real gaps. |
| 3 | Established | Consistent, documented, covers the common cases. |
| 4 | Optimized | Comprehensive, automated, monitored, improved. |

A dimension sits at the highest level whose criteria are substantially met; unmet
higher-level criteria become findings and recommendations. No fractional per-dimension levels.

## Dimensions

Eleven dimensions. Their rubrics live with the dimension-analysis skill
(`skills/02-dimension-analysis/references/`).

| Dimension | Critical | Cluster |
|-----------|:---:|:---:|
| Performance & scalability | | ★ |
| Security | ★ | |
| Testing | ★ | |
| Reliability | ★ | |
| Adaptability | | ★ |
| CI/CD & deployment | | |
| Observability | | |
| Dependency health | | ★ |
| Code quality | | ★ |
| Architecture | | ★ |
| Documentation | | |

**A ★ marks membership.** **Critical** dimensions (security, testing, reliability) drive the
readiness gate. **Cluster** dimensions (the legacy cluster) drive modernization pressure.
**Adaptability** — the inverse of a system's inherent resistance to change — is the largest
single driver of development TCO and a proxy for estimate reliability; it is scored
higher-is-better (high = low resistance) and dominates both the pressure and TCO signals.

The scorer (`build_scorecard.py`, owned by the scorecard-review skill) computes **four**
signals — never hand-compute these: (1) **weighted average** overall maturity (uses the
Weight column); (2) **production-readiness gate**, the minimum among critical dimensions;
(3) **modernization pressure**, from the legacy cluster weighted so adaptability dominates;
(4) **TCO signature**, a *relative* cost-of-ownership burden weighted so adaptability
dominates (static audits give a relative signature, not euros).

The **System Profile** captured in recon (composition, tiers, topology, coupling, data
architecture) is a recorded descriptor, not a scored dimension; it calibrates the rubrics and
anchors the TCO narrative.

## Stages & stage-skill map

| Stage | Skill to load | Advances when |
|---|---|---|
| RECON | `skills/01-recon/SKILL.md` | recon.md written; bundle scaffolded |
| SCORING | `skills/02-dimension-analysis/SKILL.md` | all applicable dimensions scored (3 files each) |
| AGGREGATE & REVIEW | `skills/03-scorecard-review/SKILL.md` | **Architect gives explicit go-signal** |
| SYNTHESIS | `skills/04-synthesis/SKILL.md` | three audience docs written; bundle COMPLETE |

## Session Start Protocol

### Step 1 — Resolve application name and folder
Arguments arrive as `for '<application-name>' in '<audit-folder-path>'`. Extract
`{{APP_NAME}}` and `{{AUDIT_FOLDER}}`. If either is missing, ask only for the missing piece.

### Step 2 — New vs resume
Check whether `{{AUDIT_FOLDER}}/STATE.md` exists.
- **Absent → New audit.** Load `skills/01-recon/SKILL.md` and begin the RECON stage.
- **Present → Resume.** Read `STATE.md` (live state), skim recent `log.md`, read the current
  stage's context. Give the Architect a concise status (stage, what's done, what's pending),
  then load the skill for the current stage and resume.

## The review gate (absolute)

After SCORING and AGGREGATE, `STATE.md` reads `Stage: AWAITING ARCHITECT REVIEW`. **Stop.**
Present the scorecard and dimension summaries and wait. The Architect may correct any level —
treat a correction like an authoritative constraint: update that dimension's `result.json` and
`detail.md`, re-run the scorer, regenerate `index.md`. Only an explicit go-signal ("generate
the documents", "proceed to synthesis") releases SYNTHESIS. If asked to skip the review, flag
it and proceed only on explicit confirmation.

## Bundle state protocol

- `STATE.md` is the **single source of live state** (current stage, dimensions scored,
  what's awaited). Update it at every stage transition.
- `index.md` is **regenerable** from frontmatter and holds no live state — rebuild it,
  grouped by type, per the rules in `references/bundle-conventions.md`, whenever the bundle
  changes.
- `log.md` records the run timeline and any Architect instructions (score corrections, the
  gate go-signal). Append; do not rewrite history.
- `scorecard.md` is **machine-owned** — always regenerated by the scorer, never hand-edited.

## Invariants

1. Every level traces to a cited file path. A score with no evidence is not valid.
2. The audit is **static (code-only) by default**; runtime properties (especially
   performance) are inferred and confidence-flagged, never asserted as measured.
3. No audience document is written before the review gate is cleared.
4. Audience docs are **seeds** — STE-styled, `expandable: true`, never shared verbatim
   externally; they are expanded or redacted from the seed for the actual reader.
5. Never fabricate evidence — "I did not find X" is a legitimate, valuable result.
6. Every session ends with `STATE.md` (and any touched `summary.md`) reflecting reality.

## Stage overview

```
RECON            scaffold bundle · orient on the codebase · write recon.md
   ↓
SCORING          fan out: score each dimension against its rubric → result.json + detail.md + summary.md
   ↓
AGGREGATE        run build_scorecard.py → scorecard.md (3 signals) · regenerate index.md
   ↓  [STATE: AWAITING ARCHITECT REVIEW]
REVIEW GATE  ←── Architect validates/corrects scores        [correction → re-score dimension, re-run scorer]
   ↓  [Architect go-signal]
SYNTHESIS        doc-technical · doc-executive (evolution-gap discipline) · doc-business  →  bundle COMPLETE
```
