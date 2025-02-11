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

Run the script, it works despit some warnings
```
% python code/estimate_current_region_metadata.py "Cloud Region Metadata.csv"           
/Users/adriancockcroft/Documents/GitHub/real-time-cloud/venv/lib/python3.11/site-packages/numpy/_core/_methods.py:52: RuntimeWarning: invalid value encountered in reduce
  return umr_sum(a, axis, dtype, out, keepdims, initial, where)
/Users/adriancockcroft/Documents/GitHub/real-time-cloud/venv/lib/python3.11/site-packages/numpy/_core/_methods.py:52: RuntimeWarning: invalid value encountered in reduce
  return umr_sum(a, axis, dtype, out, keepdims, initial, where)
Estimates for 2024 and 2025 have been saved to Cloud Region Metadata_estimate.csv.
```
