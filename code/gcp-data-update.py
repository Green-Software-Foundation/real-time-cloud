#!/usr/bin/env python3
"""
GCP Data Update Script

This script downloads Carbon Free Energy (CFE) and Grid Carbon Intensity data
from Google Cloud Platform's region-carbon-info repository and updates the 
Cloud_Region_Metadata.csv file.

The script automatically:
- Detects the year from the data and existing file
- Compares existing data and only adds new rows if data differs
- Preserves all existing metadata
- Leverages GCP's comprehensive CFE and carbon intensity data

Usage:
    python gcp-data-update.py
    python gcp-data-update.py --year 2024
"""

import pandas as pd
import requests
import sys
import argparse
from io import StringIO
from datetime import datetime
import re
import time
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError

# GCP region carbon info repository - default source for data
GCP_CARBON_INFO_BASE_URL = 'https://raw.githubusercontent.com/GoogleCloudPlatform/region-carbon-info/main/data/yearly'

def fetch_gcp_csv_data(year):
    """
    Fetch the CSV data from GCP's region-carbon-info repository.
    
    Args:
        year (int): Year for which to fetch data
        
    Returns:
        pd.DataFrame: DataFrame containing the GCP data
    """
    url = f"{GCP_CARBON_INFO_BASE_URL}/{year}.csv"
    print(f"Fetching GCP data from {url}...")
    
    try:
        # Fetch the CSV directly
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        df = pd.read_csv(StringIO(response.text))
        print(f"Successfully loaded CSV with {len(df)} rows")
        return df
        
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            print(f"No data found for year {year} at {url}")
            raise ValueError(f"GCP carbon data not available for year {year}")
        raise
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        raise
    except Exception as e:
        print(f"Error processing data: {e}")
        raise

def geocode_location(location_name, max_retries=3):
    """
    Get latitude and longitude for a location name.
    
    Args:
        location_name (str): City or location name
        max_retries (int): Maximum number of retry attempts
        
    Returns:
        str: Formatted geolocation string "lat,lon" rounded to 4 decimal places, or None
    """
    # Initialize geocoder
    geolocator = Nominatim(user_agent="gcp-region-metadata-updater/1.0")
    
    for attempt in range(max_retries):
        try:
            print(f"    Geocoding '{location_name}'...", end=' ')
            location = geolocator.geocode(location_name, timeout=10)
            
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

def detect_year_from_data(metadata_df):
    """
    Automatically detect the year to fetch based on existing metadata.
    
    Args:
        metadata_df (pd.DataFrame): Existing metadata
        
    Returns:
        int: Year to fetch
    """
    # Get the most recent year from GCP data
    gcp_data = metadata_df[metadata_df['cloud-provider'] == 'Google Cloud']
    
    if len(gcp_data) > 0:
        max_year = gcp_data['year'].max()
        current_year = datetime.now().year
        
        # Try to fetch data for the next year or current year
        if current_year > max_year:
            year = current_year
            print(f"Attempting to fetch data for {year} (most recent in metadata: {int(max_year)})")
        else:
            year = int(max_year)
            print(f"Fetching data for most recent year {year}")
        return year
    
    # Fallback to current year
    year = datetime.now().year
    print(f"No existing GCP data found, defaulting to {year}")
    return year

