---
title: 'Set a bucket type with Protocol Buffers'
description: 'Document the Protocol Buffers contract for this operation, including messages, fields, streaming behavior, examples, and errors.'
weight: 18
diataxis: 'reference'
product: 'OpenRiak KV'
product_version: '3.4.1'
status: 'editorially-rewritten'
draft: true
audience:
  - 'developers'
source_material:
  - 'legacy-3.2.5'
  - 'live-3.2.5'
  - 'proposed-kv'
legacy_3_2_5_sources:
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\developing\api\protocol-buffers\set-bucket-type.md'
tags: ['diataxis', 'kv', 'reference']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Document the Protocol Buffers contract for this operation, including messages, fields, streaming behavior, examples, and errors.

## Details

### PBC Set Bucket Type

Assigns a set of [bucket properties]({{< baseurl >}}kv/3.4.1/reference/protocol-buffers/set-bucket-properties/) to a
[bucket type]({{< baseurl >}}kv/3.4.1/how-to/develop/use-bucket-types/).

#### Request

```protobuf
message RpbSetBucketTypeReq {
    required bytes type = 1;
    required RpbBucketProps props = 2;
}
```

The `type` field specifies the name of the bucket type as a binary. The
`props` field contains an [`RpbBucketProps`]({{< baseurl >}}kv/3.4.1/reference/protocol-buffers/get-bucket-properties/).
