import pandas as pd
import numpy as np
import sys
import os

def estimate_next_years(input_file):
    # Read CSV as string to preserve structure, then convert numeric columns later
    df = pd.read_csv(input_file, dtype=str)  
    original_columns = df.columns.tolist()  # Preserve original column order

    # Normalize column names (strip spaces, lowercase)
    df.columns = df.columns.str.strip().str.lower()

    # Ensure 'year' column exists
    if 'year' not in df.columns:
        raise KeyError("The input CSV does not contain a 'year' column. Check column names.")

    # Convert 'year' to numeric
    df['year'] = pd.to_numeric(df['year'], errors='coerce')

    # Identify most recent year and next two years
    max_year = df['year'].max()
    next_years = [max_year + 1, max_year + 2]

    # Filter to most recent year's data
    most_recent_data = df[df['year'] == max_year].copy()

    # Define numeric columns that should be processed
    numeric_columns = [
        'provider-cfe-hourly', 'provider-cfe-annual', 'power-usage-effectiveness',
        'water-usage-effectiveness', 'provider-carbon-intensity-market-annual',
        'provider-carbon-intensity-average-consumption-hourly', 'grid-carbon-intensity-average-consumption-annual',
        'grid-carbon-intensity-marginal-consumption-annual', 'grid-carbon-intensity-average-production-annual',
        'grid-carbon-intensity', 'total-ict-energy-consumption-annual', 'total-water-input',
        'renewable-energy-consumption', 'renewable-energy-consumption-goe',
        'renewable-energy-consumption-ppa', 'renewable-energy-consumption-onsite'
    ]

    # Keep only numeric columns that actually exist in the dataset
    available_numeric_columns = [col for col in numeric_columns if col in df.columns]

    # Convert numeric columns to float where possible
    df[available_numeric_columns] = df[available_numeric_columns].apply(pd.to_numeric, errors='coerce')

    # Fill missing values using forward/backward fill, then default to 0
    df[available_numeric_columns] = df[available_numeric_columns].ffill().bfill().fillna(0)

    all_estimates = []  # Store estimates for both years

    for year in next_years:
        next_year_df = most_recent_data.copy()
        next_year_df['year'] = year

        # Predict numeric columns
        for col in available_numeric_columns:
            # Compute trends per provider-region
            trends = {}
            for (provider, region), group in df.groupby(['cloud-provider', 'cloud-region']):
                group = group.sort_values(by='year')
                year_diffs = group['year'].diff()
                value_diffs = group[col].diff()
                trend = (value_diffs / year_diffs).mean(skipna=True)  # Compute trend safely
                trends[(provider, region)] = trend

            # Apply trends to most recent values
            next_year_values = []
            for _, row in most_recent_data.iterrows():
                provider = row['cloud-provider']
                region = row['cloud-region']
                latest_value = row[col]

                # Ensure latest_value is a number before applying trends
                try:
                    latest_value = float(latest_value)
                except (ValueError, TypeError):
                    latest_value = np.nan

                trend = trends.get((provider, region), 0)  # Default trend is 0 if missing
                estimated_value = latest_value + trend if not np.isnan(latest_value) else np.nan

                # Apply constraints
                if col in ['provider-cfe-hourly', 'provider-cfe-annual']:
                    estimated_value = max(0, min(1.0, estimated_value))  # Clamp between 0 and 1
                elif col == 'power-usage-effectiveness':
                    estimated_value = max(1.0, estimated_value)  # Ensure >= 1.0

                next_year_values.append(estimated_value)

            next_year_df[col] = next_year_values

        all_estimates.append(next_year_df)

    # Combine estimated data for both years
    final_df = pd.concat(all_estimates, ignore_index=True)

    # Sort by year, cloud-provider, cloud-region
    final_df = final_df.sort_values(by=['year', 'cloud-provider', 'cloud-region'])

    # Ensure all original columns exist in output
    for col in original_columns:
        if col not in final_df.columns:
            final_df[col] = ""  # Add missing columns as empty strings

    # Reorder columns to match original CSV structure
    final_df = final_df[original_columns]

    # Convert fully empty columns to blank strings
    for col in final_df.columns:
        if final_df[col].isna().all():  # If entire column is NaN, make it blank
            final_df[col] = ""

    # Generate output file name
    base_name = os.path.splitext(os.path.basename(input_file))[0]
    output_file_path = f"{base_name}_estimate.csv"

    # Save output
    final_df.to_csv(output_file_path, index=False)

    print(f"Estimates for {next_years[0]} and {next_years[1]} have been saved to {output_file_path}.")

if __name__ == "__main__":
    # Check if script received a filename as an argument
    if len(sys.argv) < 2:
        print("Usage: python script.py <input_file.csv>")
    else:
        input_file = sys.argv[1]
        estimate_next_years(input_file)
