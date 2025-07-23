# Real Time Energy and Carbon Standards for Cloud Providers
Cloud providers are the largest purchasers of renewable energy in the world, but so far they have provided their customers with carbon information on a monthly basis, a few months in arrears, using a variety of metrics and models. Customers have had to produce their own real-time estimates for cloud workloads, using public information that doesn't include renewable energy purchases and overestimates carbon footprints. As part of the information technology supply chain, cloud providers need to supply real-time carbon metrics that can be aggregated by workload, allocated and apportioned through the supply chain to satisfy regulations that are in place in the UK and Europe, on the way in California, and emerging elsewhere. Cloud providers build their own custom silicon and systems designs, and optimize them for low power consumption and to reduce the carbon footprint of their supply chain. With standardized metrics the efficiency benefits combined with the renewable energy purchases of cloud providers can be compared with each other and to datacenter alternatives for specific workloads.

## Motivation
"All models are wrong, some models are useful". The goal of this project is to make the carbon emissions model for cloud based workloads less wrong, by defining a standard mechanism for cloud providers to share more information, and more useful, by having the same metadata schema for all cloud providers. We need "real time" data that can be used to estimate the carbon footprint of a workload that is running today, or is planned for future deployment.

## Target Users of this Standard
Platform teams and software as a service (SaaS) providers run multi-tenant workloads on cloud providers. To supply their own customers with carbon footprint estimates, the instance level energy and carbon data needs to be allocated and attributed across workloads. The [Kepler project](https://github.com/sustainable-computing-io/kepler) hosted by the Cloud Native Computing Foundation allocates the energy usage of a host node to the active pods and containers running in that node, so that energy and carbon data can be reported for workloads running on Kubernetes. In datacenter deployments Kepler can directly measure energy usage and obtain carbon intensity data from the datacenter operator. Cloud providers block direct access to energy usage metrics as part of their multi-tenant hypervisor security model, and in that case Kepler uses estimates for CPU energy usage. However, detailed GPU energy usage *is* available in real time for most GPUs. Given the energy usage, the next step is to lookup the cloud provider information for the region so that it can be combined with Power Usage Effectiveness, the Carbon Free Energy ratio, and the local Carbon Intensity to produce a carbon emissions estimate. We have gathered all the cloud region data we can find into a common standard for this project.

## Cloud Providers
The cloud providers disclose metadata about regions annually, around six months after the year ends. This data may include Power and Water Usage Effectiveness, carbon-free energy percentage, and the location and grid region for each cloud region. This project is gathering, normalising and releasing this metadata as a single data source, and lobbying the cloud providers to release annual metadata that is more closely aligned across providers.

In this V1.0 release, annual metadata from Amazon Web Services (AWS), Microsoft Azure and Google Cloud Platform (GCP) has been normalised into a single data source. That data, which is only currently provided for 2023 and earlier, has been projected into a 2024 and 2025 estimate. 2025 data on AWS power generation project locations has also been archived here.

Please create issues and pull requests to provide corrections and updates. We encourage cloud providers to nominate a representative that the project can contact. GSF members (including Azure and GCP) participated in defining the standard, but we also welcome discussions with non-members who can provide data.

## Updates and Version Stability
Work has started to include Oracle Cloud, and we encourage other cloud providers to release annual data aligned with the annual Cloud Region Metadata standard we have established.

In past years, Microsoft has published updates in May, Google in June and Amazon in July. When all three providers have published new data, we plan to update the metadata tables here for a new minor version release (V1.1).  If the metadata standard is changed to add new columns of data we will increment the major version (V2.0). To maintain backward compatibility we will not remove, rename or re-order existing columns of data.

## Collected Context on Data Sources and Tools
The initial work focused on collecting and discussing existing information, and a context miro board was created that is being used to crowdsource relevant information about power and carbon data sources and how they are created and used from end to end. The miro is [publicly readable here](https://miro.com/app/board/uXjVM1o59N4=/?share_link_id=388311040102) and screenshots are stored in this repo. It is proposed that slowly changing reference data will be shared via the [GSF Impact Framework](https://github.com/Green-Software-Foundation/if), and so far this includes Power Usage Efficiency (PUE), Water Usage Efficiency (WUE), Carbon Free Energy, a placeholder for EU Datacenter disclosure data, and Power Purchase Agreement location information. There are issues tracking the development of each of these.

![Miro Summary](./sup_file/rtc-miro-2024-07-01.png)

## Estimation Code
A Python script with test input and output has been produced to generate trended estimates for the current year based on previous years.

- [Cloud_Region_Metadata_estimate.csv](https://github.com/Green-Software-Foundation/real-time-cloud/blob/main/Cloud_Region_Metadata_estimate.csv)
- [estimate_current_region_metadata code](https://github.com/Green-Software-Foundation/real-time-cloud/blob/main/code/estimate_current_region_metadata.py)

# History
This standard was initially proposed as part of a talk by Adrian Cockcroft at QCon London in March 2023, that was updated and presented again at the CNCF Sustainability Week in October 2023. [March slides,](https://github.com/adrianco/slides/blob/master/Cloud%20DevSusOps%20London.pdf) [October slides.](https://github.com/adrianco/slides/blob/master/Cloud%20DevSusOps%20Oct23.pdf) that summarized the currently available carbon footprint information from the three largest cloud providers, AWS, Azure and GCP. These monthly resolution summaries are aimed at audit reporting, and the proposal was that real time data would enable new kinds of reporting, optimization and tools, and that all the cloud providers should provide the same data.

In June 2023 this proposal was [written up as a PRFAQ](https://github.com/Green-Software-Foundation/real-time-cloud/blob/main/sup_file/PRFAQ%20for%20RealTimeCarbonMetrics.md) and discussed with the GSF Standards Working Group, who decided to recommend that it become a project, which was created by the GSF in July 2023.

A summary of the state of AWS sustainability at the end of 2023 was [written up here](https://adrianco.medium.com/sustainability-talks-and-updates-from-aws-re-invent-2023-969100c46a6a). There were no substantive announcements but renewable energy purchases are continuing to grow. A comparison of the three main cloud providers disclosures for calendar year 2023 was published as a story in [The New Stack](https://thenewstack.io/sustainability-how-did-amazon-azure-google-perform-in-2023/).

In December 2024, AWS provided PUE data for 2022 and 2023 for the first time. The PUE disclosures of AWS, Azure and GCP were analyzed and published as a story in [The New Stack](https://thenewstack.io/cloud-pue-comparing-aws-azure-and-gcp-global-regions/) in January 2025.
