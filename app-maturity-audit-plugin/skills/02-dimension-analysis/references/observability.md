# Rubric: Observability

Assess whether operators can tell what the application is doing and why, when it misbehaves. Poor observability turns every incident into guesswork and hides the very bottlenecks a modernization effort needs to target.

**Static-audit caveat:** you can see *instrumentation in the code* (logging, metrics, tracing, error-tracking SDKs) but generally **cannot** verify externally-configured dashboards or alert rules from the repo alone. Score the instrumentation you can see and set `confidence` accordingly; name what you couldn't verify.

Mark `not_applicable` for a pure offline library with no operational surface, rather than scoring 0.

## What to look for (evidence checklist)

- **Logging** — structured (JSON/keyed) vs freeform strings vs `print`/`console.log`; sensible levels; request/correlation IDs to trace a request across components; sensitive data kept out of logs.
- **Metrics** — application metrics (request rate, latency, error rate, queue depth) emitted via a metrics library/exporter?
- **Tracing** — distributed tracing / spans for multi-service or multi-step flows?
- **Error tracking** — an error aggregator (Sentry/Rollbar/etc.) wired up?
- **Health/readiness** — endpoints exposed for probes (also seen under Reliability).
- **Aggregation & alerting** — evidence of log shipping, dashboards, or alert config in-repo (often lives elsewhere — flag confidence).

## Levels

**Level 0 — Absent.** `print`/`console.log` or nothing. No metrics, no tracing, no error tracking. When it breaks in prod, you're blind.

**Level 1 — Initial.** A logger is used but output is unstructured and levels are inconsistent. No metrics or tracing. No error tracking. Debugging prod means reading raw log dumps.

**Level 2 — Developing.** Structured logging with levels across most of the code, and an error tracker wired up. Perhaps some basic metrics. No distributed tracing. You can reconstruct most incidents after the fact.

**Level 3 — Established.** Structured logs with correlation/request IDs, application metrics for the key indicators, error tracking, and health endpoints. Alerting and dashboards likely exist (confirm out-of-band). An operator can answer "is it healthy, and if not where does it hurt?"

**Level 4 — Optimized.** Logs + metrics + distributed tracing correlated across the system, SLO-based alerting, maintained dashboards, and instrumentation treated as first-class (new features ship with it). Bottlenecks and failures are observable rather than inferred.

## Scoring guidance

- **Structured + correlated** logging is the Level-2→3 hinge; freeform logs don't scale past one person grepping.
- Don't over-credit config you can't see — infer conservatively and lower confidence.
- Weight what matters for *this* app's operations; an internal cron job needs less than a customer-facing API.

## Common findings → recommendations

- `print`/unstructured logging → **quick-win**: adopt a structured logger with levels.
- No request/correlation IDs → **quick-win / next**: add them so a request is traceable end-to-end.
- No error tracking → **quick-win**: wire up an error aggregator.
- No metrics → **next**: emit the key indicators (rate/latency/errors).
- No tracing across services → **strategic**: add distributed tracing where flows span components.
