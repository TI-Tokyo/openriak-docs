---
weight: 102
title: "HTTP API"
description: ""
project: "riak_kv"
project_version: "3.2.5"
lastmod: 2025-03-24T00:00:00-00:00
sitemap:
  priority: 0.9
menu:
  riak_kv-3.2.5:
    name: "HTTP API"
    identifier: "apis_http"
    weight: 102
    parent: "developing_apis"
toc: true
aliases:
  - /riak/3.2.5/dev/references/http
  - /riak/kv/3.2.5/dev/references/http
---

Riak has a rich, full-featured HTTP 1.1 API. This is an overview of the
operations you can perform via HTTP and can be used as a guide for
developing a compliant client. All URLs assume the default configuration
values where applicable. All examples use `curl` to interact with Riak.

> **URL Escaping**
>
> Buckets, keys, and link specifications may not contain unescaped
slashes. Use a URL-escaping library or replace slashes with `%2F`.

## Bucket-related Operations

Method | URL | Doc
:------|:----|:---
`GET` | `/types/<type>/buckets/<bucket>/props` | [HTTP Get Bucket Properties]({{< product-version-root >}}developing/api/http/get-bucket-props)
`PUT` | `/types/<type>/buckets/<bucket>/props` | [HTTP Set Bucket Properties]({{< product-version-root >}}developing/api/http/set-bucket-props)
`DELETE` | `/types/<type>/buckets/<bucket>/props` | [HTTP Reset Bucket Properties]({{< product-version-root >}}developing/api/http/reset-bucket-props)
`GET` | `/types/<type>/buckets?buckets=true` | [HTTP List Buckets]({{< product-version-root >}}developing/api/http/list-buckets)
`GET` | `/types/<type>/buckets/<bucket>/keys?keys=true` | [HTTP List Keys]({{< product-version-root >}}developing/api/http/list-keys)

## Object-related Operations

Method | URL | Doc
:------|:----|:---
`GET` | `/types/<type>/buckets/<bucket>/keys/<key>` | [HTTP Fetch Object]({{< product-version-root >}}developing/api/http/fetch-object)
`POST` | `/types/<type>/buckets/<bucket>/keys` | [HTTP Store Object]({{< product-version-root >}}developing/api/http/store-object)
`PUT` | `/types/<type>/buckets/<bucket>/keys/<key>` | [HTTP Store Object]({{< product-version-root >}}developing/api/http/store-object)
`POST` | `/types/<type>/buckets/<bucket>/keys/<key>` | [HTTP Store Object]({{< product-version-root >}}developing/api/http/store-object)
`DELETE` | `/types/<type>/buckets/<bucket>/keys/<key>` | [HTTP Delete Object]({{< product-version-root >}}developing/api/http/delete-object)

## Riak-Data-Type-related Operations

Method | URL
:------|:----
`GET` | `/types/<type>/buckets/<bucket>/datatypes/<key>`
`POST` | `/types/<type>/buckets/<bucket>/datatypes`
`POST` | `/types/<type>/buckets/<bucket>/datatypes/<key>`

For documentation on the HTTP API for [Riak Data Types]({{< product-version-root >}}learn/concepts/crdts),
see the `curl` examples in [Using Data Types]({{< product-version-root >}}developing/data-types/#usage-examples)
and subpages e.g. [sets]({{< product-version-root >}}developing/data-types/sets).

Advanced users may consult the technical documentation inside the Riak
KV internal module `riak_kv_wm_crdt`.

## Query-related Operations

Method | URL | Doc
:------|:----|:---
`POST` | `/mapred` | [HTTP MapReduce]({{< product-version-root >}}developing/api/http/mapreduce)
`GET` | `/types/<type>/buckets/<bucket>/index/<index>/<value>` | [HTTP Secondary Indexes]({{< product-version-root >}}developing/api/http/secondary-indexes)
`GET` | `/types/<type>/buckets/<bucket>/index/<index>/<start>/<end>` | [HTTP Secondary Indexes]({{< product-version-root >}}developing/api/http/secondary-indexes)

## Server-related Operations

Method | URL | Doc
:------|:----|:---
`GET` | `/ping` | [HTTP Ping]({{< product-version-root >}}developing/api/http/ping)
`GET` | `/stats` | [HTTP Status]({{< product-version-root >}}developing/api/http/status)
`GET` | `/` | [HTTP List Resources]({{< product-version-root >}}developing/api/http/list-resources)

## Search-related Operations

Method | URL | Doc
:------|:----|:---
`GET` | `/search/query/<index_name>` | [HTTP Search Query]({{< product-version-root >}}deprecated/riak-search/)
`GET` | `/search/index` | [HTTP Search Index Info]({{< product-version-root >}}deprecated/riak-search/)
`GET` | `/search/index/<index_name>` | [HTTP Fetch Search Index]({{< product-version-root >}}deprecated/riak-search/)
`PUT` | `/search/index/<index_name>` | [HTTP Store Search Index]({{< product-version-root >}}deprecated/riak-search/)
`DELETE` | `/search/index/<index_name>` | [HTTP Delete Search Index]({{< product-version-root >}}deprecated/riak-search/)
`GET` | `/search/schema/<schema_name>` | [HTTP Fetch Search Schema]({{< product-version-root >}}deprecated/riak-search/)
`PUT` | `/search/schema/<schema_name>` | [HTTP Store Search Schema]({{< product-version-root >}}deprecated/riak-search/)

