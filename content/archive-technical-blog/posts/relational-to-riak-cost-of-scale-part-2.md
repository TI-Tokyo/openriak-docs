---
title: "Relational to Riak – Cost of Scale"
date: "2013-11-14T11:00:07+00:00"
author: "Basho"
original_url: "http://basho.com/posts/technical/relational-to-riak-cost-of-scale-part-2/"
archive_url: "https://web.archive.org/web/20170801120757http://basho.com/posts/technical/relational-to-riak-cost-of-scale-part-2/"
categories:
  - "Architecture & Distributed Systems"
  - "Performance"
---
*November 14, 2013*

This series of blog posts will discuss how [Riak](http://basho.com/riak/) differs from traditional relational databases. For more information about any of the points discussed, download our technical overview, “[From Relational to Riak.](http://basho.com/assets/RelationaltoRiak.pdf)” The previous post in the series was [Relational to Riak – High Availability](http://basho.com/relational-to-riak-high-availability-part-1).

---

Riak is designed for scalability, which truly separates it from relational systems. As described in the [previous post](http://basho.com/relational-to-riak-high-availability-part-1), relational databases run best on a single server. If the dataset grows beyond the capacity of this single machine, it can become prohibitively expensive (or even impossible) to simply upgrade to a bigger machine. In such a scenario, the only option may be to add more machines and divide the dataset across them using a technique called sharding.

Sharding divides data into logical parts (such as alphabetical, by customer, or by geographic region) that can be distributed across multiple machines – often manually. If data continues to grow, this process may need to be repeated at great expense.

Sharding is not only difficult, it also will typically lead to hot spots – meaning certain machines are responsible for storing and serving a disproportionately high amount of both data and requests. Hot spots can cause unpredictable latency and degraded performance.

(And remember all the ways in which availability is a challenge? Combine sharding with a master/slave architecture for maximal expense and general unpleasantness.)

Instead of sharding, Riak evenly distributes data across a cluster using [consistent hashing](http://docs.basho.com/riak/latest/theory/concepts/glossary/#Consistent-Hashing). In a Riak cluster, the data space is divided into partitions which are claimed by the servers. When new data is written to the database, these objects are evenly placed around the ring and replicated 3 times (by default). This ensures that your data will always be available, even when nodes fail.

When nodes are added or removed, data is rebalanced automatically. New machines assume ownership of some of the partitions and existing machines hand off relevant partitions and associated data until data ownership is equal amongst nodes.

By eliminating the manual requirements of sharding and making hot spots highly unlikely, Riak makes it significantly easier for companies to scale, whether it’s just for a few months to handle peak loads or to support long-term growth strategies.

[Basho](https://twitter.com/Basho)
