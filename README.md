# Real Time Energy and Carbon Standard for Cloud Providers

Cloud providers are the largest purchasers of renewable energy in the world, but so far they have provided their customers with carbon information on a monthly basis, a few months in arrears, so customers have had to produce their own real-time estimates for cloud workloads, using public information that doesn't include those purchases and overestimates carbon footprints. As part of the information technology supply chain, cloud providers need to supply real-time carbon metrics that can be aggregated by workload, allocated and apportioned through the supply chain to satisfy regulations that are in place in the UK and Europe, on the way in California, and emerging elsewhere. Cloud providers build their own custom silicon and systems designs, and optimize them for low power consumption and to reduce the carbon footprint of their supply chain. Using this standard the efficiency benefits combined with the renewable energy purchases of cloud providers can be compared directly to datacenter alternatives for specific workloads.

Many software as a service (SaaS) providers run multi-tenant workloads on cloud providers. To supply their own customers with carbon footprint estimates, the instance level energy and carbon data needs to be allocated and attributed across workloads. The [Kepler project](https://github.com/sustainable-computing-io/kepler) hosted by the Cloud Native Computing Foundation allocates the energy usage of a host node to the active pods and containers running in that node, so that energy and carbon data can be reported for workloads running on Kubernetes. In datacenter deployments Kepler can directly measure energy usage and obtain carbon intensity data from the datacenter operator. Cloud providers block direct access to energy usage metrics as part of their multi-tenant security model, but could safely provide energy data to Kepler via this standard at one minute intervals.

# History
This standard was initially proposed as part of a [talk by Adrian Cockcroft at QCon London in March 2023](https://github.com/adrianco/slides/blob/master/Cloud%20DevSusOps%20London.pdf) that summarized the currently available carbon footprint information from the three largest cloud providers, AWS, Azure and GCP. These monthly resolution summaries are aimed at audit reporting, and the proposal was that real time data would enable new kinds of reporting, optimization and tools, and that all the cloud providers should provide the same data.

In June 2023 this proposal was written up as a PRFAQ and discussed with the GSF Standards Working Group, who decided to recommend that it become a project, which was created by the GSF in July 2023.
