---
title: "PBC Data Type Counter Store"
sidebar_position: 117
sidebar_label: Data Type Counter Store
pagination_label: "PBC Data Type Counter Store"
hide_table_of_contents: true
last_update:
  author: RiakDocs
  date: 2021-08-09
---
import RiakDocsNote from '@site/src/components/RiakDocs/RiakDocsNote';


An operation to update a [counter](./../../../data-types).

## Request

```protobuf
message CounterOp {
    optional sint64 increment = 1;
}
```

The `increment` value specifies how much the counter will be incremented
or decremented, depending on whether the `increment` value is positive
or negative. This operation can be used to update counters that are
stored on their own in a key or [within a map](./../dt-map-store).