def normalize_gcp_data(df, year):
    """
    Normalize the GCP data to match the Cloud_Region_Metadata.csv format.
    
    Args:
        df (pd.DataFrame): Raw GCP data
        year (int): Year for the data
        
    Returns:
        pd.DataFrame: Normalized DataFrame
    """
    print(f"\nNormalizing GCP data for year {year}...")
    
    # Print columns for debugging
    print(f"Available columns: {list(df.columns)}")
    print(f"First few rows:\n{df.head()}")
    
    # GCP CSV has specific column names
    region_col = 'Google Cloud Region'
    location_col = 'Location'
    cfe_col = 'Google CFE'
    carbon_col = 'Grid carbon intensity (gCO2eq / kWh)'
    
    # Verify columns exist
    if region_col not in df.columns:
        raise ValueError(f"Expected column '{region_col}' not found. Available: {list(df.columns)}")
    
    print(f"Identified columns - Region: {region_col}, Location: {location_col}, CFE: {cfe_col}, Carbon: {carbon_col}")
    
    # Create normalized dataframe
    normalized_data = []
    
    for _, row in df.iterrows():
        region = row[region_col]
        location = row[location_col] if location_col in df.columns else None
        
        # Extract CFE and carbon intensity values
        cfe = row[cfe_col] if cfe_col in df.columns and pd.notna(row[cfe_col]) else None
        carbon_intensity = row[carbon_col] if carbon_col in df.columns and pd.notna(row[carbon_col]) else None
        
        # Skip if no data
        if cfe is None and carbon_intensity is None:
            continue
        
        # Create entry
        entry = {
            'cloud-region': region,
            'location': location,
            'provider-cfe-annual': cfe,
            'grid-carbon-intensity-average-consumption-annual': carbon_intensity,
            'year': int(year)
        }
        
        normalized_data.append(entry)
    
    return pd.DataFrame(normalized_data)

