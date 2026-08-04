---
name: annual-cloud-data-update
description: >-
  Update the real-time-cloud Cloud_Region_Metadata.csv with a new year of cloud-provider
  sustainability data (PUE, WUE, carbon-free / renewable energy %, grid carbon intensity)
  when AWS, Google, Microsoft Azure or Oracle publish their annual reports. Use this whenever
  the user wants to add or refresh a year of cloud region metadata, extract PUE/WUE/CFE from a
  provider sustainability report, reconcile a provider's disclosures into this dataset, or open
  the annual update PRs. Providers publish on a rolling schedule (Azure ~May, Google ~June,
  Amazon ~July, Oracle ~Dec), so this is typically run several times a year as each vendor lands.
---

# Annual cloud region metadata update

This repo (`Green-Software-Foundation/real-time-cloud`) normalises annual sustainability metadata
from the major cloud providers into one CSV, `Cloud_Region_Metadata.csv`, on the schema described
in `Cloud_Region_Metadata_specification.md`. Each year the providers publish a new year of data and
this file gets extended. This skill captures how to do that cleanly, because the work is fiddly and
several mistakes are easy to make and hard to spot.

Read this file, then read the per-provider reference for whichever vendor(s) you're updating:
`references/aws.md`, `references/google.md`, `references/azure.md`, `references/oracle.md`. The two
output docs have templates: `references/metrics-doc-template.md` and `references/gaps-report-template.md`.

## The two rules that matter most

**1. Additive only.** Never modify or delete a row for a year that's already published. Providers
sometimes *restate* older numbers or *blank* a value in a later snapshot — do not chase those into
the historical rows. A correct update has `removed: 0` in the diff check below. If the user asks to
fix an older year, do it as an explicit, separate decision, not as a side effect.

**2. Per-region physical data only — not the global market claim.** Most providers claim "100%
renewable/carbon-free" on a company-wide, market-based basis that nets purchases across grids that
aren't electrically connected. That claim is **not useful per-region** and must not populate the
carbon-free-energy columns. Specifically:
- `provider-cfe-hourly` / `provider-cfe-annual` are for *location-based, per-region* carbon-free
  energy. Only fill them with a genuine per-region figure (e.g. Google's hourly CFE, Oracle's
  per-region renewable %). Do **not** set a uniform `1.0` because the provider claims global 100%.
- `provider-carbon-intensity-market-annual` is the dedicated market column. It's acceptable to set
  it to `0` **only** where the provider publishes a genuine *per-region* 100% list (AWS matches
  energy within specific grids and names those regions). Carry that per-region, never as a uniform
  value.

When in doubt about whether a figure is per-region-physical or a global-market claim, leave it blank
and flag it for the user — a blank is honest, an invented number is not.

## Workflow: three phases

The work runs in three phases — **extract → merge → gaps** — because the value of this project isn't
just the merged table, it's making the providers' metrics *comparable*. If you jump straight to the
CSV you lose the definitions, and the definitions are where the incomparability hides (one vendor's
"PUE" is a 12-month rolling average across 88% of sites; another's is Jan–Dec for operated sites; a
"100% renewable" claim can be global-market or per-grid). So capture the definitions first, merge only
what genuinely fits the schema, and write up the gaps.

Outputs land in `metrics/<year>/`: one `<vendor>-<year>-metrics.md` per provider, and one shared
`gaps-<year>.md`.

### Phase A — Extract data *and definitions* into `<vendor>-<year>-metrics.md`
For each vendor, read the source report(s) (see the per-provider reference for exact URLs) and produce
a standalone Markdown doc that a reader could use *without* the original PDF. For every metric capture:
- **Metric** and the **value(s)** per region/scope, with units.
- **The vendor's own definition, quoted** (e.g. AWS: PUE/WUE "for data centers operated by AWS between
  January 1 and December 31 of each year"). Quote it verbatim — the definition is the point.
