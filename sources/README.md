# Sources archive

Preserved copies of the primary source documents behind the cloud region metadata, because providers
periodically move or remove these files. If a link 404s later, this archive is the fallback.

## Layout

```
sources/<data-year>/<company>/[fact-sheets/]<document>
```

- **data year** — the calendar year the data *describes*, not the year the document was published. A
  provider's report published in mid-2026 covering calendar 2025 is filed under `2025/`. Fiscal-year
  sources are filed under the calendar year they were mapped to; see `metrics/<year>/` for the exact
  reporting period each provider used.
- **company** — `amazon`, `google`, `microsoft`, `oracle`. The company name, not the cloud brand, since
  several of these documents are corporate-wide reports that cover far more than the cloud business.
- `fact-sheets/` holds the per-region / per-country sheets where a provider publishes them.

88 files. Retrieved **2026-07-14** unless noted.

```
2022/  amazon (1)  google (1)  microsoft (27, incl. 26 fact sheets)
2023/  amazon (2)  google (1)  microsoft (1)
2024/  amazon (2)  google (1)  microsoft (1)
2025/  amazon (41, incl. 30 fact sheets)  google (1)  microsoft (1)  oracle (1)
google-region-carbon-info/  6 CSVs (2019-2024)
```

## Archived

### Amazon

| Path | Document | Source URL | Covers |
|---|---|---|---|
| `2022/amazon/2022-sustainability-report.pdf` | Amazon Sustainability Report 2022 | `sustainability.aboutamazon.com/2022-sustainability-report.pdf` | CY2022 |
| `2023/amazon/2023-sustainability-report.pdf` | Amazon Sustainability Report 2023 | `sustainability.aboutamazon.com/2023-amazon-sustainability-report.pdf` (published under a different filename than the local copy) | CY2023 |
| `2023/amazon/AWS_renewable_energy_2023.csv` | AWS renewable energy project list | `sustainability.aboutamazon.com` renewable-energy project data | CY2023 |
| `2024/amazon/2024-amazon-sustainability-report-aws-summary.pdf` | Amazon Sustainability Report 2024, AWS summary | `sustainability.aboutamazon.com/2024-amazon-sustainability-report-aws-summary.pdf` | CY2024 |
| `2024/amazon/Amazon-Carbon-Free-Energy-Projects-2024.csv` | Amazon carbon-free energy project list | `sustainability.aboutamazon.com` renewable-energy project data | CY2024 |
| `2025/amazon/2025-amazon-sustainability-report.pdf` | Amazon Sustainability Report 2025 | `sustainability.aboutamazon.com/2025-amazon-sustainability-report.pdf` | CY2025 |
| `2025/amazon/2025-aws-summary.pdf` | AWS sustainability summary | `sustainability.aboutamazon.com/2025-aws-summary.pdf` | CY2025 |
| `2025/amazon/Amazon-Carbon-Free-Energy-Projects-2025.csv` | Amazon carbon-free energy project list | `sustainability.aboutamazon.com` renewable-energy project data | CY2025 |
| `2025/amazon/fact-sheets/*.pdf` | 30 per-region / per-country AWS sustainability fact sheets | `sustainability.aboutamazon.com/aws-sustainability-fact-sheets/aws-fact-sheet-<loc>.pdf` | CY2022–2025 |
| `2025/amazon/*-methodology.pdf` | PUE, renewable-energy, carbon and water-positive methodologies | `sustainability.aboutamazon.com/<name>-methodology.pdf` | — |
| `2025/amazon/2025-*-assurance.pdf` | Renewable-energy, GHG scope 1-2, GHG scope 3 and environmental-attribute-certificate assurance statements | `sustainability.aboutamazon.com/2025-*-assurance.pdf` | CY2025 |

The AWS fact sheets each carry a four-year history, so the single `2025/` copy is the source for
CY2022–2025 PUE, WUE and water withdrawal — there is no need for a per-year copy unless an
*as-published* snapshot is wanted (see gaps).

### Google

