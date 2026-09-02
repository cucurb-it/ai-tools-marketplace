# Rubric: CI/CD & Deployment

Assess how safely and repeatably code gets from a commit to running in production. Slow, manual, risky deployment is a direct brake on modernization: it makes every change expensive and rollback scary.

Calibrate to context — a small internal app needs less than a multi-service platform — but *some* automation and *some* rollback story are reasonable almost everywhere.

## What to look for (evidence checklist)

- **CI** — is there a pipeline that builds and tests on push/PR? Does it **gate merges**?
- **CD** — is deployment automated, or a manual sequence of steps someone remembers?
- **Environments** — separation of dev/staging/prod, or changes straight to prod?
- **Infrastructure as code** — Dockerfile, Compose, Kubernetes manifests, Terraform/Pulumi — or hand-configured servers?
- **Release process** — versioning, tags, changelog; reproducible/pinned builds.
- **Database migrations** — versioned and run through the pipeline, or applied by hand?
- **Rollback** — a defined, practiced way back to the last good version?
- **Pipeline hygiene** — secrets injected safely (not hardcoded in CI files); minimal manual gates.

## Levels

**Level 0 — Absent.** No CI. Builds and deploys are manual and undocumented ("works on my machine"). No containerization or IaC. Migrations by hand.

**Level 1 — Initial.** CI runs something (lint or build) but doesn't reliably gate merges. Deploys are manual and tribal-knowledge. Maybe a Dockerfile, but no orchestration or environment separation.

**Level 2 — Emerging.** CI builds and tests on PRs; the app is containerized. Deployment is scripted but has manual steps. Typically one shared environment. Rollback means manually redeploying an older image. Migrations semi-automated.

**Level 3 — Established.** CI gates merges. Automated deploy to a staging environment and then production, with prod/staging/dev separated. IaC covers the core infrastructure. Migrations run in the pipeline. Rollback is documented and has been exercised.

**Level 4 — Optimized.** Full CI/CD with progressive delivery (canary or blue-green), IaC for everything, automated rollback triggers tied to health signals, reproducible builds with versioned artifacts, and deploy-time observability. Shipping is routine and low-drama.

## Scoring guidance

- **Merge-gating CI** is the Level-2→3 hinge; a pipeline that doesn't block bad merges is decoration.
- A credible **rollback** path matters as much as the deploy path — weight it.
- Level 4 leans on the Observability dimension (you can't auto-rollback on signals you don't collect); note the dependency.

## Common findings → recommendations

- CI exists but doesn't gate merges → **quick-win**: make build+test required.
- Manual deploy steps → **next**: script the whole path; remove human sequencing.
- No IaC → **next / strategic**: capture infra as code (start with a Dockerfile + Compose/manifests).
- No rollback plan → **next**: define and rehearse rollback to the previous artifact.
- Hand-run migrations → **next**: run migrations in the pipeline with a forward/back plan.
