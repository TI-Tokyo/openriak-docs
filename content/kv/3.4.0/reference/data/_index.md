---
title: 'Data reference'
description: 'Define OpenRiak identifiers, object representations, metadata, indexes, and distributed data types.'
weight: 1
diataxis: 'reference'
product: 'OpenRiak KV'
product_version: '3.4.0'
status: 'editorially-rewritten'
draft: true
audience:
  - 'developers'
  - 'operators'
source_material:
  - 'openriak-quickdocs-3.4'
  - 'live-3.2.5'
  - 'proposed-kv'
quickdocs_sources:
  - 'https://openriak.github.io/riak/ObjectAPI.html#riak-kv---object-api'
tags: ['diataxis', 'kv', 'reference']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Define OpenRiak identifiers, object representations, metadata, indexes, and distributed data types.

## Details

### OpenRiak KV - Object API

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

- [The URL](/kv/3.4.0/reference/data/keys-and-objects/)
- [The body](/kv/3.4.0/reference/data/keys-and-objects/)
- [The request and response headers](/kv/3.4.0/reference/data/object-metadata/)
- [Adding options to a request - query parameters](/kv/3.4.0/reference/http-api/object-request-options/)
- [Conditional requests](/kv/3.4.0/reference/http-api/conditional-requests/)
- [Commit hooks](/kv/3.4.0/how-to/develop/write-commit-hook/)
- [Storing an object](/kv/3.4.0/reference/http-api/store-object/)
- [Fetching an object](/kv/3.4.0/reference/http-api/fetch-object/)
- [Deleting an object](/kv/3.4.0/reference/http-api/delete-object/)
- [Legacy objects](/kv/3.4.0/reference/http-api/fetch-object/)

## In this section

- [Buckets and bucket types](/kv/3.4.0/reference/data/buckets-and-bucket-types/) — Define the fields, limits, supported operations, representations, and compatibility rules for buckets and bucket types.
- [Content types](/kv/3.4.0/reference/data/content-types/) — Define the fields, limits, supported operations, representations, and compatibility rules for content types.
- [Distributed data types](/kv/3.4.0/reference/data/distributed-data-types/) — Define the fields, limits, supported operations, representations, and compatibility rules for distributed data types.
- [Keys and objects](/kv/3.4.0/reference/data/keys-and-objects/) — Define the fields, limits, supported operations, representations, and compatibility rules for keys and objects.
- [Object metadata](/kv/3.4.0/reference/data/object-metadata/) — Define the fields, limits, supported operations, representations, and compatibility rules for object metadata.
- [Secondary indexes](/kv/3.4.0/reference/data/secondary-indexes/) — Define the fields, limits, supported operations, representations, and compatibility rules for secondary indexes.
- [Version vectors](/kv/3.4.0/reference/data/version-vectors/) — Define the fields, limits, supported operations, representations, and compatibility rules for version vectors.
