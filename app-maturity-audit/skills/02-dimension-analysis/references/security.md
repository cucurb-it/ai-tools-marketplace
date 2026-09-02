# Rubric: Security

Assess how well the codebase protects against the common ways applications get compromised. This is a **critical** dimension — a low level here gates the overall audit regardless of how the other dimensions score, because insecure software is not production-ready however well-tested or documented it is.

Calibrate to the software type: a public-facing web service carries far more security surface than an offline CLI or a pure computation library. Judge against the threats that actually apply, and note in the narrative when the software type raises or lowers the reasonable ceiling.

## What to look for (evidence checklist)

Search for evidence across these facets. Cite exact paths for both what is present and what is conspicuously absent.

- **Secrets handling** — Are credentials, API keys, and tokens kept out of source? Look for `.env` usage with a committed `.env.example` (good) versus hardcoded secrets or committed `.env` files (bad). Grep for suspicious literals (`api_key =`, `password =`, `AKIA`, private-key headers). Check `.gitignore` covers secret files. Look for a secrets manager or vault integration.
- **Dependency vulnerabilities** — Is there any scanning (Dependabot, Renovate, `pip-audit`, `npm audit`, `cargo audit`, Snyk, Trivy) wired into CI or config? Are lockfiles present and current? Obviously outdated, known-vulnerable major deps count against.
- **Authentication & authorization** — For anything with users or protected resources: is authn present and is authz enforced at the right layer (not just hidden UI)? Look for a coherent auth module rather than ad-hoc checks scattered around. Session/token handling, expiry, and password storage (hashing, never plaintext) matter.
- **Input validation & injection defense** — Parameterized queries / ORM use rather than string-built SQL; output encoding / escaping in templates; validation at trust boundaries (request handlers, deserialization, file uploads). Grep for raw query construction and unsafe deserialization.
- **Transport & data security** — TLS enforced (HSTS, no plaintext endpoints for sensitive data); sensitive data not logged; encryption at rest where warranted.
- **Security testing & tooling** — SAST (CodeQL, Semgrep, Bandit, gosec) in CI; security-focused tests; a linter security ruleset enabled.
- **Security posture & process** — A `SECURITY.md` / disclosure policy; documented threat model or security notes; dependency-update cadence; least-privilege config (CI tokens, container users, IAM).

Absence of a facet, after a genuine search, is evidence — but if you could not search exhaustively (huge monorepo, vendored code skipped), lower `confidence` accordingly rather than overstating.

## Levels

**Level 0 — Absent.** Hardcoded secrets in source and/or committed credential files. No dependency management hygiene (no lockfile, or wildly outdated with known-critical vulns). For a service with users: no real authentication, or plaintext password storage. String-built SQL or obvious injection paths. No security tooling of any kind.

**Level 1 — Initial.** Secrets are mostly out of source but handling is inconsistent (some env, some hardcoded; `.env.example` missing or `.gitignore` gaps). Lockfiles exist but nothing scans them. Authn exists but authz is ad-hoc or partly UI-only. Some input validation, applied unevenly. No security tooling in CI. No `SECURITY.md`.

**Level 2 — Emerging.** Secrets consistently externalized with `.env.example` and correct `.gitignore`; no secrets in history that a quick scan reveals. A lockfile is present and dependencies are broadly current, though scanning is not automated. Authn/authz is centralized and enforced server-side. Parameterized queries / ORM used throughout; validation present at most trust boundaries. Perhaps a linter with some security rules, but no dedicated SAST or dependency scanning in CI. Real gaps remain, but the basics are in place.

**Level 3 — Established.** Everything at Level 2, plus automated dependency vulnerability scanning **and** SAST wired into CI so insecure changes are caught before merge. TLS enforced for sensitive traffic; sensitive data kept out of logs. A `SECURITY.md` / disclosure policy exists. Auth handling is documented and covers expiry/rotation. A reviewer could rely on the security controls being consistently applied.

**Level 4 — Optimized.** Everything at Level 3, plus defense in depth and continuous improvement: secret scanning on every push (and in history), dependency updates automated with review, SAST tuned with few false positives, security tests for the sensitive paths, least-privilege enforced in CI/infra (scoped tokens, non-root containers), a documented threat model kept current, and evidence the team acts on findings (e.g. resolved advisories, an audit trail). Failure modes are anticipated rather than discovered.

## Scoring guidance

- The dimension sits at the highest level whose criteria are **substantially** met. One missing Level-3 item (say, no `SECURITY.md`) does not by itself drop an otherwise Level-3 repo to 2 — record it as a finding and keep the level, noting the gap.
- Weight real exploitability. A hardcoded secret in a public repo is a Level-0 anchor no matter how polished the rest is; call it out as a `high` severity finding and let it cap the level.
- For libraries/CLIs with no auth or network surface, mark those facets not-applicable in the narrative and score on the facets that do apply (secrets, dependencies, injection, tooling) rather than penalizing absent auth.

## Common findings → recommendations

- Secrets in source → **quick-win**: move to env + `.env.example`, rotate exposed keys, add secret scanning.
- No dependency scanning → **quick-win**: enable Dependabot/`pip-audit`/`npm audit` in CI.
- No SAST → **next**: add CodeQL/Semgrep to the pipeline.
- Ad-hoc authz → **strategic**: centralize authorization at a single enforced layer.
- No threat model → **strategic**: document trust boundaries and top risks; revisit per release.
