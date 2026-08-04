# Microsoft Azure — 2025 sustainability metrics

**Sources:** Microsoft datacenter efficiency page
`https://datacenters.microsoft.com/sustainability/efficiency/`; 2026 Environmental Data Fact Sheet
`https://cdn-dynmedia-1.microsoft.com/is/content/microsoftcorp/microsoft/msc/documents/presentations/CSR/2026-Microsoft-Environmental-Data-Fact-Sheet-PDF.pdf`;
2026 Environmental Sustainability Report (issue #161, #112).
**Reporting period:** **Fiscal year — FY2025 = July 1 2024 – June 30 2025 (ends mid-2025)**, so this is
*not* a calendar-2025 window; it is roughly H2-2024 + H1-2025. Mapped `FY25→2025` for one column per year.
**Coverage boundary:** owned + operated datacenters; PUE/WUE reported at **macro-region** granularity
(Global, Americas, Asia Pacific, EMEA) — **no per-Azure-region disclosure since 2022**.

## Metric definitions (quoted / paraphrased)
| Metric | Microsoft definition | Period | Method | RTC column | Merge? |
|---|---|---|---|---|---|
| PUE | *"PUE is measured by dividing the total energy needed for a datacenter facility, by the total energy used for computing"* | FY25 | **macro-region** (Americas/APAC/EMEA), annual | `power-usage-effectiveness` | yes, but continent-mapped approximation |
| WUE | *"WUE is measured by dividing the annual liters of water used for humidification and cooling, by the total annual kilowatt hours (kWh) used to power IT equipment"* | FY25 | **macro-region**, L/kWh | `water-usage-effectiveness` | yes, continent-mapped |
| Renewable electricity | *"total direct renewable electricity (on-site generation, PPAs, green power products and other long-term contracts …, and the renewable portion of the grid mix) divided by Microsoft's total electricity consumption"* | FY25 | **market-based, global** | `provider-cfe-*` | **no** — global market claim |
| GHG emissions by region | Table 3, mtCO₂e by region | FY25 | market/location, per broad region | — | no direct column (context) |

## Values (FY2025, macro-regional)
| Scope | PUE | WUE (L/kWh) |
|---|---|---|
| Global | 1.17 | 0.27 |
| Americas | 1.16 | 0.34 |
| Asia Pacific | 1.28 | 0.25 |
| EMEA | 1.16 | 0.03 |

FY2024 comparison: Global 1.16 / 0.30; Americas 1.16 / 0.38; Asia Pacific 1.25 / 0.03; EMEA 1.16 / 0.03.

**Merge:** each Azure region is assigned its continent's macro value (Americas / APAC / EMEA). This is
coarser than the per-region PUE values Azure published through 2022, and mixes a fiscal-year period into
a calendar-year-labelled column — both recorded as approximations.

Renewable electricity (direct, %): FY20 – → FY24 78% → **FY25 100%** (market-based; not merged as CFE).

## Metrics with no home in the RTC schema
- GHG emissions by scope / type / region (mtCO₂e); waste & circularity; land; total energy consumption (MWh).

## Notes & caveats
- **Timescale is the headline caveat:** FY periods end June 30, so Azure "2025" ≠ calendar-2025.
- No per-region PUE/WUE since 2022; the continent mapping is the best available and should be flagged
  wherever the Azure rows are consumed.
- Microsoft applies a "metrics recalculation policy" that can restate prior years — watch for changes.
