#!/usr/bin/env python3
"""
AWS Data Update Script

This script downloads WUE (Water Usage Effectiveness) and PUE (Power Usage Effectiveness)
data from AWS sustainability page and updates the Cloud_Region_Metadata.csv file.

The script automatically:
- Detects the year from the data and existing file
- Compares existing data and only adds new rows if data differs
- Preserves all existing metadata

Usage:
    python aws-data-update.py
    python aws-data-update.py --url <custom-url>
"""

import pandas as pd
import requests
from bs4 import BeautifulSoup
import sys
import argparse
from io import StringIO
from datetime import datetime
import re
import time
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError

# AWS sustainability page URL - default source for data
AWS_SUSTAINABILITY_URL = 'https://sustainability.aboutamazon.com/products-services/aws-cloud'

# AWS regions info page
AWS_REGIONS_INFO_URL = 'https://www.aws-services.info/regions.html'

def fetch_aws_csv_data(url):
    """
    Fetch the CSV data from the AWS sustainability page.
    
    Args:
        url (str): The URL of the AWS sustainability page
        
    Returns:
        pd.DataFrame: DataFrame containing the AWS data
    """
    print(f"Fetching data from {url}...")
    
    try:
        # Fetch the webpage
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        # Parse HTML to find CSV download link
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Look for CSV download links - try multiple patterns
        csv_link = None
        
        # Pattern 1: Direct CSV links
        for link in soup.find_all('a', href=True):
            href = link['href']
            if '.csv' in href.lower() or 'download' in href.lower():
                if not href.startswith('http'):
                    # Handle relative URLs
                    from urllib.parse import urljoin
                    csv_link = urljoin(url, href)
                else:
                    csv_link = href
                print(f"Found CSV link: {csv_link}")
                break
        
        # Pattern 2: Look for embedded table data
        if not csv_link:
            print("No direct CSV link found, looking for table data...")
            tables = soup.find_all('table')
            if tables:
                print(f"Found {len(tables)} table(s) on the page")
                # Try to parse the first table as CSV
                for idx, table in enumerate(tables):
                    print(f"Attempting to parse table {idx + 1}...")
                    try:
                        df = pd.read_html(StringIO(str(table)))[0]
                        if 'region' in ' '.join(df.columns).lower() or 'pue' in ' '.join(df.columns).lower():
                            print(f"Found relevant data in table {idx + 1}")
                            return df
                    except Exception as e:
                        print(f"Could not parse table {idx + 1}: {e}")
                        continue
        
        # If we found a CSV link, download it
        if csv_link:
            print(f"Downloading CSV from {csv_link}...")
            csv_response = requests.get(csv_link, timeout=30)
            csv_response.raise_for_status()
            df = pd.read_csv(StringIO(csv_response.text))
            print(f"Successfully loaded CSV with {len(df)} rows")
            return df
        
        # If no CSV or table found, print available links for debugging
        print("\nAvailable links on the page:")
        for link in soup.find_all('a', href=True)[:20]:  # Print first 20 links
            print(f"  - {link.get_text(strip=True)}: {link['href']}")
        
        raise ValueError("Could not find CSV data on the page. Please check the URL or page structure.")
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        raise
    except Exception as e:
        print(f"Error processing data: {e}")
        raise

def fetch_aws_region_info():
    """
    Fetch AWS region information from aws-services.info.
    
    Returns:
        dict: Dictionary mapping region-id to region name/city
    """
    print(f"\nFetching AWS region information from {AWS_REGIONS_INFO_URL}...")
    
    try:
        response = requests.get(AWS_REGIONS_INFO_URL, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'lxml')
        region_info = {}
        
        # Look for tables containing region information
        tables = soup.find_all('table')
        
        for table in tables:
            rows = table.find_all('tr')
            for row in rows:
                cells = row.find_all('td')
                if len(cells) >= 2:
                    # Try to find region ID and name
                    for i, cell in enumerate(cells):
                        text = cell.get_text(strip=True)
                        # AWS region IDs match pattern: xx-xxxx-N
                        if re.match(r'^[a-z]{2}-[a-z]+-\d+$', text):
                            region_id = text
                            # Look for the region name in adjacent cells
                            for j in range(max(0, i-2), min(len(cells), i+3)):
                                if j != i:
                                    name_text = cells[j].get_text(strip=True)
                                    # Look for text with parentheses (city name pattern)
                                    if '(' in name_text and ')' in name_text:
                                        region_info[region_id] = name_text
                                        break
                                    elif name_text and len(name_text) > 3 and not re.match(r'^[a-z]{2}-[a-z]+-\d+$', name_text):
                                        region_info[region_id] = name_text
        
        print(f"Found {len(region_info)} AWS regions in lookup table")
        return region_info
        
    except Exception as e:
        print(f"Warning: Could not fetch AWS region info: {e}")
        return {}

