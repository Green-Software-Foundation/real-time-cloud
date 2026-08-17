#!/usr/bin/env python3
"""Fill in missing region-identity metadata in Cloud_Region_Metadata.csv.

The identity columns - cfe-region, em-zone-id, wt-region-id, geolocation - are
static per region (Annex A of the specification lists them as "Static"), so a
blank in one year's row is a gap rather than a different value. This script
fills those gaps and repairs values that are demonstrably wrong.

Only Cloud_Region_Metadata.csv is written. Cloud_Region_Metadata_estimate.csv is
generated from it by code/complete_estimate.py and must be regenerated after
running this (see code/README.md).

Passes, in order (each is idempotent):

1. trim       strip stray whitespace from the identity columns
2. fix        replace values that are demonstrably wrong - a coordinate that
              resolves to the wrong city, a zone key that does not exist in
              Electricity Maps, a country mismatch. Applied only when the cell
              still holds the recorded wrong value.
3. propagate  copy an identity value from the most recent year that has it into
              the same region's earlier years
4. reference  fill regions that have no value in any year, from an external
              reference (see REFERENCE below)
5. zone       derive cfe-region and wt-region-id from em-zone-id, using the
              mapping the rest of the table already uses for that zone. This is
              what populates the Oracle rows, which carry em-zone-id and
              geolocation but no grid-region names.

Usage:
    python code/fill_region_metadata.py --dry-run
    python code/fill_region_metadata.py
    python code/fill_region_metadata.py --passes fix        # one pass only
"""

import argparse
import csv
import os
import sys
from collections import defaultdict

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(REPO, "Cloud_Region_Metadata.csv")

IDENTITY = ["cfe-region", "em-zone-id", "wt-region-id", "geolocation"]
PASSES = ["trim", "fix", "propagate", "reference", "zone"]

AWS = "Amazon Web Services"
GCP = "Google Cloud"
AZURE = "Microsoft Azure"
OCI = "Oracle Cloud Infrastructure"

# ---------------------------------------------------------------------------
# Pass 2 - corrections. (provider, region, column, current_value) -> (new, why)
# ---------------------------------------------------------------------------
CORRECTIONS = {
    # Electricity Maps has no NZ-NZN zone. The valid New Zealand keys are NZ,
    # NZ-NZA (the subantarctic Auckland Islands, not Auckland), NZ-NZC and
    # NZ-NZST. Azure's Auckland region already uses NZ in this table.
    (AWS, "ap-southeast-6", "em-zone-id", "NZ-NZN"):
        ("NZ", "NZ-NZN is not an Electricity Maps zone key"),

    # me-central1 is Doha, Qatar - not the UAE. wt-region-id was already QAT.
    (GCP, "me-central1", "cfe-region", "United Arab Emirates"):
        ("Qatar", "me-central1 is Doha, Qatar"),
    (GCP, "me-central1", "em-zone-id", "AE"):
        ("QA", "me-central1 is Doha, Qatar"),

    # Coordinates that resolve to the wrong place entirely.
    (AWS, "sa-east-1", "geolocation", "-3.45,-68.95"):
        ("-23.5505,-46.6333", "was a point in the Amazon, not Sao Paulo"),
    (GCP, "southamerica-east1", "geolocation", "-3.45,-68.95"):
        ("-23.5505,-46.6333", "was a point in the Amazon, not Sao Paulo"),
    (GCP, "us-south1", "geolocation", "44.9221,-123.313"):
        ("32.7767,-96.797", "was Dallas, Oregon; us-south1 is Dallas, Texas"),
    (GCP, "us-west4", "geolocation", "35.6011,-105.2206"):
        ("36.1699,-115.1398", "was Las Vegas, New Mexico; us-west4 is Las Vegas, Nevada"),
    (GCP, "us-east5", "geolocation", "41.4366,-97.3565"):
        ("39.9612,-82.9988", "was Columbus, Nebraska; us-east5 is Columbus, Ohio"),

    # Malformed coordinate - '.' where the separating ',' belongs.
    (OCI, "sa-saopaulo-1", "geolocation", "-23.5558.-46.6396"):
        ("-23.5558,-46.6396", "latitude/longitude separator was a period"),
}

