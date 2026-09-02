# Rubric: Dependency Health

Assess the currency, hygiene, and risk of the code's third-party dependencies **and its runtime/language version**. This is part of the modernization "legacy cluster": an app on an end-of-life runtime with years-stale libraries is the textbook "outdated" system, regardless of how clean its own code is.

This overlaps Security but asks a different question: Security cares about *known vulnerabilities*; this cares about *currency, support, and maintainability*. A dependency can be current yet vulnerable, or safe yet abandoned. Score currency and health here.

## What to look for (evidence checklist)

- **Lockfile** — present and committed (`poetry.lock`, `package-lock.json`, `Cargo.lock`, `go.sum`)? Reproducible installs?
- **Currency** — how far behind are direct dependencies? A few minor versions is fine; several major versions behind, or last-released-years-ago, is not.
- **Runtime/language version** — is the language runtime (Python/Node/Java/etc.) within vendor support, or at/past **end-of-life**? EOL runtimes are a major finding.
- **Deprecated/abandoned deps** — anything unmaintained, deprecated, or superseded still in use?
- **Bloat** — an unusually large dependency tree, or heavy libraries pulled in for trivial use.
- **Pinning strategy** — sensible constraints vs unpinned wildcards vs frozen-forever.
- **Update process** — any automation (Dependabot/Renovate) or evidence of a regular update cadence.
- **License posture** — obvious license incompatibilities for how the software is distributed.

## Levels

**Level 0 — Absent.** No lockfile. Dependencies wildly outdated; runtime at/past end-of-life; abandoned libraries central to the app. Reinstalling might not even reproduce.

**Level 1 — Initial.** Lockfile present but dependencies drifting years behind; some deprecated. Runtime near or at EOL. No update process — things are upgraded only when something breaks.

**Level 2 — Emerging.** Lockfile committed; most dependencies within a reasonable window though some lag; runtime supported. Updates happen manually and irregularly. No license review.

**Level 3 — Established.** Dependencies current within a sane window, lockfile enforced in CI, runtime comfortably within support. A real (if manual) update cadence exists. Licenses have been considered.

**Level 4 — Optimized.** Automated dependency updates with CI gating, minimal bloat, runtime on a current LTS with an upgrade plan, supply-chain measures (provenance/SBOM), and automated license compliance. Staying current is a routine, low-effort process.

## Scoring guidance

- An **EOL runtime** is a Level-0/1 anchor for this dimension and a headline modernization driver — surface it prominently.
- Distinguish "one major behind" (a finding) from "five majors and unmaintained" (a level cap).
- Don't double-count with Security — reference known-vuln scanning there; here, judge currency and support.

## Common findings → recommendations

- No lockfile → **quick-win**: commit one; make installs reproducible.
- No update automation → **next**: enable Dependabot/Renovate with CI gating.
- Several majors behind on a core dep → **next / strategic**: plan the upgrade; budget for breaking changes.
- EOL runtime → **strategic**: schedule a runtime upgrade — it gates security and library currency both.
