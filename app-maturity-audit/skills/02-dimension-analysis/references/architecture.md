# Rubric: Architecture

Assess the system-level structure: boundaries, coupling, separation of concerns, and whether the design still fits what the application needs to do. This is the heart of the "outdated architecture" complaint and the highest-leverage member of the modernization "legacy cluster" — architecture is the most expensive thing to change later, so getting an honest read here matters most for the modernization decision.

Distinguish **local** code quality (that's the Code Quality dimension) from **structural** quality here: a codebase can be tidy line-by-line yet architecturally tangled, or a bit rough locally yet cleanly structured.

"Old" is not automatically "bad." A sound monolith beats a tangled set of services. Judge whether the structure *supports change and the current scale needs*, not whether it follows the latest fashion.

## What to look for (evidence checklist)

- **Layering & boundaries** — clear separation between business logic, I/O/persistence, and presentation? Or is domain logic tangled into controllers, templates, and DB calls?
- **Coupling & cohesion** — god objects/modules that everything depends on; circular dependencies; changes that ripple unpredictably across unrelated areas.
- **Configuration** — externalized (env/config, 12-factor) vs hardcoded hosts/paths/secrets baked into code.
- **State** — in-process/local state that blocks scaling and complicates change (cross-reference Performance & Scalability).
- **Consistency of patterns** — one coherent way to do a given thing, or several competing approaches accreted over time.
- **Extensibility** — does a new feature have an obvious home, or does it require touching many unrelated parts?
- **Fit for purpose** — architectural patterns appropriate to the domain and load, or a mismatch (e.g. everything synchronous where async/queued is needed).

## Levels

**Level 0 — Absent.** No discernible structure. Business logic, I/O, and presentation tangled together; global state pervasive; circular dependencies; a change in one place breaks unrelated things.

**Level 1 — Initial.** Some structure, but boundaries leak badly. Large god modules. Config hardcoded. Hard to change one thing without touching many; onboarding to "where does X live" is painful.

**Level 2 — Emerging.** Recognizable layering with real leaks. Separation of concerns mostly present; config externalized. Coupling is manageable but has clear hotspots. Workable, with friction.

**Level 3 — Established.** Clear boundaries and separation of concerns; low coupling, high cohesion; configuration externalized (12-factor); consistent patterns. A new feature has an obvious home, and changes stay local.

**Level 4 — Optimized.** Deliberate, documented architecture with enforced boundaries (module/dependency rules), clean extension points, patterns that fit the domain, and a design that supports current scaling and evolution needs. Architectural decisions are recorded and revisited.

## Scoring guidance

- This dimension is usually the **biggest driver of modernization pressure** — weight statelessness and coupling, since those most directly gate the ability to modernize and scale.
- Separate "old but sound" from "actually tangled." Penalize tangle and rigidity, not age per se; say which you're seeing.
- Hardcoded configuration and in-process state are concrete, citable anchors — call them out with paths.

## Common findings → recommendations

- Domain logic tangled into controllers/UI → **strategic**: introduce a service/domain layer; re-architect the seams.
- Hardcoded configuration → **quick-win / next**: externalize to env/config.
- In-process state blocking scale-out → **strategic**: make the app stateless (also lifts Performance).
- God module / circular deps → **next / strategic**: break the cycle; split responsibilities.
- No recorded architectural decisions → **next**: start lightweight ADRs for the big choices.
