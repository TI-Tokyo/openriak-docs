---
title: "Riak vs. Cassandra – A Brief Comparison"
date: "2014-01-27T13:00:49+00:00"
author: "Tom Santero"
original_url: "http://basho.com/posts/technical/riak-vs-cassandra/"
archive_url: "https://web.archive.org/web/20170510231638http://basho.com/posts/technical/riak-vs-cassandra"
categories:
  - "Architecture & Distributed Systems"
---
*January 11, 2017*

[Riak vs. Cassandra blog update](http://basho.com/posts/business/riak-vs-cassandra-an-updated-brief-comparison/)

*January 27, 2014*

On the [official Basho docs](http://docs.basho.com/), we compare Riak to multiple other databases. We are currently working on updating these comparisons, but, in the meantime, we wanted to provide a more up-to-date comparison for one of the more common questions we’re asked: How does Riak compare to Cassandra?

Cassandra looks the most like Riak out of any other widely-deployed data storage technology in existence. Cassandra and Riak have architectural roots in [Amazon’s Dynamo](http://docs.basho.com/riak/latest/theory/dynamo/), the system Amazon engineered to handle their highly available shopping cart service. Both Riak and Cassandra are masterless, highly available stores that persist replicas and handle failure scenarios through concepts such as hinted handoff and read-repair. However, there are certain key differences between the two that should be considered when evaluating them.

## Data Model

Amazon’s Dynamo utilized a Key/Value data model. Early in Cassandra’s development, a decision was made to diverge from keys and values toward a wide-row data model (similar to [Google’s BigTable](http://static.googleusercontent.com/media/research.google.com/en/us/archive/bigtable-osdi06.pdf)). This means Cassandra is a Key/Key/Value store, which includes the concept of Column Families that contain columns. With this model, Cassandra is able to handle high write volumes, typically by appending new data to a row. This also allows Cassandra to perform very efficient range queries, with the tradeoff being a more rigid data model since rows are “fixed” and non-sequential read operations often require several disk seeks.

On the other hand, Riak is a straight Key/Value store. We believe this offers the most flexibility for data storage. Riak’s schemaless design has zero restrictions on data type, so an object can be a JSON document at one moment and a JPEG at the next.

Like Cassandra, Riak also excels at high write volumes. Range queries can be a little more costly, though still achievable through Secondary Indexes. In addition, there are a number of data modeling tips and tricks for Riak that make it easy to expose access to data in ways that sometimes aren’t as obvious at first glance. Below are a few examples:

- [Data Modeling](http://docs.basho.com/riak/latest/dev/data-modeling/) on Basho Docs
- [Throw Some Keys on It](https://speakerdeck.com/hectcastro/throw-some-keys-on-it)
- [Zombie Sample App](http://zombies.samples.basho.com/)

## Multi-Datacenter Replication

In Riak, [multi-datacenter replication](http://docs.basho.com/riakee/latest/cookbooks/Multi-Data-Center-Replication-v3-Architecture/) is achieved by connecting independent clusters, each of which own their own hash ring. Operators have the ability to manage each cluster and select all or part of the data to replicate across a WAN. Multi-datacenter replication in Riak features two primary modes of operation: [full sync](http://docs.basho.com/riakee/latest/cookbooks/Multi-Data-Center-Replication-v3-Architecture/#Fullsync-Replication) and [real-time](http://docs.basho.com/riakee/latest/cookbooks/Multi-Data-Center-Replication-v3-Architecture/#Realtime-Replication). Data transmitted between clusters can be encrypted via OpenSSL out-of-the-box. Riak also allows for per-bucket replication for more granular control.

Cassandra achieves replication across WANs by splitting the hash ring across two or more clusters, which requires operators to manually define a NetworkTopologyStrategy, Replication Factor, a Replication Placement Strategy, and a Consistency Level for both local and cross data center requests.

## Conflict Resolution and Object Versioning

Cassandra uses wall clock timestamps to establish ordering. The resolution strategy in this case is Last Write Wins (LWW), which means that data may be overwritten when there is write contention. The odds of data loss are magnified by (inevitable) server clock drift. More details on this can be found in the blog, “[Clocks are Hard, or, Welcome to the Wonderful World of Distributed Systems](./clocks-are-bad-or-welcome-to-distributed-systems.md).”

Riak uses a data structure called [vector clocks](http://docs.basho.com/riak/latest/theory/concepts/Vector-Clocks/) to track the causal ordering of updates. This per-object ancestry allows Riak to identify and isolate conflicts without using system clocks.

In the event of a concurrent update to a single key, or a network partition that leaves application servers writing to Riak on both sides of the split, Riak can be configured to keep all writes and expose them to the next reader of that key. In this case, choosing the **right** value happens at the application level, allowing developers to either apply business logic or some common function (e.g. merge union of values) to resolve the conflict. From there, that value can be written back to Riak for its key. This ensures that Riak never loses writes.

*For more information, visit Basho blog posts on [Why Vector Clocks are Easy](http://basho.com/why-vector-clocks-are-easy/) and [Why Vector Clocks are Hard](http://basho.com/why-vector-clocks-are-hard/).*

[Riak Data Types](https://gist.github.com/russelldb/7316f83ddd38965d9f76), first introduced in Riak 1.4 and expanded in the upcoming Riak 2.0, are designed to converge automatically. This means Riak will transparently manage the conflict resolution logic for concurrent writes to objects.

## Availability

In the event of server failures and network problems, Riak is designed to **always** accept read and write requests, even if the servers that are ordinarily responsible for that data are unavailable.

Cassandra will allow writes to (optionally) be stored on alternative servers, but **will not allow that data to be retrieved**. Only after the cluster is repaired and those writes are handed off to an appropriate replica server (with the potential data loss that timestamp-based conflict resolution implies, as discussed earlier) will the data that was written be available to readers.

Imagine a user working with a shopping cart when the application is unable to connect to the primary replicas. The user can re-add missing items to the cart but will never actually see the items show up in the cart (unless the application performs its own caching, which introduces more layers of complexity and points of failure).

## Data Integrity

When handling missing or divergent/stale data, Riak and Cassandra have many similarities. Both employ a passive mechanism where read operations trigger the repair of inconsistent replicas (known as read-repair). Both also use [Active Anti-Entropy](http://docs.basho.com/riak/1.3.2/references/appendices/concepts/Riak-Glossary/#Active-Anti-Entropy-AAE-), which builds a modified [Merkle tree](http://en.wikipedia.org/wiki/Merkle_tree) to track changes or new inserts on a per hash-ring-partition basis. Since the hash rings contain overlapping keys, the trees are compared and any divergent or missing data is automatically repaired in the background. This can be incredibly effective at combating problems such as bitrot, since Active Anti-Entropy does not need to wait for a read operation.

The key difference in implementation is that Cassandra uses short-lived, in-memory hash trees that are built per Column Family and generated as snapshots during major data compactions. Riak’s trees are on-disk and persistent. Persistent trees are safer and more conducive to ensuring data integrity across much larger datasets (e.g. 1 billion keys could easily cost 8-16GB of RAM in Cassandra versus 8-16GB of disk in Riak).

## Summary

Both Cassandra and Riak are eventually consistent, scalable databases that have strengths for specific use cases. Each has hundreds of thousands of hours of engineering invested and the commercial backing and support offered by their respective companies, Datastax and Basho. At Basho, we have labored to make Riak very robust and easy to operate at both large and small scale. For more information on how Riak is being used, visit our [Riak Users page](http://basho.com/riak-users/).

[Tom Santero](https://twitter.com/tsantero)