def geocode_location(location_name, max_retries=3):
    """
    Get latitude and longitude for a location name.
    
    Args:
        location_name (str): City or location name
        max_retries (int): Maximum number of retry attempts
        
    Returns:
        str: Formatted geolocation string "lat,lon" rounded to 4 decimal places, or None
    """
    # Extract city name from location string (e.g., "US East (Ohio)" -> "Ohio")
    city_match = re.search(r'\(([^)]+)\)', location_name)
    if city_match:
        city = city_match.group(1)
    else:
        city = location_name
    
    # Initialize geocoder
    geolocator = Nominatim(user_agent="aws-region-metadata-updater/1.0")
    
    for attempt in range(max_retries):
        try:
            print(f"    Geocoding '{city}'...", end=' ')
            location = geolocator.geocode(city, timeout=10)
            
            if location:
                lat = round(location.latitude, 4)
                lon = round(location.longitude, 4)
                result = f"{lat},{lon}"
                print(f"✓ {result}")
                return result
            else:
                print(f"✗ Not found")
                return None
                
        except (GeocoderTimedOut, GeocoderServiceError) as e:
            if attempt < max_retries - 1:
                print(f"⟳ Retry {attempt + 1}/{max_retries - 1}")
                time.sleep(1)  # Wait before retrying
            else:
                print(f"✗ Failed after {max_retries} attempts: {e}")
                return None
        except Exception as e:
            print(f"✗ Error: {e}")
            return None
    
    return None

def detect_year_from_data(df, url, metadata_df):
    """
    Automatically detect the year from the data, URL, or existing metadata.
    
    Args:
        df (pd.DataFrame): Raw AWS data
        url (str): URL where data was fetched from
        metadata_df (pd.DataFrame): Existing metadata
        
    Returns:
        int: Detected year
    """
    # Try to find year in the data columns
    for col in df.columns:
        if 'year' in str(col).lower():
            years = df[col].dropna().unique()
            if len(years) > 0:
                year = int(years[0])
                print(f"Detected year {year} from data column '{col}'")
                return year
    
    # Try to find year in the URL or page content
    year_matches = re.findall(r'20\d{2}', url)
    if year_matches:
        year = int(year_matches[-1])  # Take the most recent year mentioned
        print(f"Detected year {year} from URL")
        return year
    
    # Use current year or most recent year + 1 from existing data
    max_year = metadata_df[metadata_df['cloud-provider'] == 'Amazon Web Services']['year'].max()
    if pd.notna(max_year):
        # If we're in the same year, use it; otherwise use next year
        current_year = datetime.now().year
        if current_year > max_year:
            year = current_year
            print(f"Using current year {year} (most recent data is from {int(max_year)})")
        else:
            year = int(max_year)
            print(f"Using most recent year {year} from existing data")
        return year
    
    # Fallback to current year
    year = datetime.now().year
    print(f"Defaulting to current year {year}")
    return year

