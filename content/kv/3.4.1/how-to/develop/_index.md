---
title: 'Develop with OpenRiak'
description: 'Introduce task-oriented recipes for application developers using OpenRiak data and APIs.'
weight: 1
diataxis: 'how-to'
product: 'OpenRiak KV'
product_version: '3.4.1'
status: 'editorially-rewritten'
draft: true
audience:
  - 'developers'
legacy_3_2_5_sources:
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\developing.md'
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\developing\usage.md'
source_material:
  - 'legacy-3.2.5'
  - 'live-3.2.5'
  - 'proposed-kv'
  - 'openriak-quickdocs-3.4'
quickdocs_sources:
  - 'https://openriak.github.io/riak/ObjectAPI.html#riak-kv---object-api'
tags: ['diataxis', 'kv', 'how-to']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Introduce task-oriented recipes for application developers using OpenRiak data and APIs.

## Before you begin

A non-production OpenRiak KV cluster, client credentials, and disposable test data that represents the operation you need to implement.

## Overview

### Developing with OpenRiak KV

[getting started]: ../developing/getting-started
[usage index]: ../developing/usage
[client libraries]: ../developing/client-libraries
[dev data types]: ../developing/data-types
[dev data modeling]: ../developing/data-modeling
[apps index]: ../developing/app-guide
[dev api index]: ../developing/api
[dev faq]: ../developing/faq

#### In This Section

##### [Getting Started][getting started]

Step-by-step guide for getting started developing with OpenRiak KV.

[Learn More >>][getting started]

###### [Usage][usage index]

A set of tutorials covering common development tasks such as performing CRUD operations and using bucket types.

[Learn More >>][usage index]

###### [Client Libraries][client libraries]

Overview of client libraries for a variety of programming languages and environments.

[Learn More >>][client libraries]

###### [Data Types][dev data types]

Overview and guide to working with data types in OpenRiak KV.

[Learn More >>][dev data types]

###### [Data Modeling][dev data modeling]

Information on use cases and data models that are a good fit for OpenRiak KV.

[Learn More >>][dev data modeling]

###### [Application Guide][apps index]

A guide that will walk you through questions to ask about your use case before getting started developing applications with OpenRiak KV.

[Learn More >>][apps index]

###### [APIs Reference][dev api index]

Information and reference material on OpenRiak KV APIs.

[Learn More >>][dev api index]

###### [FAQ][dev faq]

Frequently asked questions when developing applications with OpenRiak KV.

[Learn More >>][dev faq]

### Usage Overview

#### In This Section

##### [Creating Objects](./creating-objects)

Creating and storing objects in OpenRiak KV.

[Learn More >>](./creating-objects)

###### [Reading Objects](./reading-objects)

Reading and fetching objects in OpenRiak KV.

[Learn More >>](./reading-objects)

###### [Updating Objects](./updating-objects)

Updating objects in OpenRiak KV.

[Learn More >>](./updating-objects)

###### [Deleting Objects](./deleting-objects)

Deleting objects in OpenRiak KV.

[Learn More >>](./deleting-objects)

###### [Content Types](./content-types)

Overview of content types and their usage.

[Learn More >>](./content-types)

###### [Using Search](./search)

Tutorial on using search.

[Learn More >>](./search)

###### [Using MapReduce](./mapreduce)

Guide to using MapReduce in applications.

[Learn More >>](./mapreduce)

###### [Using Secondary Indexes](./secondary-indexes)

Overview and usage details of Secondary Indexes (2i).

[Learn More >>](./secondary-indexes)

###### [Bucket Types](./bucket-types)

Describes how to use bucket properties.

[Learn More >>](./bucket-types)

###### [Using Commit Hooks](./commit-hooks)

Tutorial on pre-commit and post-commit hook functions.

[Learn More >>](./commit-hooks)

###### [Creating Search Schemas](./search-schemas)

Step-by-step guide on creating and using custom search schemas.

[Learn More >>](./search-schemas)

###### [Searching with Data Types](./searching-data-types)

Guide on using search with Data Types.

[Learn More >>](./searching-data-types)

###### [Implementing a Document Store](./document-store)

Tutorial on using OpenRiak KV as a document store.

[Learn More >>](./document-store)

###### [Custom Extractors](./custom-extractors)

Details on creating and registering custom extractors with Riak Search.

[Learn More >>](./custom-extractors)

###### [Client-side Security](./security)

Overview of client-side security.

[Learn More >>](./security)

###### [Replication](./replication)

Documentation on replication properties and their underlying implementation.

[Learn More >>](./replication)

###### [Conflict Resolution](./conflict-resolution)

Guide to conflict resolution during object updates.

[Learn More >>](./conflict-resolution)

#### OpenRiak KV - Object API

Objects can be fetched and updated via either a HTTP or Protocol Buffer API.  Considerations to be made when choosing a transport protocol include:

- The PB API is more performant, in particular when using significant numbers of index entries or user metadata due to the overheads of parsing HTTP headers, the delta between the APIs is generally between 5% and 15% in terms of request latency;
  - Improving relative HTTP performance is a key goal of Riak development for future releases.
- The HTTP API is generally quicker to develop against due to the ubiquity of HTTP-based tooling, and the ability for developers to switch to command line tools (e.g. curl) or graphical tools.
  - The HTTP API is not strictly standards compliant, in that it uses HTTP request headers to describe the object rather than the request.  It is not possible to describe the API using standard tooling (e.g. OpenAPI).
- The HTTP API places strict requirements on the characters supported in identifiers, user metadata and index entries.  Supporting non-HTTP safe characters is possible via the PB API but it is NOT supported.
  - Always ensure that objects will be supported via HTTP, even when using PB.
- Using the HTTP API will provide greater flexibility to control access to Riak via standard internet infrastructure (e.g. Web-Application Firewalls, Proxies and Load-Balancers).

> New APIs added to Riak will be added to the HTTP API first.  It is expected that in the long term the performance of the HTTP API will be improved, and that the relative ubiquity of HTTP will evolve the choice of API towards HTTP being the default protocol.

The [PB Object API is described in the riak_pb repository](https://github.com/OpenRiak/riak_pb/blob/e908ddaadc06cb56e248f197dc2dca7d759e53b2/src/riak_kv.proto#L45-L125), but the concepts are the same as for the HTTP API.

The Riak Object HTTP API is described here:

- [The URL]({{< baseurl >}}kv/3.4.1/reference/data/keys-and-objects/)
- [The body]({{< baseurl >}}kv/3.4.1/reference/data/keys-and-objects/)
- [The request and response headers]({{< baseurl >}}kv/3.4.1/reference/data/object-metadata/)
- [Adding options to a request - query parameters]({{< baseurl >}}kv/3.4.1/reference/http-api/object-request-options/)
- [Conditional requests]({{< baseurl >}}kv/3.4.1/reference/http-api/conditional-requests/)
- [Commit hooks]({{< baseurl >}}kv/3.4.1/how-to/develop/write-commit-hook/)
- [Storing an object]({{< baseurl >}}kv/3.4.1/reference/http-api/store-object/)
- [Fetching an object]({{< baseurl >}}kv/3.4.1/reference/http-api/fetch-object/)
- [Deleting an object]({{< baseurl >}}kv/3.4.1/reference/http-api/delete-object/)
- [Legacy objects]({{< baseurl >}}kv/3.4.1/reference/http-api/fetch-object/)

## Verify the result

Run the operation against test data, inspect the stored result and response metadata, and exercise the expected failure path.
