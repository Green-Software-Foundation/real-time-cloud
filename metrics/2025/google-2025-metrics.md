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
| Carbon-free energy (CFE) | *"the percentage of Google's electricity consumption on a given regional grid that is matched hourly with CFE"* (Contracted CFE + Consumed Grid CFE, hourly) | CY2025 | **location-based, per-region, hourly** | `provider-cfe-hourly` | yes — when published |
| PUE | *"a standard industry ratio that compares the amount of non-computing overhead energy … to the amount of energy used to power IT equipment"*; measured continuously across the whole owned+operated fleet | CY2025 | per-datacenter, annual | `power-usage-effectiveness` | yes (owned-DC regions) |
| Renewable energy (annual) | 100% annual renewable-energy match (electricity procured / consumed, netted across markets) | CY2025 | **market-based, global** | `provider-cfe-annual` | **no** — global market claim, not per-region |
| Grid carbon intensity | Electricity Maps consumption-based intensity per region | CY2025 | location-based, per-region | `grid-carbon-intensity-average-consumption-annual` | yes — when published |
| WUE | not reported as L/kWh (water reported in million gallons by location) | CY2025 | — | — | no — not provided |

## Per-region values (CY2025)
| region | hourly CFE | grid carbon | PUE | note |
|---|---|---|---|---|
| asia-east1 | *(pending)* | *(pending)* | 1.13 | Changhua, Taiwan |
| asia-northeast1 | pending | pending | 1.12 | Inzai, Japan |
| asia-southeast1 | pending | pending | 1.12 | Singapore |
| europe-north1 | pending | pending | 1.10 | Hamina, Finland |
| europe-west1 | pending | pending | 1.08 | St. Ghislain, Belgium |
| europe-west4 | pending | pending | 1.07 | Eemshaven, Netherlands |
| southamerica-west1 | pending | pending | 1.08 | Quilicura, Chile |
| us-central1 | pending | pending | 1.11 | Council Bluffs, Iowa |
| us-east1 | pending | pending | 1.09 | Berkeley County, SC |
| us-east4 | pending | pending | 1.08 | Loudoun County, VA |
| us-east5 | pending | pending | 1.06 | Columbus, OH |
| us-south1 | pending | pending | 1.10 | Midlothian, TX |
| us-west1 | pending | pending | 1.10 | The Dalles, OR |
| us-west4 | pending | pending | 1.09 | Henderson, NV |

**"pending" = not yet published for CY2025.** Google's per-region hourly CFE and grid carbon intensity
come from the `region-carbon-info` dataset, which as of this update **stops at 2024** — the CY2025
figures are not in the machine-readable source or the report, only the fleet-wide numbers below. These
columns are intentionally left blank in the merge and will be filled when Google publishes the 2025 CSV.

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
  hourly value belongs in `provider-cfe-hourly`. For 2025 both remain pending.
