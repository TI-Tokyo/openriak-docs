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

The majority of work within OpenRiak KV can be done using the [Object API]({{< product-version-root >}}reference/http-api/), and the [Query API]({{< product-version-root >}}tutorials/query-api/).  There are though additional APIs, with specific purposes:

- [The AAE Fold API]({{< product-version-root >}}reference/aae-fold-api/)
- [The Fetch API used to access replication queues]({{< product-version-root >}}reference/specialized-apis/fetch-api/)
- [The Data Type API]({{< product-version-root >}}reference/specialized-apis/data-type-api/)
- [The Map/Reduce API]({{< product-version-root >}}reference/http-api/mapreduce/)
- [The List API]({{< product-version-root >}}reference/specialized-apis/list-api/)
- [The Strong Consistency API]({{< product-version-root >}}reference/specialized-apis/strong-consistency-api/)
- [The Write Once Path API]({{< product-version-root >}}reference/specialized-apis/write-once-api/)

## In this section

- [Backend API reference]({{< product-version-root >}}reference/specialized-apis/backend-api/) — Describe the backend callback interface and supported behavior.
- [Cluster metadata reference]({{< product-version-root >}}reference/specialized-apis/cluster-metadata/) — Describe cluster metadata operations and compatibility constraints.
- [Data Type API reference]({{< product-version-root >}}reference/specialized-apis/data-type-api/) — Define endpoints, request and response formats, options, and constraints for OpenRiak distributed data types.
- [Fetch API reference]({{< product-version-root >}}reference/specialized-apis/fetch-api/) — Define Fetch API requests, responses, options, compatibility, and errors.
- [Legacy Query API reference]({{< product-version-root >}}reference/specialized-apis/legacy-query-api/) — Record the legacy query interface, compatibility boundaries, and migration guidance.
- [List API reference]({{< product-version-root >}}reference/specialized-apis/list-api/) — Define List API operations, streaming behavior, limits, and errors.
- [Strong Consistency API reference]({{< product-version-root >}}reference/specialized-apis/strong-consistency-api/) — Define strongly consistent operations, request fields, responses, constraints, and errors.
- [Write Once Path API reference]({{< product-version-root >}}reference/specialized-apis/write-once-api/) — Define immutable write requests, responses, constraints, and failure behavior.
