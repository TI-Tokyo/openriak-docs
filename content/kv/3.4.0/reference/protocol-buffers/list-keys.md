---
title: 'List keys with Protocol Buffers'
description: 'Document the Protocol Buffers contract for this operation, including messages, fields, streaming behavior, examples, and errors.'
weight: 11
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
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\developing\api\protocol-buffers\list-keys.md'
tags: ['diataxis', 'kv', 'reference']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Document the Protocol Buffers contract for this operation, including messages, fields, streaming behavior, examples, and errors.

## Details

### PBC List Keys

List all of the keys in a bucket. This is a streaming call, with
multiple response messages sent for each request.

**Not for production use**
This operation requires traversing all keys stored in the cluster and should
not be used in production.

#### Request

```protobuf
message RpbListKeysReq {
    required bytes bucket = 1;
}
```

Optional Parameters

* `bucket` - bucket to get keys from

#### Response

```protobuf
message RpbListKeysResp {
    repeated bytes keys = 1;
    optional bool done = 2;
}
```

##### Values

* **keys** - batch of keys in the bucket.
* **done** - set true on the last response packet

#### Example

##### Request

```bash
Hex      00 00 00 0B 11 0A 08 6C 69 73 74 6B 65 79 73
Erlang <<0,0,0,11,17,10,8,108,105,115,116,107,101,121,115>>

RpbListKeysReq protoc decode:
bucket: "listkeys"

```

###### Response Packet 1

```bash
Hex      00 00 00 04 12 0A 01 34
Erlang <<0,0,0,4,18,10,1,52>>

RpbListKeysResp protoc decode:
keys: "4"

```

###### Response Packet 2

```bash
Hex      00 00 00 08 12 0A 02 31 30 0A 01 33
Erlang <<0,0,0,8,18,10,2,49,48,10,1,51>>

RpbListKeysResp protoc decode:
keys: "10"
keys: "3"
```

###### Response Packet 3

```bash
Hex      00 00 00 03 12 10 01
Erlang <<0,0,0,3,18,16,1>>

RpbListKeysResp protoc decode:
done: true

```
