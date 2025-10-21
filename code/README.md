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
- **Automatically fills location and geolocation for new regions**:
  - Looks up region name/city from aws-services.info
  - Geocodes city to get latitude/longitude (rounded to 4 decimal places)
- Filters out non-AWS region entries (only processes regions with format xx-xxxx-N)
- Never overwrites existing data with NaN values
- Preserves all other metadata columns
- Sorts output consistently with existing format

## 2. Estimate Current Year Metadata (`estimate_current_region_metadata.py`)

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

## 3. Test Script and Simplified Input Data
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