# ---------------------------------------------------------------------------
# Pass 4 - regions with no value for a column in any year.
#
# em-zone-id values are checked against electricitymaps-contrib config/zones by
# --validate. wt-region-id follows WattTime's conventions already used in this
# table: ISO 3166-1 alpha-3 for country-level regions (IND, SGP, IDN, ZAF, CHN,
# ARE, ...) and the balancing-authority abbreviation in North America.
# ---------------------------------------------------------------------------
REFERENCE = {
    (AWS, "ap-southeast-5"): {"wt-region-id": "MYS"},            # Kuala Lumpur, Malaysia
    (AWS, "ap-southeast-6"): {"wt-region-id": "NZL"},            # Auckland, New Zealand
    (AWS, "ap-southeast-7"): {"wt-region-id": "THA"},            # Bangkok, Thailand
    (AWS, "ca-west-1"): {"cfe-region": "Alberta", "em-zone-id": "CA-AB",
                         "wt-region-id": "AESO"},                # Calgary, Alberta
    (AWS, "cn-north-1"): {"cfe-region": "China", "em-zone-id": "CN"},      # Beijing
    (AWS, "cn-northwest-1"): {"cfe-region": "China", "em-zone-id": "CN"},  # Ningxia

    (GCP, "africa-south1"): {"geolocation": "-26.2041,28.0473"}, # Johannesburg
    (GCP, "europe-north2"): {"cfe-region": "Sweden", "em-zone-id": "SE",
                             "wt-region-id": "SE"},              # Stockholm
    (GCP, "europe-west10"): {"cfe-region": "Germany", "em-zone-id": "DE",
                             "wt-region-id": "DE"},              # Berlin
    (GCP, "me-central1"): {"geolocation": "25.2854,51.531"},     # Doha
    (GCP, "me-central2"): {"geolocation": "26.4207,50.0888"},    # Dammam
    (GCP, "northamerica-south1"): {"cfe-region": "Mexico", "em-zone-id": "MX",
                                   "wt-region-id": "MX_SIN"},    # Queretaro
    (GCP, "us-east2"): {"cfe-region": "SOCO", "em-zone-id": "US-SE-SOCO",
                        "wt-region-id": "SOCO"},                 # Georgia

    (AZURE, "westcentralus"): {"cfe-region": "WACM", "em-zone-id": "US-NW-WACM"},  # Wyoming
    (AZURE, "westus3"): {"cfe-region": "AZPS", "em-zone-id": "US-SW-AZPS"},        # Arizona
}

# ---------------------------------------------------------------------------
# Pass 5 - em-zone-id -> (cfe-region, wt-region-id).
#
# Every entry here matches what the rest of the table already uses for that
# zone, so filling a blank from it keeps a zone's rows internally consistent.
# Zones the table did not previously cover (CO, RS, SE-SE3, US-SW-AZPS) are
# marked below.
# ---------------------------------------------------------------------------
ZONE_MAP = {
    "AE": ("United Arab Emirates", "ARE"),
    "AU-NSW": ("New South Wales", "NEM_NSW"),
    "AU-VIC": ("Victoria", "NEM_VIC"),
    "BR-CS": ("Central Brazil", "BRA"),
    "CA-ON": ("Ontario", "IESO_NORTH"),
    "CA-QC": ("Quebec", "HQ"),
    "CH": ("Switzerland", "CH"),
    "CL-SEN": ("Chile", "CHL"),
    "CO": ("Colombia", "COL"),               # new zone: Oracle Bogota
    "DE": ("Germany", "DE"),
    "ES": ("Spain", "ES"),
    "FR": ("France", "FR"),
    "GB": ("Great Britain", "UK"),
    "IL": ("Israel", "ISR"),
    "IN-SO": ("India", "IND"),
    "IN-WE": ("Maharashtra", "IND"),
    "IT-NO": ("North Italy", "IT"),
    "JP-KN": ("Kansai", "JP_KN"),
    "JP-TK": ("Tokyo", "JP_TK"),
    "KR": ("South Korea", "KOR"),
    "MX": ("Mexico", "MX_SIN"),
    "NL": ("Netherlands", "NL"),
    "RS": ("Serbia", "SRB"),                 # new zone: Oracle Jovanovac
    "SA": ("Saudi Arabia", "SAU"),
    "SE-SE3": ("Sweden", "SE"),              # new zone: Oracle Stockholm
    "SG": ("Singapore", "SGP"),
    "US-SW-AZPS": ("AZPS", "AZPS"),          # new zone: Oracle/Azure Phoenix
    "ZA": ("South Africa", "ZAF"),
    # Large US zones carry one cfe-region but several WattTime sub-regions; the
    # sub-region depends on the city, so only cfe-region is filled from the zone
    # and wt-region-id comes from ZONE_SUBREGION below.
    "US-CAL-CISO": ("CAISO", None),
    "US-MIDA-PJM": ("PJM", None),
    "US-MIDW-MISO": ("MISO", None),
}

