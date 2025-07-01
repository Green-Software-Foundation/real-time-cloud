# Real Time Cloud

## Introduction

The increasing adoption of cloud computing services has created an urgent need for standardized methodologies to assess and report the environmental impact of cloud infrastructure. Cloud service providers operate data centres across multiple geographical regions, each with distinct energy sources, efficiency characteristics, and carbon intensities.

Current industry practices for reporting cloud region metadata lack consistency, making it difficult for organizations to make informed decisions about sustainable cloud deployments. This document addresses these challenges by establishing a comprehensive framework for standardized cloud region metadata reporting.

This specification enables organizations to compare environmental performance across different cloud providers and regions, supports carbon accounting for cloud workloads, and facilitates compliance with emerging environmental regulations.

---

## Scope

This specification enhances the accuracy and utility of carbon emissions models for cloud-based workloads by establishing a unified data schema that enables cloud providers to share comprehensive, standardized carbon and energy metadata. Addressing the principle that "all models are wrong, some models are useful," this project makes cloud carbon emissions models significantly less wrong through methodological standardization, and more useful through consistent metadata disclosure across all major cloud providers.

The specification encompasses both static annual metadata for regulatory compliance and long-term planning, and dynamic real-time integration capabilities that provide minute-level granularity for energy usage tracking and hourly-to-daily granularity for carbon intensity measurements. This dual approach supports immediate ESG reporting requirements while enabling advanced carbon-aware computing applications that can optimize workload placement based on real-time grid conditions.

Core technical scope includes standardized disclosure of location-based and market-based carbon intensity methodologies, infrastructure efficiency metrics (PUE/WUE), carbon-free energy attribution with clear nuclear energy inclusion, geographic mapping between cloud regions and electrical grid boundaries, and integration protocols for real-time carbon data APIs including Electricity Maps and WattTime. The specification establishes consistent data quality standards, handles missing data scenarios to prevent calculation errors, and provides backward-compatible versioning to ensure stable implementation paths across the cloud industry.

- **Cloud Region Metadata:**
   - Define standard parameters for cloud region metadata, including cloud provider and region specifications.
   - Establish guidelines for annual updates and data lag management (6-18 months), with emphasis on specifying the year or using the latest available data.
   - Clarify the annual average location-based marginal grid-carbon-intensity value for SCI-o and its availability and handling of not-available (NA) data.
- **Standardizing Carbon Models and Data Reporting:**
   - Identify and clarify the multiple carbon models used by different cloud providers.
   - Address the variability of carbon data availability and handling of blank or not-available metrics.
- **Real-time Data Lookup and Provider Keys:**
   - Define the process for real-time lookup of cloud region data via APIs provided by data providers such as Electricity Maps and WattTime.
   - Establish protocols for annual average carbon intensity reporting for each grid region under each cloud provider's model.
- **Carbon-Free Energy and Renewable Energy Definitions:**
   - Define carbon-free energy and its inclusion of nuclear energy, which is distinct from the definition of renewable energy.
   - Address the absence of carbon-free energy data for regions that are not yet operational.
- **Power and Water Usage Effectiveness (PUE and WUE):**
   - Standardize reporting of power usage effectiveness (PUE) and water usage effectiveness (WUE) for each cloud region.
   - Align WUE reporting among cloud providers and address the variation in PUE data publication schedules.
- **Net Zero Reporting and Goals:**
   - Define the market method for calculating Net Zero goals, including energy-based offsets such as PPAs, RECs, and carbon offsets.
   - Report and align net carbon data on a region-by-region basis and identify regions that achieve zero net carbon emissions.
