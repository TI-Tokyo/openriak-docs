---
title: 'HTTP API reference'
description: 'Define HTTP resources, authentication, headers, status codes, request options, and common representations.'
weight: 1
diataxis: 'reference'
product: 'OpenRiak KV'
product_version: '3.4.0'
status: 'editorially-rewritten'
draft: true
audience:
  - 'developers'
migration_source_root: '\\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv'
migration_sources:
  - '\\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv\apis-and-clients\APIs\http-https\http-https.md'
legacy_3_2_5_sources:
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\developing\api\http.md'
source_material:
  - 'legacy-3.2.5'
  - 'openriak-quickdocs-3.4'
  - 'live-3.2.5'
  - 'proposed-kv'
quickdocs_sources:
  - 'https://openriak.github.io/riak/ObjectAPI.html#object-identifier---the-url'
  - 'https://openriak.github.io/riak/ObjectAPI.html#riak-kv---object-api'
tags: ['diataxis', 'kv', 'reference']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Define HTTP resources, authentication, headers, status codes, request options, and common representations.

## Details

### HTTP API

Riak has a rich, full-featured HTTP 1.1 API. This is an overview of the
operations you can perform via HTTP and can be used as a guide for
developing a compliant client. All URLs assume the default configuration
values where applicable. All examples use `curl` to interact with Riak.

> **URL Escaping**
>
> Buckets, keys, and link specifications may not contain unescaped
slashes. Use a URL-escaping library or replace slashes with `%2F`.

#### Bucket-related Operations

Method | URL | Doc
:------|:----|:---
`GET` | `/types/<type>/buckets/<bucket>/props` | [HTTP Get Bucket Properties]({{< product-version-root >}}reference/http-api/get-bucket-properties/)
`PUT` | `/types/<type>/buckets/<bucket>/props` | [HTTP Set Bucket Properties]({{< product-version-root >}}reference/http-api/set-bucket-properties/)
`DELETE` | `/types/<type>/buckets/<bucket>/props` | [HTTP Reset Bucket Properties]({{< product-version-root >}}reference/http-api/reset-bucket-properties/)
`GET` | `/types/<type>/buckets?buckets=true` | [HTTP List Buckets]({{< product-version-root >}}reference/http-api/list-buckets/)
`GET` | `/types/<type>/buckets/<bucket>/keys?keys=true` | [HTTP List Keys]({{< product-version-root >}}reference/http-api/list-keys/)

#### Object-related Operations

Method | URL | Doc
:------|:----|:---
`GET` | `/types/<type>/buckets/<bucket>/keys/<key>` | [HTTP Fetch Object]({{< product-version-root >}}reference/http-api/fetch-object/)
`POST` | `/types/<type>/buckets/<bucket>/keys` | [HTTP Store Object]({{< product-version-root >}}reference/http-api/store-object/)
`PUT` | `/types/<type>/buckets/<bucket>/keys/<key>` | [HTTP Store Object]({{< product-version-root >}}reference/http-api/store-object/)
`POST` | `/types/<type>/buckets/<bucket>/keys/<key>` | [HTTP Store Object]({{< product-version-root >}}reference/http-api/store-object/)
`DELETE` | `/types/<type>/buckets/<bucket>/keys/<key>` | [HTTP Delete Object]({{< product-version-root >}}reference/http-api/delete-object/)

#### Riak-Data-Type-related Operations

Method | URL
:------|:----
`GET` | `/types/<type>/buckets/<bucket>/datatypes/<key>`
`POST` | `/types/<type>/buckets/<bucket>/datatypes`
`POST` | `/types/<type>/buckets/<bucket>/datatypes/<key>`

