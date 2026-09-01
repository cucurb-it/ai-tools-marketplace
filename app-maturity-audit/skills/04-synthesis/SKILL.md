---
name: audit-synthesis
description: SYNTHESIS stage of the Application Maturity Audit, run only after the review gate is cleared. Loaded by the app-maturity-audit governing skill to write the executive, business, and technical audience documents from the reviewed scores and dimension findings. Not a standalone entry point.
---

# Audit — SYNTHESIS Stage

Write the three audience seeds from the reviewed scores. **Precondition:** `STATE.md` Stage is
`SYNTHESIS` (the review gate has been cleared). If it is not, stop and return to the
scorecard-review skill.

Read `skills/00-governing-audit/references/bundle-conventions.md` for the three templates, the
STE writing rules, and the evolution-gap discipline. All three docs go in
`{{AUDIT_FOLDER}}/docs/`, are `type: Doc` with `expandable: true`, and are STE-styled.

## Step 1 — `doc-technical.md` (development team)
Verdict (the three signals), a scorecard reference, key findings per dimension (weakest
first, each linking to that dimension's `detail.md#findings`), the prioritized roadmap
(quick-wins → next → strategic), and methodology & limitations (static audit; performance
inferred).

## Step 2 — `doc-executive.md` (executive / sponsor) — evolution-gap discipline
The fund-the-work brief. Every weakness ties to a specific dimension finding and its business
consequence. State the gap and consequence only — **no invented solution, cost, or timeline.**
Reject vague "the system is old" framing: if a claim can't point to a dimension finding, it
doesn't belong here.

## Step 3 — `doc-business.md` (business stakeholder)
The four symptoms in plain terms (slow / insecure / hard to maintain / outdated architecture),
what the debt costs today, what "future-proof" unlocks, and explicit boundaries (this is an
assessment, not a delivery plan).

## Step 4 — Close
Regenerate `index.md`. Set `STATE.md` Stage to `COMPLETE`. Report the bundle location and the
three headline signals to the Architect.
