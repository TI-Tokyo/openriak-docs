---
title: "PBC Yokozuna Schema Get"
sidebar_position: 123
sidebar_label: Yokozuna Schema Get
pagination_label: "PBC Yokozuna Schema Get"
hide_table_of_contents: true
last_update:
  author: RiakDocs
  date: 2020-12-08
---
import RiakDocsNote from '@site/src/components/RiakDocs/RiakDocsNote';


Fetch a [search schema](./../../../usage/search-schemas) from Riak Search.

## Request

In a request message, you only need to specify the name of the schema as
a binary (under `name`);

```protobuf
message RpbYokozunaSchemaGetReq {
    required bytes name  =  1;  // Schema name
}
```

## Response

```protobuf
message RpbYokozunaSchemaGetResp {
  required RpbYokozunaSchema schema =  1;
}
```

The response message will include a `RpbYokozunaSchema` structure.

```protobuf
message RpbYokozunaSchema {
    required bytes name    =  1;
    optional bytes content =  2;
}
```

This message includes the schema `name` and its xml `content`.

