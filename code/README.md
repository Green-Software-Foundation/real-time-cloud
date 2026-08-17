# Cloud Region Metadata Tools

This directory contains Python tools for managing and updating cloud region metadata.

## Setup

Create a Python virtual environment and install dependencies:

```bash
python3 -m venv venv
```

Windows:
```bash
venv\Scripts\activate
```

macOS/Linux:
```bash
source venv/bin/activate
```

Install requirements:
```bash
pip install -r requirements.txt
```

## 1. AWS Data Update Script (`aws-data-update.py`)

This script fetches the latest PUE (Power Usage Effectiveness) and WUE (Water Usage Effectiveness) 
data from the AWS sustainability page and updates the Cloud_Region_Metadata.csv file.

### Usage

Basic usage (updates with current year data):
```bash
python code/aws-data-update.py
```

Specify a different year:
```bash
python code/aws-data-update.py --year 2024
```

Specify a custom output file:
```bash
python code/aws-data-update.py --output Cloud_Region_Metadata_2024_update.csv
```

Use a different data source URL:
```bash
python code/aws-data-update.py --url https://example.com/aws-data.csv
```

### Output

The script creates a new CSV file (default: `Cloud_Region_Metadata_updated.csv`) that you should:
1. Review for accuracy
2. Compare with the original file to verify changes
3. Rename to `Cloud_Region_Metadata.csv` when ready to use

### Features

- Automatically fetches data from AWS sustainability page
- Handles both direct CSV downloads and HTML table parsing
- Updates existing regions or adds new ones based on historical data
- **Auto-detects year** from data, URL, or existing metadata (no need to specify)
- **Only creates output file when changes are detected** (use --force to override)
- **Incremental updates**: If output file exists, merges changes into it instead of overwriting
  - Allows running multiple scripts sequentially (e.g., AWS then GCP)
  - Each script adds its updates to the same output file
- **Automatically fills location and geolocation for new regions**:
  - Looks up region name/city from aws-services.info
  - Geocodes city to get latitude/longitude (rounded to 4 decimal places)
- Filters out non-AWS region entries (only processes regions with format xx-xxxx-N)
- Never overwrites existing data with NaN values
- Preserves all other metadata columns
- Sorts output consistently with existing format

## 2. GCP Data Update Script (`gcp-data-update.py`)

This script fetches the latest Carbon Free Energy (CFE) and Grid Carbon Intensity 
data from Google Cloud Platform's [region-carbon-info repository](https://github.com/GoogleCloudPlatform/region-carbon-info) and updates the Cloud_Region_Metadata.csv file.

### Usage

Basic usage (auto-detects year from existing data):
```bash
python code/gcp-data-update.py
```

Specify a specific year:
```bash
python code/gcp-data-update.py --year 2024
```

Specify a custom output file:
```bash
python code/gcp-data-update.py --output Cloud_Region_Metadata_gcp_updated.csv
```

### Output

The script creates a new CSV file (default: `Cloud_Region_Metadata_updated.csv`) that you should:
1. Review for accuracy
2. Compare with the original file to verify changes
3. Rename to `Cloud_Region_Metadata.csv` when ready to use

### Features

- Fetches data directly from GCP's official region-carbon-info GitHub repository
- **Auto-detects year** from existing metadata (or specify with --year)
- **Smart year fallback**: If requested year not available, tries previous years automatically
  - E.g., if 2025 requested but only 2024 available, uses 2024
  - Won't fallback if you explicitly specify --year
- **Only creates output file when changes are detected** (use --force to override)
- **Incremental updates**: If output file exists, merges changes into it instead of overwriting
  - Allows running multiple scripts sequentially (e.g., AWS then GCP)
  - Each script adds its updates to the same output file
- **Leverages GCP's comprehensive data**:
  - Annual Carbon Free Energy (CFE) percentage
  - Grid carbon intensity (gCO2eq / kWh)
  - Location names for each region
- **Automatically fills geolocation for new regions**:
  - Geocodes location to get latitude/longitude (rounded to 4 decimal places)
- Never overwrites existing data with NaN values
- Preserves all other metadata columns
- Sorts output consistently with existing format

