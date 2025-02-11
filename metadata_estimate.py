import pandas as pd
import numpy as np
import sys
import os

def estimate_next_year(input_file):
    # Read the CSV file
    df = pd.read_csv(input_file)

    # Identify the current year range and increment to get the next year
    max_year = df['year'].max()
    next_year = max_year + 1

    # Filter the data for the most recent year
    most_recent_data = df[df['year'] == max_year]
    
    # Create a DataFrame for the next year by copying from the most recent year
    next_year_df = most_recent_data.copy()
    next_year_df['year'] = next_year

    # List of numeric columns to estimate
    numeric_columns = [
        'provider-cfe-hourly', 'provider-cfe-annual', 'power-usage-effectiveness',
        'water-usage-effectiveness', 'provider-carbon-intensity-market-annual',
        'provider-carbon-intensity-average-consumption-hourly', 'grid-carbon-intensity-average-consumption-annual',
        'grid-carbon-intensity-marginal-consumption-annual', 'grid-carbon-intensity-average-production-annual',
        'grid-carbon-intensity', 'total-ICT-energy-consumption-annual', 'total-water-input',
        'renewable-energy-consumption', 'renewable-energy-consumption-goe',
        'renewable-energy-consumption-ppa', 'renewable-energy-consumption-onsite'
    ]

    # Fill numeric columns with trended values
    for col in numeric_columns:
        # Check if the column has any data; skip if it doesn't
        if df[col].isna().all():
            next_year_df[col] = np.nan
            continue

        # Use linear interpolation to fill missing values in the historical data
        df[col] = df[col].interpolate(method='linear', limit_direction='both')

        # Calculate the trend for each cloud-provider and cloud-region
        trends = {}
        for (provider, region), group in df.groupby(['cloud-provider', 'cloud-region']):
            # Sort the group by year
            group = group.sort_values(by='year')

            # Calculate year-over-year differences for the column
            year_diffs = group['year'].diff()
            value_diffs = group[col].diff()
            trend = (value_diffs / year_diffs).mean()  # Average trend
            trends[(provider, region)] = trend

        # Apply the trend to the most recent values
        next_year_values = []
        for index, row in most_recent_data.iterrows():
            provider = row['cloud-provider']
            region = row['cloud-region']
            latest_value = row[col]
            trend = trends.get((provider, region), 0)  # Default trend is 0 if no data
            next_year_values.append(latest_value + trend if not np.isnan(latest_value) else np.nan)

        next_year_df[col] = next_year_values

    # Sort the DataFrame by cloud-provider and cloud-region
    next_year_df = next_year_df.sort_values(by=['cloud-provider', 'cloud-region'])

    # Construct the output file name
    base_name = os.path.splitext(os.path.basename(input_file))[0]
    output_file_path = f"{base_name}_{next_year}_estimate.csv"

    # Save the next year DataFrame to a new CSV file
    next_year_df.to_csv(output_file_path, index=False)
    
    print(f"Estimates for {next_year} have been saved to {output_file_path}.")

if __name__ == "__main__":
    # Check if the script received a file name as an argument
    if len(sys.argv) < 2:
        print("Please provide the input CSV file name as an argument.")
    else:
        input_file = sys.argv[1]
        estimate_next_year(input_file)