def normalize_aws_data(df, year):
    """
    Normalize the AWS data to match the Cloud_Region_Metadata.csv format.
    
    Args:
        df (pd.DataFrame): Raw AWS data
        year (int): Year for the data
        
    Returns:
        pd.DataFrame: Normalized DataFrame
    """
    print(f"\nNormalizing AWS data for year {year}...")
    
    # Print columns for debugging
    print(f"Available columns: {list(df.columns)}")
    print(f"First few rows:\n{df.head()}")
    
    # Try to identify region, PUE, and WUE columns (case-insensitive)
    region_col = None
    pue_col = None
    wue_col = None
    year_col = None
    
    for col in df.columns:
        col_lower = str(col).lower()
        if 'region' in col_lower and not region_col:
            region_col = col
        if ('pue' in col_lower or 'power usage' in col_lower) and not pue_col:
            pue_col = col
        if ('wue' in col_lower or 'water usage' in col_lower) and not wue_col:
            wue_col = col
        if 'year' in col_lower and not year_col:
            year_col = col
    
    if not region_col:
        raise ValueError(f"Could not find region column in data. Available columns: {list(df.columns)}")
    
    print(f"Identified columns - Region: {region_col}, PUE: {pue_col}, WUE: {wue_col}")
    
    # Create normalized dataframe
    normalized_data = []
    
    for _, row in df.iterrows():
        region = row[region_col]
        
        # AWS region IDs must contain exactly two hyphens (e.g., us-east-1, eu-west-2)
        # Skip geographic regions (e.g., "us", "europe", "asia") that don't match this pattern
        if isinstance(region, str) and region.count('-') != 2:
            print(f"  Skipping non-AWS region format: {region}")
            continue
        
        # Get year from row if available, otherwise use passed year
        row_year = row[year_col] if year_col and pd.notna(row[year_col]) else year
        
        # Extract PUE and WUE values
        pue = row[pue_col] if pue_col and pd.notna(row[pue_col]) else None
        wue = row[wue_col] if wue_col and pd.notna(row[wue_col]) else None
        
        # Skip if no data
        if pue is None and wue is None:
            continue
        
        # Create entry
        entry = {
            'cloud-region': region,
            'power-usage-effectiveness': pue,
            'water-usage-effectiveness': wue,
            'year': int(row_year)
        }
        
        normalized_data.append(entry)
    
    return pd.DataFrame(normalized_data)

