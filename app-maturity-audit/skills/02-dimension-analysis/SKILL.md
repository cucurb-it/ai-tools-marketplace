---
name: audit-dimension-analysis
description: SCORING stage of the Application Maturity Audit. Loaded by the app-maturity-audit governing skill to score each engineering dimension against its rubric and emit that dimension's result.json, detail.md, and summary.md into the bundle. Not a standalone entry point — the governing skill invokes it, once per dimension.
---

# Audit — SCORING Stage (per dimension)

Score one dimension against its rubric, on evidence, and write its three bundle files.
Read `skills/00-governing-audit/references/bundle-conventions.md` for the templates and
frontmatter of `detail.md` and `summary.md`.

## Fan-out

The ten dimensions are scored independently. **In Claude Code (subagents available), the
governing skill spawns one invocation of this skill per dimension in a single turn.** Without
subagents, loop through the dimensions serially. Either way, each dimension produces the same
three files.

## Rubrics (this skill's `references/`)

`performance-scalability`, `security`, `testing`, `reliability`, `cicd-deployment`,
`observability`, `dependency-health`, `code-quality`, `architecture`, `documentation`.

## Per-dimension procedure

1. **Read the rubric** `references/<dimension>.md` in full — it defines each level 0–4 and the
   evidence to hunt for.
2. **Read** `{{AUDIT_FOLDER}}/recon.md` for shared context (software type, areas to skip).
3. **Search** the repo for the evidence the rubric calls for. Cite exact file paths.
4. **Assign a single level 0–4** per the rubric — or `not_applicable` with a reason.
5. **Write three files** into `{{AUDIT_FOLDER}}/dimensions/<dimension>/`:
   - `result.json` — the machine record (schema below), consumed by the scorer
   - `detail.md` — `type: Dimension`; full evidence / findings / recommendations, with anchors
   - `summary.md` — `type: Summary`; bounded: level, role, top finding, first move

## Scoring rules

- **Evidence first.** Every level cites concrete artifacts. A score with no evidence is invalid.
- **Absence is a finding, with a caveat.** Missing artifacts after a genuine search are
  evidence of a low level — but set `confidence: low` when you could not search exhaustively.
  Never invent files or practices you did not observe.
- **Static (code-only) by default.** Infer runtime properties (especially performance) from
  code posture; set `confidence` honestly and name what would need profiling to confirm.
- **Calibrate to the software type** from recon; say so when it affects the level.

## Result schema (`dimensions/<dim>/result.json`)

```json
{
  "dimension": "security",
  "level": 2,
  "level_label": "Developing",
  "confidence": "high",
  "not_applicable": false,
  "evidence": [{ "observation": "...", "path": "..." }],
  "findings": [{ "severity": "high", "summary": "...", "detail": "..." }],
  "recommendations": [{ "priority": "quick-win", "action": "...", "rationale": "..." }]
}
```
`severity`: high/medium/low · `priority`: quick-win/next/strategic · `confidence`: high/medium/low.

When every applicable dimension has its three files, return control to the governing skill,
which loads `skills/03-scorecard-review/SKILL.md`.
