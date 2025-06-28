---
title: "PBC Yokozuna Schema Put"
sidebar_position: 124
sidebar_label: Yokozuna Schema Put
pagination_label: "PBC Yokozuna Schema Put"
hide_table_of_contents: true
last_update:
  author: RiakDocs
  date: 2014-08-14
---
import RiakDocsNote from '@site/src/components/RiakDocs/RiakDocsNote';


Create a new Solr [search schema](./../../../usage/search-schemas).

## Request

```protobuf
message RpbYokozunaSchemaPutReq {
    required RpbYokozunaSchema schema =  1;
}
```

Each message must contain a `RpbYokozunaSchema` object structure.

```protobuf
message RpbYokozunaSchema {
    required bytes name    =  1;
    optional bytes content =  2;
}
```

This message *must* include both the schema `name` and its Solr [search schema](./../../../usage/search-schemas) `content` as XML.

## Response

Returns a [RpbPutResp](./../#message-codes) code with no data on success.
