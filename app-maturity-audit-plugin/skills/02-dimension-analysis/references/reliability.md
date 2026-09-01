# Rubric: Reliability

Assess whether the application stays up and recovers sanely when things go wrong — bad input, a slow or failing dependency, a restart. This is a **critical** dimension. It is distinct from Performance: performance asks *is it fast and does it scale?*, reliability asks *does it fail safely and keep its data intact?*

Calibrate to the software type: a payment API demands circuit breakers and idempotency a nightly batch script does not.

## What to look for (evidence checklist)

- **Error handling** — are errors caught, surfaced, and acted on, or **swallowed** (bare `except:`, empty catch blocks) so failures hide? Swallowed errors are worse than none.
- **Timeouts** — do outbound calls (HTTP, DB, queues) have timeouts, or can one slow dependency hang the whole process?
- **Retries & backoff** — transient failures retried with backoff (not tight infinite loops)?
- **Graceful degradation** — fallbacks when a non-critical dependency is down, rather than a hard crash?
- **Health & lifecycle** — health/readiness endpoints; clean startup and graceful shutdown (drain in-flight work).
- **Resource cleanup** — connections/files/locks released (context managers, `finally`, `defer`); no leaks on the error path.
- **Data integrity** — transactions around multi-step writes; idempotency where operations may retry.
- **Single points of failure** — assumptions of a single instance, in-process locks, or unreplicated local state.

Absence after a genuine search is evidence; lower `confidence` where you couldn't trace all error paths.

## Levels

**Level 0 — Absent.** Errors unhandled or swallowed; no timeouts; a failing dependency crashes or hangs the app; no health checks; resources leak on failure.

**Level 1 — Initial.** Scattered `try/except` but inconsistent, with bare catches hiding problems. No timeouts or retries. Obvious single points of failure unaddressed.

**Level 2 — Developing.** Consistent error handling on the main paths; some timeouts; a basic health check; resource cleanup mostly via context managers. Retries and degradation are spotty. Survives the common failures but not the awkward ones.

**Level 3 — Established.** Errors handled and surfaced (logged/tracked, not swallowed); timeouts **and** retries-with-backoff on external calls; health/readiness endpoints; graceful handling when a dependency is down; transactions where needed; clean startup/shutdown.

**Level 4 — Optimized.** Designed for failure: circuit breakers/bulkheads, idempotent operations, tested failure modes (fault injection/chaos), graceful degradation everywhere it matters, and documented reliability targets (SLOs) the team acts on.

## Scoring guidance

- **Swallowed exceptions cap the level** — hiding failures is a reliability anti-pattern, not neutral. Flag them `high` severity.
- Weight **external-dependency handling** (timeouts/retries/fallbacks) — that's where real systems fall over.
- Calibrate: a stateless offline tool legitimately needs less than a stateful public service; say so rather than penalizing silently.

## Common findings → recommendations

- Bare/empty exception handlers → **quick-win**: catch specific errors, log, and re-raise or handle deliberately.
- No timeouts on outbound calls → **quick-win**: set timeouts everywhere; one hang shouldn't take the process down.
- No retries on transient failures → **next**: add retry-with-backoff for idempotent calls.
- No graceful shutdown → **next**: drain in-flight work on SIGTERM.
- No idempotency / circuit breaking on critical flows → **strategic**: add for payment/order-style paths.
