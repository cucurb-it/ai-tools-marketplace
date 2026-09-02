#!/usr/bin/env python3
"""Aggregate per-dimension audit results into a scorecard.

Reads every *.json in the given dimensions directory (each following the
dimension result schema in SKILL.md), computes a weighted average and a
"gating" level (the min level among critical dimensions), and writes:
  - scorecard.md   : a Markdown table + headline numbers
  - summary.json   : machine-readable aggregate

Standard library only, so it runs anywhere Python 3 does.

Usage:
    python build_scorecard.py <dimensions-dir> --out <output-dir>
"""

import argparse
import json
import pathlib
import sys

# Default weights for the Overall average. Security and adaptability weigh highest:
# security blocks production-readiness; adaptability is the largest driver of
# development TCO. These weights affect ONLY the Overall average, not the gate,
# the modernization pressure, or the TCO signature (those have their own logic).
DEFAULT_WEIGHTS = {
    "security": 1.5,
    "adaptability": 1.5,
    "testing": 1.3,
    "reliability": 1.3,
    "performance-scalability": 1.3,
    "architecture": 1.1,
    "cicd-deployment": 1.1,
    "observability": 1.0,
    "dependency-health": 1.0,
    "code-quality": 1.0,
    "documentation": 0.8,
}

# Dimensions whose weakest level gates the production-readiness verdict.
CRITICAL = {"security", "testing", "reliability"}

# The "legacy cluster" — low scores here mean high modernization pressure.
MODERNIZATION_CLUSTER = {
    "architecture", "performance-scalability", "dependency-health", "code-quality",
    "adaptability",
}

# Weights for the modernization-pressure signal. Adaptability dominates (cost of
# change is the largest driver), at double any other cluster input.
CLUSTER_WEIGHTS = {
    "adaptability": 2.0,
    "architecture": 1.0,
    "performance-scalability": 1.0,
    "dependency-health": 1.0,
    "code-quality": 1.0,
}

# Inputs and weights for the TCO signature (relative cost of ownership). Adaptability
# is the dominant term at roughly double any other input, because cost of change is
# the largest slice of software TCO. Security is excluded — it is the readiness lens,
# not a development-cost driver.
TCO_WEIGHTS = {
    "adaptability": 3.0,
    "architecture": 1.5,
    "dependency-health": 1.5,
    "code-quality": 1.5,
    "performance-scalability": 1.0,
    "testing": 1.0,
    "reliability": 1.0,
    "observability": 1.0,
    "cicd-deployment": 1.0,
    "documentation": 1.0,
}

LEVEL_LABELS = {
    0: "Absent",
    1: "Initial",
    2: "Emerging",
    3: "Established",
    4: "Optimized",
}

LEVEL_MEANINGS = {
    0: "The practice is not present at all.",
    1: "Ad-hoc, inconsistent, undocumented.",
    2: "A basic version exists but has real gaps.",
    3: "Consistent, documented, covers the common cases.",
    4: "Comprehensive, automated, monitored, continuously improved.",
}


def load_dimensions(dim_dir: pathlib.Path):
    # Bundle form: dimensions/<dim>/result.json. Flat fallback: dimensions/<dim>.json.
    paths = sorted(dim_dir.glob("*/result.json")) or sorted(dim_dir.glob("*.json"))
    results = []
    for path in paths:
        try:
            data = json.loads(path.read_text())
        except json.JSONDecodeError as exc:
            print(f"WARNING: skipping unparseable {path}: {exc}", file=sys.stderr)
            continue
        default_name = path.parent.name if path.name == "result.json" else path.stem
        data.setdefault("dimension", default_name)
        results.append(data)
    return results


def band(score: float) -> str:
    """Map a fractional overall score to its nearest level label."""
    return LEVEL_LABELS.get(round(score), "Unknown")


