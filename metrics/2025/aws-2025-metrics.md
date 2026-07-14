# AWS (Amazon Web Services) — 2025 sustainability metrics

**Sources:** 2025 Amazon Sustainability Report; the **30 per-region/country sustainability fact sheets**
at `https://sustainability.aboutamazon.com/aws-sustainability-fact-sheets/aws-fact-sheet-<location>.pdf`
(32 files incl. French/Japanese language duplicates — all processed individually for this doc); the
PUE/WUE table on `.../products-services/aws-cloud#increasing-efficiency` (issue #158). Published July 2026.
**Reporting period:** **Calendar year 2025 (Jan 1 – Dec 31 2025)** — every fact sheet states PUE/WUE are
"for data centers operated by AWS between January 1 and December 31 of each year."
**Coverage boundary:** data centers **operated by AWS** (owned + leased under operational control).

## Metric definitions (quoted)
| Metric | AWS definition (verbatim) | Period | Method | RTC column | Merge? |
|---|---|---|---|---|---|
| PUE | *"Power Usage Effectiveness (PUE) … for data centers operated by AWS between January 1 and December 31 of each year"* | CY2025 | per-region annual average (regional average for newer/smaller regions) | `power-usage-effectiveness` | yes |
| WUE | *"Water Usage Effectiveness (WUE), in liters per kilowatt-hour … between January 1 and December 31 of each year"* | CY2025 | per-region annual, L/kWh | `water-usage-effectiveness` | yes |
| Water withdrawn | *"In 2025, AWS withdrew N litres of water in <place>"* | CY2025 | per country/region, litres | `total-water-input` | **candidate** — see notes |
| Renewable / carbon-free energy | 100% electricity matched with renewable for the 3rd year; per-grid list of within-grid-matched regions; "700+ CFE projects in 28 countries, 40+ GW" | CY2025 | market-based; per-grid 100% list | `provider-carbon-intensity-market-annual` (0 for listed regions) | partial |
| Energy-management certification | ISO 50001 + ISO 14001; conformance to the EU Code of Conduct on Data Centre Energy Efficiency | CY2025 | per-region (EU) | — | no schema home |
| Water-positive progress | *"committed to being water positive by 2030"; "75% of the way towards this goal" (global, end-2025)* | CY2025 | global | — | no schema home |

## Per-region values (CY2025)
PUE / WUE (L/kWh) / water withdrawn (litres, 2025) / market (0 = on AWS within-grid 100% list).

| region | PUE | WUE | water withdrawn 2025 (L) | market |
|---|---|---|---|---|
| us-east-1 (N. Virginia) | 1.15 | 0.06 | 996,204,576 | 0 |
| us-east-2 (Ohio) | 1.12 | 0.06 | 354,492,504 | 0 |
| us-west-1 (N. California) | 1.18 | 0.39 | 154,160,322 | 0 |
| us-west-2 (Oregon) | 1.12 | 0.12 | 914,350,635 | 0 |
| ca-central-1 (Canada Central) | 1.19 | 0.06 | 11,387,528 | 0 |
| ca-west-1 (Calgary) | 1.13 | 0.04 | 5,475,963 | — |
| sa-east-1 (São Paulo) | 1.14 | 0.09 | — | — |
| eu-central-1 (Frankfurt) | 1.24 | 0.17 | 416,264,483 | 0 |
| eu-west-1 (Ireland) | 1.10 | 0.02 | 108,902,681 | 0 |
| eu-west-2 (London) | 1.23 | 0.14 | ~303,000,000 | 0 |
| eu-west-3 (Paris) | 1.35 | — | 74,171,703 | 0 |
| eu-south-2 (Spain) | 1.06 | 0.12 | 68,000,000 (Aragón) | 0 |
| eu-north-1 (Stockholm) | 1.09 | 0.02 | 6,358,737 | 0 |
| eu-south-1 (Milan) | **1.11** (Europe avg) | 0.05 (Europe avg) | 65,611 (Italy) | 0 |
| eu-central-2 (Zurich) | **1.11** (Europe avg) | 0.05 (Europe avg) | 1,884,803 | 0 |
| me-south-1 (Bahrain) | 1.33 | — | — | — |
| me-central-1 (UAE) | 1.25 | — | — | — |
| il-central-1 (Tel Aviv) | 1.27 | — | 10,571,203 | — |
| af-south-1 (Cape Town) | 1.19 | — | 9,506,756 | — |
| ap-south-1 (Mumbai) | 1.40 | — | 383,567,863 | 0 |
| ap-south-2 (Hyderabad) | 1.43 | — | 56,061,382 | 0 |
| ap-southeast-1 (Singapore) | 1.30 | 1.57 | 1,796,931,761 | — |
| ap-southeast-2 (Sydney) | 1.14 | 0.10 | — | — |
| ap-southeast-3 (Jakarta) | 1.29 | 2.85 | 405,720,604 | — |
| ap-southeast-4 (Melbourne) | 1.07 | 0.06 | — | — |
| ap-northeast-1 (Tokyo) | 1.25 | 1.22 | 735,963,932 (Japan) | 0 |
| ap-northeast-2 (Seoul) | **1.25** (APAC avg) | 1.10 (APAC avg) | 620,248,091 (S. Korea) | — |
| ap-northeast-3 (Osaka) | 1.46 | — | *(incl. in Japan)* | 0 |
| ap-southeast-5 (Malaysia) | **1.25** (APAC avg) | 1.10 (APAC avg) | 47,989,045 | — |
| ap-southeast-6 (New Zealand) | **1.25** (APAC avg) | 1.10 (APAC avg) | 36,902 | — |
| ap-southeast-7 (Bangkok) | 1.38 | — | 7,574,300 | — |
| cn-northwest-1 (Ningxia) | 1.25 | — | — | 0 |

**Regional-average fallbacks** — AWS does **not** publish an individual PUE/WUE for every region. Newer or
smaller regions show a regional average instead: **AWS Europe** 1.11 / WUE 0.05 (Milan, Zurich);
**AWS Asia Pacific (Average / excl. China)** 1.25 / WUE 1.10 (Seoul, Malaysia, New Zealand); **AWS North
America (Average) design** PUE 1.14 / WUE 0.08 (US locations without a named region — Georgia, Indiana).

## Carbon-free energy — per-region highlights (from the fact sheets)
Global framing on every sheet: BloombergNEF-recognised largest corporate CFE purchaser; **700+ CFE
projects across 28 countries, 40+ GW** capacity; 100% renewable match for the 3rd year.
- **Australia** — 9 new PPAs (430 MW, Apr 2026, mostly solar+BESS); 20 projects underway ≈990 MW.
- **Canada** — Buffalo Plains Wind Farm (Alberta, 400+ MW, first Canadian wind); first on-site solar rooftop (Nisku).
- **Germany** — long-term RWE agreement, 110 MW from Nordseecluster B; all DCs ISO 50001/14001.
- **Ireland** — 6 wind farms (373 MW); first unsubsidised corporate PPA in Ireland; Tallaght district-heating from DC waste heat.
- **India** — 1.1 GW purchased to date; 100 MW CleanMax Koppal, 99 MW BluPine Solapur, 180 MW JSW Dharapuram.
- **Italy** — 40 projects (8 offsite solar incl. agrivoltaics + 32 rooftop); 3 new operational in 2025.
- **Japan** — 25 solar projects (>320,000 MWh); 35 MW Fukushima, 10 MW × Hokkaido/Yamaguchi.
- **Ohio** — 24 wind/solar (2.7 GW); Yellowbud 274 MW solar; ~$1.6 B local investment.
- **Singapore** — 2 renewable projects (~20,000 homes); 17.6 MW Sembcorp ground-mount solar.
- **Spain** — 100 projects (3.8 GW once operational), 17 in Aragón.
- **Sweden** — 5 utility-scale wind farms (~786 MW, ~250,000 households).
- **UK** — 40+ projects (~850,000 households); largest corporate CFE purchaser in Europe/UK.
- **Indiana** — first-of-its-kind NIPSCO framework, up to 3 GW new generation.
- **Oregon** — hydro-heavy grid + on-site solar & a wind farm.
- **Switzerland** — Graviton instances up to 60% less energy; workload migration saves up to 1,079 tCO₂/MW/yr.

## Energy efficiency & certifications
- Global PUE **1.14** (2025), vs 1.25 public-cloud and 1.63 on-prem averages cited.
- EU regions (France, Germany, Spain, Switzerland, Italy) — data centers **ISO 50001 (energy) + ISO
  14001 (environment) certified**, conforming to the **2025 EU Code of Conduct on Data Centre Energy
  Efficiency**. France cites Article L.236-3(V) of the French Energy Code.
- Cooling: Spain ~90% free-air cooling; Ireland no water for cooling >95% of the year; several US regions
  moving to direct-evaporative or reclaimed/recycled water (California −85% water via direct evaporative).

## Water stewardship (energy/water metric detail)
- Global WUE series: 2021 0.25 → 2022 0.19 → 2023 0.18 → 2024 0.15 → **2025 0.12**.
- **Per-region 2025 water withdrawal volumes** captured in the table above (from each fact sheet's
  "In 2025, AWS withdrew N litres…" line).
- Water-positive by 2030: **75% of the way as of end-2025** (global); India targets water-positive by 2027.
- Singapore uses 100% NEWater (reclaimed) — zero potable freshwater for cooling.

## Metrics with no home in the RTC schema
- Water-positive % progress; water-replenishment project volumes (litres/year returned); embodied/lifecycle
  carbon; circular-economy; ISO/EU-CoC certification status; Graviton/custom-silicon efficiency claims.

## Merge notes & caveats
- **`total-water-input` — merged.** AWS's per-region 2025 water withdrawal (litres) is now saved to
  `total-water-input` on the AWS 2025 rows. Boundary handling where the fact sheet's reporting unit
  (country) doesn't match a cloud region:
  - Single-region countries map directly (Thailand→ap-southeast-7 7,574,300 L; Germany→eu-central-1, etc.).
  - Multi-region countries reported **separately** map per region (India: Mumbai 383,567,863 / Hyderabad
    56,061,382; Canada: Montreal 11,387,528 / Calgary 5,475,963).
  - **Japan is reported combined** ("in Japan", 735,963,932 L across Tokyo + Osaka). Osaka's WUE is
    undisclosed (blank), indicating minimal separately-reported water, so the combined figure is
    **allocated to Tokyo (ap-northeast-1)** and Osaka (ap-northeast-3) is left blank to avoid
    double-counting — flagged for refinement if AWS discloses per-region.
  - To save water for regions AWS discloses but that had no 2025 row, **5 rows were added**: Milan
    (eu-south-1), Zurich (eu-central-2), Seoul (ap-northeast-2) from prior metadata, and the new
    Malaysia (ap-southeast-5) and New Zealand (ap-southeast-6) regions with geocoded city-level
    locations + Electricity Maps zones (MY-WM, NZ-NZN; grid carbon pending an EM lookup).
- **Regional-average PUE/WUE left blank** on those 5 added rows: AWS gives them only a regional-average
  PUE (Europe 1.11 / APAC 1.25), not a measured per-region value, so those cells are left blank rather
  than implying a per-region figure. The averages are recorded above for reference.
- Market carbon: 16 regions on AWS's within-grid 100% list (`0`); rest blank — per-grid matching, not the global claim.
- AWS restated/blanked some earlier-year values on the live page; historical rows left as recorded.
