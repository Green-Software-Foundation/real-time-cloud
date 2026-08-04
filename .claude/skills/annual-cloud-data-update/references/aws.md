# AWS (Amazon Web Services)

**Cadence:** Amazon publishes its sustainability report ~July; the report covers the prior calendar
year. Tracking issue is usually where the extracted PUE/WUE table gets pasted (e.g. #158 for the
2025 report).

## Sources
- **Per-region sustainability fact sheets (the primary source — download and process all of them):**
  the AWS cloud page links **~32 per-region PDF fact sheets** at
  `https://sustainability.aboutamazon.com/aws-sustainability-fact-sheets/aws-fact-sheet-<location>.pdf`.
  Discover the current list by fetching
  `https://sustainability.aboutamazon.com/products-services/aws-cloud` and grepping the HTML for
  `aws-fact-sheet-[a-z-]+\.pdf` (a couple are language variants like `-france-french`, `-japan-japanese`
  — same data). Download each and extract with `pdfplumber`. Page 1 of each carries a
  `AWS <Region> 20XX 20XX 20XX` table with **Average PUE** and **Average WUE (L/kWh)** per year, plus
  the metric definition (quote it — e.g. *"Power Usage Effectiveness (PUE) and Water Usage
  Effectiveness (WUE), in liters per kilowatt-hour, for data centers operated by AWS between January 1
  and December 31 of each year"*) and per-region carbon-free-energy / water / embodied-carbon narrative.
  Process each fact sheet individually into the `aws-<year>-metrics.md` summary (one row per region +
  the shared definitions). Fact-sheet file name → AWS region: they're named by *location*
  (virginia, ohio, oregon, california, ireland, frankfurt via germany, etc.), so map location→region
  using the friendly-name table below.
- **PUE + WUE per region (cross-check):** the popup table on the same page under `#increasing-efficiency`
  (columns `PUE 2022 | PUE 2023 | PUE 2024 | PUE 2025 | WUE 2024 | WUE 2025`) usually matches the fact
  sheets and is what gets pasted into the tracking issue. Use it to sanity-check the fact-sheet
  extraction. **Do not** rely on `code/aws-data-update.py`: it scrapes this popup and has mislabelled
  PUE as WUE in the past.
- **Metric methodology:** `https://sustainability.aboutamazon.com/pue-methodology.pdf` and
  `renewable-energy-methodology.pdf` for the full definitions to cite in the metrics doc.
- **Global figures** (for the README / sanity checks): the report states global PUE and a global WUE
  series, and that Amazon "matched 100% of electricity with renewable energy" for N years running.

## Columns to populate
- `power-usage-effectiveness` — per-region PUE for the new year, where the table shows one. Blank if
  the table shows `--` for that region/year.
- `water-usage-effectiveness` — per-region WUE for the new year, where shown. Note AWS historically
  used a single global WUE (e.g. 0.18) applied to all regions; newer years give real per-region WUE
  and blanks. Use exactly what the table shows; don't carry the old global default into a new year.
- `provider-carbon-intensity-market-annual` — **per region**, carried forward from the region's most
  recent prior year. AWS names a specific set of regions where it matches energy *within the grid*
  (100% renewable); those regions have `0` and the rest are blank. This is legitimate per-region data
  — keep the per-region pattern, never a uniform `0` across all regions.
- `total-water-input` — each fact sheet states a per-region annual water **withdrawal** ("In 20XX, AWS
  withdrew N litres of water in <place>"); convert gallons→litres where needed. Boundary handling: map
  single-region countries directly; where a country has several regions reported **separately** (India:
  Mumbai/Hyderabad) use each; where **combined** (Japan = Tokyo+Osaka together) allocate to the primary
  region and leave the other blank, documenting the interpolation.
- **Regional-average fallback** — AWS does not give every region an individual PUE/WUE. Newer/smaller
  regions show a regional average instead (**AWS Europe** ~1.11 for Milan, Zurich; **AWS Asia Pacific**
  ~1.25 for Seoul, Malaysia, New Zealand; **AWS North America design** ~1.14/0.08 for US locations
  without a named region). Prefer leaving the per-region PUE/WUE **blank** rather than writing the
  regional average into a per-region cell (record the average in the metrics doc); still add the row so
  its water/grid data is captured.
- Carry forward `cfe-region`, `em-zone-id`, `wt-region-id`, `location`, `geolocation`, and grid
  carbon intensity from the prior year's row.

## Region friendly-name → region-code map
```
Europe (Frankfurt) eu-central-1     Europe (Ireland) eu-west-1        Europe (London) eu-west-2
Europe (Paris) eu-west-3            Europe (Spain) eu-south-2         Europe (Stockholm) eu-north-1
Europe (Milan) eu-south-1          Europe (Zurich) eu-central-2      Middle East (Bahrain) me-south-1
Middle East (Tel Aviv) il-central-1 Middle East (UAE) me-central-1   Africa (Cape Town) af-south-1
Asia-Pacific (Bangkok) ap-southeast-7*  Asia-Pacific (Hyderabad) ap-south-2  Asia-Pacific (Jakarta) ap-southeast-3
Asia-Pacific (Melbourne) ap-southeast-4  Asia-Pacific (Mumbai) ap-south-1    Asia-Pacific (Osaka) ap-northeast-3
Asia-Pacific (Singapore) ap-southeast-1  Asia-Pacific (Sydney) ap-southeast-2  Asia-Pacific (Tokyo) ap-northeast-1
Asia-Pacific (Hong Kong) ap-east-1  Asia-Pacific (Seoul) ap-northeast-2  China (Ningxia) cn-northwest-1
China (Beijing) cn-north-1         South America (Sao Paulo) sa-east-1  Canada (Central) ca-central-1
Canada (West) ca-west-1            U.S. East (Northern Virginia) us-east-1  U.S. East (Ohio) us-east-2
U.S. West (Northern California) us-west-1  U.S. West (Oregon) us-west-2  GovCloud (US East) us-gov-east-1
GovCloud (US West) us-gov-west-1
```
`*` A friendly name with **no existing row** in the dataset is a **new region** (AWS adds several each
year — e.g. Bangkok `ap-southeast-7` launched early 2025). New regions have no prior metadata to carry
forward, so add them fresh: geocode a **city-level geolocation** (e.g. `geopy` Nominatim on the city
name → `13.7525,100.4935` for Bangkok), set `cfe-region` to the country/grid and `em-zone-id` to the
Electricity Maps zone (`TH` for Thailand), fill the disclosed PUE/WUE, and leave `wt-region-id` and grid
carbon intensity blank with a note that they need a WattTime / Electricity Maps lookup. Don't skip a
new region just because grid data isn't available yet — add it with what's known.

## Gotchas
- Only add rows for regions the table actually discloses for the new year. AWS restates and blanks
  older years on the live page — leave the historical rows alone (rule 1).
- 100%-renewable ≠ every region has `market = 0`; it's the specific per-grid list. Carry the prior
  year's per-region market value forward rather than reasoning it out afresh.