### Running Multiple Updates

You can run both AWS and GCP update scripts sequentially to accumulate changes:

```bash
# First run AWS updates
python code/aws-data-update.py

# Then run GCP updates - will merge into the same file
python code/gcp-data-update.py

# Review combined changes
diff Cloud_Region_Metadata.csv Cloud_Region_Metadata_updated.csv

# Apply if satisfied
mv Cloud_Region_Metadata_updated.csv Cloud_Region_Metadata.csv
```

## 3. Google PDF Extractor (`google-pdf-extract.py`)

This script downloads Google's annual Environmental Report PDF and extracts data tables 
containing PUE, WUE, and other sustainability metrics. This complements the GCP data from 
the region-carbon-info repository.

### Usage

Extract from most recent year (auto-downloads):
```bash
python code/google-pdf-extract.py
```

Extract from a specific year:
```bash
python code/google-pdf-extract.py --year 2024
```

Extract from a local PDF file:
```bash
python code/google-pdf-extract.py --pdf path/to/google-report.pdf
```

Extract from a custom URL:
```bash
python code/google-pdf-extract.py --url https://example.com/report.pdf
```

Specify custom output directory:
```bash
python code/google-pdf-extract.py --year 2024 --output-dir my_tables
```

### Output

The script creates CSV files in the output directory (default: `google_extracted_tables/`):
- Separate files for each table found (e.g., `google_2024_pue_page42_table0.csv`)
- Metadata files describing each table (`.txt` files)
- Categorized by type: PUE, WUE, combined, or other

### Features

- **Auto-downloads** Google Environmental Reports from known URLs
- **Smart table detection**: Searches for keywords (PUE, WUE, data center, etc.)
- **Categorizes tables** by type (PUE, WUE, combined, other)
- **Extracts context**: Saves surrounding text for each table
- **Multiple sources**: Can work with URLs, local files, or known report years
- **Custom keywords**: Add your own search terms with `--keywords`

### Known Report Years

The script has URLs for:
- 2024, 2023, 2022, 2021

You can use `--url` for other years or custom reports.

### Workflow

After extraction, you'll need to:
1. Review the CSV files to identify relevant data
2. Manually clean and format data as needed
3. Integrate into `Cloud_Region_Metadata.csv` or use with update scripts

## 4. Estimate Current Year Metadata (`estimate_current_region_metadata.py`)

This script generates trended estimates for current years based on historical data (for two years since 2023 data is all we have until mid-2025).

### Usage

Run the script. By default it estimates one year, with an optional parameter it will estimate N years:
```
% python code/estimate_current_region_metadata.py Cloud_Region_Metadata.csv 2
Most recent year in dataset: 2023
Estimating data for years: [np.int64(2024), np.int64(2025)]
Generating estimate for year: 2024
Generating estimate for year: 2025
Estimates saved to Cloud_Region_Metadata_estimate.csv
```

## 5. Complete Current-Year Estimate (`complete_estimate.py`)

`estimate_current_region_metadata.py` (above) trends only the regions present in the latest reported
year and leaves gaps blank. `complete_estimate.py` produces the **fully populated best-guess** table
that is published as `Cloud_Region_Metadata_estimate.csv`: every region that has ever been reported gets
a current-year row, and every metric we track is filled — with the region's own trended value where it
has history, otherwise a **regional best guess**:

- **grid carbon intensity** is a physical property of the grid, the same for every provider on it, so
  it is filled from other regions sharing the same Electricity Maps zone (`em-zone-id`), then continent;
- **provider-specific metrics** (PUE, WUE, carbon-free-energy %, market carbon, water, consumption-hourly
  carbon) are filled **only from the same provider's** regional data (provider + continent, then
  provider). They are **never estimated across providers** — if a provider doesn't report a metric
  anywhere (e.g. AWS/Azure carbon-free-energy %, Google/Azure water, Google WUE), the cell is left blank
  rather than borrowed from another provider.

Columns left blank are therefore: the EU-EED disclosure fields no provider reports at all
(`total-ICT-energy-consumption-annual`, `renewable-energy-consumption[-goe/-ppa/-onsite]`), plus any
provider-specific metric a given provider never reports.

