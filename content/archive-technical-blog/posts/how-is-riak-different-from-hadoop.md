---
title: "\"How is Riak different from Hadoop?\""
date: "2013-10-28T09:00:08+00:00"
author: "Basho"
original_url: "http://basho.com/posts/technical/how-is-riak-different-from-hadoop/"
archive_url: "https://web.archive.org/web/20170524144034http://basho.com/posts/technical/how-is-riak-different-from-hadoop"
categories:
  - "Integrations & Plugins"
---
*October 28, 2013*

The technology community is extremely agile and fast-paced. It can turn on a dime to solve business problems as they arise. However, with this agility comes budding terminology that can often provide false categorizations. This can lead to confusion, especially when companies evaluate new technologies based on a surface understanding of these terms. The world of data is full of these terms, including the notorious “[NoSQL](http://basho.com/nosql-explained/)” and “big data.”

As described in a [previous post](http://basho.com/nosql-is-a-bad-name-but-we-will-still-be-at-nosql-now/), NoSQL is a misleading term. This term represents a response to changing business priorities that require more flexible, resilient architectures (as opposed to the traditional, rigid systems that often happen to use SQL). However, within the NoSQL space, there are dozens of players that can be as different from one another as they are from any of the various SQL-speaking systems.

Big data is another term that, while fairly self-explanatory, has been overused to the point of dilution. One reason why NoSQL databases have become necessary is because of their ability to easily scale to keep up with data growth. Simply storing a lot of data isn’t the solution though. Some data is more critical than others (and should be accessible no matter what) and some data needs to be analyzed to provide business insights. When digging into a business, big data is too vague a term to describe both of these use cases.

As these terms (to highlight a few) are used, it can lead to industry confusion. One area of confusion that we have experienced relates to Basho’s own distributed database, Riak, and the distributed processing system, Hadoop.

While these two systems are actually complementary, we are often asked “How is Riak different from Hadoop?”

To help explain this, it’s important to start with a basic understanding of both systems. Riak is a distributed database that is built for high availability, fault tolerance, and scalability. It is best used to store large amounts of critical data that applications and users need to constantly be able to access. Riak is built by Basho Technologies and can be used as an alternative to or in conjunction with relational databases (such as MySQL) or to other “NoSQL” databases (such as MongoDB or Cassandra).

Hadoop is a framework that allows for the distributed parallel processing of large data sets across clusters of computers. It was originally based on the “MapReduce” system, which was invented by Google. Hadoop consists of two core parts: the underlying Hadoop Distributed File System (HDFS), which ensures stored data is always available to be analyzed, and MapReduce, which allows for scalable computation by dividing and running queries over multiple machines. Hadoop provides an inexpensive, scalable solution for bulk data processing and is mostly used as part of an overarching analytics strategy, not for primary “hot” data storage.

One easy way to distinguish between the two is to look at some of the common use cases.

## Riak Use Cases

Riak can be used by any application that needs to always have access to large amounts of critical data. Riak uses a key/value data model and is data-type agnostic, so operators can store any type of content in Riak. Due to the key/value model, certain industry use cases fit easily into Riak. These include:

- **Gaming** – storing player data, session data, etc
- **Retail** – underpinning shopping carts, product inventories, etc
- **Mobile** – social authentication, text and multimedia storage, global data locality, etc
- **Advertising** – serving ad content, session storage, mobile experiences, etc
- **Healthcare** – prescription or patient records, patient IDs, health data that must always be available across a network of providers, etc

For a full list of use cases, check out our [Users Page](http://basho.com/riak-users/).

## Hadoop Use Cases

Hadoop is designed for situations where you need to store unmodeled data and run computationally intensive analytics over that data. The original use cases of both MapReduce and Hadoop were to produce indexes for distributed search engines at Google and Yahoo respectively. Any industry that needs to do large scale analytics to better improve their business can use Hadoop. Some common examples include finance (build models to do accurate portfolio evaluations and risk analysis) and eCommerce (analyze shopping behavior to deliver product recommendations or better search results).

Riak and Hadoop are based on many of the same tenets, making their usage complementary for some companies. Many companies that utilize Riak today have created scripts, or processes, to pull data from Riak and push into other solutions (like Hadoop) for the purpose of historical archiving or future analysis. Recognizing this trend, Basho is exploring the creation of additional tools to simplify this process.

If you are interested in our thinking on these data export capabilities, please [contact us](http://basho.com/contact/).

## In Summary

Every tool has its value. Hadoop excels at being used by a relatively small subset of the business to answer big questions. Riak excels at being used by a very large number of users and powering critical data for businesses.

[Basho](http://twitter.com/basho)