- **Standard Definitions and Alignment:**
   - Establish guidelines for standard definitions and alignment of cloud region metadata, carbon models, and data reporting methodologies among cloud providers (e.g., AWS and Azure aligning with Google's location-based carbon data).

### European Union Energy Efficiency Directive compliance

The European Union Energy Efficiency Directive (EED) for data centres (DCs) comes into force in 2024 for all DCs over 500 kW, including all cloud provider DCs sited in the EU. It mandates full disclosure to a confidential central EU registry of very detailed information on the specifications of DCs and how they are operated, and public disclosure of data subject to trade secrets and confidentiality. Since the data shall be produced, key elements of the data have been added to the cloud region carbon metadata table to encourage standardized disclosure.

---

## Problem Statement

Cloud providers currently publish efficiency metrics and renewable energy data independently, creating significant challenges:

- Inconsistent reporting methodologies prevent meaningful comparisons between providers
- Data publication delays of 6-18 months limit real-time decision-making
- Missing standardization forces customers to interpret disparate data formats
- Limited transparency restricts accurate carbon footprint calculations for specific workloads

## Normative references

No normative references

---

## Terms and definitions

For the purposes of this document, the following terms and definitions apply.

| **Term** | **Definition** | **Source** |
|----------|----------------|------------|
| **24x7 Carbon-Free Energy (24x7 CFE)** | Energy procurement strategy where carbon-free energy sources are matched to consumption on an hourly basis, ensuring that every hour of energy consumption is matched with carbon-free energy generation in the same grid region | Google Cloud |
| **Annual Average** | Carbon intensity or energy metrics calculated based on a full calendar year of data, providing a stable reference value for planning and compliance reporting | GSF |
| **Balancing Authority (BA)** | Entity responsible for maintaining the balance between electricity supply and demand within a specific geographic area, used by WattTime for carbon intensity data provision | WattTime |
| **Carbon-Free Energy (CFE)** | Energy generation that produces no direct carbon dioxide emissions during operation, including renewable sources (solar, wind, hydro, geothermal) and nuclear power | GSF |
| **Carbon Intensity** | Measure of carbon dioxide equivalent emissions per unit of energy consumed, typically expressed in grams of CO2 equivalent per kilowatt-hour (gCO2eq/kWh) | GHG Protocol |
| **Cloud Region** | Geographically isolated area where a cloud provider operates multiple availability zones or data centers, providing low-latency connectivity within the region | Cloud Providers |
| **Data Lag** | Time period between the end of a reporting year and the publication of verified sustainability data, typically ranging from 6-18 months for cloud providers | GSF |
| **Electricity Maps Zone** | Standardized geographic identifier used by Electricity Maps to provide real-time grid carbon intensity data for specific electrical grid regions | Electricity Maps |
| **Grid Carbon Intensity** | Average carbon intensity of the electrical grid in a specific geographic region, reflecting the mix of generation sources feeding that grid | Various |
| **Hourly Weighted Average** | Carbon intensity calculation method where each hour's carbon intensity is weighted by the actual energy consumption during that hour | Cloud Providers |
| **Location-Based Method** | Carbon accounting approach that uses the average emission factor of the electricity grid where consumption occurs, regardless of contractual arrangements | GHG Protocol Scope 2 |
| **Marginal Carbon Intensity** | Carbon intensity of the next unit of electricity that would be generated or reduced in response to a change in demand, typically higher than average grid intensity | Research Literature |
| **Market-Based Method** | Carbon accounting approach that uses emission factors from contractual arrangements such as renewable energy certificates, power purchase agreements, or green electricity products | GHG Protocol Scope 2 |
| **Not Available (NA)** | Standardized indicator for missing or unavailable data that causes calculations to fail rather than provide incorrect results | GSF |
| **Power Purchase Agreement (PPA)** | Long-term contract between an electricity generator and a purchaser for the sale of renewable energy, often used by cloud providers to support carbon-free energy claims | Industry Standard |
| **Power Usage Effectiveness (PUE)** | Ratio of total data center energy consumption to the energy consumed by IT equipment alone, with 1.0 representing perfect efficiency | The Green Grid |
| **Real-Time Data** | Carbon intensity and energy information updated at frequencies from minutes to hours, enabling dynamic optimization of workload placement based on current grid conditions | GSF |
| **Renewable Energy Certificate (REC)** | Market-based instrument that represents the environmental attributes of one megawatt-hour of renewable electricity generation | Various Markets |
| **Renewable Energy** | Energy derived from natural processes that are replenished constantly, including solar, wind, hydroelectric, geothermal, and biomass, but excluding nuclear power | IEA Definition |
| **Scope 2 Emissions** | Indirect greenhouse gas emissions from the consumption of purchased electricity, steam, heating, and cooling | GHG Protocol |
| **Software Carbon Intensity (SCI)** | Metric that calculates the carbon intensity of a software application, expressed as carbon emissions per functional unit | ISO/IEC 21031:2024 |
| **Water Usage Effectiveness (WUE)** | Ratio of total data center water consumption to the energy consumed by IT equipment, expressed in liters per kilowatt-hour (L/kWh) | The Green Grid |
| **WattTime Balancing Authority** | Geographic region identifier used by WattTime to provide predictive carbon intensity data based on electricity market operations | WattTime |

**Notes:**
1. Terms marked "GSF" are defined specifically for this specification
2. External source definitions are adapted for cloud computing context
3. All carbon intensity values are expressed in gCO2eq/kWh unless otherwise specified
4. Geographic boundaries may overlap between different data providers

---

## Description
A user of the cloud region metadata can specify which cloud provider and region they use to run a workload and get all the relevant metadata about that region. Cloud region metadata is published annually and lags by 6-18 months, so the year must be specified, or the latest data should be used. The annual average location-based marginal grid-carbon-intensity value required for SCI-o is provided when available. Because of differences between cloud providers, data providers and reporting methodologies, there are several possible carbon models, and data may not be available (NA). Attempting to consume a not-available or blank metric should cause any calculations to fail.

The data provider keys for Electricity Maps and WattTime are returned to allow real-time lookup via their APIs, and the annual average carbon intensity is reported for each grid region.

Cloud providers have their own private carbon-free generation capacity, and they report a proportion of their energy consumption offset by carbon-free energy flowing within a “Carbon-Free Energy grid region”. This can reduce their effective grid carbon intensity, which is taken into account by the market method used for Net Zero reporting but not included in the location-based method that the SCI requires. The carbon-free energy calculation can be performed on a 24x7 hourly basis and accumulated over the year or on an annual total basis. Carbon free energy data is missing for regions that are not yet operational.

Carbon-free energy includes nuclear and is distinct from the definition of renewable energy.

Each cloud region has a power usage effectiveness (PUE) and a water usage effectiveness (WUE) that may be reported. Energy usage at the system level should be multiplied by the PUE ratio to account for losses due to cooling and energy distribution and storage within the cloud provider’s facilities. WUE is measured as litres per kilowatt-hour and was reported for each Azure region in 2022. AWS provides a global average WUE, and Google does not currently provide WUE data [Gap: we request AWS and Google match what Azure provides]. PUE data is published on different schedules; Google currently provides annual, quarterly and trailing 12-month data for data centre facilities that it owns, which is a subset of its cloud regions and we have matched the names of data centres to cloud region names. AWS also provides annual PUE data for a subset of regions. Azure provided 2022 PUE and WUE data that matched all its regions, but the 2023 data it published was less comprehensive. The 2022 data was removed from the Azure website but has been preserved by this project.

Cloud providers have Net Zero goals, calculated using the market method. This method allows for energy-based offsets, including private Power Purchase Agreements (PPAs), tradable Renewable Energy Credits (RECs), and carbon offsets. Cloud providers report their net carbon on a region-by-region basis, using in-market energy based offsets, and a global figure that uses cross region RECs and offsets. For many regions, the market method carbon is already zero.

Cloud providers have different definitions for the data they currently provide. Part of the goal of the GSF real-time cloud project is to clarify those differences and request that standard definitions and alignment occur in future updates. [Gap: Google provides location-based carbon data. Request AWS and Azure match what Google provides.]

The European Union Energy Efficiency Directive (EED) for data centres (DCs) comes into force in 2024 for all DCs over 500 kW, which will include all cloud provider DCs sited in the EU. It mandates full disclosure to a confidential central EU registry of very detailed information on the specifications of DCs and how they are operated, and public disclosure of data subject to trade secrests and confidentiality. Since the data must be produced, key elements of the data have been added to the cloud region carbon metadata table to encourage standardized disclosure.

## Metric naming scheme

The following naming conventions shall be used for metrics in this document:

a) **Provider versus grid**: Some data is cloud provider specific, and some is generic data for the local grid.

