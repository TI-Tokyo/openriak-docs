---
title: 'Specialized API reference'
description: 'Introduce specialized OpenRiak APIs that do not fit the primary object or query interfaces.'
weight: 1
diataxis: 'reference'
product: 'OpenRiak KV'
product_version: '3.4.0'
status: 'editorially-rewritten'
draft: true
audience:
  - 'developers'
legacy_3_2_5_sources:
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\developing\app-guide\reference.md'
source_material:
  - 'legacy-3.2.5'
  - 'openriak-quickdocs-3.4'
quickdocs_sources:
  - 'https://openriak.github.io/riak/OtherAPI.html#riak-kv---other-apis'
tags: ['diataxis', 'kv', 'reference']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Introduce specialized OpenRiak APIs that do not fit the primary object or query interfaces.

## Details

### Reference

**TODO: Add content**

#### OpenRiak KV - Other APIs

The majority of work within OpenRiak KV can be done using the [Object API]({{< baseurl >}}kv/3.4.0/reference/http-api/), and the [Query API]({{< baseurl >}}kv/3.4.0/tutorials/query-api/).  There are though additional APIs, with specific purposes:

- [The AAE Fold API]({{< baseurl >}}kv/3.4.0/reference/aae-fold-api/)
- [The Fetch API used to access replication queues]({{< baseurl >}}kv/3.4.0/reference/specialized-apis/fetch-api/)
- [The Data Type API]({{< baseurl >}}kv/3.4.0/reference/specialized-apis/data-type-api/)
- [The Map/Reduce API]({{< baseurl >}}kv/3.4.0/reference/http-api/mapreduce/)
- [The List API]({{< baseurl >}}kv/3.4.0/reference/specialized-apis/list-api/)
- [The Strong Consistency API]({{< baseurl >}}kv/3.4.0/reference/specialized-apis/strong-consistency-api/)
- [The Write Once Path API]({{< baseurl >}}kv/3.4.0/reference/specialized-apis/write-once-api/)

## In this section

- [Backend API reference]({{< baseurl >}}kv/3.4.0/reference/specialized-apis/backend-api/) — Describe the backend callback interface and supported behavior.
- [Cluster metadata reference]({{< baseurl >}}kv/3.4.0/reference/specialized-apis/cluster-metadata/) — Describe cluster metadata operations and compatibility constraints.
- [Data Type API reference]({{< baseurl >}}kv/3.4.0/reference/specialized-apis/data-type-api/) — Define endpoints, request and response formats, options, and constraints for OpenRiak distributed data types.
- [Fetch API reference]({{< baseurl >}}kv/3.4.0/reference/specialized-apis/fetch-api/) — Define Fetch API requests, responses, options, compatibility, and errors.
- [Legacy Query API reference]({{< baseurl >}}kv/3.4.0/reference/specialized-apis/legacy-query-api/) — Record the legacy query interface, compatibility boundaries, and migration guidance.
- [List API reference]({{< baseurl >}}kv/3.4.0/reference/specialized-apis/list-api/) — Define List API operations, streaming behavior, limits, and errors.
- [Strong Consistency API reference]({{< baseurl >}}kv/3.4.0/reference/specialized-apis/strong-consistency-api/) — Define strongly consistent operations, request fields, responses, constraints, and errors.
- [Write Once Path API reference]({{< baseurl >}}kv/3.4.0/reference/specialized-apis/write-once-api/) — Define immutable write requests, responses, constraints, and failure behavior.