For documentation on the HTTP API for [Riak Data Types]({{< product-version-root >}}explanation/data-model/distributed-data-types/),
see the `curl` examples in [Using Data Types]({{< product-version-root >}}reference/data/distributed-data-types/#usage-examples)
and subpages e.g. [sets]({{< product-version-root >}}how-to/develop/use-sets/).

Advanced users may consult the technical documentation inside the Riak
KV internal module `riak_kv_wm_crdt`.

#### Query-related Operations

Method | URL | Doc
:------|:----|:---
`POST` | `/mapred` | [HTTP MapReduce]({{< product-version-root >}}reference/http-api/mapreduce/)
`GET` | `/types/<type>/buckets/<bucket>/index/<index>/<value>` | [HTTP Secondary Indexes]({{< product-version-root >}}reference/http-api/secondary-indexes/)
`GET` | `/types/<type>/buckets/<bucket>/index/<index>/<start>/<end>` | [HTTP Secondary Indexes]({{< product-version-root >}}reference/http-api/secondary-indexes/)

#### Server-related Operations

Method | URL | Doc
:------|:----|:---
`GET` | `/ping` | [HTTP Ping]({{< product-version-root >}}reference/http-api/ping/)
`GET` | `/stats` | [HTTP Status]({{< product-version-root >}}reference/http-api/status/)
`GET` | `/` | [HTTP List Resources]({{< product-version-root >}}reference/http-api/list-resources/)

#### Search-related Operations

Method | URL | Doc
:------|:----|:---
`GET` | `/search/query/<index_name>` | [HTTP Search Query]({{< product-version-root >}}reference/specialized-apis/legacy-query-api/)
`GET` | `/search/index` | [HTTP Search Index Info]({{< product-version-root >}}reference/specialized-apis/legacy-query-api/)
`GET` | `/search/index/<index_name>` | [HTTP Fetch Search Index]({{< product-version-root >}}reference/specialized-apis/legacy-query-api/)
`PUT` | `/search/index/<index_name>` | [HTTP Store Search Index]({{< product-version-root >}}reference/specialized-apis/legacy-query-api/)
`DELETE` | `/search/index/<index_name>` | [HTTP Delete Search Index]({{< product-version-root >}}reference/specialized-apis/legacy-query-api/)
`GET` | `/search/schema/<schema_name>` | [HTTP Fetch Search Schema]({{< product-version-root >}}reference/specialized-apis/legacy-query-api/)
`PUT` | `/search/schema/<schema_name>` | [HTTP Store Search Schema]({{< product-version-root >}}reference/specialized-apis/legacy-query-api/)

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

- [The URL]({{< product-version-root >}}reference/data/keys-and-objects/)
- [The body]({{< product-version-root >}}reference/data/keys-and-objects/)
- [The request and response headers]({{< product-version-root >}}reference/data/object-metadata/)
- [Adding options to a request - query parameters]({{< product-version-root >}}reference/http-api/object-request-options/)
- [Conditional requests]({{< product-version-root >}}reference/http-api/conditional-requests/)
- [Commit hooks]({{< product-version-root >}}how-to/develop/write-commit-hook/)
- [Storing an object]({{< product-version-root >}}reference/http-api/store-object/)
- [Fetching an object]({{< product-version-root >}}reference/http-api/fetch-object/)
- [Deleting an object]({{< product-version-root >}}reference/http-api/delete-object/)
- [Legacy objects]({{< product-version-root >}}reference/http-api/fetch-object/)

#### Object Identifier - the URL

The Riak object Identifier is split into three parts:

- Bucket Type;
- Bucket;
- Key.

Internally within Riak all three elements are binary identifiers.  With the Object HTTP API, these elements are represented within the URL e.g. `/types/<BucketType>/buckets/<Bucket>/keys/<Key>`.

> Although it is possible to use identifiers that are not URL-safe through the Protocol Buffer API, it is important not to do so - as any object using such an identifier may not be accessible via the HTTP API.  Guidelines for the safe use of Unicode in cross-API identifiers, will be clarified in a future Riak release.

The [Bucket Type]({{< product-version-root >}}reference/configuration/bucket-properties/) is used to describe the properties of the object.  Properties are associated with a Bucket Type, and all Objects in the Buckets under that type will inherit those properties.

A Bucket Type cannot be used via the API until it has been created and activated, to do this see:

```console
riak admin bucket-type --help
```

The Bucket is a namespace, and a Bucket Type is allowed to have an arbitrary number of Buckets.  A Bucket cannot be moved between Bucket Types, but the properties of an individual Bucket may be changed to override that of the Bucket Type.

Keys are unique identifiers of an object within a Bucket.

>[!MEMO] The HTTP/HTTPS API
>The HTTP(S) API is split into two major sections, the Oject API and the Query API. There are also interactions with the AAE_fold API that can come via the HTTP(S) API>

## In this section

- [Conditional object request reference]({{< product-version-root >}}reference/http-api/conditional-requests/) — Define conditional request headers, validator behavior, status codes, and latch-object semantics.
- [Use counters with the HTTP API]({{< product-version-root >}}reference/http-api/counters/) — Document the complete HTTP contract for this operation, including parameters, representations, examples, and errors.
- [Delete an object with the HTTP API]({{< product-version-root >}}reference/http-api/delete-object/) — Document the complete HTTP contract for this operation, including parameters, representations, examples, and errors.
- [Fetch an object with the HTTP API]({{< product-version-root >}}reference/http-api/fetch-object/) — Document the complete HTTP contract for this operation, including parameters, representations, examples, and errors.
- [Get bucket properties with the HTTP API]({{< product-version-root >}}reference/http-api/get-bucket-properties/) — Document the complete HTTP contract for this operation, including parameters, representations, examples, and errors.
- [Walk links with the HTTP API]({{< product-version-root >}}reference/http-api/link-walking/) — Document the complete HTTP contract for this operation, including parameters, representations, examples, and errors.
- [List buckets with the HTTP API]({{< product-version-root >}}reference/http-api/list-buckets/) — Document the complete HTTP contract for this operation, including parameters, representations, examples, and errors.
- [List keys with the HTTP API]({{< product-version-root >}}reference/http-api/list-keys/) — Document the complete HTTP contract for this operation, including parameters, representations, examples, and errors.
- [List resources with the HTTP API]({{< product-version-root >}}reference/http-api/list-resources/) — Document the complete HTTP contract for this operation, including parameters, representations, examples, and errors.
- [Run MapReduce with the HTTP API]({{< product-version-root >}}reference/http-api/mapreduce/) — Document the complete HTTP contract for this operation, including parameters, representations, examples, and errors.
- [Object request options]({{< product-version-root >}}reference/http-api/object-request-options/) — Define common OpenRiak Object API GET and PUT parameters, defaults, and response behavior.
- [Ping with the HTTP API]({{< product-version-root >}}reference/http-api/ping/) — Document the complete HTTP contract for this operation, including parameters, representations, examples, and errors.
- [Reset bucket properties with the HTTP API]({{< product-version-root >}}reference/http-api/reset-bucket-properties/) — Document the complete HTTP contract for this operation, including parameters, representations, examples, and errors.
- [Query secondary indexes with the HTTP API]({{< product-version-root >}}reference/http-api/secondary-indexes/) — Document the complete HTTP contract for this operation, including parameters, representations, examples, and errors.
- [Set bucket properties with the HTTP API]({{< product-version-root >}}reference/http-api/set-bucket-properties/) — Document the complete HTTP contract for this operation, including parameters, representations, examples, and errors.
- [Status with the HTTP API]({{< product-version-root >}}reference/http-api/status/) — Document the complete HTTP contract for this operation, including parameters, representations, examples, and errors.
- [Store an object with the HTTP API]({{< product-version-root >}}reference/http-api/store-object/) — Document the complete HTTP contract for this operation, including parameters, representations, examples, and errors.
