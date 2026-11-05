---
title: "Kick off the New Year with Riak TS v1.5 and the Riak Spark Connector!"
date: "2017-01-17T10:39:37+00:00"
author: "Pavel Hardak"
original_url: "http://basho.com/posts/technical/kick-off-the-new-year-with-riak-ts-v1-5-and-the-riak-spark-connector/"
archive_url: "https://web.archive.org/web/20170211193949http://basho.com/posts/technical/kick-off-the-new-year-with-riak-ts-v1-5-and-the-riak-spark-connector/"
categories:
  - "Releases"
  - "Integrations & Plugins"
---
I am very excited to announce the release of Riak TS v1.5 and an update to the Riak Spark Connector. Since our open-source release of Riak TS in April 2016, we have been working together with customers to add new features as quickly as possible. As a leading open source company, we enjoy working in a transparent and agile way. This allows us to quickly prioritize feedback from customers and rapidly deliver new features. We completed four Riak TS public releases in 2016 and plan to do even more in 2017. Needless to say, we are committed to making upgrades very easy, including rolling cluster upgrades without downtime.

About a week before the end of the year, we released Riak TS v1.5. This release packs in new and improved features plus performance improvements. It was released in both open source and Enterprise editions.

**Riak TS v1.5 New features:**

- [ORDER BY](http://docs.basho.com/riak/ts/latest/using/querying/select/order-by/) clause in SELECT statement
- [LIMIT](http://docs.basho.com/riak/ts/latest/using/querying/select/limit/) clause in SELECT statement
- [ASC / DESC](http://docs.basho.com/riak/ts/latest/using/planning/#sort-with-local-keys) keywords in CREATE TABLE definition
- [BLOB](http://docs.basho.com/riak/ts/latest/using/planning/#column-definitions) data type to store unstructured (e.g. binary) or opaque (e.g JSON) data in Riak TS tables
- [SHOW CREATE TABLE](http://docs.basho.com/riak/ts/latest/using/querying/show-create-table/) command to review SQL definition and replication parameters
- [DELETE](http://docs.basho.com/riak/ts/latest/using/querying/delete/) command to remove Riak TS records using ‘riak-shell’
- [EXPLAIN](http://docs.basho.com/riak/ts/latest/using/querying/explain/) command to review query execution plan
- [Ubuntu 16](http://docs.basho.com/riak/ts/latest/releasenotes/#compatibility) (xenial) support (dropped support for Ubuntu 12)

**Riak TS v1.5 Improved or Updated Features:**

- Enhanced [NULL](http://docs.basho.com/riak/ts/latest/using/querying/select/#is-not-null) handling in SELECT statements
- Reduced query latency and execution plan, especially for read queries spanning multiple quanta, [new configuration parameters](http://docs.basho.com/riak/ts/latest/configuring/riakconf/#maximum-returned-data-size)
- Enhanced usability of the [riak shell](http://docs.basho.com/riak/ts/latest/using/riakshell/) tool, added multi-line paste functionality, built-in help for SQL commands, and enhanced error handling
- Integration of features from Riak KV 2.2 codebase ([Riak Core Fundamentals](http://docs.basho.com/riak/ts/latest/using/core-fundamentals/))
- Plus, many documentation and performance improvements ([Release Notes)](http://docs.basho.com/riak/ts/1.5.0/releasenotes/)

Note: If you are upgrading from a previous release of Riak TS, please review configuration changes. These changes include added and deprecated parameters in [*riak.conf*.](http://docs.basho.com/riak/ts/latest/configuring/riakconf/)

In addition to releasing Riak TS v1.5, we also release [Riak Spark Connector](http://basho.com/products/apache-spark/) v1.6.2. This release includes support for Riak TS v1.5, Apache Spark v1.6.x and several fixes for bugs, reported by the community.

**Get Started Now with Riak TS v1.5**

- [Download](http://info.basho.com/Riak-Open-Source-Download.html) Open Source
- [Sign In](http://basho.zendesk.com/) to download Enterprise Edition
- [Learn more](http://docs.basho.com/riak/ts/latest/) about developing with and deploying Riak TS
- [Basho Academy](http://academy.basho.com)

For a demo or to talk to one of our Riak Solution Architects, please [contact us](http://basho.com/contact/).

This was a great team effort at Basho. I am extremely thankful to Engineering, DevOps and Documentation teams, who worked really hard to make it happen. After a short and well-deserved vacation, we are back working on the next release for the community of Riak users. Stay tuned!

Happy New Year and best wishes for 2017!  
Pavel Hardak  
Director of Product Management, Riak TS and Integrations  
[@PavelHardak](https://twitter.com/PavelHardak)
