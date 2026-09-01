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

# Default weights. Security, testing, and reliability weigh more because a low
# score there blocks production-readiness regardless of the other dimensions;
# performance & architecture weigh up because they drive modernization value.
DEFAULT_WEIGHTS = {
    "security": 1.5,
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
}

LEVEL_LABELS = {
    0: "Absent",
    1: "Initial",
    2: "Developing",
    3: "Established",
    4: "Optimized",
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

    # Modernization pressure: average maturity of the legacy cluster, inverted.
    cluster = [r for r in scored if r["dimension"] in MODERNIZATION_CLUSTER]
    cluster_avg = sum(r["level"] for r in cluster) / len(cluster) if cluster else None
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

    return {
        "weighted_average": round(weighted, 2),
        "weighted_average_label": band(weighted),
        "gating_level": gating,
        "gating_level_label": LEVEL_LABELS.get(gating) if gating is not None else None,
        "gating_dimensions": gating_dims,
        "modernization_pressure": pressure,
        "modernization_cluster_avg": round(cluster_avg, 2) if cluster_avg is not None else None,
        "modernization_drivers": cluster_drivers,
        "scored": scored,
        "not_applicable": na,
    }


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
    ]
    lines.append(
        f"**Overall maturity (weighted): Level {agg['weighted_average']} / 4 "
        f"— {agg['weighted_average_label']}**"
    )
    if agg["gating_level"] is not None:
        gd = ", ".join(agg["gating_dimensions"])
        lines.append(
            f"**Production-readiness gate (weakest critical dimension): Level "
            f"{agg['gating_level']} — {agg['gating_level_label']}** ({gd})"
        )
    if agg["modernization_pressure"] is not None:
        md = ", ".join(agg["modernization_drivers"])
        lines.append(
            f"**Modernization pressure: {agg['modernization_pressure']}** "
            f"(legacy-cluster avg {agg['modernization_cluster_avg']} / 4; "
            f"driven by {md})"
        )
    lines.append("")
    lines.append("| Dimension | Level | Label | Weight | Confidence | Critical |")
    lines.append("|-----------|:-----:|-------|:------:|:----------:|:--------:|")
    for r in sorted(agg["scored"], key=lambda x: x["level"]):
        d = r["dimension"]
        lines.append(
            f"| {d} | {r['level']} | {LEVEL_LABELS.get(r['level'], '?')} | "
            f"{weights.get(d, 1.0)} | {r.get('confidence', '—')} | "
            f"{'★' if d in CRITICAL else ''} |"
        )
    for d in agg["not_applicable"]:
        lines.append(f"| {d} | n/a | Not applicable | — | — | |")
    lines.append("")
    lines.append("_Sorted lowest-level first: the top rows are where attention is most needed._")
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
    print(f"Wrote {out_dir/'scorecard.md'} and {out_dir/'summary.json'}")


if __name__ == "__main__":
    main()