- **Reporting period — exact dates, not just a year label**: AWS and Google report calendar year
  (Jan–Dec); **Azure (FY Jul–Jun) and Oracle (FY Jun–May) report fiscal years that end mid-calendar-year**,
  so their "2025" ends ~mid-2025 and is a different window than a calendar-2025 figure. Also the
  boundary (operated vs owned+leased, % of sites covered, rolling-12-month vs annual). Record the exact
  period per metric — sometimes different tables in one report use different bases.
- **Method**: location-based vs market-based; hourly vs annual; per-region vs macro/fleet-wide.
- Anything that has **no home in the RTC schema** (e.g. Oracle's tCO₂e/$USD, AWS embodied carbon) —
  record it so the gaps report can note it.

Follow the standard `metrics-doc` template in `references/metrics-doc-template.md`. This doc is the
input to both later phases; get it right and the merge is mechanical.

### Phase B — Merge conforming metrics into the metadata table
Only metrics whose definition genuinely matches the schema column's intended meaning get merged (see
`Cloud_Region_Metadata_specification.md` for what each column means, and rule 2 above for the
CFE/market distinction). If a vendor's metric almost-but-not-quite fits, prefer leaving the cell blank
and recording the mismatch in the gaps report over forcing a number in. The mechanics (build script,
carry-forward, verify) are steps 1–5 below.

### Phase C — Write `gaps-<year>.md`
A cross-vendor alignment report: for each metric in the schema, tabulate how each vendor defines and
reports it, then call out what each vendor should change to make it comparable. This directly serves
the project's mission of lobbying providers toward a common definition. See
`references/gaps-report-template.md` for the structure and the recurring gaps to check every year
(fiscal-vs-calendar year, PUE boundary/coverage, WUE availability, location-vs-market CFE, per-region
vs macro/fleet reporting, missing per-region grid data).

---

## Merge mechanics (Phase B, step by step)

### 1. Set up a clean working base
The authoritative state is `upstream/main` (GSF). Local `main` and the fork's `Dev` drift behind it.
```
git fetch upstream && git fetch origin
git checkout main && git merge --ff-only upstream/main    # if local main is behind and not ahead
git checkout -b <year>-<provider>-update upstream/Dev      # PRs target Dev; Dev == main data-wise
```
Confirm `Dev` and `main` hold identical data files before branching off `Dev` (they usually do; the
few `main`-only commits are release merges / issue templates). One provider per branch/PR keeps
review clean, unless the user wants them combined.

