---
title: 'Set bucket properties with Protocol Buffers'
description: 'Document the Protocol Buffers contract for this operation, including messages, fields, streaming behavior, examples, and errors.'
weight: 17
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
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\developing\api\protocol-buffers\set-bucket-props.md'
tags: ['diataxis', 'kv', 'reference']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Document the Protocol Buffers contract for this operation, including messages, fields, streaming behavior, examples, and errors.

## Details

### PBC Set Bucket Properties

Sets the properties for a bucket.

#### Request

```protobuf
message RpbSetBucketReq {
    required bytes bucket = 1;
    required RpbBucketProps props = 2;
    optional bytes type = 3;
}
```

You must specify the name of the bucket (`bucket`) and include an
`RpbBucketProps` message. More on that message type can be found in the
[PBC Get Bucket Properties](/kv/3.4.0/reference/protocol-buffers/get-bucket-properties/) documentation.

You can also specify a [bucket type](/kv/3.4.0/how-to/develop/use-bucket-types/) using the
`type` value. If you do not specify a bucket type, the `default` bucket
type will be used by Riak.

#### Response

Only the message code is returned.

#### Example

Change `allow_mult` to true for the bucket `friends`:

##### Request

```bash
Hex      00 00 00 0E 15 0A 07 66 72 69 65 6E 64 73 12 02
         10 01
Erlang <<0,0,0,14,21,10,7,102,114,105,101,110,100,115,18,2,16,1>>

RpbSetBucketReq protoc decode:
bucket: "friends"
props {
  allow_mult: true
}

```

###### Response

```bash
Hex      00 00 00 01 16
Erlang <<0,0,0,1,22>>

RpbSetBucketResp - only message code defined
```
