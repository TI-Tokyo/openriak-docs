---
title: "PBC Yokozuna Index Put"
sidebar_position: 121
sidebar_label: Yokozuna Index Put
pagination_label: "PBC Yokozuna Index Put"
hide_table_of_contents: true
last_update:
  author: RiakDocs
  date: 2017-03-15
---
import RiakDocsNote from '@site/src/components/RiakDocs/RiakDocsNote';


Create a new index or modify an existing index.

## Request

```protobuf
message RpbYokozunaIndexPutReq {
    required RpbYokozunaIndex index  =  1;
}
```

Each message must contain a `RpbYokozunaIndex` message providing
information about the index being stored.

```protobuf
message RpbYokozunaIndex {
    required bytes name   =  1;
    optional bytes schema =  2;
    optional uint32 n_val =  3;
}
```

Each message specifying an index must include the index's name as a
binary (as `name`). Optionally, you can specify a [`schema`](./../../../usage/search-schemas) name and/or an `n_val`, i.e. the number of nodes on which the index is stored (for GET requests) or on which you wish the index to be stored (for PUT requests). An index's `n_val` must match the associated bucket's `n_val`.

## Response

Returns a [RpbPutResp](./../#message-codes) code with no data on success.

