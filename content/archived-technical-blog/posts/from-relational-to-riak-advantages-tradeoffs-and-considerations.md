---
title: "From Relational to Riak- Advantages, Tradeoffs and Considerations"
date: "2012-12-19T00:00:00+00:00"
author: "Basho"
original_url: "http://basho.com/posts/technical/from-relational-to-riak-advantages-tradeoffs-and-considerations/"
archive_url: "https://web.archive.org/web/20170603173940http://basho.com/posts/technical/from-relational-to-riak-advantages-tradeoffs-and-considerations"
categories:
  - "Data Modeling"
  - "Architecture & Distributed Systems"
---
*December 19, 2012*

We work with many people building platforms and applications on Riak that have traditionally lived on relational systems. The switch to Riak can be driven by the needs of greenfield applications and growing data volumes, business requirements around scale and availability, or the desire for operational ease and multi-site replication.

Some of the most common questions we get are from teams with a primary background in MySQL, Oracle Database or other relational systems wondering about the advantages and tradeoffs of moving to Riak. To address these common questions, we’ve written up an introductory guide on moving from relational to Riak. In it, we cover:

- Scalability benefits of Riak, including an examination of limitations around master/slave architectures and sharding, and what Riak does differently
- A look at the operational aspects of Riak and where they differ from relational approaches
- Riak’s data model and benefits for developers, as well as the tradeoffs and limitations of a key/value approach
- Migration considerations, including where to start when migrating existing applications to Riak
- Riak’s eventually consistent design, how it differs from a strongly consistent design, and things you need to know about handling data conflicts in Riak
- Multi-site replication options in Riak

You can download the paper [here](http://basho.com/assets/RelationaltoRiakDEC.pdf "From Relational to Riak"), and when you’re ready to dive deeper, check out our [online documentation](http://docs.basho.com/) with more information on Riak, building applications on it, and our commercial products.

[Basho Team](https://twitter.com/basho)
