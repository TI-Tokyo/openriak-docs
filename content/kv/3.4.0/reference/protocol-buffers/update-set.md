---
title: 'Update a set with Protocol Buffers'
description: 'Document the Protocol Buffers contract for this operation, including messages, fields, streaming behavior, examples, and errors.'
weight: 24
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
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\developing\api\protocol-buffers\dt-set-store.md'
tags: ['diataxis', 'kv', 'reference']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Document the Protocol Buffers contract for this operation, including messages, fields, streaming behavior, examples, and errors.

## Details

### PBC Data Type Set Store

An operation to update a set, either on its own (at the bucket/key
level) or [inside of a map]({{< baseurl >}}kv/3.4.0/reference/protocol-buffers/update-map/).

#### Request

```protobuf
message SetOp {
    repeated bytes adds    = 1;
    repeated bytes removes = 2;
}
```

Set members are binary values that can only be added (`adds`) or removed
(`removes`) from a set. You can add and/or remove as many members of a
set in a single message as you would like.
