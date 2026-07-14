#!/usr/bin/env python3
"""
Generate the COMPLETE current-year estimate table (Cloud_Region_Metadata_estimate.csv).

Unlike estimate_current_region_metadata.py (which trends only the regions present in the
latest reported year and leaves gaps blank), this produces a *fully populated best-guess*
table for the current year: every region that has ever been reported gets a row, and every
metric cell we track is filled — with the region's own trended value where it has history,
otherwise a **regional best guess**:
  - grid-tied metrics (grid carbon intensity, consumption-hourly) are filled from the mean of
    other regions sharing the same Electricity Maps zone (em-zone-id), i.e. the same physical grid;
  - provider metrics (PUE, WUE, CFE, market carbon, water) are filled from the provider's mean
    for the region's continent, then the provider's global mean.
The reported table (Cloud_Region_Metadata.csv) is never modified and stays clean — this is the
"best guess" companion, kept deliberately separate.

The only columns left blank are the EU-EED disclosure fields that no provider reports at all
(total-ICT-energy-consumption-annual, renewable-energy-consumption[-goe/-ppa/-onsite]) — there is
no data anywhere to base a guess on.

Usage: python complete_estimate.py <reported_csv> [target_year]
"""
import pandas as pd, numpy as np, sys, os

REPORTED = sys.argv[1] if len(sys.argv) > 1 else "Cloud_Region_Metadata.csv"

TEXT = ["cfe-region", "em-zone-id", "wt-region-id", "location", "geolocation"]
# Grid carbon intensity is a physical property of the grid (em-zone) and is the same
# regardless of which provider operates there, so it may be filled from regional
# (em-zone, then geographic continent) data.
GRID = ["grid-carbon-intensity-average-consumption-annual",
        "grid-carbon-intensity-marginal-consumption-annual",
        "grid-carbon-intensity-average-production-annual",
        "grid-carbon-intensity"]
# Provider-specific metrics are filled ONLY from the same provider's regional data
# (provider + continent, then provider). They are NEVER estimated across providers:
# if a provider doesn't report a metric anywhere (e.g. AWS/Azure carbon-free-energy %,
# Google/Azure water), it is left blank rather than borrowed from another provider.
PROV = ["provider-carbon-intensity-average-consumption-hourly",
        "provider-cfe-hourly", "provider-cfe-annual",
        "power-usage-effectiveness", "water-usage-effectiveness",
        "provider-carbon-intensity-market-annual", "total-water-input"]
# never reported anywhere -> leave blank
EED = ["total-ICT-energy-consumption-annual", "renewable-energy-consumption",
       "renewable-energy-consumption-goe", "renewable-energy-consumption-ppa",
       "renewable-energy-consumption-onsite"]
NUM = GRID + PROV
CLAMP01 = {"provider-cfe-hourly", "provider-cfe-annual"}
NONNEG = set(GRID) | {"provider-carbon-intensity-market-annual", "total-water-input"}

def continent(region, cfe, loc):
    r = (region or "").lower()
    for pfx, c in [("us-", "NA"), ("ca-", "NA"), ("northamerica", "NA"),
                   ("sa-", "LATAM"), ("mx-", "LATAM"), ("southamerica", "LATAM"),
                   ("eu-", "EU"), ("uk-", "EU"), ("europe", "EU"),
                   ("me-", "ME"), ("il-", "ME"), ("af-", "AF"), ("africa", "AF"),
                   ("ap-", "APAC"), ("asia", "APAC"), ("australia", "APAC"),
                   ("cn-", "CN")]:
        if r.startswith(pfx) or pfx in r:
            return c
    # Azure-style names
    t = (region or "") + " " + (loc or "")
    tl = t.lower()
    if any(k in tl for k in ["us", "america", "canada", "virginia", "iowa", "texas"]): return "NA"
    if any(k in tl for k in ["europe", "uk", "france", "germany", "sweden", "italy", "spain", "poland", "zurich", "ireland", "denmark", "austria", "greece"]): return "EU"
    if any(k in tl for k in ["asia", "australia", "japan", "korea", "india", "singapore", "taiwan", "zealand", "indonesia"]): return "APAC"
    if any(k in tl for k in ["brazil", "chile", "mexico"]): return "LATAM"
    return "OTHER"

