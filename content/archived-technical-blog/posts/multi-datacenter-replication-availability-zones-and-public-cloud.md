---
title: "Multi-Datacenter Replication: Availability Zones and Public Cloud"
date: "2013-02-28T21:58:46+00:00"
author: "Basho"
original_url: "http://basho.com/posts/technical/multi-datacenter-replication-availability-zones-and-public-cloud/"
archive_url: "https://web.archive.org/web/20170801115204http://basho.com/posts/technical/multi-datacenter-replication-availability-zones-and-public-cloud/"
categories:
  - "Replication"
---
*February 28, 2013*

In the [last post](http://basho.com/multi-datacenter-replication-backups-and-data-locality/), we looked at how Riak Enterprise’s multi-datacenter replication can be configured for backups and data locality. In this post, we examine two other common implementations: availability zones and public cloud use cases. For more information on Riak Enterprise architecture and configuration, [download the complete whitepaper](http://info.basho.com/RiakMDC_Whitepaper.html).

## Availability Zones

Availability zones provide efficient multi-datacenter replication and data redundancy within a geographic region (such as a coast or a country). In this configuration, data is replicated within an availability zone’s series of datacenters. In the event that one of datacenters experiences an outage or serious failure, data can still be served from other datacenters within the same region.

One approach to setting this up is to have a “primary” site in a region where all reads and writes for specific users, applications, or data sets are directed. This primary cluster can then be replicated to one or more proximal secondary clusters. In other approaches, data can be replicated in real-time from one cluster to both another datacenter and other cold backups maintained for emergency conditions. The right approach is highly dependent on the requirements of users, availability, expense of bandwidth, and other constraints.

## Public Cloud Use Cases

Riak is designed to be easy to use and operate on public clouds, and is partnered with many of the leading cloud providers, including Amazon Web Services, Microsoft Azure, and Joyent. Hosted Riak is also available from Engine Yard and Riak packages can always be manually installed on any physical or virtual provider, even if a machine image isn’t explicitly supported.

There are several use cases for Riak Enterprise’s multi-datacenter replication in the public cloud. Many enterprises want to maintain a cold or hot backup of their cluster in a public cloud for business continuity in the event of a datacenter outage in their private infrastructure. For other customers, the public cloud can provide a more cost-effective way of meeting peak loads, rather than building out private infrastructure to accommodate them year-round. For example, many retailers and media providers need to offer increased capacity over the holiday season. Riak Enterprise is used to scale out capacity on public clouds over these periods, either with full-sync or real-time sync depending on the business needs.

Finally, some enterprises run certain applications or services entirely on public clouds. Riak Enterprise allows for redundancy and data locality across public cloud availability zones for this use case, ensuring optimal performance and resiliency.

For a more in-depth look at common architectures and use cases for Riak Enterprise, [download our technical overview](http://info.basho.com/RiakMDC_Whitepaper.html). You can also sign up for our [webcast](http://info.basho.com/IntroToRiakMarch7.html) on Thursday, March 7th.

[Basho](http://www.twitter.com/basho)
