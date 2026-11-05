---
title: "Riak for Advertisers"
date: "2014-04-14T14:00:27+00:00"
author: "Basho"
original_url: "http://basho.com/posts/technical/riak-for-advertisers/"
archive_url: "https://web.archive.org/web/20170801114735http://basho.com/posts/technical/riak-for-advertisers/"
categories:
  - "Use Cases"
---
*April 14, 2014*

Modern day advertisers are faced with many new challenges to ensure they can provide highly available, low latency experiences to thousands of clients and partners, and millions of users. They are also tasked with serving large amounts of data all over the world and can experience significant traffic spikes. That is why advertisers are switching to Riak for their database solution. Riak’s redundant, fault-tolerant design ensures that advertising companies can serve data reliably and quickly. Riak is also built for operational simplicity at scale and helps advertisers quickly grow to meet peak loads.

## Top Use Cases for Riak in Advertising

- **Serving Ad Content:** Riak’s rapid storage and content agnosticism makes it ideal for storing ad content and handling influxes of ad traffic.
- **Session Storage:** This type of data is naturally a good fit for Riak’s key/value model. This data can also be encoded in many different ways and can evolve without any administrative changes to the schema.
- **Mobile Experiences:** Riak is ideal for the low-latency, always-available small object storage needed to power mobile experiences across platforms.
- **Global Data Locality:** Riak Enterprise’s multi-datacenter capabilities allow advertisers to maintain a global data footprint while providing an always-on, low-latency experience, anywhere in the world.

## Riak in Production

Riak is already in production at many top advertising and marketing organizations. Here’s a look at a few that have switched to Riak.

**Tapjoy**  
Tapjoy is a mobile advertising and monetization platform that is available on over one billion devices across the world. They selected Riak due to its high availability, low-latency, and multi-datacenter replication. They store 48TB of data in Riak and operate hundreds of thousands of reads/writes per second. Learn more about why Tapjoy selected Riak from the [case study](http://basho.com/tapjoy-deploys-riak-to-support-worldwide-mobile-advertising/).

**OpenX**  
OpenX is an ad technology platform that serves trillions of ads. They use Riak for user and trafficking data behind their data services API. OpenX also uses Riak’s multi-datacenter replication across several data centers. [Watch Anthony Molinaro](http://vimeo.com/53480727) (Infrastructure Architect at OpenX) talk about how they use Riak for their serve-time data needs.

**Velti**  
Velti is a mobile marketing and advertising technology provider. They use Riak for their interactive mobile platform, including letting people interact with their TV by voting, giving feedback, participating in contests, etc. Velti runs 18 nodes across two data centers, which provides them with scale, durability, and availability. Their [case study](http://basho.com/assets/CaseStudyVelti.pdf) goes into more detail about the process of moving to Riak.

**JBA**  
JBA is a digital consultancy that specializes in developing customer understanding and behavioral targeting. They use Riak as a core part of their behavioral analysis and remarketing tool. They store over 10 million objects in Riak and can easily scale up to account for holiday sales cycles or new product releases as needed. Learn more about why they selected Riak from the beginning from their [case study](http://basho.com/riak-is-a-core-part-of-jbas-behavioral-analysis-tools/).

**Moz**  
Moz provides analytics software to track all of a website’s inbound marketing efforts on one platform. They support over 27,000 customers and 300,000 community members worldwide. Moz uses Riak to store customer campaign search engine rankings data. Learn more about how Riak outperformed Cassandra at Moz in the [case study](http://basho.com/moz-selected-riak-because-cassandra-simply-could-not-keep-up/).

## Data Modeling in Riak

Riak has a “schemaless” design. Objects are comprised of key/value pairs, which are stored in flat namespaces called buckets. Here are some common approaches to structuring advertising data with Riak’s key/value design:

| Data Type | Key | Value |
| --- | --- | --- |
| Advertisement | Campaign ID | Ad Content |
| User Data | Login, Email, UUID | User Attributes (often stored as a JSON document) |
| Image or Video Content | Content Name, ID or Integer | .JPG, .PNG, .GIF or other image format; .MOV, .MPG, .MP4 or other video file format |
| Session Information | User or Session ID | Session Data |

To learn more about how advertisers can use Riak for their data needs, check out the complete overview, “[Advertisers on Riak: A Technical Introduction](http://info.basho.com/RiakOnAdvertising.html).” To get started with Riak, [Contact Us](http://basho.com/contact/) or [download it now](http://docs.basho.com/riak/latest/downloads/).

[Basho](http://twitter.com/basho)
