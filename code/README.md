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

## 5. Test Script and Simplified Input Data
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