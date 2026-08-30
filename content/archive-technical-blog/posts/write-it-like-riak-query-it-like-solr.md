---
title: "Write it like Riak; Query it Like Solr"
date: "2014-10-02T11:20:22+00:00"
author: "Tyler Hannan"
original_url: "http://basho.com/posts/technical/write-it-like-riak-query-it-like-solr/"
archive_url: "https://web.archive.org/web/20170410060017http://basho.com/posts/technical/write-it-like-riak-query-it-like-solr/"
categories:
  - "Search & Analytics"
  - "Integrations & Plugins"
---
*October 2, 2014*

Back in June of 2012, Basho set out to build a better full-text search solution for data stored in Riak. At that time, Riak already had a full-text search solution, but as our customer’s needs were changing they were investing in the richness provided by Apache Solr. In collaboration with these customers we began to look at integration with Apache Solr to meet their requirements for search capabilities.

At around the same time, the Solr team released [Apache Solr 3.6.0](https://lucene.apache.org/solr/), its last major revision before the much anticipated 4.0 release. Despite not having a complete solution for horizontal scalability, Solr’s 3.6.0 single-node performance remained second to none.

Fast forward to today.

[Riak 2.0](http://basho.com/riak-2-0-new-capabilities-new-use-cases-available-for-download/) contains the next iteration of [Riak Search](http://docs.basho.com/riak/latest/dev/using/search/) (codenamed Yokozuna, for those who have been following its progress). Simply put, it is the result of our efforts to pair the strengths of Riak as a horizontally scalable, distributed database with the powerful full-text search functionality of Apache Solr.

If you want the search scalability of Solr, paired with a fundamentally solid data store, integrated with distributed key/value, you’ll want to take a look at Riak Search.  
How Does It Work?

To understand how Riak Search works, it’s important to know what its components are:

- Riak
- Riak Search
- Apache Solr

Despite being a part of Riak, Riak Search is a separate Erlang application. It monitors for changes to data in Riak and propagates those changes to indexes managed by Solr. As usual, incoming data is evenly distributed across all nodes in the cluster. What’s new is that each node in the cluster now also supervises an instance of Solr. Each Solr instance houses indexes for data the Riak node where it co-resides.

On the query side, Riak Search accepts standard Solr queries and expands them to [Distributed Search](https://wiki.apache.org/solr/DistributedSearch) queries behind the scenes. Distributed Search queries target multiple Solr instances (or `shards` using Solr’s terminology) to provide a complete result set across replicas. (For more details on this, see the [Advanced Search](http://docs.basho.com/riak/latest/dev/advanced/search/) section of our documentation).

## Ad-hoc queries

The update to Riak Search also gives you the ability to ask more complex questions of the data stored in Riak, without requiring as much data modeling upfront.

**Step 1. add suffix and index**   
The first step is to tell Solr the attribute type by appending a suffix.

For example, if you had a `name` attribute inside a JSON object and you wanted to index it as a string, you’d rename it to `name_s`. If, instead, you wanted to index an `age` attribute, you could do `age_i` to index it as an integer for range queries.

**Step 2: query against index**  
After the values are indexed, you can send Solr (default query engine is `lucene`) queries against the index:

Give me all runners with 10 or more miles run (open-ended range query)

`search/runners?wt=json&q=miles_run_i:[10 TO *]`

Give me all of the runners with a name that begins with Jake (wildcard query)

`search/runners?wt=json&q=name_s:Jake*`

Give me all of the runner with bios that contain references to “Roger Bannister” (exact match query)

`search/runners?wt=json&q=bio_t:”Roger Bannister”`

## Additional Search Tools

In addition to basic ad-hoc and range queries, Riak Search provides a number of powerful search enhancers, including:

- support for various MIME types, including JSON, XML, plain text and [Riak Data Types](http://docs.basho.com/riak/latest/theory/concepts/crdts/)
- [analyzer, token and filter](https://cwiki.apache.org/confluence/display/solr/Understanding+Analyzers%2C+Tokenizers%2C+and+Filters) support for 30+ languages
- term boosting
- sorting
- pagination
- scoring and ranking based on result relevancy
- result snippet [highlighting](https://cwiki.apache.org/confluence/display/solr/Highlighting)

A hands-on guide to configuring and using Riak Search is available [here](http://docs.basho.com/riak/latest/dev/using/search/).

## Keeping Indexes Fresh

In a land where many open source full-text search solutions exist, it is important to identify what makes Riak Search unique against the competition. One important answer to that question is Riak’s [Active Anti-Entropy](http://docs.basho.com/riak/2.0.0/theory/concepts/aae/) (better known as keeping your search indexes fresh, over time, as data is manipulated in Riak).

Many real world applications offer search functionality against a subset of record attributes by passing them along to a full-text search engine. Meanwhile, the source of truth for those records remains in a database.

As an example, consider an Oracle instance that contains your entire product catalog. Next to that Oracle database may be an instance of Solr that indexes only the `titles` and `descriptions` columns of your `products` table. This setup allows users to search freely against those fields on your site.

How do you keep the two systems in sync? How do you avoid situations where records exist in the database, but don’t show up in search results? How do you prevent search results from containing products that are no longer in the database?

This problem isn’t easy to deal with. With Oracle, and other relational systems, the solution is often to periodically rebuild the entire product catalog search index. But what happens when you have too many products to re-index without sacrificing some availability? What happens when there is too much activity for an index rebuild to be feasible?

With Riak Search, Riak is responsible for your data and Solr is responsible for your index. Riak ensures that your indexes in Solr are up-to-date as changes occur to your data. So, unlike the relational database to full-text search platform outlined above, Riak does all of the work to keep things aligned so that you don’t have to.

## Resources

Eric Redmond gave [a talk at RICON West](http://www.youtube.com/watch?v=-c1eynVLNMo) on Riak Search 2.0.

## Downloads

Riak Search is now available with Riak 2.0. Download Riak 2.0 on our [Downloads Page](http://docs.basho.com/riak/latest/downloads/).

[Tyler Hannan](http://twitter.com/tylerhannan)