def update_metadata_csv(normalized_gcp_data, metadata_file):
    """
    Update the Cloud_Region_Metadata.csv with new GCP data.
    Only updates rows where data has actually changed.
    
    Args:
        normalized_gcp_data (pd.DataFrame): Normalized GCP data
        metadata_file (str): Path to the existing metadata CSV
        
    Returns:
        tuple: (updated_df, has_changes, stats_dict)
    """
    print(f"\nLoading existing metadata from {metadata_file}...")
    
    # Load existing metadata
    metadata_df = pd.read_csv(metadata_file)
    
    print(f"Existing metadata has {len(metadata_df)} rows")
    
    # Get the year from the normalized data
    year = normalized_gcp_data['year'].iloc[0]
    
    # Filter existing metadata for GCP regions in the same year
    existing_gcp = metadata_df[
        (metadata_df['cloud-provider'] == 'Google Cloud') & 
        (metadata_df['year'] == year)
    ]
    
    print(f"Found {len(existing_gcp)} existing GCP entries for year {year}")
    
    # Track changes
    updated_rows = []
    new_regions = []
    unchanged_regions = []
    stats = {
        'cfe_changes': 0,
        'carbon_changes': 0,
        'location_updates': 0,
        'new_rows': 0,
        'unchanged': 0
    }
    
    for _, gcp_row in normalized_gcp_data.iterrows():
        region = gcp_row['cloud-region']
        new_cfe = gcp_row['provider-cfe-annual']
        new_carbon = gcp_row['grid-carbon-intensity-average-consumption-annual']
        new_location = gcp_row['location']
        row_year = gcp_row['year']
        
        # Find matching region in existing metadata
        matches = metadata_df[
            (metadata_df['cloud-provider'] == 'Google Cloud') & 
            (metadata_df['cloud-region'] == region) &
            (metadata_df['year'] == row_year)
        ]
        
        if len(matches) > 0:
            # Check if data actually changed
            row_idx = matches.index[0]
            existing_row = metadata_df.loc[row_idx]
            existing_cfe = existing_row['provider-cfe-annual']
            existing_carbon = existing_row['grid-carbon-intensity-average-consumption-annual']
            existing_location = existing_row['location']
            
            has_change = False
            
            # Compare CFE
            if pd.notna(new_cfe) and (pd.isna(existing_cfe) or abs(float(new_cfe) - float(existing_cfe)) > 0.001):
                has_change = True
                stats['cfe_changes'] += 1
            
            # Compare Carbon Intensity
            if pd.notna(new_carbon) and (pd.isna(existing_carbon) or abs(float(new_carbon) - float(existing_carbon)) > 0.01):
                has_change = True
                stats['carbon_changes'] += 1
            
            # Check if location needs update
            if pd.notna(new_location) and (pd.isna(existing_location) or existing_location != new_location):
                has_change = True
                stats['location_updates'] += 1
            
            if has_change:
                updated_row = existing_row.copy()
                # Only update values that have actual new data (not NaN)
                if pd.notna(new_cfe):
                    updated_row['provider-cfe-annual'] = new_cfe
                if pd.notna(new_carbon):
                    updated_row['grid-carbon-intensity-average-consumption-annual'] = new_carbon
                if pd.notna(new_location):
                    updated_row['location'] = new_location
                updated_rows.append((row_idx, updated_row))
                
                # Show what's being updated (only show changes)
                changes = []
                if pd.notna(new_cfe) and (pd.isna(existing_cfe) or abs(float(new_cfe) - float(existing_cfe)) > 0.001):
                    changes.append(f"CFE {existing_cfe} -> {new_cfe}")
                if pd.notna(new_carbon) and (pd.isna(existing_carbon) or abs(float(new_carbon) - float(existing_carbon)) > 0.01):
                    changes.append(f"Carbon {existing_carbon} -> {new_carbon}")
                if pd.notna(new_location) and (pd.isna(existing_location) or existing_location != new_location):
                    changes.append(f"Location: {new_location}")
                print(f"  Updating {region}: {', '.join(changes)}")
            else:
                unchanged_regions.append(region)
                stats['unchanged'] += 1
        else:
            # Check if this region exists in previous years
            prev_year_match = metadata_df[
                (metadata_df['cloud-provider'] == 'Google Cloud') & 
                (metadata_df['cloud-region'] == region)
            ].sort_values('year', ascending=False)
            
            if len(prev_year_match) > 0:
                # Copy data from most recent year and update with new values
                new_row = prev_year_match.iloc[0].copy()
                new_row['year'] = row_year
                # Only update values that have actual new data (not NaN)
                if pd.notna(new_cfe):
                    new_row['provider-cfe-annual'] = new_cfe
                if pd.notna(new_carbon):
                    new_row['grid-carbon-intensity-average-consumption-annual'] = new_carbon
                if pd.notna(new_location):
                    new_row['location'] = new_location
                new_regions.append(new_row)
                stats['new_rows'] += 1
                
                # Show what data we're adding
                data_parts = []
                if pd.notna(new_cfe):
                    data_parts.append(f"CFE {new_cfe}")
                if pd.notna(new_carbon):
                    data_parts.append(f"Carbon {new_carbon}")
                print(f"  Adding new year entry for {region} (year {row_year}): {', '.join(data_parts)}")
            else:
                # Completely new region - create a minimal entry with required fields
                # Use a template from any existing GCP region to get the column structure
                template_gcp = metadata_df[metadata_df['cloud-provider'] == 'Google Cloud'].iloc[0].copy()
                
                # Reset all values to empty/NaN except cloud-provider
                new_row = pd.Series(index=template_gcp.index, dtype=object)
                new_row['cloud-provider'] = 'Google Cloud'
                new_row['cloud-region'] = region
                new_row['year'] = row_year
                
                # Set the new CFE and carbon intensity values
                if pd.notna(new_cfe):
                    new_row['provider-cfe-annual'] = new_cfe
                if pd.notna(new_carbon):
                    new_row['grid-carbon-intensity-average-consumption-annual'] = new_carbon
                
                # Set location and try to geocode
                if pd.notna(new_location):
                    new_row['location'] = new_location
                    print(f"  ⚠️  Adding NEW GCP region '{region}' (year {row_year})")
                    print(f"      Location: {new_location}")
                    
                    # Try to geocode the location
                    geolocation = geocode_location(new_location)
                    if geolocation:
                        new_row['geolocation'] = geolocation
                        print(f"      Geolocation: {geolocation}")
                    else:
                        print(f"      Geolocation: Could not determine (needs manual entry)")
                else:
                    print(f"  ⚠️  Adding NEW GCP region '{region}' (year {row_year})")
                    print(f"      Location: Not provided in data (needs manual entry)")
                
                # Show CFE/Carbon data
                data_parts = []
                if pd.notna(new_cfe):
                    data_parts.append(f"CFE {new_cfe}")
                if pd.notna(new_carbon):
                    data_parts.append(f"Carbon {new_carbon}")
                print(f"      Data: {', '.join(data_parts)}")
                
                # Leave other fields empty (they can be filled in manually later)
                # Set empty strings for text fields to maintain CSV consistency
                for col in new_row.index:
                    if col not in ['cloud-provider', 'cloud-region', 'year', 'provider-cfe-annual',
                                   'grid-carbon-intensity-average-consumption-annual', 'location', 'geolocation']:
                        if pd.isna(new_row[col]):
                            new_row[col] = ''
                
                new_regions.append(new_row)
                stats['new_rows'] += 1
    
    # Determine if there are any changes
    has_changes = len(updated_rows) > 0 or len(new_regions) > 0
    
    if not has_changes:
        print(f"\n✓ No changes detected. All {len(unchanged_regions)} GCP regions already have current data.")
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
    print(f"  - {stats['cfe_changes']} CFE value changes")
    print(f"  - {stats['carbon_changes']} Carbon intensity changes")
    print(f"  - {stats['location_updates']} Location updates")
    
    return result_df, has_changes, stats