### 2. Find the source data
Each provider has a tracking issue where the report link (and sometimes an extracted table) is
posted — check open issues labelled `action item` (e.g. AWS #158, Google #159, Azure #161, Oracle
#86). The report itself is the source of truth; a pasted table in an issue is a convenience. See the
per-provider reference for exact URLs, which page/table to read, and the region-name→region-code
mapping.

### 3. Build the new rows
Prefer a small, explicit, reviewable Python script that encodes the source table and writes rows,
over the older scraper scripts in `code/` (`aws-data-update.py` scrapes a popup and has historically
mislabelled columns; trust the report/issue table instead). `gcp-data-update.py` pulling from the
`region-carbon-info` repo is reliable for Google's CFE/grid data.

Carry forward slowly-changing metadata (`cfe-region`, `em-zone-id`, `wt-region-id`, `location`,
`geolocation`, and grid carbon intensity) from the region's most recent prior year — no new
Electricity Maps / WattTime lookup happens here. Only populate PUE/WUE/CFE for the new year where
the provider actually disclosed it.

**New regions appear every year** (each provider launches several). A region with disclosed data but
no prior row has nothing to carry forward — add it fresh rather than skipping it: **geocode a
city-level geolocation** (`geopy` Nominatim on the city name, rounded to 4 dp — the dataset uses
city-level, not exact datacenter coordinates), set `cfe-region`/`em-zone-id` from the country/grid
(the Electricity Maps zone), fill the disclosed PUE/WUE/CFE, and leave `wt-region-id` + grid carbon
intensity blank with a note that they need a WattTime / Electricity Maps lookup. Adding the region now
with partial metadata is better than dropping it — the grid columns can be filled when the lookup runs.

**Water (`total-water-input`).** Some providers report a per-region annual water **withdrawal** in
litres (AWS does, on each fact sheet). That maps to `total-water-input`. Watch the reporting boundary:
where a provider reports by **country** but has several regions there, allocate/interpolate — if the
regions are reported separately (AWS India: Mumbai/Hyderabad) use each; if combined (AWS Japan =
Tokyo+Osaka together) allocate to the primary region and leave the other blank (or split on a stated
basis), and document the choice. Convert gallons to litres where needed.

**Grid data (Electricity Maps / WattTime).** `em-zone-id`/`wt-region-id` are the lookup keys; the actual
`grid-carbon-intensity-*` values come from those services. Electricity Maps publishes yearly zone data
but via an **account-gated free portal** (`app.electricitymaps.com/datasets`, ~5 downloads) — not a
fetchable URL; WattTime marginal data is **API-gated** (credentials). So for a brand-new region set the
`em-zone-id` and leave grid carbon blank, and flag it for whoever has portal/API access to fill (the
project has done this before — see issue #86). Don't block the row on it.

**Critical file-format details** (getting these wrong makes the diff look enormous):
- The file is **CRLF**. Always write with `df.to_csv(path, index=False, lineterminator="\r\n")`.
- Read with `dtype=str` so existing numeric strings aren't reformatted.
- Sort `year` descending, then provider, then region (matches the repo convention).
- The `geolocation` field contains a comma inside quotes, so **never parse this CSV with `awk -F,`**
  — it mis-splits every subsequent column. Use Python's `csv` module or pandas.

### 4. Verify before committing
```
python3 -c "import csv;r=list(csv.reader(open('Cloud_Region_Metadata.csv')));n=len(r[0]);\
print('cols',n,'bad',[i for i,x in enumerate(r) if len(x)!=n][:5])"          # expect 24 cols, no bad rows
grep -c $'\r' Cloud_Region_Metadata.csv                                        # CRLF preserved on every line
diff <(git show upstream/Dev:Cloud_Region_Metadata.csv|sort) <(sort Cloud_Region_Metadata.csv)|grep -c '^<'   # MUST be 0 (additive)
```
Then spot-check a handful of rows against the source report (right PUE in the PUE column, right WUE
in WUE, CFE where expected, market column per the rules above).

### 5. Regenerate the estimate, sanity-check it, and update the README
The published estimate table is the **complete best-guess** current-year table. Its purpose: be *the*
central resource so that anyone who needs a number to use today gets one consistent best guess, instead
of everyone inventing their own. Every region gets a row and every tracked metric is filled (from the
region's own history where available, otherwise a regional best guess). Generate it with:
```
python3 code/complete_estimate.py Cloud_Region_Metadata.csv <next-year>   # e.g. 2026
```
Fill rules that matter:
- **Grid carbon intensity** is a physical grid property → fill from the same `em-zone-id` / continent
  (across providers is fine — it's the same grid).
- **Provider-specific metrics** (PUE, WUE, CFE %, market carbon, water) fill **only from the same
  provider's** regional data — **never estimate one provider's metric from another's**. If a provider
  doesn't report a metric anywhere (AWS/Azure CFE %, Google/Azure water, Google WUE), leave it blank.
- **Keep it conservative**: project only PUE/WUE/CFE, one *capped* step from the latest reported value;
  **carry forward** the noisy annual measurements (grid/consumption-hourly carbon, market carbon, water).
  Extrapolating a linear trend on those produces nonsense — a low-carbon grid trending to 0, CFE to 1.0.
- The never-reported EU-EED fields (`total-ICT-energy-consumption-annual`, `renewable-energy-*`) stay blank.

**Then sanity-check the estimate against the reported data — always:**
```
python3 code/sanity_check_estimate.py Cloud_Region_Metadata.csv Cloud_Region_Metadata_estimate.csv
```
It flags out-of-range absolutes (PUE < 1.04 / > 2, CFE outside 0–1, negative carbon), big jumps from a
region's latest reported value, regional-fill outliers, and coverage gaps. Aim for `TOTAL flags: 0`;
investigate any flag — some large moves are legitimate (a new grid, a restated value), but most point to
an over-eager extrapolation to fix. This is how the "central best guess" stays trustworthy.

**Keep the reported table (`Cloud_Region_Metadata.csv`) clean — never fill best-guesses into it; the
estimate table is the only place guesses belong.** (`estimate_current_region_metadata.py` is the older
trend-only estimator, kept for reference/testing; it leaves gaps blank.) Update the "Cloud Providers"
paragraph in `README.md` to state the latest real year and the projected year.

### 6. Open the PR and update the tracking issue
Base the PR on `Dev`. Include the CSV/estimate/README changes **and** the phase-A `metrics/<year>/`
docs and the phase-C `gaps-<year>.md` — they're deliverables, and they're the evidence for every
merge decision and caveat. In the body, state the sources (with links), the per-provider column
mapping, and every caveat/approximation. Comment on the provider's tracking issue with what landed and
what's still missing. Commit trailer: `Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>`;
PR-body trailer: `🤖 Generated with [Claude Code](https://claude.com/claude-code)`.

### 7. Archive the source documents
Providers periodically move or delete these files (the AWS popup, gstatic-hosted Google reports and
Oracle's data sheets have all changed URLs). Save the PDFs you used to `sources/<data-year>/<provider>/`
with a `sources/README.md` manifest (document each file's source URL, retrieval date, and a **gaps table**
for documents still needed — e.g. Oracle's CY report, Electricity Maps/WattTime data, prior-year fact
sheets). Download prior years too where the URLs are still live. This is bulky (~180 MB/year of PDFs);
keep it on its own branch/PR and flag **Git LFS or an external release-asset store** vs a plain commit so
the WG decides before merging binaries into history.

## Tooling notes
- PDFs: `pdfplumber` (reports) and `openpyxl` (Google-Sheet exports of working data). A working
  `venv` may have a Python-version/site-packages mismatch — if `import` fails, run the system
  `python3` with `PYTHONPATH=code/venv/lib/python3.XX/site-packages` pointing at wherever the
  packages actually installed.
- Google Sheets shared by the user export as CSV/XLSX via
  `https://docs.google.com/spreadsheets/d/<ID>/export?format=xlsx`.
- The scratchpad dir (per session) is the place for these one-off builder scripts, not the repo.

## Outputs of a full run
A complete update produces, and the PR(s) should include: new **reported** rows in
`Cloud_Region_Metadata.csv` (clean, real data only); the regenerated **complete estimate**
`Cloud_Region_Metadata_estimate.csv` (best-guess, every cell filled, **sanity-checked** vs reported); the phase-A
`metrics/<year>/<vendor>-<year>-metrics.md` docs and phase-C `metrics/<year>/gaps-<year>.md`; a README
update; and the `sources/<year>/` archive (own branch). Reported table clean, estimate table filled —
never mix the two.

## What each provider gives you (summary — details in the references)
| Provider | Per-region disclosed | Notes |
|----------|----------------------|-------|
| AWS      | PUE, WUE, water withdrawal (per-region); per-grid 100%-renewable list | `references/aws.md` — **~32 per-region PDF fact sheets** to download + process individually; friendly-name→code map; market=0 only for listed regions; regional-average PUE for newer regions |
| Google   | hourly CFE + grid carbon (region-carbon-info repo); per-datacenter PUE (report PDF) | `references/google.md` — annual CFE left blank; don't use the 100% claim |
| Azure    | only macro-regional (Americas/APAC/EMEA), fiscal-year PUE/WUE; detailed data fact sheet PDF for definitions | `references/azure.md` — map by continent; no per-region since 2022 |
| Oracle   | renewable % per region; PUE (CY report); grid via Electricity Maps | `references/oracle.md` — key→identifier map; gov regions inherit co-located grid |
| Others   | IBM/Alibaba/OVHcloud publish only fleet-wide PUE — not usable per-region | skip unless per-region data appears; still note them in the gaps report |
