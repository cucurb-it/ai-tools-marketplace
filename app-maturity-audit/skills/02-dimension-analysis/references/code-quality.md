# Rubric: Code Quality

Assess the internal quality and maintainability of the code itself — how hard it is to read, change, and extend safely. This is the core of the "hard to maintain" complaint and a central member of the modernization "legacy cluster."

Scope note: this dimension is about **local** quality (readability, complexity, duplication, consistency, type safety). System-level structure and coupling live in the Architecture dimension — cross-reference rather than double-count.

## What to look for (evidence checklist)

- **Linting & formatting** — a linter and formatter configured, and **enforced in CI** (not just present in a config nobody runs)?
- **Type safety** — for typed languages, are types used meaningfully, or is everything `any`/`interface{}`/untyped? For dynamic languages, is there gradual typing (type hints/TS) and is it checked?
- **Complexity** — oversized functions/files, deep nesting, sprawling conditionals; any complexity hotspots that resist change.
- **Duplication** — copy-pasted logic that must be changed in many places at once.
- **Consistency** — coherent naming and patterns, or every module doing its own thing.
- **Dead code & debt markers** — unreachable code, commented-out blocks, density of `TODO`/`FIXME`/`HACK`.
- **Readability aids** — comments/docstrings where intent is non-obvious (not narrating the obvious).

## Levels

**Level 0 — Absent.** No linting or formatting. Huge tangled files, heavy duplication, inconsistent style. Typed language used effectively untyped. Every change is archaeology.

**Level 1 — Initial.** Maybe a formatter, not enforced. Style drifts across the codebase. Real complexity and duplication hotspots. Typing sparse or ignored.

**Level 2 — Emerging.** Linter and formatter configured and run locally; style mostly consistent. Some complexity/duplication hotspots remain. Typing present but partial. Readable in the main, rough at the edges.

**Level 3 — Established.** Linting and formatting **enforced in CI**; type checking enforced where the language supports it. Complexity generally controlled; little duplication; consistent conventions. A new contributor can read and change code with confidence.

**Level 4 — Optimized.** Strict linting and typing enforced, complexity kept within budgets, near-zero duplication, static analysis for code smells, and low, actively-managed debt. Conventions are documented and applied uniformly.

## Scoring guidance

- **Enforced-in-CI** is the Level-2→3 hinge; tooling that isn't enforced decays.
- Judge the **common code**, not one ugly legacy file — but a pervasive pattern (duplication everywhere, no types anywhere) caps the level.
- High `TODO`/`FIXME` density and large commented-out blocks are debt signals worth citing concretely.

## Common findings → recommendations

- Linter/formatter not enforced → **quick-win**: add it to CI as a required check.
- No type checking on a typed/typable codebase → **next**: enable and enforce it, incrementally.
- Complexity hotspot in `<module>` → **next**: refactor the worst offenders; add tests first.
- Pervasive duplication → **next / strategic**: extract shared logic; consolidate the copies.
