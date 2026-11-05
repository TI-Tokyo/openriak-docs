---
title: "Replication is the Key for Scalability & High Availability"
date: "2014-12-18T09:00:59+00:00"
author: "Tyler Hannan"
original_url: "http://basho.com/posts/technical/replication-is-the-key-for-scalability-high-availability/"
archive_url: "https://web.archive.org/web/20170527071141http://basho.com/posts/technical/replication-is-the-key-for-scalability-high-availability"
categories:
  - "Replication"
---
*December 18, 2014*  
One of the interesting things about attending industry events, like [AWS re:Invent](https://reinvent.awsevents.com/), is identifying common trends that arise in conversations. Recent conversations point to a renewed interest in “enterprise ready replication” for [NoSQL databases](http://basho.com/nosql-explained/).

As business data continues to grow, there is an entirely new set of challenges that are presented related to availability, scalability, and fault-tolerance. While most NoSQL databases work at small scale, availability is often compromised as applications reach full production or peak capacity. Having the right replication functionality is key to ensuring that availability requirements are not compromised as your system grows.

“Replication” may mean different things based on context. In this case, we are referring to the movement of data in a database cluster — or across datacenters — for the purpose of redundancy or data locality. If your database experience began in an RDBMS context, then replication implies a specific contextual understanding of multi-master transactional deployment and, perhaps, shipping transaction logs between incremental backups in a hot/warm database configuration. In contrast, for those who began in the NoSQL era, the term may evoke images of replica-sets on a sharded infrastructure and the operational overhead associated therewith.

In a distributed NoSQL database, like Riak, the term replication is used to encompass two distinct concepts. First, intra-cluster replication for high availability and fault tolerance within the datacenter; and second, multi-datacenter replication for data locality and global availability. There is none of the complexity of log shipping or dealing with a sharded infrastructure.

## Intra-cluster Replication

Data replication is a core feature of Riak’s basic architecture. Riak was designed to operate as a clustered system containing multiple nodes (commodity servers or cloud instances). The replication implementation allows data to live on multiple machines at once, with a single write request, in case a node in the cluster goes down or is unavailable due to issues like network partitioning.

Intra-cluster replication is fundamental and automatic in Riak, so that your data is always available. All data stored in Riak is replicated to a number of nodes in the cluster according to a configurable parameter (`n_val`) set in a buckets [bucket type](http://docs.basho.com/riak/latest/dev/advanced/bucket-types/).

With the default `n_val` setting of 3, there are always three copies of all data. These copies will be on three different partitions/vnodes. A detailed explanation and analysis of this replication capability is discussed in the Riak documentation – *[Understanding replication by example](http://docs.basho.com/riak/latest/theory/concepts/Replication/#Understanding-replication-by-example)*.

In the case of intra-cluster replication, or what we would refer to simply as “replication”, data distribution ensures redundant data such that high availability is maintained in a failure state.

## Multi-Datacenter Replication

In contrast to intra-cluster replication, multi-datacenter replication (a feature of [Riak Enterprise](http://basho.com/riak-enterprise/)) is a critical part of modern application infrastructures. Riak Enterprise offers multi-datacenter replication features so that data stored in Riak can be replicated to multiple sites (vs. multiple servers in the same site).

As we are all aware, understanding application latency (for an end user) begins with the realization data can’t travel faster than the speed of light. So, inherently, as source information moves further from it’s consumption latency is introduced. As such, there is a set amount of latency for a customer connecting to your application hosted in New York when they are accessing the application from San Francisco. This latency profile increases, and becomes more complex, as the geographic distribution of your customer base increases.

With multi-datacenter replication in Riak Enterprise, data can be replicated across locations and geographic areas providing for disaster recovery, data locality, compliance with regulatory requirements, the ability to “burst” peak loads into public cloud infrastructure, amongst others.

Riak’s multi-datacenter replication is masterless. One cluster acts as a primary, or source, cluster. The primary cluster handles replication requests from one or more secondary, or sink, clusters (generally located in datacenters in other regions or countries). If the datacenter with the primary cluster goes down, a secondary cluster can automatically take over as the primary cluster.

More architectural strategies for multi-datacenter implementations, are covered in the Basho whitepaper entitled *[Riak Enterprise: Multi-Datacenter Replication – A Technical Overview & Use Cases](http://info.basho.com/RiakMDC_Whitepaper.html)* or in the Basho Documentation section ~~*Multi-Datacenter Replication: v3 Architecture*~~.

## In Summary

Replication, inside a cluster, is a core design tenant of Riak. This is used to provide the availability and fault-tolerance characteristics — with a low operational overhead — that many unstructured data workloads demand.

Multi-datacenter replication, while related, is an entirely different approach and architecture to enable the geographic distribution of data to solve for redundancy, geo-data locality, etc.

Replication is an important scalability feature of any database deployment. Ensuring that your NoSQL database replicates data in a way that is scalable, operationally simple and achieves your business objectives is key to your success.

[Tyler Hannan](http://twitter.com/tylerhannan)
