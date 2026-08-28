---
title: 'Get a bucket type with Protocol Buffers'
description: 'Document the Protocol Buffers contract for this operation, including messages, fields, streaming behavior, examples, and errors.'
weight: 9
diataxis: 'reference'
product: 'OpenRiak KV'
product_version: '3.4.0'
status: 'editorially-rewritten'
draft: true
audience:
  - 'developers'
source_material:
  - 'legacy-3.2.5'
  - 'live-3.2.5'
  - 'proposed-kv'
legacy_3_2_5_sources:
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\developing\api\protocol-buffers\get-bucket-type.md'
tags: ['diataxis', 'kv', 'reference']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Document the Protocol Buffers contract for this operation, including messages, fields, streaming behavior, examples, and errors.

## Details

### PBC Get Bucket Type

Gets the bucket properties associated with a [bucket type]({{< baseurl >}}kv/3.4.0/how-to/operate/manage-bucket-types/).

#### Request

```protobuf
message RpbGetBucketTypeReq {
    required bytes type = 1;
}
```

Only the name of the bucket type needs to be specified (under `name`).

#### Response

A bucket type's properties will be sent to the client as part of an
[`RpbBucketProps`]({{< baseurl >}}kv/3.4.0/reference/protocol-buffers/get-bucket-properties/) message.