b) **24×7 versus hourly versus annual**: Some provider metrics use a 24×7 hourly energy matching scheme and report data based on an hourly weighted average, labelled hourly (rather than 24×7). Other metrics are generated based on annual averages and labelled annual.

c) **Location versus market**: The Greenhouse Gas Protocol specifies location and market methodologies for carbon reporting. Market methodology allows energy to be matched across grids, but AWS states that it matches energy exclusively within grids for 22 of its regions for 2023 and reports market data on a per-grid basis.

d) **Consumption versus production**: Within a grid, the energy sources add up to a production-based metric; however, energy flows between grids across interconnects, and the actual energy mix consumption in a region takes this into account.

e) **Average versus marginal**: The average carbon intensity gives the total emissions mixture over a time period. The marginal emissions account for changes in demand and depend on what kind of energy source is used to supply variable demand, with other energy sources providing base load capacity.

f) **Not available**: Accessing blank or unavailable data shall cause an exception and interrupt an Impact Framework calculation.

---

## Metadata categories and parameters

### Cloud region metadata table

Each cloud region entry must include the following standardized parameters:

| Name | Units | Example | Description |
|------|-------|---------|-------------|
| year | numeric | 2022 | Calendar year over which the data is averaged |
| cloud-provider | string | "Google Cloud" | Cloud provider name |
| cloud-region | string | "asia-northeast-3" | Cloud provider region identifier |
| cfe-region | string | "South Korea" | Carbon-free energy grid region name as reported by the cloud provider |
| em-zone-id | string | "KR" | Electricity Maps zone identifier for this region |
| wt-region-id | string | "KOR" | WattTime region identifier for this region |
| location | string | "Seoul" | Location of the region, as reported by the cloud provider |
| geolocation | numeric, numeric | 37.532600, 127.024612 | Latitude and longitude of the location, city level |
| provider-cfe-hourly | numeric proportion 0,0 to 1,0 | 0,31 | Carbon-free energy proportion for this cloud provider and region, weighted by the hourly usage through the year |
| provider-cfe-annual | numeric proportion 0,0 to 1,0 | 0,28 | Carbon-free energy proportion for this cloud provider and region, calculated on an annual totals basis |
| power-usage-effectiveness | numeric | 1,18 | Power usage effectiveness (PUE) ratio for the region, averaged across individual data centres |
| water-usage-effectiveness | L/kWh | 2,07 | Water usage effectiveness in litres per kilowatt-hour for the region, averaged across individual data centres |
| provider-carbon-intensity-market-annual | gCO₂eq/kWh | 0 | Scope 2 market-based carbon intensity, including any energy and carbon offsets obtained by the provider |
| provider-carbon-intensity-average-consumption-hourly | gCO₂eq/kWh | 354 | Electricity Maps consumption-based carbon intensity weighted by the provider's hourly usage through the year as part of a 24×7 calculation |
| grid-carbon-intensity-average-consumption-annual | gCO₂eq/kWh | 429 | Electricity Maps consumption-based carbon intensity annual average for the em-zone-id |
| grid-carbon-intensity-marginal-consumption-annual | gCO₂eq/kWh | 686,0136038 | WattTime marginal carbon intensity annual average for the wt-region-id |
| grid-carbon-intensity | gCO₂eq/kWh | 686 | Location-based grid carbon intensity for Impact Framework model consumed by SCI-o |
| total-ICT-energy-consumption-annual | kWh | 100 000 000 | Total energy for all data centres in cloud region (EED requirement) |
| total-water-input | L | 100 000 000 | Total water for all data centres in cloud region (EED requirement) |
| renewable-energy-consumption | kWh | 90 000 000 | Total renewable energy (EED requirement) |
| renewable-energy-consumption-goe | kWh | 10 000 000 | Total renewable energy from Guarantees of Origin/Renewable Energy Certificates (EED requirement) |
| renewable-energy-consumption-ppa | kWh | 75 000 000 | Total renewable energy from power purchase agreements (EED requirement) |
| renewable-energy-consumption-onsite | kWh | 5 000 000 | Total renewable energy from on-site generation (EED requirement) |

