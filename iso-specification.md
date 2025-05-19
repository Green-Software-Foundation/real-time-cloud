# Cloud Region Metadata Specification

## Foreword

ISO (the International Organization for Standardization) is a worldwide federation of national standards bodies (ISO member bodies). The work of preparing International Standards is normally carried out through ISO technical committees. Each member body interested in a subject for which a technical committee has been established has the right to be represented on that committee. International organizations, governmental and non-governmental, in liaison with ISO, also take part in the work.

Draft International Standards adopted by the technical committees are circulated to the member bodies for voting. Publication as an International Standard requires approval by at least 75% of the member bodies casting a vote.

Attention is drawn to the possibility that some of the elements of this document may be the subject of patent rights. ISO shall not be held responsible for identifying any or all such patent rights.

ISO/IEC XXXXX was prepared by Technical Committee ISO/IEC JTC 1, Information technology, Subcommittee SC XX, Cloud computing.

## Introduction

Cloud providers are recognized as significant global procurers of renewable energy. This International Standard addresses the need for accurate and timely carbon information provision to customers utilizing cloud services, aiming to align with regulatory requirements across various jurisdictions.

Historically, cloud providers have supplied carbon information to their customers every month, with a delay of several months, and provided public information on an annual basis with six to eighteen months lag. Consequently, customers have been compelled to estimate the real-time carbon footprint of their cloud workloads using incomplete public information.

Cloud providers will be required to supply carbon metrics to meet regulatory standards in the UK, Europe, California, and emerging elsewhere. So far, cloud providers have developed custom silicon and system designs to optimize low power consumption, mitigated the carbon footprint within supply chains, and invested in renewable energy production. They have published generic estimates of efficiency gains achieved with renewable energy purchases compared to data centre alternatives. Still, the data needed for a customer to make the same comparison for a specific workload, and to make comparisons across cloud regions, is lacking.

This International Standard outlines the necessity for real-time carbon reporting to address these concerns and proposes a standardized approach to achieve accurate and timely carbon footprint estimates for cloud workloads. Additionally, it highlights the significance of metadata disclosure by cloud providers for the regions they operate in and the ongoing efforts to consolidate and distribute this information as a singular data source.

## 1 Scope

This International Standard aims to enhance the accuracy of the carbon emissions model for cloud-based workloads. It establishes a standard mechanism for cloud providers to share detailed and useful information using the same data schema. The scope includes enabling real-time updates to provide minute-level granularity for energy usage and hourly or daily granularity for carbon intensity.

This International Standard covers:

a) Cloud Region Metadata:
   - Definition of standard parameters for cloud region metadata, including cloud provider and region specifications.
   - Guidelines for annual updates and data lag management (6-18 months), with emphasis on specifying the year or using the latest available data.
   - Clarification of the annual average location-based marginal grid-carbon-intensity value for SCI-o and its availability and handling of not-available (NA) data.

b) Standardizing Carbon Models and Data Reporting:
   - Identification and clarification of the multiple carbon models used by different cloud providers.
   - Addressing the variability of carbon data availability and handling of blank or not-available metrics.

c) Real-time Data Lookup and Provider Keys:
   - Definition of the process for real-time lookup of cloud region data via APIs provided by data providers such as Electricity Maps and WattTime.
   - Establishment of protocols for annual average carbon intensity reporting for each grid region under each cloud provider's model.

d) Carbon-Free Energy and Renewable Energy Definitions:
   - Definition of carbon-free energy and its inclusion of nuclear energy, which is distinct from the definition of renewable energy.
   - Addressing the absence of carbon-free energy data for regions that are not yet operational.

e) Power and Water Usage Effectiveness (PUE and WUE):
   - Standardization of reporting of power usage effectiveness (PUE) and water usage effectiveness (WUE) for each cloud region.
   - Alignment of WUE reporting among cloud providers and addressing the variation in PUE data publication schedules.

f) Net Zero Reporting and Goals:
   - Definition of the market method for calculating Net Zero goals, including energy-based offsets such as PPAs, RECs, and carbon offsets.
   - Reporting and alignment of net carbon data on a region-by-region basis and identification of regions that achieve zero net carbon emissions.

