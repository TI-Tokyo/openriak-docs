---
title: 'Reset bucket properties with Protocol Buffers'
description: 'Document the Protocol Buffers contract for this operation, including messages, fields, streaming behavior, examples, and errors.'
weight: 14
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
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\developing\api\protocol-buffers\reset-bucket-props.md'
tags: ['diataxis', 'kv', 'reference']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Document the Protocol Buffers contract for this operation, including messages, fields, streaming behavior, examples, and errors.

## Details

### PBC Reset Bucket Properties

Request to reset the properties of a given bucket or bucket type.

#### Request

```protobuf
message RpbResetBucketReq {
    required bytes bucket = 1;
    optional bytes type = 2;
}
```

You must specify the name of the bucket (`bucket`) and optionally a
[bucket type]({{< product-version-root >}}how-to/develop/use-bucket-types/) using the `type` value. If you do not
specify a bucket type, the `default` bucket type will be used by Riak.

#### Response

Only the message code is returned.

#### Example

Request to reset the properties for the bucket `friends`:

##### Request

```bash
Hex      00 00 00 0A 1D 0A 07 66 72 69 65 6E 64 73
Erlang <<0,0,0,10,29,10,7,102,114,105,101,110,100,115>>

RpbResetBucketReq protoc decode:
bucket: "friends"

```

###### Response

```bash
Hex      00 00 00 01 1E
Erlang <<0,0,0,1,30>>

RpbResetBucketResp - only message code defined
```