---

## Requirements

### Cloud region metadata framework

#### General framework

The cloud region metadata framework shall comprise four main categories:

a) energy efficiency metrics: parameters related to data centre energy consumption and efficiency;

b) carbon intensity metrics: parameters related to carbon emissions and renewable energy;

c) infrastructure metrics: parameters related to physical infrastructure characteristics;

d) operational metrics: parameters related to service delivery and performance.

#### Data hierarchy

Cloud region metadata shall be organized in a hierarchical structure:

a) provider level: metadata applicable to the entire cloud service provider;

b) region level: metadata specific to a geographical region;

c) availability zone level: metadata specific to individual availability zones within a region;

d) service level: metadata specific to particular cloud services (where applicable).

#### Temporal granularity

Metadata shall be provided at multiple temporal granularities:

a) annual averages: for long-term planning and compliance reporting;

b) monthly averages: for seasonal variation analysis;

c) hourly data: for operational optimization;

d) real-time data: for dynamic workload scheduling.

#### Data format requirements

All metadata shall be provided in machine-readable formats supporting:

a) JSON (JavaScript Object Notation) as the primary format;

b) XML (eXtensible Markup Language) as an alternative format;

c) CSV (Comma-Separated Values) for bulk data exports;

d) API access with standard HTTP methods and RESTful architecture.

### Energy efficiency metrics

#### Power usage effectiveness (PUE)

