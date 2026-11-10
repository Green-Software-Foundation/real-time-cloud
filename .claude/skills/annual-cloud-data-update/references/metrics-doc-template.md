# Metrics-doc template (`metrics/<year>/<vendor>-<year>-metrics.md`)

One per vendor per year. Goal: a self-contained record of *what the vendor published and how they
define it*, so the merge decisions are traceable and the gaps report can be written without re-reading
the PDFs. Quote definitions verbatim — paraphrasing loses the incomparability that this project exists
to surface.

Keep it factual; don't editorialise here (that's the gaps report's job). Do flag any metric that has
no schema home so the gaps report can pick it up.

```markdown
# <Vendor> — <year> sustainability metrics

**Sources:** <report title(s)> — <url(s)>, published <date>.
**Reporting period — state exact start/end dates, not just a year label:** e.g. `calendar year 2025
(Jan 1 – Dec 31 2025)`, or `FY2025 (Jul 1 2024 – Jun 30 2025)` for Azure, `FY2025 (Jun 1 2024 – May 31
2025)` for Oracle. Fiscal-year vendors **end mid-calendar-year**, so their "year N" is not the same
window as a calendar-year vendor's "year N" — this is a first-class comparability fact, capture it up
front. If different tables in the same report use different periods (e.g. calendar-year PUE but
fiscal-year emissions), note the period **per metric** in the table below.
Coverage boundary: <operated | owned+leased | % of sites | region set>.

## Metric definitions (quoted)
| Metric | Vendor's definition (verbatim) | Period | Method (location/market, hourly/annual, per-region/fleet) | RTC column | Merge? |
|---|---|---|---|---|---|
| PUE | "<quote>" | <Jan–Dec 20XX> | per-region, 12-mo … | power-usage-effectiveness | yes |
| WUE | "<quote>" | … | per-region, L/kWh | water-usage-effectiveness | yes |
| Carbon-free / renewable % | "<quote>" | … | <market, global> or <location, hourly, per-region> | provider-cfe-* / market | yes/no + why |
| <metric with no schema home> | "<quote>" | … | … | — | no — see gaps |

## Per-region values
| region-code | PUE | WUE | CFE/RE% | market carbon | grid carbon | notes |
|---|---|---|---|---|---|---|
| … | | | | | | |
(Only include what the vendor actually discloses; leave cells blank otherwise. Note where a value is
carried forward vs freshly disclosed.)

## Fleet / global figures (context, not merged per-region)
- Global PUE / WUE / renewable %: …

## Metrics with no home in the RTC schema
- <e.g. tCO₂e/$USD, embodied carbon, GHG-by-region, water in gallons> — recorded for the gaps report.

## Notes & caveats
- Restatements of prior years, coverage changes, fiscal-vs-calendar mismatch, ambiguous mappings, etc.
```
