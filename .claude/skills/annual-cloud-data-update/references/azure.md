# Microsoft Azure

**Cadence:** Microsoft publishes its Environmental Sustainability Report ~May. Tracking issues: #161, #112.

## Timescale — read this before mapping any year
Microsoft reports on a **fiscal year that runs July 1 – June 30**, so its periods **end in the middle
of the calendar year**, not at Dec 31:
- **FY2025 = July 1 2024 – June 30 2025** (ends mid-2025)
- **FY2024 = July 1 2023 – June 30 2024** (ends mid-2024)

This matters because AWS and Google report **calendar year** (Jan 1 – Dec 31). So Microsoft's "FY25"
and everyone else's "2025" cover **different windows** — FY25 is mostly H2-2024 + H1-2025. When you
merge Azure, map `FY(N) → calendar year N` (FY25→2025) to keep one column per nominal year, but this
is a **lossy approximation**: record the exact period (`Jul 2024–Jun 2025`) in `azure-<year>-metrics.md`
and call it out explicitly in `gaps-<year>.md` as a real comparability gap — a customer comparing a
2025 Azure region to a 2025 AWS region is comparing offset time periods. (Oracle has the same issue: its
fiscal year is Jun–May, also ending mid-year — see `oracle.md`.) Not every Microsoft table is fiscal in
the same way, and some figures may be stated on other bases, so capture the stated period for **each**
metric rather than assuming.

## The key constraint
Microsoft **stopped publishing per-Azure-region PUE/WUE after 2022** (the old datacenter fact sheets
were frozen in Dec 2024 with no new data — see the WG's conclusion on #112). What it does publish is
**macro-regional, fiscal-year** PUE and WUE for three buckets: Global, Americas, Asia Pacific, and
EMEA. That's the best available, so the project's approach (agreed with the user) is to **map each
macro-regional figure onto every Azure region by continent**.

## Sources
- **Efficiency page — the PUE/WUE numbers:** `https://datacenters.microsoft.com/sustainability/efficiency/`
  (and the annual report PDF) give the macro-regional PUE/WUE table below.
- **Environmental Data Fact Sheet — the definitions + detailed data:** the detailed data workbook
  PDF, e.g. `https://cdn-dynmedia-1.microsoft.com/is/content/microsoftcorp/microsoft/msc/documents/presentations/CSR/2026-Microsoft-Environmental-Data-Fact-Sheet-PDF.pdf`
  (bump the year each cycle). ~28 pages of tabulated metrics with methodology footnotes: GHG emissions
  by scope/type/**region** (Table 3), energy consumption, **renewable-energy metrics** (Table 6 —
  "Percentage of direct renewable electricity", e.g. FY24 78% → FY25 100%, with its full definition),
  water, waste, land. Use this for the metric definitions in `azure-<year>-metrics.md` and for the
  gaps report. Note it's **fiscal year** and the renewable % is a market-based global figure (rule 2)
  — don't merge it as per-region CFE; record it in the metrics doc and gaps report.

The efficiency page gives a table like:

| | FY-2 (→ year-2) | FY-1 (→ year-1) |
|---|---|---|
| Global | PUE / WUE | PUE / WUE |
| Americas | 1.16 / 0.38 | 1.16 / 0.34 |
| Asia Pacific | 1.25 / 0.03 | 1.28 / 0.25 |
| EMEA | 1.16 / 0.03 | 1.16 / 0.03 |

(Those numbers are the FY24/FY25 values; refresh them from the current page each year.)

## Columns to populate
- `power-usage-effectiveness`, `water-usage-effectiveness` — the macro-regional value for the region's
  continent, mapped `FY(N)` → calendar year `N`.
- Carry forward `cfe-region`, `em-zone-id`, `wt-region-id`, `location`, `geolocation`, and grid carbon
  intensity from the region's prior year.
- Leave `provider-cfe-*` blank (Microsoft's 100% CFE claim is the global market claim — see the main
  skill's rule 2). Leave `provider-carbon-intensity-market-annual` blank unless the user decides
  otherwise.

## Region → continent map
```
Americas: brazilsouth, centralus, eastus, eastus2, eastus3, mexicocentral, northcentralus,
          southcentralus, westcentralus, westus, westus3
Asia Pacific: asiapacific, australiaeast, australiasoutheast, indiasouthcentral, newzealandnorth,
          southeastasia, taiwannorth
EMEA: austriaeast, denmarkeast, greececentral, italynorth, northeurope, polandcentral, spaincentral,
          swedencentral, westeurope
```
(Derive the continent for any new region from its name/geography.)

## Gotchas
- The 2023 Azure rows carry *real per-region* PUE values (finer-grained than these macro averages).
  This continent mapping is deliberately coarser — flag it clearly in the PR as an approximation, and
  never overwrite the older per-region rows with it (rule 1).
- Fiscal-vs-calendar year: see the "Timescale" section above — FY periods end mid-year, so this is a
  real comparability gap, not a footnote. Record the exact `Jul–Jun` window per metric and flag it.
- One region may appear twice in the historical data (a known duplicate `northeurope`); when carrying
  metadata forward, dedupe by picking the most-populated prior row.