| Path | Document | Source URL | Covers |
|---|---|---|---|
| `2022/google/google-2023-environmental-report.pdf` | Google Environmental Report 2023 | `gstatic.com/…/google-2023-environmental-report.pdf` | CY2022 |
| `2023/google/google-2024-environmental-report.pdf` | Google Environmental Report 2024 | `gstatic.com/…/google-2024-environmental-report.pdf` | CY2023 |
| `2024/google/google-2025-environmental-report.pdf` | Google Environmental Report 2025 | `gstatic.com/gumdrop/sustainability/google-2025-environmental-report.pdf` | CY2024 |
| `2025/google/google-2026-environmental-report.pdf` | Google Environmental Report 2026 | `storage.googleapis.com/gweb-mobius-cdn/sustainability/uploads/7f477…pdf` (issue #159) | CY2025 |
| `google-region-carbon-info/2019.csv` … `2024.csv` | Google per-region carbon-free energy and grid carbon intensity | `github.com/GoogleCloudPlatform/region-carbon-info` → `data/yearly/` | 2019–2024 |

Note that Google names each report for its *publication* year, one ahead of the data year it is filed
under here.

### Microsoft

| Path | Document | Source URL | Covers |
|---|---|---|---|
| `2022/microsoft/2022-Environmental-Sustainability-Report.pdf` | MS Environmental Sustainability Report 2022 | `msftstories.thesourcemediaassets.com/sites/42/2023/05/2022-Environmental-Sustainability-Report.pdf` — filename matches, but the file served there is ~100 KB smaller than the archived copy, so treat as probable rather than confirmed | FY22 (→2022) |
| `2022/microsoft/fact-sheets/*.pdf` | 26 per-region datacenter fact sheets, named `Location (Azure region).pdf` | `datacenters.microsoft.com/globe/fact-sheets/` | FY22 (→2022) |
| `2023/microsoft/The-2023-Impact-Summary.pdf` | MS 2023 Impact Summary | not recorded | FY23 (→2023) |
| `2024/microsoft/2025-Microsoft-Environmental-Sustainability-Report.pdf` | MS Environmental Sustainability Report 2025 | `cdn-dynmedia-1.microsoft.com/…/2025-Microsoft-Environmental-Sustainability-Report.pdf` | FY24 (→2024) |
| `2025/microsoft/2026-Microsoft-Environmental-Data-Fact-Sheet.pdf` | MS Environmental Data Fact Sheet 2026 | `cdn-dynmedia-1.microsoft.com/…/2026-Microsoft-Environmental-Data-Fact-Sheet-PDF.pdf` | FY25 (→2025) |

The 2022 fact sheets are the **only** per-region PUE/WUE Azure has ever published; every later Azure
report is macro-regional (Americas / APAC / EMEA), which is why the dataset still leans on them. They
are also the source for the Helsinki figures now carried as `finlandcentral`. Microsoft's current
reports are listed at `microsoft.com/en-us/corporate-responsibility/reports-hub`.

### Oracle

| Path | Document | Source URL | Covers |
|---|---|---|---|
| `2025/oracle/clean-cloud-oci-fy2025.pdf` | Oracle Clean Cloud OCI Data Sheet FY2025 | `oracle.com/a/ocom/docs/corporate/citizenship/clean-cloud-oci.pdf` | FY24–FY25 |

## Relationship to `sup_file/`

Three CSVs appear both here and in `sup_file/`, and they are **not** interchangeable:

- `Amazon-Carbon-Free-Energy-Projects-2024.csv` and `-2025.csv` — identical to the `sup_file/` copies
  apart from a trailing newline.
- `AWS_renewable_energy_2023.csv` — **different files**. The copy here is as-published; the `sup_file/`
  copy is an annotated working version with two extra derived columns (`aws_percent`, `aws_size_MW`)
  and a different row set. Use the `sources/` copy as the provenance record and the `sup_file/` copy
  as the working input.

## Gaps — still needed (help wanted / from private archives)

| Missing | Why it matters | How to get it |
|---|---|---|
| **Oracle CY2023 sustainability report** (per-region PUE) | Only source of Oracle per-region PUE now in the dataset | No stable public URL found; from a private archive or an Oracle contact (issue #86) |
| **Oracle FY2023/FY2024 data sheets** | Oracle history before FY2025 | Oracle replaces `clean-cloud-oci.pdf` in place, so prior versions only exist in archives |
| **Electricity Maps yearly carbon intensity per zone** (e.g. `TH` for Bangkok, `FI` for 2019–2020, `SE` for 2021) | Fills the blank `grid-carbon-intensity-*` cells for new regions, and the three cells cleared when the mis-transcribed Google/AWS rows were restated | Free but **account-gated**, 5 downloads, 2021–2025, at `app.electricitymaps.com/datasets`; needs portal access (the project did this before via Electricity Maps directly — see GSF discussion #48 and issue #86) |
| **WattTime marginal carbon intensity** per region | `grid-carbon-intensity-marginal-consumption-annual` | API-gated (credentials required) — not freely downloadable |
| **Prior-year AWS fact sheets** (2024 and earlier, *as published*) | Provider-of-record snapshots | The current sheets already carry CY2022–2025 data; earlier as-published PDFs would come from `web.archive.org` or a private archive |
| **Microsoft source URLs** for the 2022 and 2023 reports | Provenance | Recorded as "not recorded"/"probable" above; fill in if the original download location is known |
| **Microsoft / Oracle earlier fact sheets** | Complete the back-catalogue | Private archives / web.archive.org |

## Note on size / git strategy

This archive is ~277 MB of PDFs — the 30 AWS fact sheets are ~80 MB, the four Google reports ~63 MB,
the Microsoft reports and 26 fact sheets ~73 MB, and the Amazon corporate reports ~53 MB.

About 190 MB of that is already committed to this repository as ordinary git objects, so the history
cost has largely been paid and is not reversible without a rewrite. The remainder is committed the same
way for consistency. If the archive keeps growing year over year, moving `sources/**` to **Git LFS**,
a release asset, or an external store is worth revisiting before the next annual update — a rewrite
gets more expensive with every year added.

`.DS_Store` files are ignored via the repository `.gitignore`.
