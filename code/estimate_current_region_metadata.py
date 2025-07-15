#!/usr/bin/env python3
"""
Cloud Region Metadata Estimator

Generates estimates for future cloud region metadata based on historical trends,
Compliant with Green Software Foundation Real Time Cloud specification.

Author: Generated based on GSF Real Time Cloud project requirements
License: MIT (compatible with GSF project licensing)
"""

import pandas as pd
import numpy as np
import sys
import logging
import warnings
from typing import Dict, List, Tuple, Optional, Any, Set
from pathlib import Path
from datetime import datetime
import argparse
from dataclasses import dataclass

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@dataclass
class EstimationConfig:
    """Configuration for estimation parameters"""
    min_pue: float = 1.0  # Theoretical minimum PUE
    max_cfe: float = 1.0  # Maximum CFE percentage
    min_cfe: float = 0.0  # Minimum CFE percentage
    min_carbon_intensity: float = 0.0  # Minimum carbon intensity
    max_estimate_years: int = 3  # Maximum years to estimate into future
    min_data_points: int = 2  # Minimum data points required for trend calculation
    outlier_threshold: float = 3.0  # Z-score threshold for outlier detection


class CloudMetadataEstimator:
    """
    Estimates future cloud region metadata based on historical trends.
    
    Implements improved statistical methods and validation according to
    Green Software Foundation specification requirements.
    """
    
    # Required columns according to GSF specification
    REQUIRED_COLUMNS = {
        'year', 'cloud-provider', 'cloud-region'
    }
    
    # Numeric columns that should be validated
    CARBON_INTENSITY_COLUMNS = {
        'provider-carbon-intensity-market-annual',
        'provider-carbon-intensity-average-consumption-hourly', 
        'grid-carbon-intensity-average-consumption-annual',
        'grid-carbon-intensity-marginal-consumption-annual',
        'grid-carbon-intensity-average-production-annual',
        'grid-carbon-intensity'
    }
    
    CFE_COLUMNS = {
        'provider-cfe-hourly',
        'provider-cfe-annual'
    }
    
    EFFICIENCY_COLUMNS = {
        'power-usage-effectiveness',
        'water-usage-effectiveness'
    }
    
    def __init__(self, config: Optional[EstimationConfig] = None):
        """Initialize estimator with configuration."""
        self.config = config or EstimationConfig()
        self.df: Optional[pd.DataFrame] = None
        self.numeric_columns: Set[str] = set()
        self.estimation_metadata: Dict[str, Any] = {}
        
    def load_and_validate_data(self, input_file: str) -> None:
        """
        Load and validate input dataset.
        
        Args:
            input_file: Path to input CSV file
            
        Raises:
            FileNotFoundError: If input file doesn't exist
            ValueError: If data validation fails
        """
        input_path = Path(input_file)
        if not input_path.exists():
            raise FileNotFoundError(f"Input file not found: {input_file}")
            
        logger.info(f"Loading dataset from {input_file}")
        
        try:
            self.df = pd.read_csv(input_file)
        except Exception as e:
            raise ValueError(f"Failed to read CSV file: {e}")
            
        logger.info(f"Loaded {len(self.df)} rows and {len(self.df.columns)} columns")
        
        # Validate required columns
        missing_cols = self.REQUIRED_COLUMNS - set(self.df.columns)
        if missing_cols:
            raise ValueError(f"Missing required columns: {missing_cols}")
            
        # Validate year column
        try:
            self.df['year'] = pd.to_numeric(self.df['year'], errors='coerce')
            invalid_years = self.df['year'].isna().sum()
            if invalid_years > 0:
                logger.warning(f"Found {invalid_years} invalid year values")
                
            self.df = self.df.dropna(subset=['year'])
            self.df['year'] = self.df['year'].astype(int)
            
        except Exception as e:
            raise ValueError(f"Failed to process year column: {e}")
            
        # Identify numeric columns (excluding year and identifier columns)
        identifier_cols = {'year', 'cloud-provider', 'cloud-region'}
        self.numeric_columns = set(
            col for col in self.df.select_dtypes(include=[np.number]).columns 
            if col not in identifier_cols
        )
        
        logger.info(f"Identified {len(self.numeric_columns)} numeric columns for estimation")
        
        # Validate data ranges
        self._validate_data_ranges()
        
    def _validate_data_ranges(self) -> None:
        """Validate that data values are within expected ranges."""
        current_year = datetime.now().year
        
        # Check year range
        max_year = self.df['year'].max()
        min_year = self.df['year'].min()
        
        if max_year > current_year:
            logger.warning(f"Data contains future years (max: {max_year}, current: {current_year})")
            
        if current_year - max_year > 2:
            logger.warning(f"Data may be outdated (latest: {max_year}, current: {current_year})")
            
        # Validate CFE percentages
        for col in self.CFE_COLUMNS.intersection(self.numeric_columns):
            invalid_cfe = self.df[(self.df[col] < 0) | (self.df[col] > 1)][col].dropna()
            if len(invalid_cfe) > 0:
                logger.warning(f"Found {len(invalid_cfe)} invalid CFE values in {col} (outside 0-1 range)")
                
        # Validate PUE values
        if 'power-usage-effectiveness' in self.numeric_columns:
            invalid_pue = self.df[self.df['power-usage-effectiveness'] < 1.0]['power-usage-effectiveness'].dropna()
            if len(invalid_pue) > 0:
                logger.warning(f"Found {len(invalid_pue)} invalid PUE values < 1.0")
                
        # Validate carbon intensity (should be non-negative)
        for col in self.CARBON_INTENSITY_COLUMNS.intersection(self.numeric_columns):
            negative_ci = self.df[self.df[col] < 0][col].dropna()
            if len(negative_ci) > 0:
                logger.warning(f"Found {len(negative_ci)} negative carbon intensity values in {col}")
    
    def _detect_outliers(self, series: pd.Series) -> pd.Series:
        """
        Detect outliers using z-score method.
        
        Args:
            series: Data series to check for outliers
            
        Returns:
            Boolean series indicating outliers
        """
        if len(series.dropna()) < 3:
            return pd.Series([False] * len(series), index=series.index)
            
        z_scores = np.abs((series - series.mean()) / series.std())
        return z_scores > self.config.outlier_threshold
    
    def _calculate_weighted_trend(self, group: pd.DataFrame, column: str) -> float:
        """
        Calculate weighted trend giving more importance to recent data.
        
        Args:
            group: Grouped data for a provider-region pair
            column: Column to calculate trend for
            
        Returns:
            Weighted trend value
        """
        if len(group) < self.config.min_data_points:
            return 0.0
            
        group = group.sort_values('year').dropna(subset=[column])
        
        if len(group) < self.config.min_data_points:
            return 0.0
            
        # Remove outliers
        outliers = self._detect_outliers(group[column])
        group_clean = group[~outliers]
        
        if len(group_clean) < self.config.min_data_points:
            logger.debug(f"Too many outliers detected for trend calculation")
            return 0.0
            
        # Calculate differences between consecutive years
        diffs = group_clean[column].diff().dropna()
        
        if len(diffs) == 0:
            return 0.0
            
        # Apply exponential weighting (more recent = higher weight)
        weights = np.exp(np.linspace(0, 1, len(diffs)))
        weights = weights / weights.sum()
        
        return np.average(diffs, weights=weights)
    
    def _apply_constraints(self, column: str, value: float) -> float:
        """
        Apply business logic constraints to estimated values.
        
        Args:
            column: Column name
            value: Estimated value
            
        Returns:
            Constrained value
        """
        if np.isnan(value):
            return value
            
        # Carbon intensity constraints
        if column in self.CARBON_INTENSITY_COLUMNS:
            return max(self.config.min_carbon_intensity, value)
            
        # CFE percentage constraints  
        elif column in self.CFE_COLUMNS:
            return np.clip(value, self.config.min_cfe, self.config.max_cfe)
            
        # PUE constraints
        elif column == 'power-usage-effectiveness':
            return max(self.config.min_pue, value)
            
        # WUE constraints (non-negative)
        elif column == 'water-usage-effectiveness':
            return max(0.0, value)
            
        return value
    
    def _preserve_precision(self, column: str) -> int:
        """
        Determine appropriate decimal precision for a column.
        
        Args:
            column: Column name
            
        Returns:
            Number of decimal places to preserve
        """
        if column not in self.numeric_columns:
            return 0
            
        values = self.df[column].dropna()
        if len(values) == 0:
            return 3  # Default precision
            
        # Calculate decimal places for each value
        decimal_places = []
        for val in values:
            if isinstance(val, (int, np.integer)):
                decimal_places.append(0)
            else:
                str_val = f"{val:.10f}".rstrip('0')
                if '.' in str_val:
                    decimal_places.append(len(str_val.split('.')[1]))
                else:
                    decimal_places.append(0)
                    
        return min(max(decimal_places), 6)  # Cap at 6 decimal places
    
    def estimate_future_years(self, num_years: int = 1) -> pd.DataFrame:
        """
        Generate estimates for future years.
        
        Args:
            num_years: Number of years to estimate
            
        Returns:
            DataFrame with estimated values
            
        Raises:
            ValueError: If estimation parameters are invalid
        """
        if self.df is None:
            raise ValueError("No data loaded. Call load_and_validate_data() first.")
            
        if num_years < 1 or num_years > self.config.max_estimate_years:
            raise ValueError(f"num_years must be between 1 and {self.config.max_estimate_years}")
            
        max_year = self.df['year'].max()
        current_year = datetime.now().year
        
        # Warn if data is old
        if current_year - max_year > 2:
            logger.warning(f"Estimating based on data from {max_year}, which is {current_year - max_year} years old")
            
        logger.info(f"Generating estimates for {num_years} year(s) based on data through {max_year}")
        
        # Get most recent data
        most_recent_data = self.df[self.df['year'] == max_year].copy()
        
        if len(most_recent_data) == 0:
            raise ValueError(f"No data found for most recent year {max_year}")
            
        estimated_years = list(range(max_year + 1, max_year + num_years + 1))
        estimated_data = []
        
        # Calculate trends for each provider-region-column combination
        trends = {}
        uncertainties = {}
        
        for column in self.numeric_columns:
            trends[column] = {}
            uncertainties[column] = {}
            
            historical_data = self.df[['year', 'cloud-provider', 'cloud-region', column]].dropna()
            
            for (provider, region), group in historical_data.groupby(['cloud-provider', 'cloud-region']):
                key = (provider, region)
                trend = self._calculate_weighted_trend(group, column)
                trends[column][key] = trend
                
                # Calculate uncertainty based on trend variance
                if len(group) >= 3:
                    diffs = group.sort_values('year')[column].diff().dropna()
                    uncertainties[column][key] = diffs.std() if len(diffs) > 1 else 0.0
                else:
                    uncertainties[column][key] = 0.0
        
        # Generate estimates for each year
        for year in estimated_years:
            logger.info(f"Estimating year {year}")
            year_estimate = most_recent_data.copy()
            year_estimate['year'] = year
            
            years_ahead = year - max_year
            
            for column in self.numeric_columns:
                new_values = []
                precision = self._preserve_precision(column)
                
                for _, row in year_estimate.iterrows():
                    key = (row['cloud-provider'], row['cloud-region'])
                    
                    if key in trends[column]:
                        trend = trends[column][key]
                        uncertainty = uncertainties[column].get(key, 0.0)
                        
                        # Get the most recent value
                        latest_value = row[column]
                        
                        if pd.notna(latest_value):
                            # Apply trend with years multiplier
                            estimated_value = latest_value + (trend * years_ahead)
                            
                            # Apply constraints
                            estimated_value = self._apply_constraints(column, estimated_value)
                            
                            # Round to appropriate precision
                            if precision > 0:
                                new_values.append(round(estimated_value, precision))
                            else:
                                new_values.append(int(round(estimated_value)))
                        else:
                            # No recent value available
                            new_values.append("NA")
                    else:
                        # No trend data available
                        if pd.notna(row[column]):
                            new_values.append(row[column])  # Keep most recent value
                        else:
                            new_values.append("NA")
                
                year_estimate[column] = new_values
            
            estimated_data.append(year_estimate)
        
        # Combine all estimates
        final_df = pd.concat(estimated_data, ignore_index=True)
        final_df = final_df.sort_values(['year', 'cloud-provider', 'cloud-region'], 
                                       ascending=[False, True, True])
        
        # Store estimation metadata
        self.estimation_metadata = {
            'estimation_date': datetime.now().isoformat(),
            'base_year': max_year,
            'estimated_years': estimated_years,
            'num_regions': len(most_recent_data),
            'methodology': 'weighted_trend_extrapolation',
            'outlier_threshold': self.config.outlier_threshold,
            'min_data_points': self.config.min_data_points
        }
        
        logger.info(f"Generated estimates for {len(final_df)} region-year combinations")
        return final_df
    
    def save_estimates(self, estimates_df: pd.DataFrame, output_file: str) -> None:
        """
        Save estimates to CSV file with metadata.
        
        Args:
            estimates_df: DataFrame with estimates
            output_file: Output file path
        """
        # Ensure output directory exists
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Save main estimates
        estimates_df.to_csv(output_file, index=False, na_rep='NA')
        logger.info(f"Estimates saved to {output_file}")
        
        # Save metadata
        metadata_file = output_path.with_suffix('.metadata.json')
        import json
        with open(metadata_file, 'w') as f:
            json.dump(self.estimation_metadata, f, indent=2)
        logger.info(f"Estimation metadata saved to {metadata_file}")


