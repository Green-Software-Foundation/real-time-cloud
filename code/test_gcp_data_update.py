"""
Tests for gcp_data_update.py to verify the fix for issue #151.

Issue: Google CFE values were incorrectly mapped to provider-cfe-annual
instead of provider-cfe-hourly. For Google Cloud, provider-cfe-annual
uses GOOGLE_ANNUAL_MATCHING_CLAIM (1.0) reflecting Google's fleet-wide
annual renewable energy matching claim, while the dataset's "Google CFE"
column represents hourly CFE values.
"""

import pytest
import pandas as pd
import sys
import os
from io import StringIO

# Add the code directory to the path so we can import the module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gcp_data_update import normalize_gcp_data, update_metadata_csv, GOOGLE_ANNUAL_MATCHING_CLAIM


@pytest.fixture
def sample_gcp_csv_data():
    """Sample GCP CSV data mimicking the real source format."""
    csv_content = """Google Cloud Region,Location,Google CFE,Grid carbon intensity (gCO2eq / kWh)
africa-south1,Johannesburg,0.15,656.85
asia-east1,Taiwan,0.17,439.29
europe-west10,Berlin,0.68,275.82
europe-north2,Stockholm,1.00,2.73
"""
    return pd.read_csv(StringIO(csv_content))


@pytest.fixture
def sample_metadata_df():
    """Sample metadata DataFrame with existing GCP entries for 2023."""
    data = {
        'year': [2023, 2023, 2024, 2024],
        'cloud-provider': ['Google Cloud', 'Google Cloud', 'Google Cloud', 'Google Cloud'],
        'cloud-region': ['africa-south1', 'asia-east1', 'africa-south1', 'asia-east1'],
        'location': ['Johannesburg', 'Taiwan', 'Johannesburg', 'Taiwan'],
        'geolocation': ['', '25.0375,121.5625', '', '25.0375,121.5625'],
        'provider-cfe-hourly': [0.16, 0.18, 0.16, 0.18],
        'provider-cfe-annual': [None, None, 0.15, 0.17],
        'grid-carbon-intensity-average-consumption-annual': [646.0, 451.0, 656.85, 439.29],
    }
    df = pd.DataFrame(data)
    # Add remaining columns that exist in the real CSV
    remaining_cols = [
        'cfe-region', 'em-zone-id', 'wt-region-id', 'power-usage-effectiveness',
        'water-usage-effectiveness', 'provider-carbon-intensity-market-annual',
        'provider-carbon-intensity-average-consumption-hourly',
        'grid-carbon-intensity-marginal-consumption-annual',
        'grid-carbon-intensity-average-production-annual', 'grid-carbon-intensity',
        'total-ICT-energy-consumption-annual', 'total-water-input',
        'renewable-energy-consumption', 'renewable-energy-consumption-goe',
        'renewable-energy-consumption-ppa', 'renewable-energy-consumption-onsite'
    ]
    for col in remaining_cols:
        df[col] = None
    return df


class TestNormalizeGcpData:
    """Tests for the normalize_gcp_data function."""

    def test_maps_google_cfe_to_provider_cfe_hourly(self, sample_gcp_csv_data):
        """Google CFE column should map to provider-cfe-hourly."""
        result = normalize_gcp_data(sample_gcp_csv_data, year=2024)

        assert 'provider-cfe-hourly' in result.columns
        assert 'provider-cfe-annual' in result.columns

        # Verify specific values are in hourly, not annual
        berlin_row = result[result['cloud-region'] == 'europe-west10']
        assert len(berlin_row) == 1
        assert berlin_row.iloc[0]['provider-cfe-hourly'] == 0.68

    def test_sets_provider_cfe_annual_to_google_claim(self, sample_gcp_csv_data):
        """provider-cfe-annual should use GOOGLE_ANNUAL_MATCHING_CLAIM."""
        result = normalize_gcp_data(sample_gcp_csv_data, year=2024)

        # All rows should have provider-cfe-annual equal to Google's annual claim
        assert all(result['provider-cfe-annual'] == GOOGLE_ANNUAL_MATCHING_CLAIM), \
            f"Expected all provider-cfe-annual to be {GOOGLE_ANNUAL_MATCHING_CLAIM}, " \
            f"got: {result['provider-cfe-annual'].tolist()}"

    def test_preserves_carbon_intensity(self, sample_gcp_csv_data):
        """Grid carbon intensity should be preserved."""
        result = normalize_gcp_data(sample_gcp_csv_data, year=2024)

        berlin_row = result[result['cloud-region'] == 'europe-west10']
        assert berlin_row.iloc[0]['grid-carbon-intensity-average-consumption-annual'] == 275.82

    def test_includes_all_regions(self, sample_gcp_csv_data):
        """All regions from source should be present."""
        result = normalize_gcp_data(sample_gcp_csv_data, year=2024)

        expected_regions = {'africa-south1', 'asia-east1', 'europe-west10', 'europe-north2'}
        actual_regions = set(result['cloud-region'].tolist())
        assert actual_regions == expected_regions

    def test_stockholm_cfe_hourly_is_one(self, sample_gcp_csv_data):
        """Even when Google CFE is 1.0 (e.g., Stockholm), it should go to hourly."""
        result = normalize_gcp_data(sample_gcp_csv_data, year=2024)

        stockholm_row = result[result['cloud-region'] == 'europe-north2']
        assert stockholm_row.iloc[0]['provider-cfe-hourly'] == 1.0
        assert stockholm_row.iloc[0]['provider-cfe-annual'] == GOOGLE_ANNUAL_MATCHING_CLAIM


