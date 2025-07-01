# Real Time Cloud

## Introduction

The increasing adoption of cloud computing services has created an urgent need for standardized methodologies to assess and report the environmental impact of cloud infrastructure. Cloud service providers operate data centres across multiple geographical regions, each with distinct energy sources, efficiency characteristics, and carbon intensities.

Current industry practices for reporting cloud region metadata lack consistency, making it difficult for organizations to make informed decisions about sustainable cloud deployments. This document addresses these challenges by establishing a comprehensive framework for standardized cloud region metadata reporting.

This specification enables organizations to compare environmental performance across different cloud providers and regions, supports carbon accounting for cloud workloads, and facilitates compliance with emerging environmental regulations.

---

## Scope

This document specifies requirements for cloud region metadata reporting to enable accurate carbon footprint assessment and energy efficiency evaluation of cloud computing services.

This document covers:

— standardized parameters for cloud region metadata including energy efficiency, carbon intensity, and renewable energy metrics;

— data collection and reporting methodologies for cloud service providers;

— API specifications for real-time and historical metadata access;

— validation and quality assurance requirements for metadata accuracy;

— conformance criteria for cloud service provider implementations.

This document applies to public cloud service providers, hybrid cloud environments, and private cloud infrastructure operators who provide computational resources across multiple geographical regions.

This document does not cover:

— specific carbon accounting methodologies for end-user applications;

— detailed technical specifications for data centre equipment;

— financial or contractual aspects of cloud services.

---

## Normative references

The following documents are referred to in the text in such a way that some or all of their content constitutes requirements of this document. For dated references, only the edition cited applies. For undated references, the latest edition of the referenced document (including any amendments) applies.

### Normative references for cloud region metadata specification

| Standard Number | Document Type | Title | Application in Cloud Metadata |
|-----------------|---------------|-------|-------------------------------|
| **ISO 14040** | International Standard | Environmental management — Life cycle assessment — Principles and framework | Establishes environmental assessment principles for cloud infrastructure impact evaluation |
| **ISO 14044** | International Standard | Environmental management — Life cycle assessment — Requirements and guidelines | Provides methodology requirements for carbon footprint calculations and environmental impact assessments |
| **ISO 50001** | International Standard | Energy management systems — Requirements with guidance for use | Defines energy management framework applicable to cloud data centre operations and efficiency reporting |
| **ISO/IEC 23053** | International Standard | Framework for AI systems using machine learning (ML) | Addresses AI and machine learning workload considerations in cloud sustainability metrics and carbon accounting |
| **ISO/IEC 30134 series** | International Standard Series | Information technology — Data centres — Key performance indicators | Provides standardized KPIs for data centre efficiency measurements including PUE, WUE, and carbon usage effectiveness |
| **ISO/IEC TR 23188** | Technical Report | Information technology — Cloud computing — Edge computing landscape | Defines cloud computing architecture context and regional deployment considerations for metadata frameworks |
| **IEC 61850 series** | International Standard Series | Communication protocols for intelligent electronic devices | Specifies communication standards for energy monitoring, smart grid integration, and real-time data exchange |

---

## Terms and definitions

For the purposes of this document, the following terms and definitions apply.

ISO and IEC maintain terminological databases for use in standardization at the following addresses:

— ISO Online browsing platform: available at https://www.iso.org/obp

— IEC Electropedia: available at https://www.electropedia.org/

# Terms and definitions for cloud region metadata

| Term | Definition | Notes to Entry |
|------|------------|----------------|
| **carbon-free energy** | electrical energy generated from sources that do not produce carbon dioxide emissions during the generation process, including renewable sources and nuclear energy | — |
| **cloud region** | geographical area within which a cloud service provider operates one or more data centres that provide cloud computing resources | — |
| **cloud region metadata** | structured information describing the environmental, operational, and technical characteristics of a cloud region | — |
| **grid carbon intensity** | mass of carbon dioxide equivalent emissions per unit of electrical energy consumed from the electrical grid, expressed in grams of CO₂ equivalent per kilowatt-hour (gCO₂eq/kWh) | Grid carbon intensity varies by location and time based on the energy mix of the electrical grid |
| **location-based carbon intensity** | carbon intensity calculated based on the average emissions factor of grids on which energy consumption occurs | — |
| **marginal grid carbon intensity** | carbon intensity of the next unit of energy generated or consumed on the electrical grid | — |
| **power purchase agreement** (PPA) | contractual agreement between an energy generator and a purchaser for the sale and purchase of renewable energy | — |
| **power usage effectiveness** (PUE) | ratio of total amount of energy used by a data centre facility to the energy delivered to computing equipment | PUE is calculated as total facility energy divided by IT equipment energy |
| **renewable energy certificate** (REC) | tradeable certificate that represents proof that one megawatt-hour of electricity was generated from renewable sources | — |
| **water usage effectiveness** (WUE) | ratio of total amount of water used by a data centre facility to the energy delivered to computing equipment | WUE is expressed in litres per kilowatt-hour (L/kWh) |