Cloud service providers shall report the annual average PUE for each cloud region calculated according to the following formula:

PUE = Total Facility Energy / IT Equipment Energy

Where:
— Total Facility Energy includes all energy consumed by the data centre facility.
— IT Equipment Energy includes energy consumed by servers, storage, and networking equipment.

PUE values shall be reported to two decimal places and updated annually.

#### Water usage effectiveness (WUE)

Cloud service providers shall report the annual average WUE for each cloud region calculated as:

WUE = Total Water Usage (L) / IT Equipment Energy (kWh)

WUE values shall be reported in litres per kilowatt-hour (L/kWh) to one decimal place.

#### Carbon usage effectiveness (CUE)

Cloud service providers should report the annual average CUE calculated as:

CUE = Total CO₂ Emissions (kg) / IT Equipment Energy (kWh)

### Carbon intensity metrics

#### Location-based carbon intensity

Cloud service providers shall report:

a) annual average location-based carbon intensity in gCO₂eq/kWh;

b) monthly average location-based carbon intensity for the most recent 12-month period;

c) source of carbon intensity data (e.g. national grid operator, third-party provider).

#### Market-based carbon intensity

Cloud service providers shall report market-based carbon intensity accounting for:

a) power purchase agreements (PPAs);

b) renewable energy certificates (RECs);

c) direct renewable energy procurement;

d) residual grid mix after accounting for renewable energy claims.

#### Carbon-free energy percentage

Cloud service providers shall report the percentage of energy consumption matched with carbon-free energy sources, calculated as:

CFE% = (Carbon-free Energy Matched / Total Energy Consumption) × 100

Carbon-free energy includes renewable energy sources and nuclear energy.

#### Renewable energy percentage

Cloud service providers should report the percentage of energy consumption matched with renewable energy sources, excluding nuclear energy.

### Infrastructure metrics

#### Geographic coordinates

Cloud service providers shall provide approximate geographic coordinates (latitude and longitude) for each cloud region to enable grid region mapping.

#### Grid region identification

Cloud service providers shall identify the electrical grid region(s) serving each cloud region using standard grid operator identifiers, where available.

#### Climate zone

Cloud service providers should provide climate zone classification according to international standards to enable cooling efficiency assessment.

### Operational metrics

#### Service availability

Cloud service providers should report annual average service availability percentages for core services in each region.

#### Data residency

Cloud service providers shall specify data residency requirements and restrictions for each region.

---

## Data access requirements

Cloud providers shall:

a) make the cloud region metadata accessible to customers in a machine-readable format;

b) provide appropriate identifiers (em-zone-id and wt-region-id) to enable customers to access real-time data from third-party providers;

c) document any changes to the metadata format or calculation methodologies in subsequent releases.

---

## Conformance

### General

Conformance to this document requires implementation of all normative requirements specified in Clauses 4 through 7 and Annex A.

### Conformance levels

This document defines two levels of conformance:

a) **Level 1 (Basic conformance)**: Implementation of mandatory metadata parameters as specified in Annex A and basic reporting capabilities.

b) **Level 2 (Advanced conformance)**: Implementation of all Level 1 requirements plus real-time API access and advanced data quality validation.

### Conformance declaration

Cloud service providers claiming conformance to this document shall provide a conformance declaration that specifies:

a) the conformance level achieved (Level 1 or Level 2);

b) the scope of implementation (regions covered, services included);

c) the date of conformance assessment;

d) identification of any limitations or exceptions.

---

## Annex A (normative) Mandatory metadata parameters

### A.1 Level 1 conformance requirements

Cloud service providers claiming Level 1 conformance shall provide the following mandatory parameters for each cloud region:

**Table A.1 — Mandatory metadata parameters for Level 1 conformance**

| Parameter | Unit | Update Frequency | Required |
|-----------|------|------------------|----------|
| year | numeric | Annual | Yes |
| cloud-provider | string | Static | Yes |
| cloud-region | string | Static | Yes |
| location | string | Static | Yes |
| geolocation | decimal degrees | Static | Yes |
| power-usage-effectiveness | ratio | Annual | Yes |
| grid-carbon-intensity | gCO₂eq/kWh | Annual | Yes |
| provider-cfe-annual | proportion | Annual | Yes |

### A.2 Level 2 conformance requirements

Cloud service providers claiming Level 2 conformance shall provide all Level 1 parameters plus the additional parameters specified in Table 1.

---

## Annex B (informative) Example implementation

### B.1 JSON format example

The following example shows cloud region metadata in JSON format:

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

---
