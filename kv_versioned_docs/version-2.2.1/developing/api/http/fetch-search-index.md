---
title: "HTTP Fetch Search Index"
sidebar_position: 115
sidebar_label: Fetch Search Index
pagination_label: "HTTP Fetch Search Index"
hide_table_of_contents: true
last_update:
  author: RiakDocs
  date: 2017-03-08
---
import RiakDocsNote from '@site/src/components/RiakDocs/RiakDocsNote';


Retrieves information about a Riak Search [index](./../../../usage/search/#simple-setup).

## Request

```
GET /search/index/<index_name>
```

## Normal Response Codes

* `200 OK`

## Typical Error Codes

* `404 Object Not Found` --- No Search index with that name is currently
    available
* `503 Service Unavailable` --- The request timed out internally

## Response

If the index is found, Riak will output a JSON object describing the
index, including its name, the [`n_val`](./../../../app-guide/replication-properties/#a-primer-on-n-r-and-w) associated with it, and the [search schema](./../../../usage/search-schemas) used by the index. Here is an example:

```json
{
  "name": "my_index",
  "n_val": 3,
  "schema": "_yz_default"
}
```
