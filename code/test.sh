#!/bin/bash

# Clean up any existing output file
rm -f test_input_estimate.csv

# Run the estimation algorithm
echo "Running estimation on test_input.csv..."
python3 estimate_current_region_metadata.py test_input.csv 2

# Check if the output file was created
if [ ! -f test_input_estimate.csv ]; then
    echo "ERROR: Output file test_input_estimate.csv was not created."
    exit 1
fi

# Compare the output with the expected output using diff
echo "Comparing test_input_estimate.csv with expected_output.csv..."
if diff -q test_input_estimate.csv expected_output.csv > /dev/null; then
    echo "TEST PASSED! Output matches expected file."
    exit 0
else
    echo "TEST FAILED! Output does not match expected file."
    echo "Differences:"
    diff test_input_estimate.csv expected_output.csv
    exit 1
fi 