def aggregate(results, weights):
    scored, na = [], []
    for r in results:
        if r.get("not_applicable"):
            na.append(r["dimension"])
            continue
        level = r.get("level")
        if not isinstance(level, (int, float)):
            print(f"WARNING: {r['dimension']} has no numeric level; skipping",
                  file=sys.stderr)
            continue
        scored.append(r)

    total_w = sum(weights.get(r["dimension"], 1.0) for r in scored)
    weighted = (
        sum(r["level"] * weights.get(r["dimension"], 1.0) for r in scored) / total_w
        if total_w else 0.0
    )

    crit_levels = [r["level"] for r in scored if r["dimension"] in CRITICAL]
    gating = min(crit_levels) if crit_levels else None
    gating_dims = (
        [r["dimension"] for r in scored
         if r["dimension"] in CRITICAL and r["level"] == gating]
        if gating is not None else []
    )

    # Modernization pressure: WEIGHTED maturity of the legacy cluster (adaptability
    # dominates), inverted. Lower maturity -> higher pressure.
    cluster = [r for r in scored if r["dimension"] in MODERNIZATION_CLUSTER]
    if cluster:
        cw = sum(CLUSTER_WEIGHTS.get(r["dimension"], 1.0) for r in cluster)
        cluster_avg = sum(r["level"] * CLUSTER_WEIGHTS.get(r["dimension"], 1.0)
                          for r in cluster) / cw
    else:
        cluster_avg = None
    if cluster_avg is None:
        pressure = None
    elif cluster_avg <= 1.5:
        pressure = "High"
    elif cluster_avg <= 2.5:
        pressure = "Medium"
    else:
        pressure = "Low"
    # The weakest cluster dimensions are the modernization drivers to name first.
    cluster_drivers = (
        sorted((r["dimension"] for r in cluster
                if r["level"] == min(x["level"] for x in cluster)))
        if cluster else []
    )

    # TCO signature: relative cost of ownership, weighted so adaptability dominates.
    # Lower cost-weighted maturity -> higher TCO burden. Relative, not monetary.
    tco_dims = [r for r in scored if r["dimension"] in TCO_WEIGHTS]
    if tco_dims:
        tw = sum(TCO_WEIGHTS[r["dimension"]] for r in tco_dims)
        tco_maturity = sum(r["level"] * TCO_WEIGHTS[r["dimension"]] for r in tco_dims) / tw
        if tco_maturity <= 1.5:
            tco_burden = "High"
        elif tco_maturity <= 2.5:
            tco_burden = "Moderate"
        else:
            tco_burden = "Low"
        tco_drivers = sorted(
            r["dimension"] for r in tco_dims
            if r["level"] == min(x["level"] for x in tco_dims)
        )
    else:
        tco_maturity = tco_burden = None
        tco_drivers = []

    return {
        "weighted_average": round(weighted, 2),
        "weighted_average_label": band(weighted),
        "gating_level": gating,
        "gating_level_label": LEVEL_LABELS.get(gating) if gating is not None else None,
        "gating_dimensions": gating_dims,
        "modernization_pressure": pressure,
        "modernization_cluster_avg": round(cluster_avg, 2) if cluster_avg is not None else None,
        "modernization_drivers": cluster_drivers,
        "tco_burden": tco_burden,
        "tco_maturity": round(tco_maturity, 2) if tco_maturity is not None else None,
        "tco_drivers": tco_drivers,
        "scored": scored,
        "not_applicable": na,
    }


