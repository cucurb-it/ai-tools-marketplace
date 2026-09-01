---
name: audit-scorecard-review
description: AGGREGATE & REVIEW stage of the Application Maturity Audit. Loaded by the app-maturity-audit governing skill to compute the scorecard from the scored dimensions, regenerate the index, and enforce the human review gate before any audience document is written. Not a standalone entry point.
---

# Audit — AGGREGATE & REVIEW Stage

Turn the scored dimensions into the three headline signals, then hold the gate.

## Step 1 — Compute the scorecard (machine-owned)

Run the scorer:
```bash
python skills/03-scorecard-review/scripts/build_scorecard.py {{AUDIT_FOLDER}}/dimensions --out {{AUDIT_FOLDER}}
```
It reads every `dimensions/*/result.json` and writes:
- `scorecard.md` (`type: Scorecard`) — the table plus the three signals
- `summary.json` — machine-readable aggregate

The three signals: **weighted average** (overall maturity), **production-readiness gate**
(minimum level among security / testing / reliability), and **modernization pressure** (from
the legacy cluster — architecture / performance / dependency-health / code-quality). A repo
can pass the gate yet carry High pressure — safe to run today, but a growing brake. Use the
script's numbers verbatim; never hand-edit `scorecard.md`.

## Step 2 — Regenerate the index

Rebuild `index.md` from frontmatter, grouped by type (Bundle Control · Scorecard · Dimensions
lowest-level-first · Audience Documents · ADRs), per bundle-conventions.

## Step 3 — Open the review gate

Set `STATE.md` Stage to `AWAITING ARCHITECT REVIEW`, `Awaiting: architect review of scores`.
Present the scorecard and the dimension summaries to the Architect. **Stop here.**

## Step 4 — Apply corrections (loop)

If the Architect corrects a level, treat it as authoritative:
1. Update that dimension's `result.json` and `detail.md` to reflect the corrected level and
   the reason.
2. Re-run the scorer (Step 1) and regenerate `index.md` (Step 2).
3. Log the correction verbatim in `log.md`.
Stay at the gate until the Architect gives an explicit go-signal.

## Step 5 — Release

On an explicit go-signal ("generate the documents" / "proceed to synthesis"), set Stage to
`SYNTHESIS`, log the signal, and return control to the governing skill, which loads
`skills/04-synthesis/SKILL.md`. Never advance without the signal.