---

## Cloud region metadata description

### General

A user of the cloud region metadata can specify which cloud provider and region they use to run a workload and get all the relevant metadata about that region. Cloud region metadata is published annually and lags by 6 months to 18 months, so the year shall be specified, or the latest data should be used. 

The annual average location-based marginal grid-carbon-intensity value required for SCI-o is provided when available. Because of differences between cloud providers, data providers and reporting methodologies, there are several possible carbon models, and data may not be available. Attempting to consume a not-available or blank metric shall cause any calculations to fail.

The data provider keys for Electricity Maps and WattTime are returned to allow real-time lookup via their APIs, and the annual average carbon intensity is reported for each grid region.

Cloud providers have their own private carbon-free generation capacity, and they report a proportion of their energy consumption offset by carbon-free energy flowing within a carbon-free energy grid region. This can reduce their effective grid carbon intensity, which is taken into account by the market method used for Net Zero reporting but not included in the location-based method that the SCI requires. The carbon-free energy calculation can be performed on a 24×7 hourly basis and accumulated over the year or on an annual total basis. Carbon-free energy data is missing for regions that are not yet operational.

Carbon-free energy includes nuclear and is distinct from the definition of renewable energy.

Each cloud region has a power usage effectiveness (PUE) and a water usage effectiveness (WUE) that may be reported. Energy usage at the system level should be multiplied by the PUE ratio to account for losses due to cooling and energy distribution and storage within the cloud provider's facilities. WUE is measured as litres per kilowatt-hour.

Cloud providers have Net Zero goals, calculated using the market method. This method allows for energy-based offsets, including private power purchase agreements (PPAs), tradeable renewable energy certificates (RECs), and carbon offsets. Cloud providers report their net carbon on a region-by-region basis, using in-market energy-based offsets, and a global figure that uses cross-region RECs and offsets. For many regions, the market method carbon is already zero.

### European Union Energy Efficiency Directive compliance

The European Union Energy Efficiency Directive (EED) for data centres (DCs) comes into force in 2024 for all DCs over 500 kW, including all cloud provider DCs sited in the EU. It mandates full disclosure to a confidential central EU registry of very detailed information on the specifications of DCs and how they are operated, and public disclosure of data subject to trade secrets and confidentiality. Since the data shall be produced, key elements of the data have been added to the cloud region carbon metadata table to encourage standardized disclosure.

### Metric naming scheme

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

Table 1 defines the standard metadata fields for cloud regions.

**Cloud region metadata parameters**

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
— Total Facility Energy includes all energy consumed by the data centre facility;
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

## Bibliography

[1] Amazon Web Services. **Renewable Energy Methodology**. Available at: https://sustainability.aboutamazon.com/renewable-energy-methodology.pdf

[2] Amazon Web Services. **Carbon Methodology**. Available at: https://sustainability.aboutamazon.com/carbon-methodology.pdf

[3] Microsoft Corporation. **Azure Datacenter Fact Sheets for 2022**. Available at: https://web.archive.org/web/20240308233631/https://datacenters.microsoft.com/globe/fact-sheets/

[4] Google LLC. **Carbon-Free Energy by Region**. Available at: https://cloud.google.com/sustainability/region-carbon

[5] Google LLC. **Sustainability Report for 2023**. Available at: https://www.gstatic.com/gumdrop/sustainability/google-2023-environmental-report.pdf

[6] Greenhouse Gas Protocol. **Scope 2 Guidance: An amendment to the GHG Protocol Corporate Standard**. World Resources Institute, 2015

[7] European Commission. **Directive (EU) 2023/1791 on energy efficiency (recast)**. Official Journal of the European Union, 2023

[8] Green Software Foundation. **Software Carbon Intensity (SCI) Specification**. Version 1.0, 2022
