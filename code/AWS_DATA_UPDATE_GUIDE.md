# AWS Data Update Guide

This guide explains how to use the `aws-data-update.py` script to fetch and update AWS region metadata with the latest PUE and WUE data.

## Prerequisites

The virtual environment has been set up with all required packages:
- pandas
- requests
- beautifulsoup4
- numpy

## Quick Start

1. **Activate the virtual environment** (if not already activated):
   ```bash
   cd code
   source venv/bin/activate
   ```

2. **Run the script** from the project root:
   ```bash
   cd /Users/adrian.cockcroft.advisor/Documents/GitHub/real-time-cloud
   python code/aws-data-update.py
   ```

3. **Check the output**: 
   - If changes detected: Reviews `Cloud_Region_Metadata_updated.csv`
   - If no changes: Script reports "data is already up to date" and doesn't create output file

4. **Review and verify** any changes before replacing the original file

## How It Works

The script performs the following steps:

1. **Fetches region information** from aws-services.info to get region names and cities

2. **Fetches PUE/WUE data** from the AWS sustainability page at:
   https://sustainability.aboutamazon.com/products-services/aws-cloud

3. **Parses the data** - it can handle:
   - Direct CSV download links
   - HTML tables embedded in the page

4. **Auto-detects the year** from:
   - Year column in the data (if present)
   - Year mentioned in the URL
   - Current year vs. most recent data year

5. **Filters regions** - only processes valid AWS region IDs (format: xx-xxxx-N like us-east-1)
   - Skips geographic entries that don't match this pattern

6. **Normalizes the data** - extracts region names, PUE, and WUE values

7. **Updates metadata** - for each AWS region in the downloaded data:
   - If the region exists for the target year:
     - Compares existing PUE/WUE values
     - Only updates if values actually changed (never overwrites with NaN)
   - If the region exists in previous years but not target year:
     - Copies the most recent year's data
     - Updates year, PUE, and WUE values
   - If the region is completely new:
     - Looks up location name from aws-services.info
     - Geocodes the city to get latitude/longitude (rounded to 4 decimal places)
     - Creates new entry with PUE/WUE, location, and geolocation
     - Other fields left empty for manual entry

8. **Saves output** - only creates file if changes detected:
   - Creates a new CSV file sorted by year, provider, and region
   - If no changes, reports "data is already up to date"
   - Use --force to create output file even without changes

## Usage Examples

### Basic usage (auto-detects year):
```bash
python code/aws-data-update.py
```

### Force output file creation (even if no changes):
```bash
python code/aws-data-update.py --force
```

### Custom output filename:
```bash
python code/aws-data-update.py --output Cloud_Region_Metadata_2024_AWS.csv
```

### All options together:
```bash
python code/aws-data-update.py --output my_custom_output.csv --force
```

## Troubleshooting

### Finding the CSV Data

If the script can't find the CSV data automatically, you may need to:

1. **Visit the AWS sustainability page** manually:
   https://sustainability.aboutamazon.com/products-services/aws-cloud

2. **Look for the data table or download link** - it might be in a popup window or 
   an interactive element on the page

3. **If there's a direct CSV link**, you can provide it:
   ```bash
   python code/aws-data-update.py --url https://example.com/direct-csv-link.csv
   ```

4. **If the data is only in a popup/modal**, you may need to:
   - Manually download the CSV from the popup
   - Save it locally
   - Modify the script or manually merge the data

### Script Output

The script provides detailed logging:
- URL being fetched
- Links and tables found on the page
- Columns identified in the data
- Regions being updated
- Number of rows updated/added

If the script fails, check this output for clues about what went wrong.

## Verification Steps

After running the script, you should:

1. **Compare files** to see what changed:
   ```bash
   diff Cloud_Region_Metadata.csv Cloud_Region_Metadata_updated.csv
   ```

2. **Check PUE values** - should typically be between 1.04 and 1.5
   - Lower is better (more efficient)
   - 1.0 would be theoretically perfect

3. **Check WUE values** - should typically be between 0.01 and 2.5 L/kWh
   - Lower is better (less water usage)
   - 0.0 means no water cooling

4. **Verify regions** - make sure the right AWS regions were updated

5. **Look for anomalies** - unusual spikes or drops in values

## Manual CSV Processing

If the automatic fetch doesn't work, you can manually download the CSV and process it:

1. Download the CSV from the AWS sustainability page
2. Save it as `aws_data_manual.csv` in the project root
3. The script can be modified to read from this file instead

## Next Steps

After you have a verified `Cloud_Region_Metadata_updated.csv`:

1. **Backup the current file**:
   ```bash
   cp Cloud_Region_Metadata.csv Cloud_Region_Metadata_backup.csv
   ```

2. **Replace with the new data**:
   ```bash
   mv Cloud_Region_Metadata_updated.csv Cloud_Region_Metadata.csv
   ```

3. **Run the estimation script** to project future years if needed:
   ```bash
   python code/estimate_current_region_metadata.py Cloud_Region_Metadata.csv 2
   ```

4. **Commit changes** to the repository (after review)

## Support

For issues or questions:
- Check the main README.md
- Review the script comments in `aws-data-update.py`
- Open an issue in the GitHub repository

