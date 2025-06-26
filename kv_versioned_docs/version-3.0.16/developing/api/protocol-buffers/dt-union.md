---
title: "PBC Data Type Union"
sidebar_position: 115
sidebar_label: Data Type Union
pagination_label: "PBC Data Type Union"
hide_table_of_contents: true
last_update:
  author: RiakDocs
  date: 2023-06-23
---
import RiakDocsNote from '@site/src/components/RiakDocs/RiakDocsNote';


A "union" type for update operations.

## Request

```protobuf
message DtOp {
    optional CounterOp counter_op = 1;
    optional SetOp     set_op     = 2;
    optional MapOp     map_op     = 3;
}
```

The included operation depends on the Data Type that is being updated.
`DtOp` messages are sent only as part of a [`DtUpdateReq`](./../dt-store) message.

