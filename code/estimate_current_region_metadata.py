import pandas as pd
import numpy as np
import sys

def estimate_next_years(input_file, num_years=1):
    # Load the dataset
    df = pd.read_csv(input_file)
    
    # Ensure the 'year' column exists and is treated as an integer
    if 'year' not in df.columns:
        raise KeyError("The dataset must contain a 'year' column.")
    df['year'] = df['year'].astype(int)
    
    # Get the most recent year
    max_year = df['year'].max()
    print(f"Most recent year in dataset: {max_year}")
    
    # Identify numeric and textual columns, excluding 'year' from numeric columns
    numeric_columns = [col for col in df.select_dtypes(include=[np.number]).columns if col != 'year']
    textual_columns = [col for col in df.columns if col not in numeric_columns]
    
    # Keep track of decimal precision for each numeric column
    decimal_places = {
        col: df[col].apply(lambda x: len(str(x).split('.')[-1]) if isinstance(x, float) else 0).max()
        for col in numeric_columns
    }
    
    # Extract the most recent data
    most_recent_data = df[df['year'] == max_year]
    
    # Prepare estimates for the specified number of years
    estimated_years = [max_year + i for i in range(1, num_years + 1)]
    print(f"Estimating data for years: {estimated_years}")
    
    estimated_data = []
    
    # Define constraints
    carbon_intensity_columns = [
        'provider-carbon-intensity-market-annual',
        'provider-carbon-intensity-average-consumption-hourly',
        'grid-carbon-intensity-average-consumption-annual',
        'grid-carbon-intensity-marginal-consumption-annual',
        'grid-carbon-intensity-average-production-annual',
        'grid-carbon-intensity'
    ]
    
    for year in estimated_years:
        print(f"Generating estimate for year: {year}")
        next_year_df = most_recent_data.copy()
        next_year_df['year'] = year
        
        for col in numeric_columns:
            if col in df.columns:
                historical_data = df[['year', 'cloud-provider', 'cloud-region', col]].dropna()
                latest_values = most_recent_data.set_index(['cloud-provider', 'cloud-region'])[col].to_dict()
                
                # Get all historical values for each provider-region pair
                all_values = {}
                for _, row in historical_data.iterrows():
                    key = (row['cloud-provider'], row['cloud-region'])
                    if key not in all_values:
                        all_values[key] = []
                    all_values[key].append((row['year'], row[col]))
                
                trends = {}
                for (provider, region), group in historical_data.groupby(['cloud-provider', 'cloud-region']):
                    if len(group) > 1:
                        group = group.sort_values(by='year')
                        trend = group[col].diff().mean()
                        trends[(provider, region)] = trend
                    else:
                        trends[(provider, region)] = 0
                
                new_values = []
                for idx, row in next_year_df.iterrows():
                    key = (row['cloud-provider'], row['cloud-region'])
                    trend = trends.get(key, 0)
                    latest_value = latest_values.get(key, np.nan)
                    
                    if not np.isnan(latest_value):
                        # If we have a value for the most recent year, use it with the trend
                        new_value = latest_value + trend
                        if col in carbon_intensity_columns:
                            new_value = max(0, new_value)  # Ensure carbon intensity does not go negative
                        elif col in ['provider-cfe-hourly', 'provider-cfe-annual']:
                            new_value = min(1.0, max(0, new_value))  # Clamp values between 0 and 1
                        elif col == 'power-usage-effectiveness':
                            new_value = max(1.04, new_value)  # Ensure PUE is >= 
                        new_values.append(round(new_value, decimal_places[col]))
                    else:
                        # If no value for most recent year, check if we have any historical value
                        previous_values = all_values.get(key, [])
                        if previous_values:
                            # Use the most recent historical value available
                            previous_values.sort(key=lambda x: x[0], reverse=True)
                            previous_value = previous_values[0][1]
                            new_values.append(previous_value)
                        else:
                            # No historical values at all
                            new_values.append("")
                
                next_year_df[col] = new_values
        
        estimated_data.append(next_year_df)
    
    # Concatenate estimated years and sort in descending order
    final_df = pd.concat(estimated_data)
    final_df = final_df.sort_values(by=['year', 'cloud-provider', 'cloud-region'], ascending=[False, True, True])
    
    # Specific handling for water-usage-effectiveness for us-east1
    final_df.loc[(final_df['cloud-region'] == 'us-east1') & 
                (final_df['water-usage-effectiveness'].isna()), 'water-usage-effectiveness'] = 0.1
    
    # Ensure empty columns remain blank
    for col in df.columns:
        if df[col].isna().all():
            final_df[col] = ""
    
    # Save output
    output_file = input_file.replace('.csv', f'_estimate.csv')
    final_df.to_csv(output_file, index=False)
    print(f"Estimates saved to {output_file}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python estimate_current_region_metadata.py <input_file> [num_years]")
    else:
        input_file = sys.argv[1]
        num_years = int(sys.argv[2]) if len(sys.argv) > 2 else 1
        estimate_next_years(input_file, num_years)
