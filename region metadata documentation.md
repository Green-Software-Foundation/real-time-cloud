# Cloud Region Metadata Documentation

A user of the cloud region metada can specify which cloud provider and region they are using to run a workload, and get all the relevant metadata about that region. Cloud region metadata is published annually and is always lagging by 6-18 months, so the year must be specified, or the latest data should be used. The annual average location based marginal grid-carbon-intensity value required for SCI-o is provided when available. Because of differences between cloud providers, data providers and reporting methodologies there are several different possible carbon models and data may be not available (NA). Attempting to consume a not available or blank metric should cause any calculations to fail.

The data provider keys for Electricity Maps and WattTime are returned to allow real time lookup via their APIs, and the annual average carbon intensity is reported for each grid region for each cloud provider model.

Cloud providers have their own private carbon free generation capacity, and they report a proportion of their energy consumption that is offset by carbon free energy flowing within a “Carbon Free Energy grid region”. This can reduce their effective grid carbon intensity and is taken into account by the market method that is used for Net Zero reporting, but is not included in the location based method that is required by SCI. The carbon free energy calculation can be performed on a 24x7 hourly basis and accumulated over the year, or on an annual total basis. CFE data is missing for regions that are not yet operational.

Carbon free energy includes nuclear, and is distinct from the definition of renewable energy.

Each cloud region has a power usage effectiveness (PUE) and a water usage effectiveness (WUE) that may be reported. Energy usage at the system level should be multiplied by the PUE ratio to account for losses due to cooling and energy distribution and storage within the cloud provider’s facilities. WUE is measured as litres per kilowatt and is reported for each Azure region. AWS provides a global average WUE, and Google does not currently provide WUE data [Gap: we request AWS and Google match what Azure provides].  PUE data is published on different schedules, Google currently provides quarterly and trailing 12 month data for datacenter facilities that it owns, which is a subset of its cloud regions, but doesn’t match the names of datacenters to cloud region names. AWS doesn’t provide any specific PUE data but has claimed that it operates in the range 1.07-1.15 globally. Azure provides PUE and WUE data that matches all its regions. [Gap: we request AWS and Google match what Azure provides].

Cloud providers have Net Zero goals which are calculated using the market method which allows for energy based offsets including both private Power Purchase Agreements (PPAs) and tradable Renewable Energy Credits (RECs), as well as carbon offsets, and they report the net carbon on a region by region basis. This is already zero for many regions.

Cloud providers have different definitions for the data they currently provide. Part of the goal of the GSF real-time-cloud project is to clarify those differences, and request that common definitions and alignment occur in future updates. [Gap: Google provides location based carbon data. Request AWS and Azure match what Google provides].


### Metric Naming Scheme

Provider vs. Grid - Some data is cloud **provider** specific, and some is generic data for the local **grid**.

24x7 vs. Hourly vs. Annual - Some provider metrics use a 24x7 hourly energy matching scheme, and report data based on an **hourly** weighted average, this is labelled hourly (rather than 24x7). Other metrics are generated based on annual averages and labelled **annual**.

Location vs. Market - The Greenhouse Gas Protocol specifies **location** and **market** methodologies for carbon reporting. Market methodology allows energy to be purchased across grids, but AWS states that it purchases within grids “wherever feasible”, and reports **market** data on a per-grid basis.

Consumption vs. Production - Within a grid, the energy sources add up to a **production** based metric, however there are energy flows between grids across interconnects, and the actual energy mix **consumption** in a region takes this into account.

Average vs. Marginal - The **average** carbon intensity gives the total emissions mixture over a time period. The **marginal** emissions account for changes in demand, and depends on what kind of energy source is being used to supply variable demand, with other energy sources providing base load capacity. For example, many regions use gas powered peaker plants overnight, so marginal carbon could be purely from gas. At other times the same region may be curtailing solar power during the day, so marginal carbon would be purely from solar. The average carbon would report the proportional mix of these sources.

Not Available - Accessing data that is blank or not available should cause an exception and interrupt an Impact Framework calculation.


