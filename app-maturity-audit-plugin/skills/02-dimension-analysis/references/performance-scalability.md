# Rubric: Performance & Scalability

Assess whether the application is fast enough for its purpose and able to grow with load — the "slow" and "won't scale" complaints that most often trigger a modernization decision. This dimension is distinct from Reliability: reliability asks *does it stay up and recover from errors?*, while this asks *is it fast, and does it get slower gracefully or fall over as load grows?*

**Honesty note — static vs. runtime.** A code-only audit cannot measure real latency or throughput. It can identify performance *risks and anti-patterns* with high confidence (N+1 queries, unindexed lookups, blocking I/O on hot paths, no caching, stateful design that blocks horizontal scaling) but it cannot confirm they *bite* in production without runtime data. Score on observed code posture, set `confidence` accordingly, and say plainly in the narrative what would need profiling or telemetry to confirm. If the user supplies runtime data (APM traces, slow-query logs, load-test results), fold it in and raise confidence.

Calibrate to the software type: an internal batch tool, a low-traffic CRUD app, and a high-throughput public API have very different reasonable ceilings. Judge against the load this software actually needs to handle.

## What to look for (evidence checklist)

- **Data-access efficiency** — N+1 query patterns (queries inside loops / per-item ORM lazy loads); missing indexes on filtered/joined columns; `SELECT *` on wide tables; unbounded result sets with no pagination; queries that fan out per request.
- **Caching** — Any caching layer (in-memory, Redis/Memcached, HTTP/CDN, computed-result memoization)? Or is every request recomputing/refetching from scratch? Cache invalidation strategy present?
- **Concurrency & blocking** — Blocking I/O on request paths in an async runtime; synchronous external calls with no timeout; work that should be backgrounded (email, image processing) done inline; thread/connection pool configuration.
- **Horizontal scalability** — Is the app stateless (session/state externalized) so it can run as N replicas? Or does it hold state in-process, write to local disk, or assume a single instance? Are long jobs offloaded to a queue/worker rather than tying up a web process?
- **Payload & network shape** — Chatty APIs (many small round-trips), oversized responses, missing compression, no pagination/streaming for large collections.
- **Resource management** — Connection pooling for DB/HTTP; unbounded in-memory accumulation; obvious memory leaks (growing global state); file handles/sockets closed.
- **Performance testing & budgets** — Any load/stress tests, benchmarks, or performance budgets in CI? Any evidence performance is measured rather than assumed?
- **Known bottlenecks** — TODO/FIXME/"slow"/"optimize" comments, issues, or docs pointing at hotspots; obvious algorithmic problems (nested loops over large collections, repeated sorts).

Absence of a facet after a genuine search is evidence — but for a very large or partly-generated codebase you couldn't traverse fully, lower `confidence` rather than overstating.

## Levels

**Level 0 — Absent.** Pervasive N+1 and unindexed queries on core paths; no caching anywhere; blocking work inline; state held in-process so the app cannot run as more than one instance. No pagination on collections. Performance is neither measured nor considered.

**Level 1 — Initial.** A few efficiency measures exist where an individual happened to add them, but the common paths still show N+1s, missing indexes, or unbounded queries. Little/no caching. Mostly single-instance assumptions (local session/state). No performance testing. Scaling would mean rework.

**Level 2 — Developing.** Core queries are reasonable (indexed, no glaring N+1 on hot paths), pagination exists on large collections, and some caching is in place. The app is broadly stateless or close to it, so it *could* scale horizontally with modest effort. Heavy work is sometimes backgrounded. But there are real gaps, and performance is not systematically measured.

**Level 3 — Established.** Efficient data access is the norm (indexes, no N+1 on hot paths, bounded/paginated queries), a coherent caching strategy exists with sensible invalidation, and the app is genuinely stateless so it scales horizontally behind a load balancer. Long/expensive work runs on background workers/queues. Timeouts and pooling are configured. Some performance testing or budgets exist. A reviewer could trust it to handle its expected load.

**Level 4 — Optimized.** Everything at Level 3, plus performance is engineered and measured continuously: load/stress tests (and ideally budgets enforced in CI), profiling or APM in use, capacity/scaling headroom understood, and evidence of deliberate optimization (query plans reviewed, caching tuned, hotspots addressed). Autoscaling or a clear horizontal-scaling story. Degradation under load is graceful and anticipated.

## Scoring guidance

- Score the **common paths**, not the worst isolated line. One N+1 in a rarely-used admin screen is a finding, not a Level-0 anchor; an N+1 on the main request path is.
- Statelessness is the hinge for scalability. In-process session/state or local-disk writes cap this dimension at roughly Level 1–2 no matter how efficient individual queries are, because the app fundamentally can't scale out — call that out explicitly, since "won't scale" is usually the business's real complaint.
- Be explicit about confidence. If you're inferring from code without runtime data, say so and name what profiling would confirm.

## Common findings → recommendations

- N+1 on a hot path → **quick-win**: eager-load / batch the query; add the missing index.
- No caching on expensive reads → **quick-win / next**: add a cache with a clear invalidation rule.
- Inline heavy work → **next**: move to a background queue/worker.
- In-process state blocking scale-out → **strategic**: externalize session/state; make the app stateless.
- Performance never measured → **next**: add a load test and a budget in CI, or wire up APM.