def update_metadata_csv(normalized_aws_data, metadata_file, aws_region_info=None):
    """
    Update the Cloud_Region_Metadata.csv with new AWS data.
    Only updates rows where data has actually changed.
    
    Args:
        normalized_aws_data (pd.DataFrame): Normalized AWS data
        metadata_file (str): Path to the existing metadata CSV
        aws_region_info (dict): Optional dictionary of region IDs to names/cities
        
    Returns:
        tuple: (updated_df, has_changes, stats_dict)
    """
    print(f"\nLoading existing metadata from {metadata_file}...")
    
    # Load existing metadata
    metadata_df = pd.read_csv(metadata_file)
    
    print(f"Existing metadata has {len(metadata_df)} rows")
    
    # Get the year from the normalized data
    year = normalized_aws_data['year'].iloc[0]
    
    # Filter existing metadata for AWS regions in the same year
    existing_aws = metadata_df[
        (metadata_df['cloud-provider'] == 'Amazon Web Services') & 
        (metadata_df['year'] == year)
    ]
    
    print(f"Found {len(existing_aws)} existing AWS entries for year {year}")
    
    # Track changes
    updated_rows = []
    new_regions = []
    unchanged_regions = []
    stats = {
        'pue_changes': 0,
        'wue_changes': 0,
        'new_rows': 0,
        'unchanged': 0
    }
    
    for _, aws_row in normalized_aws_data.iterrows():
        region = aws_row['cloud-region']
        new_pue = aws_row['power-usage-effectiveness']
        new_wue = aws_row['water-usage-effectiveness']
        row_year = aws_row['year']
        
        # Find matching region in existing metadata
        matches = metadata_df[
            (metadata_df['cloud-provider'] == 'Amazon Web Services') & 
            (metadata_df['cloud-region'] == region) &
            (metadata_df['year'] == row_year)
        ]
        
        if len(matches) > 0:
            # Check if data actually changed
            row_idx = matches.index[0]
            existing_row = metadata_df.loc[row_idx]
            existing_pue = existing_row['power-usage-effectiveness']
            existing_wue = existing_row['water-usage-effectiveness']
            
            has_change = False
            
            # Compare PUE
            if pd.notna(new_pue) and (pd.isna(existing_pue) or abs(float(new_pue) - float(existing_pue)) > 0.001):
                has_change = True
                stats['pue_changes'] += 1
            
            # Compare WUE
            if pd.notna(new_wue) and (pd.isna(existing_wue) or abs(float(new_wue) - float(existing_wue)) > 0.001):
                has_change = True
                stats['wue_changes'] += 1
            
            if has_change:
                updated_row = existing_row.copy()
                # Only update values that have actual new data (not NaN)
                if pd.notna(new_pue):
                    updated_row['power-usage-effectiveness'] = new_pue
                if pd.notna(new_wue):
                    updated_row['water-usage-effectiveness'] = new_wue
                updated_rows.append((row_idx, updated_row))
                
                # Show what's being updated (only show changes)
                changes = []
                if pd.notna(new_pue) and (pd.isna(existing_pue) or abs(float(new_pue) - float(existing_pue)) > 0.001):
                    changes.append(f"PUE {existing_pue} -> {new_pue}")
                if pd.notna(new_wue) and (pd.isna(existing_wue) or abs(float(new_wue) - float(existing_wue)) > 0.001):
                    changes.append(f"WUE {existing_wue} -> {new_wue}")
                print(f"  Updating {region}: {', '.join(changes)}")
            else:
                unchanged_regions.append(region)
                stats['unchanged'] += 1
        else:
            # Check if this region exists in previous years
            prev_year_match = metadata_df[
                (metadata_df['cloud-provider'] == 'Amazon Web Services') & 
                (metadata_df['cloud-region'] == region)
            ].sort_values('year', ascending=False)
            
            if len(prev_year_match) > 0:
                # Copy data from most recent year and update with new values
                new_row = prev_year_match.iloc[0].copy()
                new_row['year'] = row_year
                # Only update values that have actual new data (not NaN)
                if pd.notna(new_pue):
                    new_row['power-usage-effectiveness'] = new_pue
                if pd.notna(new_wue):
                    new_row['water-usage-effectiveness'] = new_wue
                new_regions.append(new_row)
                stats['new_rows'] += 1
                
                # Show what data we're adding
                data_parts = []
                if pd.notna(new_pue):
                    data_parts.append(f"PUE {new_pue}")
                if pd.notna(new_wue):
                    data_parts.append(f"WUE {new_wue}")
                print(f"  Adding new year entry for {region} (year {row_year}): {', '.join(data_parts)}")
            else:
                # Completely new region - create a minimal entry with required fields
                # Use a template from any existing AWS region to get the column structure
                template_aws = metadata_df[metadata_df['cloud-provider'] == 'Amazon Web Services'].iloc[0].copy()
                
                # Reset all values to empty/NaN except cloud-provider
                new_row = pd.Series(index=template_aws.index, dtype=object)
                new_row['cloud-provider'] = 'Amazon Web Services'
                new_row['cloud-region'] = region
                new_row['year'] = row_year
                
                # Set the new PUE/WUE values
                if pd.notna(new_pue):
                    new_row['power-usage-effectiveness'] = new_pue
                if pd.notna(new_wue):
                    new_row['water-usage-effectiveness'] = new_wue
                
                # Try to fill in location and geolocation from AWS region info
                location_name = None
                if aws_region_info and region in aws_region_info:
                    location_name = aws_region_info[region]
                    new_row['location'] = location_name
                    print(f"  ⚠️  Adding NEW AWS region '{region}' (year {row_year})")
                    print(f"      Location: {location_name}")
                    
                    # Try to geocode the location
                    geolocation = geocode_location(location_name)
                    if geolocation:
                        new_row['geolocation'] = geolocation
                        print(f"      Geolocation: {geolocation}")
                    else:
                        print(f"      Geolocation: Could not determine (needs manual entry)")
                else:
                    print(f"  ⚠️  Adding NEW AWS region '{region}' (year {row_year})")
                    print(f"      Location: Not found in lookup (needs manual entry)")
                
                # Show PUE/WUE data
                data_parts = []
                if pd.notna(new_pue):
                    data_parts.append(f"PUE {new_pue}")
                if pd.notna(new_wue):
                    data_parts.append(f"WUE {new_wue}")
                print(f"      Data: {', '.join(data_parts)}")
                
                # Leave other fields empty (they can be filled in manually later)
                # Set empty strings for text fields to maintain CSV consistency
                for col in new_row.index:
                    if col not in ['cloud-provider', 'cloud-region', 'year', 'power-usage-effectiveness', 
                                   'water-usage-effectiveness', 'location', 'geolocation']:
                        if pd.isna(new_row[col]):
                            new_row[col] = ''
                
                new_regions.append(new_row)
                stats['new_rows'] += 1
    
    # Determine if there are any changes
    has_changes = len(updated_rows) > 0 or len(new_regions) > 0
    
    if not has_changes:
        print(f"\n✓ No changes detected. All {len(unchanged_regions)} AWS regions already have current data.")
        return metadata_df, False, stats
    
    # Apply updates
    result_df = metadata_df.copy()
    
    for row_idx, updated_row in updated_rows:
        result_df.loc[row_idx] = updated_row
    
    if new_regions:
        result_df = pd.concat([result_df, pd.DataFrame(new_regions)], ignore_index=True)
    
    # Sort by year (descending), then provider, then region
    result_df = result_df.sort_values(
        by=['year', 'cloud-provider', 'cloud-region'], 
        ascending=[False, True, True]
    )
    
    print(f"\n✓ Changes detected:")
    print(f"  - Updated {len(updated_rows)} existing rows")
    print(f"  - Added {len(new_regions)} new rows")
    print(f"  - {stats['unchanged']} regions unchanged")
    print(f"  - {stats['pue_changes']} PUE value changes")
    print(f"  - {stats['wue_changes']} WUE value changes")
    
    return result_df, has_changes, stats