def compute_insights(agg):
    """Data-specific, auto-generated reading of the numbers."""
    scored = agg["scored"]
    overall = agg["weighted_average"]
    gate = agg["gating_level"]
    gating_dims = agg["gating_dimensions"]
    bullets = []

    crit = [(r["dimension"], r["level"]) for r in scored if r["dimension"] in CRITICAL]
    if gate is not None and crit:
        # Spread: is the average masking an acute critical weakness?
        if overall - gate >= 0.5 and gating_dims:
            who = ", ".join(f"**{d}**" for d in gating_dims)
            verb = "is" if len(gating_dims) == 1 else "are"
            bullets.append(
                f"The overall average ({overall}) sits above the readiness gate "
                f"(Level {gate}): {who} {verb} holding trustworthiness below the general "
                f"maturity level. Read the gate, not the average, as the verdict."
            )
        # Leverage: what single move raises the gate the most?
        crit_levels = sorted({lvl for _, lvl in crit})
        if len(crit_levels) == 1:
            bullets.append(
                f"All critical dimensions sit at Level {gate}; the readiness gate rises "
                f"only when every one of them does."
            )
        else:
            next_level = min(lvl for _, lvl in crit if lvl > gate)
            who = ", ".join(f"**{d}**" for d in gating_dims)
            plural = len(gating_dims) > 1
            bullets.append(
                f"**Highest-leverage move:** raising {who} from Level {gate} to "
                f"Level {next_level} would lift the readiness gate to Level {next_level} "
                f"in one step ({'those are' if plural else 'that is'} the only critical "
                f"dimension{'s' if plural else ''} below Level {next_level})."
            )

    # Confidence caveat (this is a static, code-only audit).
    lows = sorted(r["dimension"] for r in scored if r.get("confidence") == "low")
    if lows:
        many = len(lows) > 1
        bullets.append(
            f"Lowest certainty: {', '.join(f'**{d}**' for d in lows)} "
            f"(confidence low) — check {'their' if many else 'its'} `detail.md` first. "
            f"All levels are inferred from code, not measured at runtime."
        )
    else:
        bullets.append(
            "Every level is inferred from code — this is a static audit, so runtime "
            "properties (especially performance) are estimated, not measured. Confirm "
            "against each dimension's `detail.md` before acting on a score."
        )
    return bullets


def _lens(dimension):
    if dimension in CRITICAL:
        return "★ gate"
    if dimension in MODERNIZATION_CLUSTER:
        return "cluster"
    return "—"


