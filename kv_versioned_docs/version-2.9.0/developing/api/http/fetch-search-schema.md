---
title: "HTTP Fetch Search Schema"
sidebar_position: 116
sidebar_label: Fetch Search Schema
pagination_label: "HTTP Fetch Search Schema"
hide_table_of_contents: true
last_update:
  author: RiakDocs
  date: 2019-11-21
---
import RiakDocsNote from '@site/src/components/RiakDocs/RiakDocsNote';


Retrieves a Riak KV [search schema](./../../../usage/search-schemas).

## Request

```
GET /search/schema/<schema_name>
```

## Normal Response Codes

* `200 OK`

## Typical Error Codes

* `404 Object Not Found`
* `503 Service Unavailable` --- The request timed out internally

## Response

If the schema is found, Riak will return the contents of the schema as
XML (all Riak Search schemas are XML).