g) Standard Definitions and Alignment:
   - Establishment of guidelines for standard definitions and alignment of cloud region metadata, carbon models, and data reporting methodologies among cloud providers.

## 2 Normative references

There are no normative references in this document.

## 3 Terms and definitions

For the purposes of this document, the following terms and definitions apply.

ISO and IEC maintain terminological databases for use in standardization at the following addresses:
- ISO Online browsing platform: available at https://www.iso.org/obp
- IEC Electropedia: available at http://www.electropedia.org/

### 3.1
**carbon-free energy**  
energy generated from sources that do not emit carbon dioxide during operation, including renewable energy sources and nuclear energy

### 3.2
**cloud provider**  
entity that makes cloud services available to cloud service customers

### 3.3
**cloud region**  
geographical area where a cloud provider's data centers are located and provide cloud services

### 3.4
**location-based method**  
method for quantifying GHG emissions based on average energy generation emission factors for defined geographic locations, including local, subnational, or national boundaries

### 3.5
**market-based method**  
method for quantifying GHG emissions based on GHG emissions emitted by the generators from which the reporting entity contractually purchases electricity bundled with instruments, or unbundled instruments on their own

### 3.6
**marginal carbon intensity**  
measurement of the carbon emissions associated with changes in electricity demand, representing the emissions from the specific power source that responds to fluctuations in demand

### 3.7
**power purchase agreement**  
PPA  
long-term contract between an electricity producer and a buyer where the buyer agrees to purchase energy at a predetermined price for a specified time period

### 3.8
**power usage effectiveness**  
PUE  
ratio of the total amount of energy used by a data center facility to the energy delivered to computing equipment

### 3.9
**renewable energy credit**  
REC  
market-based instrument that represents the property rights to the environmental, social, and other non-power attributes of renewable electricity generation

### 3.10
**water usage effectiveness**  
WUE  
metric that assesses the water efficiency of a data center, measured as liters of water used per kilowatt-hour of energy consumed

## 4 Cloud Region Metadata Description

### 4.1 General

A user of the cloud region metadata can specify which cloud provider and region they use to run a workload and get all the relevant metadata about that region. Cloud region metadata is published annually and lags by 6-18 months, so the year must be specified, or the latest data should be used. The annual average location-based marginal grid-carbon-intensity value required for SCI-o is provided when available. Because of differences between cloud providers, data providers and reporting methodologies, there are several possible carbon models, and data may not be available (NA). Attempting to consume a not-available or blank metric shall cause any calculations to fail.

The data provider keys for Electricity Maps and WattTime are returned to allow real-time lookup via their APIs, and the annual average carbon intensity is reported for each grid region.

Cloud providers have their own private carbon-free generation capacity, and they report a proportion of their energy consumption offset by carbon-free energy flowing within a "Carbon-Free Energy grid region". This can reduce their effective grid carbon intensity, which is taken into account by the market method used for Net Zero reporting but not included in the location-based method that the SCI requires. The carbon-free energy calculation can be performed on a 24x7 hourly basis and accumulated over the year or on an annual total basis. Carbon free energy data is missing for regions that are not yet operational.

Carbon-free energy includes nuclear and is distinct from the definition of renewable energy.

Each cloud region has a power usage effectiveness (PUE) and a water usage effectiveness (WUE) that may be reported. Energy usage at the system level should be multiplied by the PUE ratio to account for losses due to cooling and energy distribution and storage within the cloud provider's facilities. WUE is measured as litres per kilowatt-hour.

Cloud providers have Net Zero goals, calculated using the market method. This method allows for energy-based offsets, including private Power Purchase Agreements (PPAs), tradable Renewable Energy Credits (RECs), and carbon offsets. Cloud providers report their net carbon on a region-by-region basis, using in-market energy based offsets, and a global figure that uses cross region RECs and offsets. For many regions, the market method carbon is already zero.

The European Union Energy Efficiency Directive (EED) for data centres (DCs) comes into force in 2024 for all DCs over 500 kW, which will include all cloud provider DCs sited in the EU. It mandates full disclosure to a confidential central EU registry of very detailed information on the specifications of DCs and how they are operated, and public disclosure of data subject to trade secrets and confidentiality. Since the data must be produced, key elements of the data have been added to the cloud region carbon metadata table to encourage standardized disclosure.

