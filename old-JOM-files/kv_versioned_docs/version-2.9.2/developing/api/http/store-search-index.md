---
title: "HTTP Store Search Index"
sidebar_position: 115
sidebar_label: Store Search Index
pagination_label: "HTTP Store Search Index"
hide_table_of_contents: true
last_update:
  author: RiakDocs
  date: 2020-04-08
---
import RiakDocsNote from '@site/src/components/RiakDocs/RiakDocsNote';


Creates a new Riak Search [index](./../../../usage/search/#simple-setup).

## Request

```
PUT /search/index/<index_name>
```

## Optional Request Body

If you run a `PUT` request to this endpoint without a request body, Riak
will create a new Search index that uses the [default Search schema](./../../../usage/search-schemas/#the-default-schema), i.e. `_yz_default`.

To specify a different schema, however, you must pass Riak a JSON object
as the request body in which the `schema` field specifies the name of
the schema to use. If you've [stored a schema](./../../../usage/search-schemas/#custom-schemas) called `my_custom_schema`, the following `PUT`
request would create an index called `my_index` that used that schema:

```curl
curl -XPUT http://localhost:8098/search/index/my_index \
  -H "Content-Type: application/json" \
  -d '{"schema": "my_custom_schema"}'
```

More information can be found in [Using Search](./../../../usage/search).

## Normal Response Codes

* `204 No Content` --- The index has been successfully created

## Typical Error Codes

* `409 Conflict` --- The index cannot be created because there is
    already an index with that name
* `503 Service Unavailable` --- The request timed out internally