def to_num(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return np.nan

def main():
    df = pd.read_csv(REPORTED, dtype=str)
    df["_yr"] = df["year"].astype(int)
    target = int(sys.argv[2]) if len(sys.argv) > 2 else df["_yr"].max() + 1
    cols = [c for c in df.columns if c != "_yr"]

    rows = []
    for (prov, region), g in df.groupby(["cloud-provider", "cloud-region"]):
        g = g.sort_values("_yr")
        latest = g.iloc[-1]
        row = {c: ("" if pd.isna(latest[c]) else latest[c]) for c in cols}
        row["year"] = str(target)
        # trend / carry-forward each numeric metric from this region's own history
        for col in NUM:
            hist = [(int(y), to_num(v)) for y, v in zip(g["year"], g[col])]
            hist = [(y, v) for y, v in hist if not np.isnan(v)]
            if not hist:
                row[col] = np.nan            # regional fill later
                continue
            if len(hist) >= 2:
                diffs = np.diff([v for _, v in hist])
                val = hist[-1][1] + float(np.mean(diffs)) * (target - hist[-1][0])
            else:
                val = hist[-1][1]
            if col == "power-usage-effectiveness":
                val = max(1.04, val)
            if col in CLAMP01:
                val = min(1.0, max(0.0, val))
            if col in NONNEG:
                val = max(0.0, val)
            row[col] = val
        row["_cont"] = continent(region, row.get("cfe-region"), row.get("location"))
        rows.append(row)

    est = pd.DataFrame(rows)

    # ---- regional fill for cells still NaN ----
    def groupmean(mask_cols, keys):
        # mean of a column within groups defined by keys, over rows that have a value
        return {col: est[est[col].notna()].groupby(keys)[col].mean().to_dict() for col in mask_cols}

    def fill_from(col, keysets):
        for keys in keysets:
            if not est[col].isna().any():
                break
            gm = est[est[col].notna()].groupby(keys)[col].mean()
            for i in est.index[est[col].isna()]:
                if any(pd.isna(est.loc[i, k]) or est.loc[i, k] == "" for k in keys):
                    continue                     # can't group without a valid key
                key = est.loc[i, keys[0]] if len(keys) == 1 else tuple(est.loc[i, k] for k in keys)
                if key in gm.index:
                    est.at[i, col] = gm.loc[key]

    # Grid carbon intensity: regional (grid) data only — em-zone, then geographic continent.
    # No provider key: the grid's carbon intensity is a shared regional fact. Anything still
    # missing (no regional data at all) is left blank rather than globally fabricated.
    for col in GRID:
        fill_from(col, (["em-zone-id"], ["_cont"]))

    # Provider metrics: SAME provider only — provider+continent, then provider. Never across
    # providers, so a metric a provider doesn't report anywhere stays blank.
    for col in PROV:
        fill_from(col, (["cloud-provider", "_cont"], ["cloud-provider"]))

    # clamps + rounding
    for col in NUM:
        if col == "power-usage-effectiveness":
            est[col] = est[col].clip(lower=1.04).round(3)
        elif col in CLAMP01:
            est[col] = est[col].clip(0, 1).round(2)
        elif col in ("total-water-input",):
            est[col] = est[col].clip(lower=0).round(0)
        else:
            est[col] = est[col].clip(lower=0).round(2)

    # EED columns stay blank (no data anywhere)
    for col in EED:
        est[col] = ""

    est = est[cols]
    est["_y"] = est["year"].astype(int)
    est = est.sort_values(["_y", "cloud-provider", "cloud-region"], ascending=[False, True, True]).drop(columns="_y")
    out = REPORTED.replace(".csv", "_estimate.csv")
    est.to_csv(out, index=False, lineterminator="\r\n")
    filled = {c: int(est[c].astype(str).str.strip().replace("nan", "").ne("").sum()) for c in NUM}
    print(f"Complete estimate for {target}: {len(est)} rows -> {out}")
    print("filled per metric:", {k: v for k, v in filled.items()})

if __name__ == "__main__":
    main()
