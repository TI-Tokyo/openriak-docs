---
title: "PBC Set Bucket Type"
sidebar_position: 113
sidebar_label: Set Bucket Type
pagination_label: "PBC Set Bucket Type"
hide_table_of_contents: true
last_update:
  author: RiakDocs
  date: 2017-03-08
---
import RiakDocsNote from '@site/src/components/RiakDocs/RiakDocsNote';


Assigns a set of [bucket properties](./../set-bucket-props) to a
[bucket type](./../../../usage/bucket-types).

## Request

```protobuf
message RpbSetBucketTypeReq {
    required bytes type = 1;
    required RpbBucketProps props = 2;
}
```

The `type` field specifies the name of the bucket type as a binary. The
`props` field contains an [`RpbBucketProps`](./../get-bucket-props).
