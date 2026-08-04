# Gaps-report template (`metrics/<year>/gaps-<year>.md`)

One shared report per year, built from the per-vendor metrics docs. Its purpose is the project's core
mission: show where the providers' metrics *aren't comparable* and say concretely what each should
change so a customer could compare regions across clouds on a like-for-like basis. Be specific and
even-handed — name the exact definitional difference, not a vague "they should do better".

```markdown
# Cross-vendor metric alignment gaps — <year>

Comparability assessment of AWS, Google Cloud, Microsoft Azure, and Oracle Cloud sustainability
metrics for <year>, against the Cloud Region Metadata schema. Built from the per-vendor metrics docs
in this folder.

## Metric-by-metric comparison
For each metric: how each vendor defines/reports it, and the resulting incomparability.

### Power Usage Effectiveness (PUE)
| Vendor | Reports? | Granularity | Period | Boundary | Definitional notes |
|---|---|---|---|---|---|
| AWS | yes | per-region | Jan–Dec | operated DCs | … |
| Google | yes | per-datacenter (→region) | annual | owned+operated | … |
| Azure | partial | macro-region only | fiscal yr | … | no per-region since 2022 |
| Oracle | yes | per-region | 12-mo rolling, ~88% sites | … | … |
**Gap → ask:** <e.g. "Azure and Oracle should publish per-region, calendar-year PUE for operated
datacenters to match AWS/Google.">

### Water Usage Effectiveness (WUE)
(same structure — note who doesn't publish it at all, e.g. Google reports water in gallons not L/kWh)

### Carbon-free / renewable energy
Distinguish **location-based, per-region, hourly** (Google CFE) from **market-based, annual, matched**
(AWS/Azure/Oracle 100% claims that net across unconnected grids). This is the biggest comparability
gap — state clearly which vendors publish a physically-meaningful per-region figure and which only
publish a market claim.
**Gap → ask:** <e.g. "AWS/Azure/Oracle should publish per-region, location-based, ideally hourly
carbon-free-energy percentages like Google, rather than only a global market-matched claim.">

### Grid carbon intensity / market carbon intensity
(who provides per-region location-based grid data vs relies on third parties; per-grid market lists)

### Reporting period & boundary
The most-overlooked comparability gap. AWS and Google report **calendar year** (Jan 1 – Dec 31), while
**Azure (FY Jul 1 – Jun 30) and Oracle (FY Jun 1 – May 31) report fiscal years that end in the middle
of the calendar year.** So an Azure/Oracle "2025" figure covers roughly H2-2024 + H1-2025 and ends
~mid-2025 — it is *not* the same window as an AWS/Google "2025" figure. State each vendor's exact
period, and make explicit that the per-year columns in the merged table align fiscal→calendar only
nominally. Also cover: operated vs owned+leased boundary; % of sites covered; rolling-12-month vs
annual PUE. **Gap → ask:** vendors on fiscal reporting should additionally disclose calendar-year
figures (or clearly state the period) so cross-cloud, same-year comparisons are like-for-like.

### Metrics published by some vendors with no common schema home
Oracle tCO₂e/$USD, embodied carbon, GHG-by-region, etc. — note whether the schema should grow to
capture them.

## Summary of recommendations per vendor
- **AWS:** …
- **Google:** …
- **Azure:** …
- **Oracle:** …

## Year-over-year
What improved or regressed in comparability since last year's gaps report.
```

## Recurring gaps to check every year
- **Fiscal vs calendar year** — Azure and Oracle report fiscal; note the mapping and its distortion.
- **PUE boundary/coverage** — operated vs owned, % of sites, 12-month-rolling vs Jan–Dec.
- **WUE availability** — Google doesn't publish L/kWh WUE; Azure only macro-regional.
- **Location vs market CFE** — the central gap; only Google gives per-region location-based CFE.
- **Per-region vs macro/fleet** — Azure stopped per-region PUE/WUE after 2022.
- **Per-region grid carbon** — most rely on Electricity Maps/WattTime rather than publishing their own.
