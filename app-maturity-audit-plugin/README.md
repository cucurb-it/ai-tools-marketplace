# Application Maturity Audit — Skill Set

A structured, gated workflow that audits a codebase's **production maturity** and
**modernization needs**, governed by a Software Architect and supported by AI (Claude Code
CLI or Copilot CLI). It scores ten engineering dimensions against evidence, pauses for human
review, and produces a sliced analysis bundle for three audiences.

---

## Skills

| Folder | Skill | Stage |
|---|---|---|
| `00-governing-audit/` | Governing Audit | All stages — orchestrator |
| `01-recon/` | Recon | RECON — scaffold bundle, orient on the codebase |
| `02-dimension-analysis/` | Dimension Analysis | SCORING — score each dimension against its rubric |
| `03-scorecard-review/` | Scorecard & Review | AGGREGATE & REVIEW — compute signals, hold the gate |
| `04-synthesis/` | Synthesis | SYNTHESIS — write the audience documents |

Each run produces an **analysis bundle** — a folder of markdown files, not one document.

---

## Installation

### Via Claude Code CLI
```bash
/plugin marketplace add https://github.com/cucurb-it/app-maturity-audit-skills.git
/plugin install app-maturity-audit@cucurb-it-app-maturity-audit
```

### Local installation
```bash
# Project-level
cp -r skills/ .claude/skills/
# User-level
cp -r skills/ ~/.claude/skills/
```

## How to start

Load the governing skill and follow its Session Start Protocol:
```
Read skills/00-governing-audit/SKILL.md and start an audit for '<app-name>' in '<audit-folder>'.
```
The governing skill scaffolds the bundle and orchestrates the stages from there — new or resume.

---

## Core principles

### The analysis bundle
Output is a folder of small markdown files, one per concept, with YAML frontmatter and
bundle-relative links — because not every reader needs all the information at once. It is
*inspired by* the Open Knowledge Format (OKF) but is **not OKF-conformant**: this is
single-run audit state, not a shared knowledge base.

### Two axes
- **Vertical = the ten dimensions.** Each is a self-contained folder under `dimensions/` with
  a full `detail.md` and a bounded `summary.md`.
- **Horizontal = layers across all dimensions.** Depth (`index.md` → `summary.md` →
  `scorecard.md` → `detail.md`) and audience (`docs/doc-executive.md`, `doc-business.md`,
  `doc-technical.md`).

### Two verdicts
- **Production-readiness gate** — the weakest of the critical dimensions (security, testing,
  reliability). Answers: can you responsibly keep running this?
- **Modernization pressure** — from the legacy cluster (architecture, performance,
  dependency health, code quality). Answers: how urgently should you act? A repo can pass the
  gate yet carry High pressure — safe today, a growing brake.

### The review gate
The audit scores autonomously, then **stops** at `AWAITING ARCHITECT REVIEW`. No audience
document is written until the Architect validates or corrects the scores and gives an explicit
go-signal. A correction is treated like an authoritative constraint: re-score the dimension,
re-run the scorer, regenerate the index.

### Audience documents
Three seeds, written only after the gate, in the style of Simplified Technical English,
marked `expandable: true`, never shared verbatim externally. The **executive** brief follows
an *evolution-gap discipline*: every weakness ties to a specific dimension finding and its
business consequence — no invented solution, cost, or timeline, and no vague "the system is
old" framing.

### Governing rules
- The scorecard is **machine-computed** (`build_scorecard.py`) and never hand-edited.
- Every level traces to a cited **file path**; absence of evidence is a finding, not a guess.
- The audit is **static (code-only)** by default; runtime properties are inferred and
  confidence-flagged.
- `STATE.md` is the single source of live state; `index.md` is regenerable and holds none.

---

## Stage overview

```
RECON            scaffold bundle · orient · recon.md
   ↓
SCORING          fan out: each dimension → result.json + detail.md + summary.md
   ↓
AGGREGATE        build_scorecard.py → scorecard.md (3 signals) · regenerate index.md
   ↓  [STATE: AWAITING ARCHITECT REVIEW]
REVIEW GATE  ←── Architect validates/corrects scores   [correction → re-score → re-run scorer]
   ↓  [Architect go-signal]
SYNTHESIS        doc-technical · doc-executive · doc-business  →  COMPLETE
```
