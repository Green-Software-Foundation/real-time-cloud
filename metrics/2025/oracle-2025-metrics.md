# Oracle Cloud Infrastructure (OCI) — 2025 sustainability metrics

**Sources:** Oracle Clean Cloud OCI Data Sheet, Fiscal Year 2025 Results (Dec 2025) —
`https://www.oracle.com/a/ocom/docs/corporate/citizenship/clean-cloud-oci.pdf`; Oracle CY2023
sustainability report (per-region PUE); Electricity Maps working data (issue #86).
**Reporting period:** **Mixed basis** — the renewable-electricity % is **fiscal year, FY2025 = Jun 1
2024 – May 31 2025 (ends mid-2025)**; the per-region **PUE is calendar-year CY2023** (Oracle has not
published newer per-region PUE). Mapped `FY25→2025`.
**Coverage boundary:** "all revenue-generating regions during the fiscal period"; PUE is "12-month
rolling data as reported by approximately 88% of sites on a weighted-average basis."

## Metric definitions (quoted)
| Metric | Oracle definition (verbatim / paraphrased) | Period | Method | RTC column | Merge? |
|---|---|---|---|---|---|
| Renewable Electricity (RE%) | percentage of a region's electricity matched with renewable/carbon-free sources | FY25 | **market-based match**, per region, annual | `provider-cfe-annual` | yes — per-region, varies 0–100% |
| PUE | *"12 month rolling data as reported by approximately 88% of sites on a weighted average basis"* | CY2023 | per-region, rolling-12-mo, ~88% coverage | `power-usage-effectiveness` | yes (2023 rows only) |
| tCO₂e/$USD | *"emissions intensity based on spend in USD (Oracle Scope 1 and Scope 2 emissions divided by revenue)"* | FY25 | per-region intensity-per-revenue | — | **no schema home** |

## Per-region values (RE% FY2024 → FY2025; PUE = CY2023)
Selected — full set is 47 regions (40 commercial + 7 US/UK gov/DoD). RE% as %; market column left blank
(Oracle's 100% is a market-based match, not a per-grid within-grid list).

| region | RE% FY24 | RE% FY25 | PUE (CY2023) |
|---|---|---|---|
| us-ashburn-1 | 95 | 100 | 1.34 |
| us-chicago-1 | 99 | 100 | 1.33 |
| us-phoenix-1 | 99 | 100 | 1.37 |
| us-sanjose-1 | 100 | 100 | 1.24 |
| eu-frankfurt-1 | 100 | **84** | 1.30 |
| eu-jovanovac-1 (Serbia) | 100 | **40** | 1.71 |
| uk-london-1 | 100 | 100 | 1.36 |
| sa-saopaulo-1 | 100 | 100 | 1.60 |
| ap-tokyo-1 | 1 | 2 | 1.38 |
| ap-osaka-1 | 0 | **51** | 1.38 |
| ap-sydney-1 | 0 | 0 | 1.30 |
| ap-melbourne-1 | 0 | **49** | 1.39 |
| ap-seoul-1 | 36 | 43 | 1.60 |
| ap-chuncheon-1 | 100 | **1** | 1.30 |

Notable: RE% **regressed** in several regions FY24→FY25 (Frankfurt 100→84, Serbia 100→40, S. Korea
North 100→1) while others improved (Osaka 0→51, Melbourne 0→49).

## Fleet / global figures (context)
- Total renewable electricity: FY24 88% → FY25 92%. By macro-region FY25: N. America 100%, Latin
  America 96%, Europe 92%, MEA 41%, Asia Pacific 19%.

## Metrics with no home in the RTC schema
- `tCO₂e/$USD` emissions intensity (per region); site certifications (ISO 14001/50001, LEED, etc.).

## Notes & caveats
- **Mixed timescale:** RE% is fiscal (ends May 2025), PUE is calendar CY2023 — a region's row combines
  two different periods.
- RE% is a market-based renewable match (excludes the nuclear nuance in Google's location-based CFE).
- 7 gov/DoD regions have RE%/PUE but no native Electricity Maps zone — they inherit the grid zone +
  carbon intensity of the co-located commercial region.
- Not included: Canberra dedicated region (no RE%/PUE) and Dallas / Salt Lake City (no identifier).