### 4.2 Metric Naming Scheme

The following naming conventions shall be used for metrics in this standard:

a) **Provider vs. Grid** - Some data is cloud provider specific, and some is generic data for the local grid.

b) **24x7 vs. Hourly vs. Annual** - Some provider metrics use a 24x7 hourly energy matching scheme and report data based on an hourly weighted average, labelled hourly (rather than 24x7). Other metrics are generated based on annual averages and labelled annual.

c) **Location vs. Market** - The Greenhouse Gas Protocol specifies location and market methodologies for carbon reporting. Market methodology allows energy to be matched across grids, but AWS states that it matches energy exclusively within grids for 22 of its regions for 2023 and reports market data on a per-grid basis.

d) **Consumption vs. Production** - Within a grid, the energy sources add up to a production-based metric; however, energy flows between grids across interconnects, and the actual energy mix consumption in a region takes this into account.

e) **Average vs. Marginal** - The average carbon intensity gives the total emissions mixture over a time period. The marginal emissions account for changes in demand and depend on what kind of energy source is used to supply variable demand, with other energy sources providing base load capacity.

f) **Not Available** - Accessing blank or unavailable data shall cause an exception and interrupt an Impact Framework calculation.

### 4.3 Cloud Region Metadata Table

The following table defines the standard metadata fields for cloud regions:

| Name | Units | Example | Description |
|------|-------|---------|-------------|
| year | numeric | 2022 | Specify which calendar year the data is averaged over. The IF timestamp is used to select a year. |
| cloud-provider | string | "Google Cloud" | Cloud Provider name. One of the required input keys for IF model. |
| cloud-region | string | "asia-northeast-3" | Cloud provider region. One of the required input keys for IF model. |
| cfe-region | string | "South Korea" | Carbon Free Energy grid region name as reported by the cloud provider. |
| em-zone-id | string | "KR" | Electricity Maps zone identifier for this region. Can be used to get real-time data from their API. |
| wt-region-id | string | "KOR" | WattTime region identifier. Can be used to get real-time data from their API. |
| location | string | "Seoul" | Location of the region, as reported by the cloud provider. |
| geolocation | numeric, numeric | 37.532600, 127.024612 | Latitude and longitude of the location, city level, not exact datacenter coordinates. |
| provider-cfe-hourly | numeric proportion 0.0-1.0 | 0.31 | Carbon Free Energy proportion for this cloud provider and region, weighted by the hourly usage through the year. |
| provider-cfe-annual | numeric proportion 0.0-1.0 | 0.28 | Carbon Free Energy proportion for this cloud provider and region, calculated on an annual totals basis. |
| power-usage-effectiveness | numeric | 1.18 | Power Usage Effectiveness (PUE) ratio for the region, averaged across individual datacenters. |
| water-usage-effectiveness | litres/kWh | 2.07 | Water Usage Effectiveness in litres per kilowatt hour for the region, averaged across individual datacenters. |
| provider-carbon-intensity-market-annual | gCO2e/kWh | 0 | Scope 2 market-based carbon intensity, including any energy and carbon offsets obtained by the provider, that rolls up to their Net Zero reporting. |
| provider-carbon-intensity-average-consumption-hourly | gCO2e/kWh | 354 | Electricity Maps consumption-based carbon intensity weighted by the provider's hourly usage through the year as part of a 24x7 calculation. |
| grid-carbon-intensity-average-consumption-annual | gCO2e/kWh | 429 | Electricity Maps consumption-based carbon intensity annual average for the em-zone-id |
| grid-carbon-intensity-marginal-consumption-annual | gCO2e/kWh | 686.0136038 | WattTime marginal carbon intensity annual average for the wt-region-id |
| grid-carbon-intensity | gCO2e/kWh | 686 | Specific named output for Impact Framework model consumed by SCI-o. SCI defines it as location-based and is currently set to the same value as grid-carbon-intensity-marginal-consumption-annual. |
| total-ICT-energy-consumption-annual | kWh | 100000000 | EED total energy for all datacenters in cloud region |
| total-water-input | litres | 100000000 | EED total water for all datacenters in cloud region |
| renewable-energy-consumption | kWh | 90000000 | EED total renewable energy |
| renewable-energy-consumption-goe | kWh | 10000000 | EED total renewable energy from Guarantees of Origin/Renewable Energy Certificates |
| renewable-energy-consumption-ppa | kWh | 75000000 | EED total renewable energy from power purchase agreements |
| renewable-energy-consumption-onsite | kWh | 5000000 | EED total renewable energy from on-site generation |

