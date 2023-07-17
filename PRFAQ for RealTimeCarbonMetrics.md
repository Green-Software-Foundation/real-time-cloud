[THIS IS A PRE-DRAFT PR-FAQ EVERYTHING HERE IS SPECULATIVE, NO CLOUD PROVIDERS HAVE AGREED TO DO ANYTHING YET]

**AMAZON, MICROSOFT AND GOOGLE JOINTLY ANNOUNCE SUPPORT FOR GREEN SOFTWARE FOUNDATION STANDARDIZED REAL-TIME ENERGY AND CARBON METRICS**

Carbon measurement reports move from monthly totals to minute by minute metrics, allowing real time feedback and optimization of cloud workload carbon footprints by providing information that is otherwise only available to datacenter workloads.

**Seattle, Washington–October 17th, 2023** – The three leading cloud providers have agreed to provide real-time energy and carbon metrics according to the Metrics for Energy and Carbon in Real-Time Standard (MEC-RT) defined by the Green Software Foundation.

Cloud providers are the largest purchasers of renewable energy in the world, but so far they have provided their customers with carbon information on a monthly basis, a few months in arrears, so customers have had to produce their own real-time estimates for cloud workloads, using public information that doesn't include those purchases and overestimates carbon footprints. As part of the information technology supply chain, cloud providers need to supply real-time carbon metrics that can be aggregated by workload, allocated and apportioned through the supply chain to satisfy regulations that are in place in Europe and California, and emerging elsewhere. Cloud providers build their own custom silicon and systems designs, and optimize them for low power consumption and to reduce the carbon footprint of their supply chain. Using MEC-RT the efficiency benefits combined with the renewable energy purchases of cloud providers can be compared directly to datacenter alternatives for specific workloads.

Many software as a service (SaaS) providers run multi-tenant workloads on cloud providers. To supply their own customers with carbon footprint estimates, the instance level data from MEC-RT needs to be allocated and attributed across workloads. The Kepler project hosted by the Cloud Native Computing Foundation allocates the energy usage of a host node to the active pods and containers running in that node, so that energy and carbon data can be reported for workloads running on Kubernetes. In datacenter deployments Kepler can directly measure energy usage and obtain carbon intensity data from the datacenter operator. Cloud providers block direct access to energy usage metrics as part of their multi-tenant security model, but can safely provide energy data to Kepler via MEC-RT at one minute intervals.

The carbon intensity of electricity obtained from the grid depends on location and varies continuously, but estimates are available on an hourly basis. These have been used for so-called "24x7 Location Model" monthly carbon reports by GCP in particular. However these estimates don't take into account private power purchase agreements (PPAs) where cloud providers have their own supply of renewable energy. The alternative is to report data based on the energy that has been purchased according to the so-called "Market model" which includes PPAs, and is the basis of the AWS and Azure monthly reports. MEC-RT includes both of these standard reporting models, and AWS, Azure and GCP all plan to report data using both models.

Energy usage is defined as Scope 2 by the greenhouse gas consortium standard. There is also a small amount of Scope 1 fuel burned in backup generators, in heating buildings, and by staff commuting to work. Scope 3 reports on the supply chain including silicon and computer hardware manufacturing, transport, datacenter construction, and recycling. The proportion of renewable energy is increasing over time, and as a result Scope 3 is tending to dominate carbon footprints. All three scopes are reported by MEC-RT.

The current monthly reports are delayed by several months so that there is time to gather accurate data in all regions around the world for a definitive report. In order to provide data in real time, preliminary estimates of the carbon intensity and supply chain data need to be supported. MEC-RT reports energy as a single value, but uses a confidence interval and a most likely value for the carbon footprint of each scope. As better carbon intensity data becomes available over time, the energy data can be re-processed to produce new carbon data, and the confidence interval narrows. The same metric schema can be used to produce MEC-Monthly roll-up data that isn't useful for optimization, but is well suited for carbon audit reports.

Customers and partners will access the MEC-RT metrics as time-series data via the cloud provider's default metric interface: AWS CloudWatch, Azure Monitor, and Google Cloud Monitoring. For Kubernetes Kepler will export to Prometheus on all cloud platforms.

Amazon VP Sustainability Kara Hurst said [MADE UP QUOTE]_"Our customers and partners asked us for detailed information on the carbon footprint of their workloads in a standard format, as they optimize for upcoming regulations and deliver on The Climate Pledge, and we're happy to be working with the GSF and cooperating with our colleagues at other cloud providers to meet this need."_

Google VP Sustainability Kate Brandt said [MADE UP QUOTE]_"Google pioneered the hourly 24x7 carbon measurement capability, to support optimizations in time and space, we're very happy to extend this into a standardized minute by minute data feed that is optimized to support Kubernetes based workloads"._

Microsoft VP Sustainability Melanie Nakagawa said [MADE UP QUOTE]_"When we helped launch the Green Software Foundation our intent was to collaborate across the industry to come up with standards that our partners and customers can use to reduce their carbon footprint. We're very happy to support this real-time data feed, and to provide the first reference_ _implementation as a proof of concept"._

Harness CEO Jyoti Bansai said [APPROVED REAL QUOTE] _"We always wanted to provide our customers the ability to view their carbon footprint in the context of their cloud cost spend and idle/unused resources across all cloud providers. By ingesting the MEC-RT data, we may finally be able to get the information we need in a standard form"__._

Salesforce VP Sustainability Patrick Flynn said[MADE UP QUOTE]_"Salesforce is dedicated to using its full power to save the planet, and that means we need to be able to measure and optimize our own workloads, and to be able to tell our customers what the carbon footprint of their use of Salesforce amounts to. In the past we've used crude carbon footprint estimation methods, and we're excited to be able to give much more precise and actionable data to our engineers and customers"._

