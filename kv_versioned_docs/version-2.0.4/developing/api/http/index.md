---
title: "HTTP API"
sidebar_position: 102
sidebar_label: HTTP API
pagination_label: "HTTP API"
hide_table_of_contents: true
last_update:
  author: RiakDocs
  date: 2015-01-10
---
import RiakDocsNote from '@site/src/components/RiakDocs/RiakDocsNote';


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
`GET` | `/types/<type>/buckets/<bucket>/props` | [HTTP Get Bucket Properties](./get-bucket-props)
`PUT` | `/types/<type>/buckets/<bucket>/props` | [HTTP Set Bucket Properties](./set-bucket-props)
`DELETE` | `/types/<type>/buckets/<bucket>/props` | [HTTP Reset Bucket Properties](./reset-bucket-props)
`GET` | `/types/<type>/buckets?buckets=true` | [HTTP List Buckets](./list-buckets)
`GET` | `/types/<type>/buckets/<bucket>/keys?keys=true` | [HTTP List Keys](./list-keys)

## Object-related Operations

Method | URL | Doc
:------|:----|:---
`GET` | `/types/<type>/buckets/<bucket>/keys/<key>` | [HTTP Fetch Object](./fetch-object)
`POST` | `/types/<type>/buckets/<bucket>/keys/<key>` | [HTTP Store Object](./store-object)
`PUT` | `/types/<type>/buckets/<bucket>/keys/<key>` | [HTTP Store Object](./store-object)
`DELETE` | `/types/<type>/buckets/<bucket>/keys/<key>` | [HTTP Delete Object](./delete-object)

## Riak-Data-Type-related Operations

For documentation on the HTTP API for [Riak Data Types](./../../../learn/concepts/crdts),
see the `curl` examples in [Using Data Types](./../../data-types).

## Query-related Operations

Method | URL | Doc
:------|:----|:---
`POST` | `/mapred` | [HTTP MapReduce](./mapreduce)
`GET` | `/types/<type>/buckets/<bucket>/index/<index>/<value>` | [HTTP Secondary Indexes](./secondary-indexes)
`GET` | `/types/<type>/buckets/<bucket>/index/<index>/<start>/<end>` | [HTTP Secondary Indexes](./secondary-indexes)

## Server-related Operations

Method | URL | Doc
:------|:----|:---
`GET` | `/ping` | [HTTP Ping](./ping)
`GET` | `/stats` | [HTTP Status](./status)
`GET` | `/` | [HTTP List Resources](./list-resources)

## Search-related Operations

Method | URL | Doc
:------|:----|:---
`GET` | `/search/query/<index_name>` | [HTTP Search Query](./search-query)
`GET` | `/search/index` | [HTTP Search Index Info](./search-index-info)
`GET` | `/search/index/<index_name>` | [HTTP Fetch Search Index](./fetch-search-index)
`PUT` | `/search/index/<index_name>` | [HTTP Store Search Index](./store-search-index)
`DELETE` | `/search/index/<index_name>` | [HTTP Delete Search Index](./delete-search-index)
`GET` | `/search/schema/<schema_name>` | [HTTP Fetch Search Schema](./fetch-search-schema)
`PUT` | `/search/schema/<schema_name>` | [HTTP Store Search Schema](./store-search-schema)
