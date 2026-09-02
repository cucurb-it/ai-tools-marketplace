# Rubric: Adaptability

Assess how cheaply the system absorbs new capability and changed behaviour over its life —
the inverse of its **inherent resistance to change**. This is a member of the modernization
"legacy cluster" and the single largest driver of development TCO: maintenance and evolution
dominate lifecycle cost, and most of that is *change* work. Score it higher-is-better: a high
level means low resistance (the system bends to change), a low level means high resistance
(the system is ossified and fights back).

**The axis is inverted relative to the concept, on purpose.** The concept is resistance; the
score stays maturity, so it aggregates consistently with the other ten dimensions. Level 4 =
low resistance / designed for change. Level 0 = high resistance / ossified. Never emit a
"resistance score" where high is bad — describe resistance in the finding, assign maturity in
the level.

**Passive vs. active resistance.** Two kinds, and the distinction drives finding severity:
- *Passive resistance* is inertia — nothing helps you change, so change is tedious and
  expensive but **predictable**. Mark these findings `medium`.
- *Active resistance* is when the system **fights back** — a change here silently breaks
  something there through hidden coupling. It is **unpredictable**, and unpredictability is
  what destroys estimates far more than raw effort. Mark these findings `high`.

**Why this dimension predicts budget overruns.** Low adaptability doesn't just make change
expensive, it makes change cost *unpredictable*: a change that looks local has a ripple radius
no estimator can see, so actuals overshoot estimates — and because hidden coupling only ever
*adds* work, the misses run one-directional. Layered on the well-known human bias to
underestimate, high resistance turns mild optimism into systematic overrun. So this dimension
is a proxy for **estimate reliability**: the lower it scores, the more roadmap estimates
should be discounted.

Calibrate to the software type: a stable, near-finished internal tool needs less adaptability
than a product on an active roadmap. Judge against the change the system actually has to
absorb.

## What to look for (evidence checklist — sources of resistance)

- **Volatility-fit (the spine).** Is the decomposition aligned to axes of *change* (what tends
  to vary together lives together) or to *functional* axes (layers/CRUD) that cut across every
  change? Functional decomposition means a typical feature smears across many modules — the
  classic hidden-ripple source. This is the strongest single signal.
- **Ripple radius.** For a representative change (add a new variant of an existing concept —
  a new payment method, report type, device), how many files/modules must be touched? One
  place (add) is adaptable; many places (edit everywhere) is resistant.
- **Encapsulation of what varies.** Is the thing most likely to change hidden behind a stable
  interface, or exposed so its every change propagates? Look for strategy/plugin patterns,
  interfaces at volatility boundaries, vs. concrete types used directly everywhere.
- **Hidden / implicit coupling (active resistance).** Shared mutable state, temporal coupling
  (must-call-A-before-B), order dependencies, implicit contracts, reach-through to internals,
  God objects everything imports. These are what make change *fight back*.
- **Afterthought change-hostility.** Adding a new case means editing many `switch`/`if`
  ladders and parallel structures rather than adding one unit (open/closed failure).
- **Extension seams.** Deliberate extension points, hooks, or plugin boundaries — or must you
  modify core code for every addition?
- **Config- vs code-driven variation.** Is expected variation data/config-driven, or does
  every variant require a code change and redeploy?
- **Contract & versioning.** For APIs/interfaces others depend on: versioning and
  backward-compatibility discipline, or do changes break consumers?

Absence of adaptability mechanisms after a genuine search is evidence of resistance; lower
`confidence` where you could not trace change ripple across a very large codebase.

## Levels

**Level 0 — Ossified / brittle.** Any change triggers a disproportionate reaction. Functional
decomposition throughout; pervasive hidden coupling; a small feature touches much of the
codebase; no seams. Change is both expensive and unpredictable — estimates here are guesses.

**Level 1 — Reluctant.** Change is possible but painful and forced. Some structure exists but
boundaries leak; large `switch`/`if` ladders must be edited in parallel for each new variant;
notable hidden coupling. Ripple radius is large and hard to predict.

**Level 2 — Adaptable with effort.** Parts flex, others dig in. Recognizable boundaries with
real leaks; the common variations have a home, but some changes still ripple unexpectedly.
Estimates are workable for known change types, unreliable for the rest.

**Level 3 — Flexible.** Accommodates change where it was expected. Decomposition broadly
follows volatility; what-varies is encapsulated behind interfaces; new variants of known
concepts slot in with a bounded, predictable ripple. Hidden coupling is rare. Estimates for
roadmap-shaped change are dependable.

**Level 4 — Designed for change.** New capability slots in rather than requiring edits across
the system. Decomposition is deliberately volatility-aligned; extension seams are explicit;
expected variation is config/data-driven; contracts are versioned. Change cost is low *and*
predictable — the property that makes roadmaps hit their estimates.

## Scoring guidance

- **Higher is better = less resistant.** Re-check the inversion before assigning: an ossified
  system is Level 0, not Level 4.
- **Weight active over passive resistance.** Predictable-but-tedious (passive) caps the level
  softly; fight-back coupling (active) caps it hard, because it's what wrecks estimates.
- **Volatility-fit is the spine.** Functional-only decomposition with cross-cutting change is a
  Level 0–1 anchor however tidy the code looks locally; don't let clean *code quality* mask
  resistant *structure* — those are different dimensions.
- **Name the hotspots, not just a number.** Resistance is never uniform. In `detail.md`,
  identify the specific high-resistance zones (the modules whose ripple radius is large) —
  that is the actionable output, and the place estimates will silently overrun.

## Common findings → recommendations, and the executive translation

- Functional decomposition on a volatile domain → **strategic**: re-decompose along axes of
  change around the highest-volatility areas first.
- Hidden/temporal coupling (active) → **[high] next/strategic**: make dependencies explicit;
  break the fight-back paths.
- `switch`/`if` ladders per variant (passive) → **[medium] next**: replace with a
  polymorphic/registry seam so new variants are additive.
- Concrete types at a volatility boundary → **next**: introduce an interface; encapsulate
  what varies.
- Code-change-per-variant → **next**: move expected variation to config/data.

**Executive translation (for `doc-executive.md`):** never "the system is stubborn." State it
as estimate reliability and overrun risk, evidenced — e.g. *"the structure concentrates change
cost in [hotspot]; roadmap items touching it will tend to run over their estimates, and
predictably in one direction. Budget and timeline confidence should be discounted there."*

**Honesty boundary.** The audit scores the *architectural conditions* that make estimates
unreliable; it cannot measure the team's actual estimation accuracy without historical
estimate-vs-actual data. Assert elevated *risk* of overrun from structure, not a measured
overrun rate.
