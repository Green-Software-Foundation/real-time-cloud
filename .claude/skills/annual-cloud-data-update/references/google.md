# Google Cloud

**Cadence:** Google publishes its Environmental Report ~June; the report is named for the *following*
year (e.g. the "2026 Environmental Report" covers calendar year 2025). The machine-readable per-region
data lands separately in a GitHub repo and can lag the PDF. Tracking issues: #159 (report link), #116,
and #151 (a real data-quality fix — see below).

## Sources
- **Per-region hourly CFE + grid carbon intensity:**
  `https://github.com/GoogleCloudPlatform/region-carbon-info` → `data/yearly/<year>.csv`, columns
  `Google Cloud Region, Location, Google CFE, Grid carbon intensity (gCO2eq / kWh)`. This is the
  authoritative per-region source and what `code/gcp-data-update.py` pulls. **Check the repo actually
  has the new year** — it often stops a year behind the PDF, in which case Google's per-region CFE/grid
  for the newest year simply isn't published yet; leave those columns blank and say so.
- **Per-datacenter PUE:** the Environmental Report PDF, in the "Data center energy efficiency (PUE)"
  table (around p.94), with a column per year 2021…latest. This is by *datacenter location*, not by
  cloud region, so map location→region (below). Google does not publish per-region WUE (water is
  reported in million gallons by location, not L/kWh) — leave WUE blank.

## Columns to populate
- `provider-cfe-hourly` — the `Google CFE` value from the yearly CSV. This is Google's per-region,
  hourly-matched, location-based carbon-free-energy figure. **This is the useful column.**
- `provider-cfe-annual` — **leave blank.** Google's only annual figure is the company-wide 100%
  renewable *market* match, which nets across unconnected grids and isn't useful per-region (issue
  #151 / WG position). Do not set it to `1.0`. (`code/gcp_data_update.py` in PR #156 gates this behind
  a `GOOGLE_ANNUAL_MATCHING_CLAIM` constant — set it to `None`.)
- `grid-carbon-intensity-average-consumption-annual` — the grid carbon intensity from the yearly CSV.
- `power-usage-effectiveness` — from the report's per-datacenter PUE table, for regions with a
  Google-owned datacenter. These values differ slightly year-to-year and don't always match the
  region-carbon repo methodology, so note the source. Multi-facility metros (Singapore, Council
  Bluffs, The Dalles, Loudoun) are ambiguous — pick the primary facility and flag it, or leave blank.
- Carry forward `cfe-region`, `em-zone-id`, `wt-region-id`, `location`, `geolocation`.

## Location → region-code map (owned datacenters with PUE)
```
Changhua County/Taiwan asia-east1   Inzai/Japan asia-northeast1   Singapore asia-southeast1
Hamina/Finland europe-north1        St. Ghislain/Belgium europe-west1   Eemshaven/Netherlands europe-west4
Quilicura/Chile southamerica-west1  Council Bluffs/Iowa us-central1  Berkeley County SC us-east1
Loudoun County VA us-east4          Columbus/New Albany OH us-east5  Midlothian TX (Dallas) us-south1
The Dalles/Oregon us-west1          Henderson NV (Las Vegas) us-west4
```
(The full region↔location list is already in the dataset's `location` column — join on it.)

## The #151 lesson (verify this every year)
Google's per-region CFE had been mis-filed: the correct `Google CFE` value ended up in
`provider-cfe-annual` while `provider-cfe-hourly` held a stale/wrong number. The fix is to put the
authoritative `Google CFE` into `provider-cfe-hourly` and leave `provider-cfe-annual` blank. Always
verify the new year's `provider-cfe-hourly` equals the `Google CFE` column from the source CSV
(a quick per-region diff — expect zero mismatches).