**The reported table (`Cloud_Region_Metadata.csv`) is never touched and stays clean** — this best-guess
table is a deliberately separate companion.

```
% python code/complete_estimate.py Cloud_Region_Metadata.csv 2026
Complete estimate for 2026: 106 rows -> Cloud_Region_Metadata_estimate.csv
```

Because the estimate table is meant to be *the* central best-guess anyone can use today, the metric
values are kept conservative: PUE, WUE and carbon-free-energy % are projected one capped step from the
latest reported value, while noisy annual measurements (grid/consumption-hourly carbon, market carbon,
water) are carried forward — extrapolating a linear trend on those produces nonsense (e.g. a low-carbon
grid trending to 0).

### Sanity check (`sanity_check_estimate.py`)

Always run this after regenerating the estimate. It compares each estimate value against the reported
data and flags anything implausible — out-of-range absolutes (PUE < 1.04 / > 2, CFE outside 0–1,
negative carbon), large jumps from a region's latest reported value, regionally-filled cells that fall
outside their fill group, and coverage gaps. Review any flags (some large moves are legitimate, e.g. a
new grid or a restated value); a clean run prints `TOTAL flags: 0`.

```
% python code/sanity_check_estimate.py Cloud_Region_Metadata.csv Cloud_Region_Metadata_estimate.csv
Estimate rows: 106 | reported pairs: 106
...
TOTAL flags: 0  (clean)
```

## 6. Fill Region Identity Metadata (`fill_region_metadata.py`)

The identity columns - `cfe-region`, `em-zone-id`, `wt-region-id` and `geolocation` - are static per
region (Annex A of the specification lists them as "Static"), so a blank in one year's row is a gap
rather than a different value. This script fills those gaps in `Cloud_Region_Metadata.csv` and repairs
values that are demonstrably wrong.

```
% python code/fill_region_metadata.py --dry-run     # report only
% python code/fill_region_metadata.py               # apply
% python code/fill_region_metadata.py --passes fix  # run a single pass
```

It runs five idempotent passes, and prints every cell it changes with the reason:

1. **trim** - strip stray whitespace from the identity columns.
2. **fix** - replace values that are demonstrably wrong: a coordinate that resolves to the wrong city,
   a zone key that does not exist in Electricity Maps, a country mismatch. Each correction is keyed on
   the wrong value, so the pass is a no-op once applied and never silently rewrites new data.
3. **propagate** - copy an identity value from the most recent year that has it into the same region's
   earlier years.
4. **reference** - fill regions that have no value in any year, from the external reference table in
   the script (each entry carries the city it was looked up for).
5. **zone** - derive `cfe-region` and `wt-region-id` from `em-zone-id`, using the mapping the rest of
   the table already uses for that zone. This is what populates the Oracle rows, which arrive with
   `em-zone-id` and `geolocation` but no grid-region names. Where one Electricity Maps zone spans
   several WattTime sub-regions (`US-MIDA-PJM`, `US-MIDW-MISO`, `US-CAL-CISO`) the sub-region is chosen
   per region by city rather than from the zone.

Values filled by passes 4 and 5 are inferred by this project, not reported by the provider - the same
status as the `cfe-region` names already carried for AWS and Azure, which do not publish carbon-free
energy regions.

The script finishes with a structural check that every `geolocation` parses as a `lat,lon` pair in
range, and a list of any remaining blanks.

`Cloud_Region_Metadata.csv` is the only file written. **Regenerate the estimate table afterwards**,
since it is derived from the reported table:

```
% python code/complete_estimate.py Cloud_Region_Metadata.csv 2026
% python code/sanity_check_estimate.py Cloud_Region_Metadata.csv Cloud_Region_Metadata_estimate.csv
```

## 7. Test Script and Simplified Input Data
```
% cd code
% sh test.sh
Running estimation on test_input.csv...
Most recent year in dataset: 2023
Estimating data for years: [np.int64(2024), np.int64(2025)]
Generating estimate for year: 2024
Generating estimate for year: 2025
Estimates saved to test_input_estimate.csv
Comparing test_input_estimate.csv with expected_output.csv...
TEST PASSED! Output matches expected file.
```