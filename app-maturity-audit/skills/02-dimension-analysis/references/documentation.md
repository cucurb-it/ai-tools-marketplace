# Rubric: Documentation

Assess whether someone other than the original author can understand, run, operate, and change the application. Thin or stale documentation raises the "bus factor," slows onboarding, and compounds the "hard to maintain" problem — it's the difference between institutional knowledge that's written down and knowledge that walks out the door.

## What to look for (evidence checklist)

- **README** — does it say what the app is, why it exists, and how to run it? Or is it a stub / the framework default?
- **Setup / onboarding** — can a new developer get it running from the docs alone? Are the steps complete and current (dependencies, env vars, services)?
- **Architecture / design docs** — an overview of how the pieces fit; decision records (ADRs) for the big choices.
- **API documentation** — for services/libraries: endpoints or public interfaces documented (generated from code or written), and current.
- **Operational docs / runbooks** — how to deploy, roll back, and handle common incidents.
- **Inline docs** — docstrings/comments where intent is non-obvious (not narrating the obvious).
- **Currency** — do the docs match the code, or describe a system that no longer exists? Stale docs can be worse than none.

## Levels

**Level 0 — Absent.** No README, or a stub with nothing usable. Nothing to onboard from; knowledge lives only in people's heads.

**Level 1 — Initial.** A minimal README with incomplete or outdated setup steps. No architecture or API docs. Getting started requires asking someone.

**Level 2 — Emerging.** A README with setup steps that actually work, and some inline documentation. Scattered notes exist, but no architecture overview and no runbooks. A determined newcomer can get running.

**Level 3 — Established.** README plus working onboarding, an architecture overview, and API docs where relevant. Docs are largely current. A new developer can become productive without shoulder-tapping the author.

**Level 4 — Optimized.** Comprehensive and maintained: onboarding, architecture, API, runbooks, decision records, and a changelog. Docs are kept current (sometimes checked in CI) and genuinely lower the bus factor.

## Scoring guidance

- Mentally **run the onboarding path**: can you go from clone to running using only the README? That test largely separates Level 1 from Level 2–3.
- **Stale docs** that actively mislead are a finding in their own right — note them rather than crediting mere existence.
- Score what the docs *are*, not what they promise elsewhere. (And remember: documentation claims are evidence only for *this* dimension — verify other dimensions against code.)

## Common findings → recommendations

- Setup steps incomplete/outdated → **quick-win**: fix the README so a clean clone runs.
- No architecture overview → **next**: add a one-page "how it fits together."
- No runbooks → **next**: document deploy, rollback, and the top few incident responses.
- Big decisions undocumented → **next**: start lightweight ADRs.
- Docs drift from code → **strategic**: put the critical docs where they're checked (or generated).
