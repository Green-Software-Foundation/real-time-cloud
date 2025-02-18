# Generating Estimates for Current Year Metadata

Python code to automatically generate trended data for current years (two years since 2023 data is all we have until mid-2025)                   

```
python3 -m venv venv
```
Windows:
```
venv\Scripts\activate
```
macOS/Linux:
```
source venv/bin/activate
```
```
pip install -r requirements.txt
```

Run the script, by default it caluculates one year, with an optional parameter it will calculate N years.
```
% python code/estimate_current_region_metadata.py Cloud_Region_Metadata.csv 2
Most recent year in dataset: 2023
Estimating data for years: [np.int64(2024), np.int64(2025)]
Generating estimate for year: 2024
Generating estimate for year: 2025
Estimates saved to Cloud_Region_Metadata_estimate.csv
```