## 5 Requirements

### 5.1 Data Publication Requirements

Cloud providers shall:

a) Publish cloud region metadata in accordance with the metadata table defined in section 4.3.

b) Update the metadata at least annually, with the update occurring no later than 18 months after the end of the reporting period.

c) Clearly indicate the year to which the metadata applies.

d) Ensure completeness of the provided data, marking unavailable data points explicitly as "NA" (Not Available).

e) Provide all required fields for carbon intensity calculations according to both location-based and market-based methodologies.

### 5.2 Data Calculation Requirements

When calculating cloud region metadata, cloud providers shall:

a) Use consistent methodologies across all regions for calculating PUE, WUE, and carbon intensity metrics.

b) Apply appropriate weighting when calculating hourly metrics, taking into account the actual usage patterns through the year.

c) Follow the Greenhouse Gas Protocol for location-based and market-based carbon intensity calculations.

d) Clearly document the methodology used for calculating carbon-free energy proportions, specifying whether 24x7 hourly matching or annual total matching is used.

### 5.3 Data Access Requirements

Cloud providers shall:

a) Make the cloud region metadata accessible to customers in a machine-readable format.

b) Provide appropriate identifiers (em-zone-id and wt-region-id) to enable customers to access real-time data from third-party providers.

c) Document any changes to the metadata format or calculation methodologies in subsequent releases.

## 6 Conformance

A cloud provider conforms to this International Standard when they:

a) Publish cloud region metadata containing all mandatory fields defined in section 4.3.

b) Update the metadata at least annually, with clear indication of the reporting year.

c) Follow the calculation requirements defined in section 5.2.

d) Make the metadata accessible as required by section 5.3.

## Annex A (informative) References

- Amazon Renewable Energy Methodology: https://sustainability.aboutamazon.com/renewable-energy-methodology.pdf

- Amazon Carbon Methodology: https://sustainability.aboutamazon.com/carbon-methodology.pdf

- Azure Datacenter Fact Sheets for 2022: https://web.archive.org/web/20240308233631/https://datacenters.microsoft.com/globe/fact-sheets/

- Google Carbon-Free Energy by Region: https://cloud.google.com/sustainability/region-carbon

- Google Sustainability Report for 2023: https://www.gstatic.com/gumdrop/sustainability/google-2023-environmental-report.pdf#page=90

## Annex B (informative) Example Implementation

This annex provides an example implementation of cloud region metadata in JSON format:

```json
{
  "year": 2022,
  "cloud-provider": "Google Cloud",
  "cloud-region": "asia-northeast-3",
  "cfe-region": "South Korea",
  "em-zone-id": "KR",
  "wt-region-id": "KOR",
  "location": "Seoul",
  "geolocation": [37.532600, 127.024612],
  "provider-cfe-hourly": 0.31,
  "provider-cfe-annual": 0.28,
  "power-usage-effectiveness": 1.18,
  "water-usage-effectiveness": 2.07,
  "provider-carbon-intensity-market-annual": 0,
  "provider-carbon-intensity-average-consumption-hourly": 354,
  "grid-carbon-intensity-average-consumption-annual": 429,
  "grid-carbon-intensity-marginal-consumption-annual": 686.0136038,
  "grid-carbon-intensity": 686,
  "total-ICT-energy-consumption-annual": 100000000,
  "total-water-input": 100000000,
  "renewable-energy-consumption": 90000000,
  "renewable-energy-consumption-goe": 10000000,
  "renewable-energy-consumption-ppa": 75000000,
  "renewable-energy-consumption-onsite": 5000000
}
```
