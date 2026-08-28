---
title: 'Build a first OpenRiak application'
description: 'Introduce language-specific learning paths for storing, reading, updating, querying, and deleting data.'
weight: 1
diataxis: 'tutorial'
product: 'OpenRiak KV'
product_version: '3.4.0'
status: 'editorially-rewritten'
draft: true
audience:
  - 'new-developers'
source_material:
  - 'legacy-3.2.5'
  - 'live-3.2.5'
  - 'proposed-kv'
legacy_3_2_5_sources:
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\developing\app-guide.md'
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\developing\getting-started.md'
tags: ['diataxis', 'kv', 'tutorial']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Introduce language-specific learning paths for storing, reading, updating, querying, and deleting data.

## Overview

### OpenRiak KV Application Guide

[usage conflict resolution]: {{< baseurl >}}kv/3.4.0/how-to/develop/resolve-conflicts/
[dev data model#log]: {{< baseurl >}}kv/3.4.0/how-to/plan/map-data-to-objects/
[dev data model#sensor]: {{< baseurl >}}kv/3.4.0/how-to/plan/map-data-to-objects/
[concept eventual consistency]: {{< baseurl >}}kv/3.4.0/explanation/consistency/eventual-consistency/
[dev data model#user]: {{< baseurl >}}kv/3.4.0/how-to/plan/map-data-to-objects/
[dev kv model]: {{< baseurl >}}kv/3.4.0/how-to/plan/map-data-to-objects/
[dev data types]: {{< baseurl >}}kv/3.4.0/reference/data/distributed-data-types/
[dev data types#counters]: {{< baseurl >}}kv/3.4.0/reference/data/distributed-data-types/
[dev data types#sets]: {{< baseurl >}}kv/3.4.0/reference/data/distributed-data-types/
[dev data types#maps]: {{< baseurl >}}kv/3.4.0/reference/data/distributed-data-types/
[usage create objects]: {{< baseurl >}}kv/3.4.0/how-to/develop/create-object/
[usage search]: {{< baseurl >}}kv/3.4.0/reference/specialized-apis/legacy-query-api/
[use ref search]: {{< baseurl >}}kv/3.4.0/reference/specialized-apis/legacy-query-api/
[usage 2i]: {{< baseurl >}}kv/3.4.0/how-to/develop/query-secondary-indexes/
[dev client libraries]: {{< baseurl >}}kv/3.4.0/reference/client-libraries/
[concept crdts]: {{< baseurl >}}kv/3.4.0/explanation/data-model/distributed-data-types/
[dev data model]: {{< baseurl >}}kv/3.4.0/how-to/plan/map-data-to-objects/
[usage mapreduce]: {{< baseurl >}}kv/3.4.0/how-to/develop/run-mapreduce/
[apps mapreduce]: {{< baseurl >}}kv/3.4.0/how-to/develop/run-mapreduce/
[use ref 2i]: {{< baseurl >}}kv/3.4.0/reference/data/secondary-indexes/
[plan backend leveldb]: {{< baseurl >}}kv/3.4.0/explanation/storage/leveldb/
[plan backend bitcask]: {{< baseurl >}}kv/3.4.0/explanation/storage/bitcask/
[plan backend memory]: {{< baseurl >}}kv/3.4.0/explanation/storage/memory/
[plan backend leveled]: {{< baseurl >}}kv/3.4.0/explanation/storage/leveled/
[obj model java]: {{< baseurl >}}kv/3.4.0/tutorials/first-application/java/
[obj model ruby]: {{< baseurl >}}kv/3.4.0/tutorials/first-application/ruby/
[obj model python]: {{< baseurl >}}kv/3.4.0/tutorials/first-application/python/
[obj model csharp]: {{< baseurl >}}kv/3.4.0/tutorials/first-application/csharp/
[obj model nodejs]: {{< baseurl >}}kv/3.4.0/tutorials/first-application/nodejs/
[obj model erlang]: {{< baseurl >}}kv/3.4.0/tutorials/first-application/erlang/
[obj model golang]: {{< baseurl >}}kv/3.4.0/tutorials/first-application/golang/
[concept strong consistency]: {{< baseurl >}}kv/3.4.0/reference/specialized-apis/strong-consistency-api/
[use ref strong consistency]: {{< baseurl >}}kv/3.4.0/reference/specialized-apis/strong-consistency-api/
[cluster ops strong consistency]: {{< baseurl >}}kv/3.4.0/explanation/consistency/strong-consistency/
[config strong consistency]: {{< baseurl >}}kv/3.4.0/how-to/configure/strong-consistency/
[apps strong consistency]: {{< baseurl >}}kv/3.4.0/reference/specialized-apis/strong-consistency-api/
[usage update objects]: {{< baseurl >}}kv/3.4.0/how-to/develop/update-object/
[apps replication properties]: {{< baseurl >}}kv/3.4.0/explanation/replication/references-and-triggers/
[install index]: {{< baseurl >}}kv/3.4.0/how-to/install/
[getting started]: {{< baseurl >}}kv/3.4.0/tutorials/first-application/
[usage index]: {{< baseurl >}}kv/3.4.0/how-to/develop/
[glossary]: {{< baseurl >}}kv/3.4.0/explanation/foundations/glossary/

So you've decided to build an application using Riak as a data store. We
think that this is a wise choice for a broad variety of use cases. But
using Riak isn't always straightforward, especially if you're used to
developing with relational databases like like MySQL or PostgreSQL or
non-persistent key/value stores like Redis. So in this guide, we'll walk
you through a set of questions that should be asked about your use case
before getting started. The answer to those questions may inform
decisions about which Riak features you should use, what kind of
replication and conflict resolution strategies you should employ, and
perhaps even how parts of your application should be built.

#### What Kind of Data Are You Storing?

This is an important initial question for two reasons:

1. Not all data is a good fit for Riak. If your data isn't a good fit,
we would advise that you seek out a storage system that better suits
your needs.
2. The kinds of data that you're storing should guide your decision both
about _how_ to store and access your data in Riak and about which Riak
features would be helpful (and which ones might even be harmful).

##### Good Fits for Riak

Riak tends to be an excellent choice if you're dealing with any of the
following:

* **Immutable data** - While Riak provides several means of
  [resolving conflicts][usage conflict resolution] between different replicas
  of objects, those processes can lead to slower performance in some
  cases. Storing immutable data means that you can avoid those processes
  altogether and get the most out of Riak.
* **Small objects** - Riak was not built as a store for large objects
  like video files or other
  [BLOB](http://en.wikipedia.org/wiki/Binary_large_object)s. We built
  [Riak CS](https://riak.com/riak-cloud-storage/) for that. Riak is
  great, however, for JSON, [log files][dev data model#log], [sensor data][dev data model#sensor], HTML files, and other objects that tend
  to run smaller than 1 MB.
* **Independent objects** - Objects that do not have interdependencies
  on other objects are a good fit for OpenRiak's [eventually consistent][concept eventual consistency] nature.
* **Objects with "natural" keys** - It is almost always advisable to
  build keys for objects out of timestamps, [usernames][dev data model#user],
  or other ["natural" markers][dev kv model] that distinguish
  that object from other objects. Data that can be modeled this way fits
  nicely with Riak because Riak emphasizes extremely fast object lookup.
* **Data compatible with [Riak Data Types][dev data types]** - If
  you're working with mutable data, one option is to run basic CRUD
  operations on that data in a standard key/value fashion and either
  manage conflict resolution yourself or allow Riak to do so. But if
  your data can be modeled as a [counter][dev data types#counters],
  [set][dev data types#sets], or [map][dev data types#maps], you
  should seriously consider using [Riak Data Types][dev data types],
  which can speed application development and transfer a great deal of
  complexity away from the application and to Riak itself.

##### Not-so-good Fits for Riak

Riak may not such be a good choice if you use it to store:

* **Objects that exceed 1-2MB in size** - If you will be
  storing a lot of objects over that size, we would recommend checking
  out [Riak CS]({{< baseurl >}}riak/cs/latest/) instead, as Riak
  CS was built to solve this problem. Storing large objects in Riak will
  typically lead to substandard performance.
* **Objects with complex interdependencies** - If your data cannot be
  easily denormalized or if it requires that objects can be easily
  assembled into and accessible as larger wholes---think columns or
  tables---then you might want to consider a relational database
  instead.

##### Conclusion

If it sounds like Riak is a good choice for some or all of your
application's data needs, move on to the next sections, where you can
find out more about which Riak features are recommendable for your use
case, how you should model your data, and what kinds of data modeling
and development strategies we recommend.

#### Which Features Should You Consider?

Basic CRUD key/value operations are almost always the most performant
operations when using Riak. If your needs can be served using CRUD
operations, we recommend checking out our tutorial on [key/value modeling][dev kv model] for some basic guidelines. But if basic CRUD key/value
operations don't quite suffice for your use case, Riak offers a variety
of features that may be just what you're looking for. In the sections
immediately below, you can find brief descriptions of those features as
well as relevant links to Basho documentation.

#### Riak Data Types

When performing basic K/V operations, Riak is agnostic toward the actual
data stored within objects. Beginning with Riak 2.0, however, you now
have access to operations-based objects based on academic research on
[CRDTs](http://hal.upmc.fr/docs/00/55/55/88/PDF/techreport.pdf). Riak
Data Types enable you to update and read [counters][dev data types#counters],
[sets][dev data types#sets], and [maps][dev data types#maps] directly in Riak, as well as [registers][dev data types#maps] and [flags][dev data types#maps] inside of Riak maps.

The beauty of Riak Data Types is that all convergence logic is handled
by Riak itself according to deterministic, Data Type-specific rules,
which means that your application doesn't need to reason about
[siblings][usage conflict resolution]. In many cases, this can
unburden applications of the need to handle object convergence on their
own.

* [Using Data Types][dev data types] - A guide to setting up Riak to use Data Types,
  including a variety of code samples for all of the Basho's official
  [client libraries][dev client libraries]
* [Data Types][concept crdts] - A theoretical treatment of Riak Data Types, along
  with implementation details
* [Data Modeling with Riak Data Types][dev data model] - An object modeling example that relies on Riak Data Types.

##### When to Use Riak Data Types

* **When your data fits** - If the data that you're storing can be
  modeled as one of the five available types, Riak Data Types could be a
  very good option. Please note that in many cases there may not be a
  1:1 correspondence between the five available types and the data that
  you'd like to store, but there may be workarounds to close the gap.
  Most things that can be stored as JSON, for example, can be stored as
  maps (though with modifications).
* **When you don't need to reason about siblings** - If your use case
  doesn't require that your application have access to siblings and
  allows for sibling convergence logic to take place at the Riak level
  rather than at the application level, then Riak Data Types are well
  worth exploring.

##### When Not to Use Riak Data Types

* **When you need to provide your own convergence logic** - If your
  application needs to have access to all sibling values, then Riak Data
  Types are not a good choice because they by definition do not produce
  siblings.
* **When your data just doesn't fit** - While the five existing Data
  Types allow for a great deal of flexibility and a wide range of use
  cases, they don't cover all use cases. If you have data that requires
  a modeling solution that can't be covered, you should stick to
  standard K/V operations.
* **When object size is of significant concern** - Riak Data Types
  behave much like other Riak objects, but they tend to carry more
  metadata than normal Riak objects, especially maps. In most cases the
  metadata payload will be a small percentage of the object's total
  size, but if you want to keep objects as lean as possible, it may be
  better to stick to normal K/V operations.

#### MapReduce

OpenRiak's MapReduce feature enables you to perform batch processing jobs in
a way that leverages OpenRiak's distributed nature. When a MapReduce job is
sent to Riak, Riak automatically distributes the processing work to
where the target data lives, which can reduce network bandwidth. Riak
comes equipped with a set of default MapReduce jobs that you can employ,
or you can write and run your own MapReduce jobs in
[Erlang](http://www.erlang.org/).

* [Using MapReduce][usage mapreduce] - A general guide to using MapReduce
* [Advanced MapReduce][apps mapreduce] - A more in-depth guide to MapReduce,
  including code samples and implementation details

##### When to Use MapReduce

* **Batch processing only** - You should use MapReduce only when truly
  truly necessary. MapReduce jobs are very computationally expensive and
  can degrade performance in production clusters. You should restrict
  MapReduce usage to infrequent batch processing operations, preferably
  carried out at times when your cluster is experiencing load that is
  well below average.

##### When Not to Use MapReduce

In general, you should not think of MapReduce as, for example, Hadoop
within Riak. While it can be useful for certain types of
non-primary-key-based queries, it is neither a "Big Data" processing
tool nor an indexing mechanism. If you do need a tool like Hadoop or Apache Spark, you should
consider using Riak in conjunction with a more suitable data processing
tool.

#### Secondary Indexes (2i)

Using basic key/value operations in Riak sometimes leads to the
following problem: how do I know which keys I should look for? Secondary
indexes (2i) provide a solution to this problem, enabling you to tag
objects with either binary or integer metadata and then query Riak for
all of the keys that share specific tags. 2i is especially useful if
you're storing binary data that is opaque.

* [Using Secondary Indexes][usage 2i] - A general guide to using 2i, along
  with code samples and information on 2i features like pagination,
  streaming, and sorting
* [Advanced Secondary Indexes][use ref 2i] - Implementation details behind 2i

##### When to Use Secondary Indexes

##### When Not to Use Secondary Indexes

* **If you're using Bitcask** - 2i is available only in the
    [LevelDB][plan backend leveldb] backend. If you'd like to use [Bitcask][plan backend bitcask] or the [Memory][plan backend memory] backend, you will not be able to use 2i.

#### Mixed Approach

One thing to always bear in mind is that Riak enables you to mix and
match a wide variety of approaches in a single cluster. You can use
basic CRUD operations for some of your data, use Riak Data Types for another subset, etc.
You are always free to use a wide array of Riak features---or you can
use none at all and stick to key/value operations.

#### How Should You Model Your Data?

It's difficult to offer universally applicable data modeling guidelines
because data models differ so markedly from use case to use case. What
works when storing [user data][dev data model#user], for example, might
be a poor fit when working with [sensor data][dev data model#sensor].
Nonetheless, there's a variety of material in our documentation that
might be helpful when thinking about data modeling:

* Object Modeling in OpenRiak KV:
    - [Java][obj model java]
    - [Ruby][obj model ruby]
    - [Python][obj model python]
    - [C#][obj model csharp]
    - [NodeJS][obj model nodejs]
    - [Erlang][obj model erlang]
    - [Go][obj model golang]
* [Key/Value Modeling][dev kv model]

##### Data Types

One feature to always bear in mind when using Riak is [Riak Data Types][dev data types]. If some or all of your data can be modeled in
accordance with one of the available Data Types---flags (similar to
Booleans), registers (good for storing small binaries or text snippets),
[counters][dev data types#counters], [sets][dev data types#sets],
or [maps][dev data types#maps]---you might be able to streamline
application development by using them as an alternative to key/value
operations. In some cases, it might even be worthwhile to transform your
data modeling strategy in accordance with To see if this feature might
be a good fit for your application, we recommend checking out the
following documentation:

* [Data Types][concept crdts]
* [Using Data Types][dev data types]
* [Data Modeling with Riak Data Types][dev data model]

#### What are Your Consistency Requirements?

Riak has traditionally been thought of as an [eventually consistent][concept eventual consistency], AP system, i.e. as a system that
favors availability and partition tolerance over data consistency. In
Riak versions 2.0 and later, the option of applying strong consistency
guarantees is available to developers that want to use Riak as a strict
CP system. One of the advantages of OpenRiak's approach to strong
consistency is that you don't need to store all of your data in a
strongly consistent fashion if you use this feature. Instead, you can
mix and match a CP approach with an AP approach in a single cluster in
any way you wish.

If you need some or all of your data to be subject to strong consistency
requirements, we recommend checking out the following documentation:

* [Strong Consistency][use ref strong consistency]
* [Using Strong Consistency][apps strong consistency]
* [Managing Strong Consistency][cluster ops strong consistency]

#### Are Your Objects Mutable?

Although Riak always performs best when storing and retrieving immutable
data, Riak also handles mutable objects very ably using a variety of
eventual consistency principles. Storing mutable data in Riak, however,
can get tricky because it requires you to choose and implement a
conflict resolution strategy for when object conflicts arise, which is a
normal occurrence in Riak. For more implementation details, we recommend
checking out the following docs:

* [Conflict Resolution][usage conflict resolution]
* [Object Updates][usage update objects]
* [Replication Properties][apps replication properties]

#### Getting Started

If you have a good sense of how you will be using Riak for your
application (or if you just want to experiment), the following guides
will help you get up and running:

* [Installing OpenRiak KV][install index] - Install OpenRiak KV and start up a 5-node Riak
  cluster
* [Client Libraries][dev client libraries] - A listing of official and non-official client
  libraries for building applications with Riak
* [Getting Started with Client Libraries][getting started] - How to
  get up and going with one of Basho's official client libraries (Java,
  Ruby, Python, and Erlang)
* [Developing with OpenRiak KV: Usage][usage index] - A guide to basic key/value operations and other common tasks in OpenRiak KV.
* [OpenRiak KV Glossary][glossary] - A listing of frequently used terms in OpenRiak's
  documentation

### Getting Started Overview

[install index]: {{< baseurl >}}kv/3.4.0/how-to/install/
[dev client libraries]: {{< baseurl >}}kv/3.4.0/reference/client-libraries/

Welcome, new Riak developer! This guide will get you started developing
against OpenRiak KV with minimal fuss.

#### Installing OpenRiak KV

The easiest way to get started with OpenRiak KV is to complete the
[installation][install index] process.

#### Choose Your Programming Language

Basho officially supports a number of open-source [client libraries][dev client libraries]
for various programming languages and environments. Please select the
language with which you'd like to proceed:

<ul class="clearfix   client-library-logos">
  <li class="float-left"><a class="block   client-library-logo" href="java/"><img src="{{< baseurl >}}images/client_library_logos/java.png" alt="Java" /></a></li>
  <li class="float-left"><a class="block   client-library-logo" href="ruby/"><img src="{{< baseurl >}}images/client_library_logos/ruby_small.png" alt="Ruby" /></a></li>
  <li class="float-left"><a class="block   client-library-logo" href="python/"><img src="{{< baseurl >}}images/client_library_logos/python.png" alt="Python" /></a></li>
  <li class="float-left"><a class="block   client-library-logo" href="csharp/"><img src="{{< baseurl >}}images/client_library_logos/c_sharp.png" alt="CSharp" /></a></li>
  <li class="float-left"><a class="block   client-library-logo" href="nodejs/"><img src="{{< baseurl >}}images/client_library_logos/nodejs.png" alt="Node.js" /></a></li>
  <li class="float-left"><a class="block   client-library-logo" href="erlang/"><img src="{{< baseurl >}}images/client_library_logos/erlang.png" alt="Erlang" /></a></li>
  <li class="float-left"><a class="block   client-library-logo" href="php/"><img src="{{< baseurl >}}images/client_library_logos/php.png" alt="PHP" /></a></li>
  <li class="float-left"><a class="block   client-library-logo" href="golang/"><img src="{{< baseurl >}}images/client_library_logos/golang.png" alt="GoLang" /></a></li>
</ul>

##### Community-supported Client Libraries

Please see our [client libraries][dev client libraries] page for a listing of
community-supported clients.

## What you will learn

By completing this tutorial, you will build the workflow described above and learn how to validate each stage before moving on.

## Before you begin

Use a disposable OpenRiak KV environment that matches this documentation version, and keep cluster status and logs available while you work.

## Verify the result

Repeat the completed workflow, inspect the stored or operational result, and confirm that the cluster remains healthy.

## Next steps

- [Build a first OpenRiak application with C#]({{< baseurl >}}kv/3.4.0/tutorials/first-application/csharp/)
- [Build a first OpenRiak application with Erlang]({{< baseurl >}}kv/3.4.0/tutorials/first-application/erlang/)
- [Build a first OpenRiak application with Go]({{< baseurl >}}kv/3.4.0/tutorials/first-application/golang/)

## In this section

- [Build a first OpenRiak application with C#]({{< baseurl >}}kv/3.4.0/tutorials/first-application/csharp/) — Guide a developer through modeling, storing, retrieving, querying, and updating a small dataset with C#.
- [Build a first OpenRiak application with Erlang]({{< baseurl >}}kv/3.4.0/tutorials/first-application/erlang/) — Guide a developer through modeling, storing, retrieving, querying, and updating a small dataset with Erlang.
- [Build a first OpenRiak application with Go]({{< baseurl >}}kv/3.4.0/tutorials/first-application/golang/) — Guide a developer through modeling, storing, retrieving, querying, and updating a small dataset with Go.
- [Build a first OpenRiak application with Java]({{< baseurl >}}kv/3.4.0/tutorials/first-application/java/) — Guide a developer through modeling, storing, retrieving, querying, and updating a small dataset with Java.
- [Build a first OpenRiak application with Node.js]({{< baseurl >}}kv/3.4.0/tutorials/first-application/nodejs/) — Guide a developer through modeling, storing, retrieving, querying, and updating a small dataset with Node.js.
- [Build a first OpenRiak application with PHP]({{< baseurl >}}kv/3.4.0/tutorials/first-application/php/) — Guide a developer through modeling, storing, retrieving, querying, and updating a small dataset with PHP.
- [Build a first OpenRiak application with Python]({{< baseurl >}}kv/3.4.0/tutorials/first-application/python/) — Guide a developer through modeling, storing, retrieving, querying, and updating a small dataset with Python.
- [Build a first OpenRiak application with Ruby]({{< baseurl >}}kv/3.4.0/tutorials/first-application/ruby/) — Guide a developer through modeling, storing, retrieving, querying, and updating a small dataset with Ruby.
- [Build a first OpenRiak application with Rust]({{< baseurl >}}kv/3.4.0/tutorials/first-application/rust/) — Guide a developer through modeling, storing, retrieving, querying, and updating a small dataset with Rust.
