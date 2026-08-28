---
title: "PBC Get Bucket Type"
sidebar_position: 112
sidebar_label: Get Bucket Type
pagination_label: "PBC Get Bucket Type"
hide_table_of_contents: true
last_update:
  author: RiakDocs
  date: 2019-11-21
---
import RiakDocsNote from '@site/src/components/RiakDocs/RiakDocsNote';


Gets the bucket properties associated with a [bucket type](./../../../../using/cluster-operations/bucket-types).

## Request

```protobuf
message RpbGetBucketTypeReq {
    required bytes type = 1;
}
```

Only the name of the bucket type needs to be specified (under `name`).

## Response

A bucket type's properties will be sent to the client as part of an
[`RpbBucketProps`](./../get-bucket-props) message.
