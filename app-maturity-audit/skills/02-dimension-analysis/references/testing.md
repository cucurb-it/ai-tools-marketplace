# Rubric: Testing

Assess whether the code is verified by tests that actually run and actually catch regressions. This is a **critical** dimension — untested code is a modernization hazard, because you can't safely change what you can't verify, and "hard to maintain" usually starts here.

The hinge is not test *count* but test *enforcement* and *meaningfulness*: tests that don't run in CI don't protect anything, and tests that assert nothing meaningful give false comfort.

Calibrate to the software type and the criticality of its paths — a payments flow demands far more coverage than a throwaway internal tool.

## What to look for (evidence checklist)

- **Presence & layout** — test directories/files (`tests/`, `*_test.py`, `*.spec.ts`, etc.); ratio of test to source code as a rough signal.
- **Types** — unit tests, integration tests (real DB/HTTP boundaries), end-to-end tests. A pile of unit tests with no integration coverage still leaves the seams unverified.
- **CI enforcement** — do tests run in CI, and do failures **block merge**? Grep the CI config. Tests that only run locally are optional in practice.
- **Coverage signal** — is coverage measured? Is there a threshold/floor? (Treat the % as signal, not truth — 90% coverage of getters proves little.)
- **Critical-path coverage** — are the paths that would hurt most if broken (auth, payments, core domain logic) actually tested?
- **Quality & stability** — meaningful assertions vs smoke-only; fixtures/mocks used sanely; signs of flakiness (retries, `skip`, `xfail`, disabled tests).

Absence after a genuine search is evidence; lower `confidence` if a large monorepo prevented exhaustive traversal.

## Levels

**Level 0 — Absent.** No tests, or a token test that doesn't run. Changes are verified by hand, if at all.

**Level 1 — Initial.** A handful of tests exist where someone happened to add them. Not run in CI (or not gating). Happy-path only; coverage unknown. Provides little real protection.

**Level 2 — Developing.** A genuine unit suite that runs, and perhaps runs in CI though it may not block merge. Integration tests sparse. Coverage may be measured but has no enforced floor. Some critical paths remain untested. Useful, but with real holes.

**Level 3 — Established.** Unit and integration tests cover the common and critical paths. Tests run in CI and **block merge** on failure. Coverage is measured with a sensible floor. The suite is reasonably stable. A reviewer could trust a green build.

**Level 4 — Optimized.** Comprehensive unit + integration + e2e coverage, enforced in CI, with critical paths well covered. The suite is fast and stable (flakiness actively managed). Testing is first-class — e.g. contract tests across service boundaries, or mutation testing to check the tests themselves.

## Scoring guidance

- **Enforcement beats volume.** A modest suite that gates merges (Level 3 territory) protects more than a large suite nobody runs (Level 1).
- Weight **critical-path** coverage heavily — untested auth/payments caps the level regardless of coverage elsewhere.
- A visibly flaky suite is a finding even at otherwise-high levels; flaky tests get ignored, which erodes the whole safety net.

## Common findings → recommendations

- Tests exist but don't gate CI → **quick-win**: make the test job required to merge.
- No coverage floor → **quick-win**: add a coverage threshold (start where you are, ratchet up).
- No integration tests for `<module>` → **next**: add coverage for its critical paths.
- Flaky suite → **next**: quarantine and fix flaky tests; they train the team to ignore red.
- No e2e / contract tests across seams → **strategic**: add them where integration risk is highest.