class TestUpdateMetadataCsv:
    """Tests for the update_metadata_csv function."""

    def test_updates_existing_rows_with_correct_columns(self, sample_gcp_csv_data, sample_metadata_df):
        """When updating existing 2024 rows, hourly CFE should be updated."""
        normalized = normalize_gcp_data(sample_gcp_csv_data, year=2024)

        # Filter to only regions that exist in our sample metadata
        normalized = normalized[normalized['cloud-region'].isin(['africa-south1', 'asia-east1'])]

        # Write sample metadata to a temp CSV so update_metadata_csv can read it
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            sample_metadata_df.to_csv(f.name, index=False)
            temp_path = f.name

        try:
            updated_df, has_changes, stats = update_metadata_csv(normalized, temp_path)

            assert has_changes, "Expected changes to be detected"

            # Check africa-south1 2024 row
            row = updated_df[
                (updated_df['cloud-provider'] == 'Google Cloud') &
                (updated_df['cloud-region'] == 'africa-south1') &
                (updated_df['year'] == 2024)
            ]
            assert len(row) == 1
            # Google CFE from source is 0.15 for africa-south1 -> should be in hourly
            assert row.iloc[0]['provider-cfe-hourly'] == 0.15
            # Annual should reflect Google's fleet-wide claim
            assert row.iloc[0]['provider-cfe-annual'] == GOOGLE_ANNUAL_MATCHING_CLAIM
        finally:
            os.unlink(temp_path)

    def test_new_region_gets_hourly_and_annual(self, sample_gcp_csv_data, sample_metadata_df):
        """New regions (e.g., europe-west10) should get both hourly and annual CFE set."""
        normalized = normalize_gcp_data(sample_gcp_csv_data, year=2024)

        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            sample_metadata_df.to_csv(f.name, index=False)
            temp_path = f.name

        try:
            updated_df, has_changes, stats = update_metadata_csv(normalized, temp_path)

            assert has_changes, "Expected changes to be detected"

            # Check europe-west10 row (new region for 2024 in this metadata)
            row = updated_df[
                (updated_df['cloud-provider'] == 'Google Cloud') &
                (updated_df['cloud-region'] == 'europe-west10') &
                (updated_df['year'] == 2024)
            ]
            assert len(row) == 1, f"Expected europe-west10 2024 row, got {len(row)} rows"
            assert row.iloc[0]['provider-cfe-hourly'] == 0.68
            assert row.iloc[0]['provider-cfe-annual'] == GOOGLE_ANNUAL_MATCHING_CLAIM
        finally:
            os.unlink(temp_path)

    def test_berlin_example_from_issue(self, sample_gcp_csv_data, sample_metadata_df):
        """
        Regression test for the specific example from issue #151.
        europe-west10 (Berlin) should have:
        - provider-cfe-hourly = 0.68 (from Google CFE source)
        - provider-cfe-annual = GOOGLE_ANNUAL_MATCHING_CLAIM (Google's fleet-wide annual claim)
        """
        normalized = normalize_gcp_data(sample_gcp_csv_data, year=2024)

        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            sample_metadata_df.to_csv(f.name, index=False)
            temp_path = f.name

        try:
            updated_df, has_changes, stats = update_metadata_csv(normalized, temp_path)

            berlin = updated_df[
                (updated_df['cloud-provider'] == 'Google Cloud') &
                (updated_df['cloud-region'] == 'europe-west10')
            ]
            assert len(berlin) == 1
            assert berlin.iloc[0]['provider-cfe-hourly'] == 0.68, \
                f"provider-cfe-hourly should be 0.68, got {berlin.iloc[0]['provider-cfe-hourly']}"
            assert berlin.iloc[0]['provider-cfe-annual'] == GOOGLE_ANNUAL_MATCHING_CLAIM, \
                f"provider-cfe-annual should be {GOOGLE_ANNUAL_MATCHING_CLAIM}, " \
                f"got {berlin.iloc[0]['provider-cfe-annual']}"
        finally:
            os.unlink(temp_path)


class TestIntegration:
    """Integration tests using real CSV data patterns."""

    def test_real_2024_source_data_pattern(self):
        """
        Test with the actual 2024 source data structure from Google.
        This ensures the normalization handles the real CSV format correctly.
        """
        csv_content = """Google Cloud Region,Location,Google CFE,Grid carbon intensity (gCO2eq / kWh)
europe-west10,Berlin,0.68,275.82
me-central2,Dammam,0.01,382.23
northamerica-south1,Mexico,0.19,305.00
us-east2,Georgia,0.42,340.42
us-east5,Columbus,0.62,323.05
"""
        df = pd.read_csv(StringIO(csv_content))
        result = normalize_gcp_data(df, year=2024)

        # All should use Google's fleet-wide annual matching claim
        assert all(result['provider-cfe-annual'] == GOOGLE_ANNUAL_MATCHING_CLAIM)

        # Hourly should match source
        berlin = result[result['cloud-region'] == 'europe-west10']
        assert berlin.iloc[0]['provider-cfe-hourly'] == 0.68

        mexico = result[result['cloud-region'] == 'northamerica-south1']
        assert mexico.iloc[0]['provider-cfe-hourly'] == 0.19

        us_east5 = result[result['cloud-region'] == 'us-east5']
        assert us_east5.iloc[0]['provider-cfe-hourly'] == 0.62
