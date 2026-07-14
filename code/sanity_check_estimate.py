#!/usr/bin/env python3
"""
Sanity-check the complete estimate table against the reported data table.

The estimate table is meant to be *the* central best-guess anyone can use today, so its numbers must be
plausible next to what providers actually reported. This script flags estimate values that look wrong:
  - out-of-range absolutes (PUE < 1.04 or > 2.0, CFE outside 0-1, negative carbon/water);
  - large jumps from a region's own most recent reported value (metric-specific thresholds);
  - regionally-filled cells (no reported value for that region) that fall outside the range of the
    reported values in their fill group (em-zone for grid metrics, provider+continent for provider ones);
  - coverage gaps (a reported region missing from the estimate).
Exit status is 0 with a summary; findings are printed for review, not treated as hard failures, because
some large moves are legitimate (a new grid, a restated value).

Usage: python sanity_check_estimate.py [reported_csv] [estimate_csv]
"""
import csv, sys, statistics as st

REPORTED = sys.argv[1] if len(sys.argv) > 1 else "Cloud_Region_Metadata.csv"
ESTIMATE = sys.argv[2] if len(sys.argv) > 2 else "Cloud_Region_Metadata_estimate.csv"

# absolute plausible ranges
RANGE = {
    "power-usage-effectiveness": (1.04, 2.0),
    "water-usage-effectiveness": (0.0, 5.0),
    "provider-cfe-hourly": (0.0, 1.0),
    "provider-cfe-annual": (0.0, 1.0),
    "provider-carbon-intensity-market-annual": (0.0, 1200.0),
    "provider-carbon-intensity-average-consumption-hourly": (0.0, 1200.0),
    "grid-carbon-intensity-average-consumption-annual": (0.0, 1200.0),
    "grid-carbon-intensity-marginal-consumption-annual": (0.0, 1200.0),
    "grid-carbon-intensity-average-production-annual": (0.0, 1200.0),
    "grid-carbon-intensity": (0.0, 1200.0),
    "total-water-input": (0.0, 1e11),
}
# max plausible jump from the latest reported value (abs, in the column's units)
JUMP = {
    "power-usage-effectiveness": 0.15,
    "water-usage-effectiveness": 0.6,
    "provider-cfe-hourly": 0.2,
    "provider-cfe-annual": 0.2,
}
# relative jump threshold for carbon/water columns (fraction)
JUMP_REL = 0.4
GRID = {"grid-carbon-intensity-average-consumption-annual", "grid-carbon-intensity-marginal-consumption-annual",
        "grid-carbon-intensity-average-production-annual", "grid-carbon-intensity"}


def num(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def load(path):
    return list(csv.DictReader(open(path)))


rep, est = load(REPORTED), load(ESTIMATE)
metrics = [c for c in RANGE]

# latest reported value + full reported history per (provider, region, metric)
latest, hist = {}, {}
for r in sorted(rep, key=lambda x: x["year"]):
    for m in metrics:
        v = num(r[m])
        if v is not None:
            latest[(r["cloud-provider"], r["cloud-region"], m)] = (int(r["year"]), v)
            hist.setdefault((r["cloud-provider"], m), []).append((r["em-zone-id"], r["_cont"] if "_cont" in r else None, v))

flags = {"out-of-range": [], "big-jump": [], "regional-outlier": [], "coverage": []}

# coverage: reported provider-region pairs missing from estimate
est_pairs = {(r["cloud-provider"], r["cloud-region"]) for r in est}
for p in {(r["cloud-provider"], r["cloud-region"]) for r in rep}:
    if p not in est_pairs:
        flags["coverage"].append(f"{p[0]} {p[1]} reported but not in estimate")

# reported group ranges for regional-outlier check
grp_grid = {}   # (metric, em-zone) -> [values]
grp_prov = {}   # (metric, provider) -> [values]
for r in rep:
    for m in metrics:
        v = num(r[m])
        if v is None:
            continue
        if m in GRID:
            grp_grid.setdefault((m, r["em-zone-id"]), []).append(v)
        grp_prov.setdefault((m, r["cloud-provider"]), []).append(v)

for r in est:
    prov, reg = r["cloud-provider"], r["cloud-region"]
    for m in metrics:
        v = num(r[m])
        if v is None:
            continue
        lo, hi = RANGE[m]
        if v < lo or v > hi:
            flags["out-of-range"].append(f"{prov} {reg} {m}={v} (range {lo}-{hi})")
        key = (prov, reg, m)
        if key in latest:                        # region has its own reported value -> jump check
            yr, rv = latest[key]
            if m in JUMP and abs(v - rv) > JUMP[m]:
                flags["big-jump"].append(f"{prov} {reg} {m}: reported {rv} ({yr}) -> est {v}")
            elif m not in JUMP and rv > 0 and abs(v - rv) / rv > JUMP_REL:
                flags["big-jump"].append(f"{prov} {reg} {m}: reported {rv} ({yr}) -> est {v} ({(v-rv)/rv:+.0%})")
        else:                                    # regionally filled -> outlier vs fill group
            grp = grp_grid.get((m, r["em-zone-id"])) if m in GRID else grp_prov.get((m, prov))
            if grp and len(grp) >= 3:
                lo_g, hi_g = min(grp), max(grp)
                pad = (hi_g - lo_g) * 0.25 + 1e-9
                if v < lo_g - pad or v > hi_g + pad:
                    flags["regional-outlier"].append(f"{prov} {reg} {m}={v} filled outside group range {lo_g:.2f}-{hi_g:.2f}")

print(f"Estimate rows: {len(est)} | reported pairs: {len({(r['cloud-provider'],r['cloud-region']) for r in rep})}")
total = 0
for k, v in flags.items():
    print(f"\n== {k}: {len(v)} ==")
    for line in v[:25]:
        print("  -", line)
    if len(v) > 25:
        print(f"  ... and {len(v)-25} more")
    total += len(v)
print(f"\nTOTAL flags: {total}  ({'clean' if total == 0 else 'review the above — some may be legitimate'})")