def main():
    """Main function to orchestrate the data update process."""
    parser = argparse.ArgumentParser(
        description='Update Cloud_Region_Metadata.csv with latest GCP CFE and carbon intensity data'
    )
    parser.add_argument(
        '--year',
        type=int,
        help='Year for the data (default: auto-detect from existing data)'
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
        output_path = os.path.join(os.path.dirname(script_dir), args.output)
        
        if not os.path.exists(metadata_file):
            print(f"✗ Error: Could not find {metadata_file}", file=sys.stderr)
            sys.exit(1)
        
        # Check if output file already exists - if so, use it as the base
        if os.path.exists(output_path):
            print(f"📝 Found existing output file: {args.output}")
            print(f"   Will merge changes into existing file instead of overwriting")
            base_file = output_path
        else:
            base_file = metadata_file
        
        # Load metadata first to help detect year
        metadata_df = pd.read_csv(base_file)
        
        # Determine year to fetch
        if args.year:
            year = args.year
            print(f"Using specified year: {year}")
        else:
            year = detect_year_from_data(metadata_df)
        
        # Fetch GCP data
        print(f"\nFetching GCP carbon data for {year}...")
        gcp_data = fetch_gcp_csv_data(year)
        
        # Normalize the data
        normalized_data = normalize_gcp_data(gcp_data, year=year)
        
        if len(normalized_data) == 0:
            print("\n✗ Error: No valid GCP region data found in the fetched data", file=sys.stderr)
            sys.exit(1)
        
        print(f"\nFound data for {len(normalized_data)} GCP regions")
        
        # Update metadata and check for changes
        updated_metadata, has_changes, stats = update_metadata_csv(normalized_data, base_file)
        
        # Save output file if changes detected or forced
        if has_changes or args.force:
            updated_metadata.to_csv(output_path, index=False)
            
            if has_changes:
                if os.path.exists(output_path) and base_file == output_path:
                    print(f"\n✓ Success! Merged GCP updates into: {output_path}")
                else:
                    print(f"\n✓ Success! Updated metadata saved to: {output_path}")
                print(f"\nNext steps:")
                print(f"  1. Review the changes:")
                print(f"     diff Cloud_Region_Metadata.csv {args.output}")
                print(f"  2. Verify CFE values are between 0.0-1.0")
                print(f"  3. Verify Carbon intensity values are reasonable")
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

