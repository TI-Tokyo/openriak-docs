---
title: "PBC Yokozuna Index Delete"
sidebar_position: 122
sidebar_label: Yokozuna Index Delete
pagination_label: "PBC Yokozuna Index Delete"
hide_table_of_contents: true
last_update:
  author: RiakDocs
  date: 2016-06-24
---
import RiakDocsNote from '@site/src/components/RiakDocs/RiakDocsNote';


Delete a search index.

## Request

The `name` parameter is the name of the index to delete, as a binary.

```protobuf
message RpbYokozunaIndexDeleteReq {
    required bytes name  =  1;
}
```

## Response

 Returns a [RpbDelResp](./../#message-codes) code with no data on success.
