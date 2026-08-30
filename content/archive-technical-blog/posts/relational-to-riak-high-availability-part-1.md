---
title: "Relational to Riak – High Availability"
date: "2013-11-13T11:00:11+00:00"
author: "Basho"
original_url: "http://basho.com/posts/technical/relational-to-riak-high-availability-part-1/"
archive_url: "https://web.archive.org/web/20170801120753http://basho.com/posts/technical/relational-to-riak-high-availability-part-1/"
categories:
  - "Architecture & Distributed Systems"
---
*November 13, 2013*

This series of blog posts will discuss how [Riak](http://basho.com/riak/) differs from traditional relational databases. For more information about any of the points discussed, download our technical overview, “[From Relational to Riak](http://basho.com/assets/RelationaltoRiak.pdf).”

---

One of the biggest differences between Riak and relational systems is our focus on availability. Riak is designed to be deployed to, and runs best on, multiple servers. It can continue to function normally in the presence of hardware and network failures. Relational databases, conversely, are simplest to set up on a single server.

Most relational databases offer a master/slave architecture for availability, in which only the master server is available for data updates. If the master fails, the slave is (hopefully) able to step in and take over.

However, even with this simple model, coping with failure (or even properly defining it) is non-trivial. What happens if the master and slave server cannot talk to each other? How do you recover from a split brain scenario, where both servers think they’re the master and accept updates? What happens if the slave is slow to respond to updates sent from the master database? Can clients read from a slave? If so, does the master need to verify that the slave has received all updates before it commits them locally and responds to the client that requested the updates?

Conversely, Riak is explicitly designed to expect server and network failure. Riak is a masterless system, meaning any server can respond to read or write requests. If one fails, others will continue to service client requests. Once this server becomes available again, the cluster will feed it any updates that it missed through a process we call [hinted handoff](http://docs.basho.com/riak/latest/theory/concepts/glossary/#Hinted-Handoff).

Because Riak’s system allows for reads and writes when multiple servers are offline or otherwise unreachable, data may not always be consistent across the environment (usually only for a few milliseconds). However, through self-healing mechanisms like [read repair](http://docs.basho.com/riak/latest/theory/concepts/glossary/#Read-Repair) and [Active Anti-Entropy](http://docs.basho.com/riak/latest/theory/concepts/glossary/#Active-Anti-Entropy-AAE-), all updates will propagate to all servers making data eventually consistent.

For many use cases, high availability is more important than strict consistency. Data unavailability can negatively impact revenue, damage user trust, lead to poor user experience, and cause lost critical data. Industries like gaming, mobile, retail, and advertising require always-on availability. Visit our [Users](http://basho.com/riak-users) Page to see how companies in various industries use Riak.

[Basho](https://twitter.com/Basho)
