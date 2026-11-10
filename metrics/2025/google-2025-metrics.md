# Google Cloud — 2025 sustainability metrics

**Sources:** Google 2026 Environmental Report (CY2025) —
`https://storage.googleapis.com/gweb-mobius-cdn/sustainability/uploads/7f477eb723fe0c23d03f94b90a08882b9f28187d.pdf`
(issue #159); machine-readable per-region data at
`https://github.com/GoogleCloudPlatform/region-carbon-info` (`data/yearly/`). Report published mid-2026.
**Reporting period:** **Calendar year 2025 (Jan 1 – Dec 31 2025)** for the report tables.
**Coverage boundary:** Google-owned and -operated data centers (PUE table is explicitly the entire
owned+operated fleet, "not just the newest or most efficient facilities").

## Metric definitions (quoted)
| Metric | Google definition (verbatim) | Period | Method | RTC column | Merge? |
|---|---|---|---|---|---|
| Carbon-free energy (CFE) | *"the percentage of Google's electricity consumption on a given regional grid that is matched hourly with CFE"* (Contracted CFE + Consumed Grid CFE, hourly) | CY2025 | **location-based, per-region, hourly** | `provider-cfe-hourly` | yes |
| PUE | *"a standard industry ratio that compares the amount of non-computing overhead energy … to the amount of energy used to power IT equipment"*; measured continuously across the whole owned+operated fleet | CY2025 | per-datacenter, annual | `power-usage-effectiveness` | yes (owned-DC regions) |
| Renewable energy (annual) | 100% annual renewable-energy match (electricity procured / consumed, netted across markets) | CY2025 | **market-based, global** | `provider-cfe-annual` | **no** — global market claim, not per-region |
| Grid carbon intensity | Electricity Maps consumption-based intensity per region | CY2025 | location-based, per-region | `grid-carbon-intensity-average-consumption-annual` | yes |
| WUE | not reported as L/kWh (water reported in million gallons by location) | CY2025 | — | — | no — not provided |

## Per-region values (CY2025)
Hourly CFE and grid carbon intensity from `region-carbon-info` `data/yearly/2025.csv` (published by
Google 2026-09-15, archived at `sources/google-region-carbon-info/2025.csv`); PUE from the report's
per-datacenter table, for the 14 regions with a Google-owned datacenter mapped to them.

| region | location | hourly CFE | grid carbon (gCO₂e/kWh) | PUE |
|---|---|---|---|---|
| africa-south1 | Johannesburg | 0.15 | 641.42 | — |
| asia-east1 | Taiwan | 0.15 | 427.95 | 1.13 |
| asia-east2 | Hong Kong | 0.02 | 488.52 | — |
| asia-northeast1 | Tokyo | 0.23 | 449.23 | 1.12 |
| asia-northeast2 | Osaka | 0.45 | 298.92 | — |
| asia-northeast3 | Seoul | 0.37 | 359.05 | — |
| asia-south1 | Mumbai | 0.2 | 598.45 | — |
| asia-south2 | Delhi | 0.39 | 472.55 | — |
| asia-southeast1 | Singapore | 0.05 | 365.66 | 1.12 |
| asia-southeast2 | Jakarta | 0.15 | 587.8 | — |
| asia-southeast3 | Bangkok | 0.19 | 364.68 | — |
| australia-southeast1 | Sydney | 0.37 | 468.34 | — |
| australia-southeast2 | Melbourne | 0.44 | 415.89 | — |
| europe-central2 | Warsaw | 0.81 | 498.57 | — |
| europe-north1 | Finland | 0.98 | 29.84 | 1.10 |
| europe-north2 | Stockholm | 1 | 19.39 | — |
| europe-southwest1 | Madrid | 0.87 | 95.75 | — |
| europe-west1 | Belgium | 0.79 | 126.43 | 1.08 |
| europe-west10 | Berlin | 0.7 | 275.81 | — |
| europe-west12 | Turin | 0.79 | 202.03 | — |
| europe-west2 | London | 0.75 | 109.39 | — |
| europe-west3 | Frankfurt | 0.7 | 275.81 | — |
| europe-west4 | Eemshaven | 0.82 | 194.35 | 1.07 |
| europe-west5 | N/A | 0.7 | 275.81 | — |
| europe-west6 | Zürich | 0.97 | 21.2 | — |
| europe-west8 | Milan | 0.79 | 202.03 | — |
| europe-west9 | Paris | 0.96 | 15.83 | — |
| me-central1 | Doha | 0 | 370 | — |
| me-central2 | Dammam | 0.01 | 381.29 | — |
| me-west1 | Tel Aviv | 0.13 | 380.95 | — |
| northamerica-northeast1 | Montréal | 0.97 | 11.36 | — |
| northamerica-northeast2 | Toronto | 0.8 | 74.2 | — |
| northamerica-south1 | Mexico | 0.25 | 293.25 | — |
| southamerica-east1 | Sāo Paulo | 0.87 | 73.25 | — |
| southamerica-west1 | Santiago | 0.9 | 209.94 | 1.08 |
| us-central1 | Iowa | 0.88 | 431.95 | 1.11 |
| us-central2 | Oklahoma | 0.84 | 417.39 | — |
| us-east1 | South Carolina | 0.31 | 579.44 | 1.09 |
| us-east2 | Georgia | 0.42 | 391.2 | — |
| us-east4 | Northern Virginia | 0.57 | 343.48 | 1.08 |
| us-east5 | Columbus | 0.57 | 343.48 | 1.06 |
| us-east7 | Alabama and Tennessee | 0.58 | 339.89 | — |
| us-south1 | Dallas | 0.83 | 299.13 | 1.10 |
| us-west1 | Oregon | 0.83 | 97.85 | 1.10 |
| us-west2 | Los Angeles | 0.66 | 149.91 | — |
| us-west3 | Salt Lake City | 0.36 | 567.51 | — |
| us-west4 | Las Vegas | 0.65 | 360 | 1.09 |

**New regions in 2025** (no prior row, so no carry-forward): `asia-southeast3` (Bangkok), `us-central2`
(Oklahoma), `us-east7` (Alabama and Tennessee) and `europe-west5` (location given as "N/A" by Google; its
CFE/grid values are identical to the German regions, so `em-zone-id` is set to `DE` as an inference —
flagged). `cfe-region`/`em-zone-id` were set from the grid (Thailand/TH, SPP/US-CENT-SWPP, TVA/US-TEN-TVA);
geolocation is city-level following the dataset convention (Bangkok, Oklahoma City, Chattanooga for the
TVA region; blank for `europe-west5`); `wt-region-id` is blank for the three US/unknown ones and needs a
WattTime lookup. `me-central1` (Doha) returns after a gap and carries forward its 2023 metadata.

## Fleet / global figures (context, not merged per-region)
- Average annual fleet-wide PUE: **1.09** for 2025 (flat vs 2024).
- Achieved ≥80% CFE across 9 of 22 grid regions (report narrative).
- 100% annual renewable-energy match (company-wide, market-based).

## Metrics with no home in the RTC schema
- Water by location in million gallons (withdrawal / discharge / consumption) — not L/kWh WUE.
- Compute Carbon Intensity (CCI) of AI accelerator hardware (gCO₂e/FLOP); TPU lifecycle emissions.

## Notes & caveats
- The PUE values are per **datacenter location** from the report's efficiency table (p.94), mapped to
  the region with a Google-owned datacenter. Multi-facility metros (Singapore, Council Bluffs, The
  Dalles, Loudoun) are represented by the primary facility.
- Per issue #151, do **not** put the 100% annual match in `provider-cfe-annual`; the per-region
  hourly value belongs in `provider-cfe-hourly`. For 2025 `provider-cfe-annual` is blank for every region and
  `provider-cfe-hourly` was verified equal to the source `Google CFE` column (0 mismatches across 47 regions).
