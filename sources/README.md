# Sources archive

Preserved copies of the primary source documents behind the cloud region metadata, because providers
periodically move or remove these files. Organised by **data year** (the calendar year the data describes)
then provider. Fiscal-year sources are filed under the calendar year they were mapped to (see the
per-provider metrics docs in `metrics/<year>/` for the exact reporting periods).

Retrieved **2026-07-14** unless noted. If a link 404s later, this archive is the fallback.

## Archived

| Path | Document | Source URL | Covers |
|---|---|---|---|
| `2025/aws/fact-sheets/*.pdf` | 30 per-region/country AWS sustainability fact sheets | `sustainability.aboutamazon.com/aws-sustainability-fact-sheets/aws-fact-sheet-<loc>.pdf` | CY2022–2025 |
| `2025/aws/2025-aws-summary.pdf` | AWS sustainability summary | `sustainability.aboutamazon.com/2025-aws-summary.pdf` | CY2025 |
| `2025/aws/2025-amazon-sustainability-report.pdf` | Amazon sustainability report | `.../2025-amazon-sustainability-report.pdf` | CY2025 |
| `2025/aws/*-methodology.pdf` | PUE, renewable-energy, carbon, water-positive methodologies | `.../<name>-methodology.pdf` | — |
| `2025/aws/2025-*-assurance.pdf` | Renewable-energy, GHG scope 1-2 & 3, EAC assurance statements | `.../2025-*-assurance.pdf` | CY2025 |
| `2025/google/google-2026-environmental-report.pdf` | Google Environmental Report 2026 | `storage.googleapis.com/gweb-mobius-cdn/sustainability/uploads/7f477…​pdf` (issue #159) | CY2025 |
| `2024/google/google-2025-environmental-report.pdf` | Google Environmental Report 2025 | `gstatic.com/gumdrop/sustainability/google-2025-environmental-report.pdf` | CY2024 |
| `2023/google/google-2024-environmental-report.pdf` | Google Environmental Report 2024 | `gstatic.com/…/google-2024-environmental-report.pdf` | CY2023 |
| `2022/google/google-2023-environmental-report.pdf` | Google Environmental Report 2023 | `gstatic.com/…/google-2023-environmental-report.pdf` | CY2022 |
| `google-region-carbon-info/2019–2024.csv` | Google per-region CFE + grid carbon | `github.com/GoogleCloudPlatform/region-carbon-info` `data/yearly/` | 2019–2024 |
| `2025/microsoft/2026-Microsoft-Environmental-Data-Fact-Sheet.pdf` | MS Environmental Data Fact Sheet 2026 | `cdn-dynmedia-1.microsoft.com/…/2026-Microsoft-Environmental-Data-Fact-Sheet-PDF.pdf` | FY25 (→2025) |
| `2024/microsoft/2025-Microsoft-Environmental-Sustainability-Report.pdf` | MS Sustainability Report 2025 | `cdn-dynmedia-1.microsoft.com/…/2025-Microsoft-Environmental-Sustainability-Report.pdf` | FY24 (→2024) |
| `2025/oracle/clean-cloud-oci-fy2025.pdf` | Oracle Clean Cloud OCI Data Sheet FY2025 | `oracle.com/a/ocom/docs/corporate/citizenship/clean-cloud-oci.pdf` | FY24–FY25 |

## Gaps — still needed (help wanted / from private archives)

| Missing | Why it matters | How to get it |
|---|---|---|
| **Oracle CY2023 sustainability report** (per-region PUE) | Only source of Oracle per-region PUE now in the dataset | No stable public URL found; from a private archive or Oracle contact (issue #86) |
| **Electricity Maps yearly carbon intensity per zone** (e.g. `TH` for Bangkok) | Fills the blank `grid-carbon-intensity-*` cells for new regions | Free but **account-gated**, 5 downloads, 2021–2025, at `app.electricitymaps.com/datasets`; needs portal access (the project did this before via Electricity Maps directly — see GSF discussion #48 and issue #86) |
| **WattTime marginal carbon intensity** per region | `grid-carbon-intensity-marginal-consumption-annual` | API-gated (credentials required) — not freely downloadable |
| **Prior-year AWS fact sheets** (2024 and earlier, as-published) | Provider-of-record snapshots | Current fact sheets already carry CY2022–2025 data; earlier *as-published* PDFs would come from `web.archive.org` or a private archive |
| **Microsoft / Oracle earlier fact sheets** | Complete the back-catalogue | Private archives / web.archive.org |

*(Adrian to add items from his own archive where available.)*

## Note on size / git strategy
This archive is ~180 MB of PDFs (30 AWS fact sheets ≈ 90 MB, four Google reports ≈ 65 MB, two Microsoft
reports ≈ 40 MB). Committing binaries of this size directly bloats git history irreversibly — consider
**Git LFS** for `sources/**` (or keeping the archive as a release asset / external store) rather than a
plain commit. Left uncommitted pending that decision.