def render_scorecard(agg, weights) -> str:
    pressure = agg.get("modernization_pressure") or "n/a"
    lines = [
        "---",
        "type: Scorecard",
        f"description: Overall Level {agg['weighted_average']} ({agg['weighted_average_label']}); "
        f"readiness gate Level {agg['gating_level']}; modernization pressure {pressure}",
        "---",
        "",
        "# Scorecard",
        "",
        "## Levels",
        "",
        "The 0–4 scale applied to every dimension:",
        "",
        "| Level | Label | Meaning |",
        "|:---:|-------|---------|",
        *[f"| {n} | {LEVEL_LABELS[n]} | {LEVEL_MEANINGS[n]} |" for n in range(5)],
        "",
        "## Headline",
        "",
        f"- **Overall maturity (weighted):** Level {agg['weighted_average']} / 4 "
        f"— {agg['weighted_average_label']}",
    ]
    if agg["gating_level"] is not None:
        gd = ", ".join(agg["gating_dimensions"])
        lines.append(
            f"- **Production-readiness gate (weakest critical dimension):** Level "
            f"{agg['gating_level']} — {agg['gating_level_label']} ({gd})"
        )
    if agg["modernization_pressure"] is not None:
        md = ", ".join(agg["modernization_drivers"])
        lines.append(
            f"- **Modernization pressure:** {agg['modernization_pressure']} "
            f"(legacy-cluster avg {agg['modernization_cluster_avg']} / 4; driven by {md})"
        )
    if agg.get("tco_burden") is not None:
        td = ", ".join(agg["tco_drivers"])
        lines.append(
            f"- **TCO signature (relative):** {agg['tco_burden']} cost-of-ownership burden "
            f"(cost-weighted maturity {agg['tco_maturity']} / 4; heaviest drivers {td})"
        )

    lines += [
        "",
        "## How to read this",
        "",
        "Four signals answer four different questions — keep them apart:",
        "",
        "- **Overall** — the weighted blend of all dimensions. A one-glance summary, "
        "*not* the verdict: an average can hide an acute problem in a single area.",
        "- **Readiness gate** — *can you responsibly keep running this as-is?* It is the "
        "**minimum** of the critical dimensions (security, testing, reliability), so the "
        "weakest one caps it — not the average.",
        "- **Modernization pressure** — *how urgently should you act?* From the legacy "
        "cluster (architecture, performance, dependency-health, code-quality, adaptability), "
        "weighted so adaptability dominates: the lower they score, the higher the pressure. "
        "A repo can pass the gate yet carry pressure — safe to run today, but a growing brake.",
        "- **TCO signature** — *what will it cost to own?* A **relative** (not euro) burden "
        "from the cost-of-ownership dimensions, weighted so **adaptability dominates**, "
        "because cost of change is the largest slice of software TCO. A static audit yields "
        "a relative signature only; actual spend needs infra/licence/effort data fed in.",
        "",
        "## What the numbers say",
        "",
    ]
    lines += [f"- {b}" for b in compute_insights(agg)]

    lines += [
        "",
        "## Dimensions",
        "",
        "| Dimension | Level | Label | Weight | Confidence | Lens |",
        "|-----------|:-----:|-------|:------:|:----------:|:----:|",
    ]
    for r in sorted(agg["scored"], key=lambda x: x["level"]):
        d = r["dimension"]
        lines.append(
            f"| {d} | {r['level']} | {LEVEL_LABELS.get(r['level'], '?')} | "
            f"{weights.get(d, 1.0)} | {r.get('confidence', '—')} | {_lens(d)} |"
        )
    for d in agg["not_applicable"]:
        lines.append(f"| {d} | n/a | Not applicable | — | — | — |")

    lines += [
        "",
        "_Sorted lowest-level first: the top rows are where attention is most needed._",
        "",
        "## Reading the table",
        "",
        "- **Weight** affects only the Overall average — it does **not** change the gate "
        "or the pressure.",
        "- **★** marks a **critical** dimension (security, testing, reliability) — the "
        "three that set the readiness gate.",
        "- **Lens `★ gate`** = a critical dimension; the readiness gate takes their "
        "**worst** level, not their average.",
        "- **Lens `cluster`** = a legacy-cluster dimension (architecture, performance, "
        "dependency-health, code-quality, adaptability); these drive modernization pressure.",
        "- **Modernization pressure** and the **TCO signature** are cost lenses, weighted "
        "separately from the Overall (adaptability dominates both); the Overall average uses "
        "the Weight column shown above.",
        "- **Confidence** reflects how exhaustively the evidence could be gathered; this "
        "is a static (code-only) audit, so runtime properties are inferred.",
    ]
    return "\n".join(lines) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("dimensions_dir", help="directory of per-dimension *.json files")
    ap.add_argument("--out", default=".", help="output directory")
    ap.add_argument("--weights", help="optional JSON file overriding default weights")
    args = ap.parse_args()

    dim_dir = pathlib.Path(args.dimensions_dir)
    out_dir = pathlib.Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    weights = dict(DEFAULT_WEIGHTS)
    if args.weights:
        weights.update(json.loads(pathlib.Path(args.weights).read_text()))

    results = load_dimensions(dim_dir)
    if not results:
        sys.exit(f"No dimension JSON files found in {dim_dir}")

    agg = aggregate(results, weights)
    (out_dir / "scorecard.md").write_text(render_scorecard(agg, weights))
    summary = {k: v for k, v in agg.items() if k != "scored"}
    summary["dimensions"] = [
        {"dimension": r["dimension"], "level": r.get("level"),
         "confidence": r.get("confidence")}
        for r in agg["scored"]
    ]
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2))

    print(f"Overall (weighted): Level {agg['weighted_average']} — {agg['weighted_average_label']}")
    if agg["gating_level"] is not None:
        print(f"Readiness gate: Level {agg['gating_level']} ({', '.join(agg['gating_dimensions'])})")
    if agg["modernization_pressure"] is not None:
        print(f"Modernization pressure: {agg['modernization_pressure']} "
              f"(drivers: {', '.join(agg['modernization_drivers'])})")
    if agg.get("tco_burden") is not None:
        print(f"TCO signature (relative): {agg['tco_burden']} "
              f"(drivers: {', '.join(agg['tco_drivers'])})")
    print(f"Wrote {out_dir/'scorecard.md'} and {out_dir/'summary.json'}")


if __name__ == "__main__":
    main()