# City-level WattTime sub-region for the multi-sub-region US zones above.
ZONE_SUBREGION = {
    (OCI, "us-ashburn-1"): "PJM_DC",
    (OCI, "us-gov-ashburn-1"): "PJM_DC",
    (OCI, "us-langley-1"): "PJM_DC",         # Oracle reports this one at Ashburn
    (OCI, "us-chicago-1"): "MISO_SPRINGFIELD",
    (OCI, "us-gov-chicago-1"): "MISO_SPRINGFIELD",
    (OCI, "us-sanjose-1"): "CAISO_NORTH",
}


def load(path):
    with open(path, newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        return reader.fieldnames, list(reader)


def save(path, fieldnames, rows):
    with open(path, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--passes", default=",".join(PASSES),
                    help="comma-separated subset of " + ",".join(PASSES))
    args = ap.parse_args()
    active = {p.strip() for p in args.passes.split(",")}

    fieldnames, rows = load(DATA)
    changes = []

    def key(r):
        return (r["cloud-provider"], r["cloud-region"])

    def record(kind, r, col, new, why):
        changes.append((kind, r["year"], key(r), col, r[col], new, why))
        r[col] = new

    if "trim" in active:
        for r in rows:
            for col in IDENTITY:
                if r[col] != r[col].strip():
                    record("trim", r, col, r[col].strip(), "stray whitespace")

    if "fix" in active:
        for r in rows:
            for col in IDENTITY:
                fix = CORRECTIONS.get(key(r) + (col, r[col]))
                if fix:
                    record("fix", r, col, fix[0], fix[1])

    if "propagate" in active:
        latest = defaultdict(dict)
        for r in sorted(rows, key=lambda x: x["year"]):
            for col in IDENTITY:
                if r[col]:
                    latest[key(r)][col] = r[col]
        for r in rows:
            for col in IDENTITY:
                if not r[col] and col in latest[key(r)]:
                    record("propagate", r, col, latest[key(r)][col],
                           "from the latest year that has it")

    if "reference" in active:
        for r in rows:
            for col, val in REFERENCE.get(key(r), {}).items():
                if not r[col]:
                    record("reference", r, col, val, "external reference")

    if "zone" in active:
        for r in rows:
            zone = ZONE_MAP.get(r["em-zone-id"])
            if not zone:
                continue
            cfe, wt = zone
            if not r["cfe-region"] and cfe:
                record("zone", r, "cfe-region", cfe, f"from em-zone-id {r['em-zone-id']}")
            if not r["wt-region-id"]:
                sub = ZONE_SUBREGION.get(key(r), wt)
                if sub:
                    record("zone", r, "wt-region-id", sub,
                           f"from em-zone-id {r['em-zone-id']}")

    # ---- report ----
    for kind in PASSES:
        sub = [c for c in changes if c[0] == kind]
        if not sub and kind not in active:
            continue
        print(f"\n=== {kind.upper()} ({len(sub)} cells) ===")
        agg = defaultdict(list)
        for _, year, k, col, old, new, why in sub:
            agg[(k, col, old, new, why)].append(year)
        for (k, col, old, new, why), years in sorted(agg.items()):
            span = f"{min(years)}-{max(years)}" if len(years) > 1 else years[0]
            print(f"  {k[0][:6]:6} {k[1]:22} {col:12} {old or '(blank)':22} -> {new:20} "
                  f"[{span}] {why}")

    print("\n=== REMAINING BLANKS ===")
    remaining = defaultdict(set)
    for r in rows:
        for col in IDENTITY:
            if not r[col]:
                remaining[key(r)].add(col)
    for k, cols in sorted(remaining.items()):
        print(f"  {k[0][:6]:6} {k[1]:22} {sorted(cols)}")
    if not remaining:
        print("  none")

    # ---- structural checks ----
    print("\n=== CHECKS ===")
    problems = []
    for r in rows:
        geo = r["geolocation"]
        if geo:
            try:
                lat, lon = (float(p) for p in geo.split(","))
                if not (-90 <= lat <= 90 and -180 <= lon <= 180):
                    problems.append(f"{key(r)} {r['year']}: coordinate out of range {geo!r}")
            except ValueError:
                problems.append(f"{key(r)} {r['year']}: unparseable geolocation {geo!r}")
    for p in sorted(set(problems)):
        print("  " + p)
    if not problems:
        print("  geolocation: all values parse as lat,lon in range")

    if args.dry_run:
        print("\n(dry run - nothing written)")
        return 0
    save(DATA, fieldnames, rows)
    print(f"\nWrote {DATA} ({len(rows)} rows).")
    print("Now regenerate the estimate table:")
    print("  python code/complete_estimate.py Cloud_Region_Metadata.csv 2026")
    print("  python code/sanity_check_estimate.py Cloud_Region_Metadata.csv "
          "Cloud_Region_Metadata_estimate.csv")
    return 0


if __name__ == "__main__":
    sys.exit(main())
