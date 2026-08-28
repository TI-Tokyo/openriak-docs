---
title: "PBC Data Type Set Store"
sidebar_position: 118
sidebar_label: Data Type Set Store
pagination_label: "PBC Data Type Set Store"
hide_table_of_contents: true
last_update:
  author: RiakDocs
  date: 2022-10-12
---
import RiakDocsNote from '@site/src/components/RiakDocs/RiakDocsNote';


An operation to update a set, either on its own (at the bucket/key
level) or [inside of a map](./../dt-map-store).

## Request

```protobuf
message SetOp {
    repeated bytes adds    = 1;
    repeated bytes removes = 2;
}
```

Set members are binary values that can only be added (`adds`) or removed
(`removes`) from a set. You can add and/or remove as many members of a
set in a single message as you would like.