def main():
    """Main function to orchestrate the data update process."""
    parser = argparse.ArgumentParser(
        description='Update Cloud_Region_Metadata.csv with latest AWS PUE/WUE data from AWS sustainability page'
    )
    parser.add_argument(
        '--url',
        type=str,
        default=AWS_SUSTAINABILITY_URL,
        help=f'URL to fetch AWS data from (default: {AWS_SUSTAINABILITY_URL})'
    )
    parser.add_argument(
        '--output',
        type=str,
        default='Cloud_Region_Metadata_updated.csv',
        help='Output file name (default: Cloud_Region_Metadata_updated.csv)'
    )
    parser.add_argument(
        '--force',
        action='store_true',
        help='Force output file creation even if no changes detected'
    )
    
    args = parser.parse_args()
    
    try:
        # Determine the metadata file path (go up one directory from code/)
        import os
        script_dir = os.path.dirname(os.path.abspath(__file__))
        metadata_file = os.path.join(os.path.dirname(script_dir), 'Cloud_Region_Metadata.csv')
        
        if not os.path.exists(metadata_file):
            print(f"✗ Error: Could not find {metadata_file}", file=sys.stderr)
            sys.exit(1)
        
        # Load metadata first to help detect year
        metadata_df = pd.read_csv(metadata_file)
        
        # Fetch AWS region information for location lookup
        aws_region_info = fetch_aws_region_info()
        
        # Fetch AWS data
        print(f"\nFetching AWS sustainability data...")
        print(f"URL: {args.url}\n")
        aws_data = fetch_aws_csv_data(args.url)
        
        # Detect year from data, URL, and existing metadata
        year = detect_year_from_data(aws_data, args.url, metadata_df)
        
        # Normalize the data
        normalized_data = normalize_aws_data(aws_data, year=year)
        
        if len(normalized_data) == 0:
            print("\n✗ Error: No valid AWS region data found in the fetched data", file=sys.stderr)
            sys.exit(1)
        
        print(f"\nFound data for {len(normalized_data)} AWS regions")
        
        # Update metadata and check for changes
        updated_metadata, has_changes, stats = update_metadata_csv(normalized_data, metadata_file, aws_region_info)
        
        # Save output file if changes detected or forced
        if has_changes or args.force:
            output_path = os.path.join(os.path.dirname(script_dir), args.output)
            updated_metadata.to_csv(output_path, index=False)
            
            if has_changes:
                print(f"\n✓ Success! Updated metadata saved to: {output_path}")
                print(f"\nNext steps:")
                print(f"  1. Review the changes:")
                print(f"     diff Cloud_Region_Metadata.csv {args.output}")
                print(f"  2. Verify PUE values are between 1.04-1.5")
                print(f"  3. Verify WUE values are between 0.0-2.5")
                print(f"  4. If satisfied, replace the original:")
                print(f"     mv {args.output} Cloud_Region_Metadata.csv")
            else:
                print(f"\n✓ Output file created at: {output_path} (forced, no changes)")
        else:
            print(f"\n✓ No output file created - data is already up to date!")
            print(f"   Use --force to create output file anyway.")
        
    except Exception as e:
        import traceback
        print(f"\n✗ Error: {e}", file=sys.stderr)
        print(f"\nFull traceback:", file=sys.stderr)
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()