CloudZero CEO Erik Petersen said [APPROVED REAL QUOTE]_“Sustainability has long been a concern for cloud engineering teams. But for as long as it’s been on engineers’ minds, the missing link in making sustainability a non-functional requirement has been the data. Every engineering decision is a buying decision — and consequently, an emissions decision — but without real-time data on cloud infrastructure’s cost and carbon consequences, engineers haven’t been able to prioritize efficiency as they build. MEC-RT is a crucial step in establishing a universal definition of cloud sustainability; now it’s up to organizations to quantify and optimize their cloud efficiency in the name of sustainability — an existentially urgent concern for all of us.” — Erik Peterson CTO and Founder, CloudZero_.

To learn more, go to [https://greensoftware.foundation/projects](https://greensoftware.foundation/projects) and to see the MEC-RT specification see [https://github.com/Green-Software-Foundation/real-time-cloud/](https://github.com/Green-Software-Foundation/real-time-cloud).

**FREQUENTLY ASKED QUESTIONS**

**Question:** Why are the quotes made up?

**Answer:** The quotes are initially intended to indicate how we think key supporters will react to this announcement. The people are real, but the words are suggested. As this document is shared and refined, they will be replaced by real quotes. Jyoti Bansai of Harness approved his quote. Erik Petersen has been asked for a real quote. Other people mentioned have not been contacted directly, although versions of this document have been supplied to AWS, Azure and GCP.

**Question:** Why do cloud providers need to support MEC-RT? Should other cloud providers implement it as well?

**Answer:** The underlying information is only available internally at cloud providers, and there needs to be a common mechanism to share it, so that customers can measure the carbon footprint of their workloads, and so that cloud workloads aren't at a disadvantage compared to datacenter workloads. We encourage all cloud providers to adopt MEC-RT.

**Question:** How does MEC-RT relate to other Green Software Foundation standards like Software Carbon Intensity (SCI)?

**Answer:** MEC-RT is needed to obtain underlying carbon measurements that are then apportioned to transactions and other business metrics so that SCI can be calculated for a cloud based workload.

**Question:** What are the security issues around energy measurement?

**Answer:** There is a class of attacks that use very accurate measurements of CPU energy use to detect the different code paths that decryption algorithms take when they check whether keys are valid, and these can be used to break the algorithm. In addition, in a multi-tenant platform there may be more than one customer workload sharing a physical host, and the energy usage of that host is affected by the total workload in ways that break the strong isolation guarantees made by cloud providers. By providing energy data summaries at one minute intervals the energy data is good enough for carbon estimation, and if necessary can be dithered to mask any signal that could possibly cause security issues.

**Question:** What metric format does MEC-RT use?

**Answer:** MEC-RT uses the same OpenMetrics standard for metrics as Prometheus and other recent tools. Each data point consists of a timestamp, a metric, and name/value pairs that describe it. Metrics consist of metadata such as name, type, units, and a stream of data points. [https://github.com/OpenObservability/OpenMetrics/blob/main/specification/OpenMetrics.md](https://github.com/OpenObservability/OpenMetrics/blob/main/specification/OpenMetrics.md)

**Question:** What carbon footprint information is currently available from cloud providers?

**Answer:** Monthly totals are provided by AWS, Azure and GCP, with varying levels of detail. Currently, AWS and Azure only provide data using the Market Model, and GCP only provides data using the Location Model. This is suitable for audit reports, but not useful for optimization tools and projects, and doesn't give enough detail to allow allocation and attribution for SaaS providers to pass on carbon footprint data to their customers.

**Question:** Why are MEC-RT carbon metrics reported as a confidence interval, how does that work, and how should they be produced and consumed?

**Answer:** The input data comes from many sources of varying quality, in particular as cloud regions are scattered around the world, there are different standards and interfaces for obtaining carbon intensity from the grid, as well as high variability over time in some areas. Where estimates are being produced, the most likely value is reported, but in addition a confidence interval provides a separate upper value and lower value with 95% confidence that the actual value is in that range. When computing with imprecise data, a common technique is to use Monte-Carlo methods, which work with distributions as inputs or outputs that can be specified using these three values. In regions that have very low carbon grids like France (Nuclear) or Sweden (Hydro), the variation is low so the confidence interval will be narrow. In regions that rely on solar and wind backed up by carbon based generation, there will be a much wider confidence interval.

**Question:** Why are confidence intervals also used for Scope 3 supply chain carbon metrics?

**Answer:** For scope 3 supply chain data, there are a lot of unknowns and estimated values, as well as batch to batch variation in builds of otherwise identical hardware. As the data sources improve, confidence intervals will narrow over time.

**Question:** How can optimization algorithms use confidence intervals?

**Answer:** For statistically valid comparisons between two values, the _values are only significantly different if they have non-overlapping confidence intervals_. So an optimization algorithm should treat input metric confidence intervals that overlap as _not significantly different_, and try to generate results that don't overlap before claiming success. The energy metrics provide a more precise value to optimize for.

**Question:** What is the California supply chain rule?

**Answer: The rule is in progress as of June, but should be settled one way it the other by October, which is the suggested date of the PRFAQ. https://www.motherjones.com/environment/2023/06/california-bill-climate-corporate-data-accountability-supply-chain-carbon-emissions/**

**Question:**

**Answer:**

**Question:**

**Answer:**

**Question:**

**Answer:**

**Question:**

**Answer:**

**Question:**

**Answer:**