<table>
  <tr>
   <td><strong>Name</strong>
   </td>
   <td><strong>Units</strong>
   </td>
   <td><strong>Example</strong>
   </td>
   <td><strong>Description</strong>
   </td>
  </tr>
  <tr>
   <td>year
   </td>
   <td>numeric
   </td>
   <td>2022
   </td>
   <td>Specify which calendar year the data is averaged over. The IF timestamp is used to select a year.
   </td>
  </tr>
  <tr>
   <td>cloud-provider
   </td>
   <td>string
   </td>
   <td>“Google Cloud”
   </td>
   <td>Cloud Provider name. One of the three required input keys for IF model.
   </td>
  </tr>
  <tr>
   <td>cloud-region
   </td>
   <td>string
   </td>
   <td>“asia-northeast-3”
   </td>
   <td>Cloud provider region. One of the three required input keys for IF model.
   </td>
  </tr>
  <tr>
   <td>cfe-region
   </td>
   <td>string
   </td>
   <td>“South Korea”
   </td>
   <td>Carbon Free Energy grid region name as reported by the cloud provider.
   </td>
  </tr>
  <tr>
   <td>em-zone-id
   </td>
   <td>string
   </td>
   <td>“KR”
   </td>
   <td>Electricity Maps zone identifier for this region. Can be used to get real time data from their API.
   </td>
  </tr>
  <tr>
   <td>wt-region-id
   </td>
   <td>string
   </td>
   <td>“KOR”
   </td>
   <td>WattTime region identifier. Can be used to get real time data from their API.
   </td>
  </tr>
  <tr>
   <td>location
   </td>
   <td>string
   </td>
   <td>“Seoul”
   </td>
   <td>Location of the region, as reported by the cloud provider.
   </td>
  </tr>
  <tr>
   <td>geolocation
   </td>
   <td>numeric,numeric
   </td>
   <td>37.532600, 127.024612
   </td>
   <td>Latitude and longitude of the location, city level, not exact datacenter coordinates.
   </td>
  </tr>
  <tr>
   <td>provider-cfe-hourly
   </td>
   <td>numeric proportion 0.0-1.0
   </td>
   <td>0.31
   </td>
   <td>Carbon Free Energy proportion for this cloud provider and region, weighted by the hourly usage through the year.
   </td>
  </tr>
  <tr>
   <td>provider-cfe-annual
   </td>
   <td>numeric proportion 0.0-1.0
   </td>
   <td>0.28
   </td>
   <td>Carbon Free Energy proportion for this cloud provider and region, calculated on an annual totals basis.
   </td>
  </tr>
  <tr>
   <td>power-usage-effectiveness
   </td>
   <td>numeric
   </td>
   <td>1.18
   </td>
   <td>Power Usage Effectiveness (PUE) ratio for the region, averaged across individual datacenters.
   </td>
  </tr>
  <tr>
   <td>water-usage-effectiveness
   </td>
   <td>litres/kWh
   </td>
   <td>2.07
   </td>
   <td>Water Usage Effectiveness in litres per kilowatt for the region, averaged across individual datacenters.
   </td>
  </tr>
  <tr>
   <td>provider-carbon-intensity-market-annual 
   </td>
   <td>gCO2e/kWh
   </td>
   <td>0
   </td>
   <td>Scope 2 market based carbon intensity including any energy and carbon offsets obtained by the provider, that rolls up to their Net Zero reporting.
   </td>
  </tr>
  <tr>
   <td>provider-carbon-intensity-average-consumption-hourly
   </td>
   <td>gCO2e/kWh
   </td>
   <td>354
   </td>
   <td>Electricity Maps consumption based carbon intensity weighted by the provider’s hourly usage through the year as part of a 24x7 calculation.
   </td>
  </tr>
  <tr>
   <td>grid-carbon-intensity-average-consumption-annual
   </td>
   <td>gCO2e/kWh
   </td>
   <td>429
   </td>
   <td>Electricity Maps consumption based carbon intensity annual average for the em-zone-id
   </td>
  </tr>
  <tr>
   <td>grid-carbon-intensity-marginal-consumption-annual
   </td>
   <td>gCO2e/kWh
   </td>
   <td>686.0136038
   </td>
   <td>WattTime marginal carbon intensity annual average for the wt-region-id
   </td>
  </tr>
  <tr>
   <td>grid-carbon-intensity
   </td>
   <td>gCO2e/kWh
   </td>
   <td>686
   </td>
   <td>Specific named output for Impact Framework model that is consumed by SCI-o. It’s defined by SCI to be location based and is currently set to the same value as grid-carbon-intensity-marginal-consumption-annual.
   </td>
  </tr>
</table>



### References

1. Amazon Renewable Energy Methodology

[https://sustainability.aboutamazon.com/renewable-energy-methodology.pdf](https://sustainability.aboutamazon.com/renewable-energy-methodology.pdf)

2. Amazon Carbon Methodology

[https://sustainability.aboutamazon.com/carbon-methodology.pdf](https://sustainability.aboutamazon.com/carbon-methodology.pdf%0A)

3. Azure Datacenter Fact Sheets for 2022

[https://web.archive.org/web/20240308233631/https://datacenters.microsoft.com/globe/fact-sheets/](https://web.archive.org/web/20240308233631/https://datacenters.microsoft.com/globe/fact-sheets/)

4. Google Carbon Free Energy by Region

[https://cloud.google.com/sustainability/region-carbon](https://cloud.google.com/sustainability/region-carbon)

5.. Google Sustainability Report for 2023

[https://www.gstatic.com/gumdrop/sustainability/google-2023-environmental-report.pdf#page=90](https://www.gstatic.com/gumdrop/sustainability/google-2023-environmental-report.pdf#page=90)