def main():
    """Main function with command line interface."""
    parser = argparse.ArgumentParser(
        description='Generate cloud region metadata estimates based on historical trends',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python estimate_metadata.py data.csv
  python estimate_metadata.py data.csv --years 2 --output estimates.csv
  python estimate_metadata.py data.csv --years 3 --min-pue 1.05 --verbose
        """
    )
    
    parser.add_argument('input_file', help='Input CSV file with historical data')
    parser.add_argument('--years', type=int, default=1, 
                       help='Number of years to estimate (default: 1)')
    parser.add_argument('--output', help='Output file path (default: input_file_estimate.csv)')
    parser.add_argument('--min-pue', type=float, default=1.0,
                       help='Minimum PUE value (default: 1.0)')
    parser.add_argument('--outlier-threshold', type=float, default=3.0,
                       help='Z-score threshold for outlier detection (default: 3.0)')
    parser.add_argument('--verbose', action='store_true',
                       help='Enable verbose logging')
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Configure estimation parameters
    config = EstimationConfig(
        min_pue=args.min_pue,
        outlier_threshold=args.outlier_threshold
    )
    
    try:
        # Initialize estimator
        estimator = CloudMetadataEstimator(config)
        
        # Load and validate data
        estimator.load_and_validate_data(args.input_file)
        
        # Generate estimates
        estimates = estimator.estimate_future_years(args.years)
        
        # Determine output file
        if args.output:
            output_file = args.output
        else:
            input_path = Path(args.input_file)
            output_file = str(input_path.with_suffix('').with_suffix('')) + '_estimate.csv'
        
        # Save results
        estimator.save_estimates(estimates, output_file)
        
        logger.info("Estimation completed successfully")
        
    except Exception as e:
        logger.error(f"Estimation failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
