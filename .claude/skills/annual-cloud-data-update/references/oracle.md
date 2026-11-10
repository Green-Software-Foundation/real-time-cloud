# Oracle Cloud Infrastructure (OCI)

**Cadence:** Oracle publishes the "Clean Cloud OCI Data Sheet" ~December, on a **fiscal year that runs
June 1 – May 31**; e.g. **FY2025 = Jun 2024 – May 2025** (ends mid-2025, not Dec 31). The sheet (Dec
2025) has FY2024 and FY2025 columns. Like Azure, Oracle's fiscal periods end mid-calendar-year, so its
"FY25" doesn't line up with AWS/Google calendar-2025 — map `FY(N) → year N` but record the exact window
(`Jun 2024–May 2025`) in the metrics doc and flag the offset in `gaps-<year>.md`. A separate, older CY
report carries the per-region PUE (which *is* calendar-year — note the mixed basis). Tracking issue: #86.
Provider name in the CSV: `Oracle Cloud Infrastructure`.

## Sources (three, joined on region identifier)
1. **Renewable-electricity % per region, FY24/FY25:**
   `https://www.oracle.com/a/ocom/docs/corporate/citizenship/clean-cloud-oci.pdf` — a per-region table
   grouped by continent, with `RE%` and a `tCO₂e/$USD` intensity metric (the latter has **no schema
   home** — ignore it). It also lists the 3-letter region key (IAD, FRA, NRT, …).
2. **CY PUE + RE% per region:** Oracle's CY sustainability report (the older one). This is the only
   source of Oracle per-region **PUE**.
3. **Electricity Maps grid mapping** (`cfe-region`, `em-zone-id`, `wt-region-id`, `geolocation`, grid
   carbon intensity): assembled in the project's OCI working data (a Google Sheet linked from #86,
   with an `IF Source` tab already in the 24-column schema and an `Oracle Cloud` tab holding RE%/PUE
   keyed by identifier). Export the sheet as xlsx (`.../export?format=xlsx`) and read with `openpyxl`.

Join all three on the OCI **region identifier**. The 3-letter key → identifier mapping comes from
Oracle's official list, `https://docs.oracle.com/en-us/iaas/Content/General/Concepts/regions.htm`.

## Columns to populate
- `provider-cfe-annual` — the per-region **renewable-electricity %** (as a 0–1 proportion). Oracle's
  RE% genuinely varies by region (0–100%), so it *is* legitimate per-region data — keep it here. (It
  is market-based matching, unlike Google's location-based hourly CFE; note that in the PR.)
- `power-usage-effectiveness` — CY per-region PUE, on the CY-year rows only. Oracle hasn't disclosed
  newer per-region PUE, so leave PUE blank on the FY-derived (2024/2025) rows rather than inventing it.
  Treat a PUE of `0` in the source as "not disclosed" (blank).
- `cfe-region`, `em-zone-id`, `wt-region-id`, `geolocation`, grid carbon intensity — from the
  Electricity Maps mapping (`IF Source`); carry the year-independent values across all years.
- `provider-carbon-intensity-market-annual` — leave **blank** (Oracle's 100% is market-based matching,
  the global-claim family; see rule 2). Unlike AWS, Oracle doesn't publish a per-grid within-grid list,
  so don't set market = 0.

## Region key → identifier examples
```
IAD us-ashburn-1   ORD us-chicago-1   PHX us-phoenix-1   SJC us-sanjose-1
YUL ca-montreal-1  YYZ ca-toronto-1   GRU sa-saopaulo-1  VCP sa-vinhedo-1  SCL sa-santiago-1
FRA eu-frankfurt-1 CDG eu-paris-1     LHR uk-london-1    CWL uk-cardiff-1  AMS eu-amsterdam-1
NRT ap-tokyo-1     KIX ap-osaka-1     SIN ap-singapore-1 SYD ap-sydney-1   ICN ap-seoul-1
```
Gov/DoD identifiers aren't in the commercial list; from the working sheet:
`RIC us-gov-ashburn-1, PIA us-gov-chicago-1, TUS us-gov-phoenix-1, LFI us-langley-1,
LUF us-luke-1, LTN uk-gov-london-1, BRS uk-gov-cardiff-1`.

## Gov / DoD regions
Include them if the user wants them. They have RE%/PUE but no Electricity Maps zone in the working
data — assign each the grid zone + carbon intensity of the **co-located commercial region** in the
same metro (they share the physical grid): `us-gov-ashburn-1`/`us-langley-1` ← `us-ashburn-1`,
`us-gov-chicago-1` ← `us-chicago-1`, `us-gov-phoenix-1`/`us-luke-1` ← `us-phoenix-1`,
`uk-gov-london-1` ← `uk-london-1`, `uk-gov-cardiff-1` ← `uk-cardiff-1`.

## Gotchas
- Fiscal year (Jun–May) mapped FY24→2024, FY25→2025 — state the caveat.
- Regions where FY24 RE% is `N/A` (not yet active) get no 2024 row; only add years the sheet covers.
- Regions in Oracle's data but not resolvable to an identifier (e.g. a Dallas or Salt Lake City entry
  with no key, or the Canberra dedicated region with no RE%/PUE) — skip and note for the user.
