---
title: 'Protocol Buffers API reference'
description: 'Define framing, message conventions, authentication, errors, and operation compatibility for Protocol Buffers.'
weight: 1
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
migration_source_root: '\\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv'
migration_sources:
  - '\\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv\apis-and-clients\APIs\protocol_buffers\protocol-buffers.md'
legacy_3_2_5_sources:
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\developing\api\protocol-buffers.md'
tags: ['diataxis', 'kv', 'reference']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Define framing, message conventions, authentication, errors, and operation compatibility for Protocol Buffers.

## Details

### Protocol Buffers Client API

This is an overview of the operations you can perform using the
[Protocol Buffers](https://code.google.com/p/protobuf/) Client (PBC)
interface to Riak, and can be used as a guide for developing a
PBC-compliant Riak client.

#### Protocol

Riak listens on a TCP port (8087 by default) for incoming connections.
Once connected, the client can send a stream of requests on the same
connection.

Each operation consists of a [request message](https://developers.google.com/protocol-buffers/docs/encoding) and one or more response messages. Messages are all encoded the same way, consisting of:

* 32-bit length of message code + Protocol Buffers message in network
  order
* 8-bit message code to identify the Protocol Buffers message
* N bytes of Protocol Buffers-encoded message

##### Example

```
00 00 00 07 09 0A 01 62 12 01 6B
|----Len---|MC|----Message-----|

Len = 0x07
Message Code (MC) = 0x09 = RpbGetReq
RpbGetReq Message = 0x0A 0x01 0x62 0x12 0x01 0x6B

Decoded Message:
bucket: "b"
key: "k"
```

#### Message Codes

Code | Message |
:----|:--------|
0 | `RpbErrorResp` |
1 | `RpbPingReq` |
2 | `RpbPingResp` |
3 | `RpbGetClientIdReq` |
4 | `RpbGetClientIdResp` |
5 | `RpbSetClientIdReq` |
6 | `RpbSetClientIdResp` |
7 | `RpbGetServerInfoReq` |
8 | `RpbGetServerInfoResp` |
9 | `RpbGetReq` |
10 | `RpbGetResp` |
11 | `RpbPutReq` |
12 | `RpbPutResp` |
13 | `RpbDelReq` |
14 | `RpbDelResp` |
15 | `RpbListBucketsReq` |
16 | `RpbListBucketsResp` |
17 | `RpbListKeysReq` |
18 | `RpbListKeysResp` |
19 | `RpbGetBucketReq` |
20 | `RpbGetBucketResp` |
21 | `RpbSetBucketReq` |
22 | `RpbSetBucketResp` |
23 | `RpbMapRedReq` |
24 | `RpbMapRedResp` |
25 | `RpbIndexReq` |
26 | `RpbIndexResp` |
27 | `RpbSearchQueryReq` |
28 | `RbpSearchQueryResp` |
29 | `RpbResetBucketReq` |
30 | `RpbResetBucketResp` |
31 | `RpbGetBucketTypeReq` |
32 | `RpbSetBucketTypeResp` |
40 | `RpbCSBucketReq` |
41 | `RpbCSUpdateReq` |
50 | `RpbCounterUpdateReq` |
51 | `RpbCounterUpdateResp` |
52 | `RpbCounterGetReq` |
53 | `RpbCounterGetResp` |
80 | `DtFetchReq` |
81 | `DtFetchResp` |
82 | `DtUpdateReq` |
83 | `DtUpdateResp` |
253 | `RpbAuthReq` |
254 | `RpbAuthResp` |
255 | `RpbStartTls` |

**Message Definitions**
All Protocol Buffers messages are defined in the `riak.proto` and other
`.proto` files in the `/src` directory of the
<a href="https://github.com/basho/riak_pb">RiakPB</a> project.

##### Error Response

If the request does not result in an error, Riak will return one of a
variety of response messages, e.g. `RpbGetResp` or `RpbPutResp`,
depending on which request message is sent.

If the server experiences an error processing a request, however, it
will return an `RpbErrorResp` message instead of the response expected
for the given request (e.g. `RbpGetResp` is the expected response to
`RbpGetReq`). Error messages contain an error string and an error code,
like this:

```protobuf
message RpbErrorResp {
    required bytes errmsg = 1;
    required uint32 errcode = 2;
}
```

##### Values

* `errmsg` - A string representation of what went wrong
* `errcode` - A numeric code. Currently, only `RIAKC_ERR_GENERAL=1`
  is defined.

#### Bucket Operations

* [PBC List Buckets](/kv/3.4.0/reference/protocol-buffers/list-buckets/)
* [PBC List Keys](/kv/3.4.0/reference/protocol-buffers/list-keys/)
* [PBC Get Bucket Properties](/kv/3.4.0/reference/protocol-buffers/get-bucket-properties/)
* [PBC Set Bucket Properties](/kv/3.4.0/reference/protocol-buffers/set-bucket-properties/)
* [PBC Reset Bucket Properties](/kv/3.4.0/reference/protocol-buffers/reset-bucket-properties/)

#### Object/Key Operations

* [PBC Fetch Object](/kv/3.4.0/reference/protocol-buffers/fetch-object/)
* [PBC Store Object](/kv/3.4.0/reference/protocol-buffers/store-object/)
* [PBC Delete Object](/kv/3.4.0/reference/protocol-buffers/delete-object/)

#### Query Operations

* [PBC MapReduce](/kv/3.4.0/reference/protocol-buffers/mapreduce/)
* [PBC Secondary Indexes](/kv/3.4.0/reference/protocol-buffers/secondary-indexes/)
* [PBC Search](/kv/3.4.0/reference/specialized-apis/legacy-query-api/)

#### Server Operations

* [PBC Ping](/kv/3.4.0/reference/protocol-buffers/ping/)
* [PBC Server Info](/kv/3.4.0/reference/protocol-buffers/server-information/)

#### Bucket Type Operations

* [PBC Get Bucket Type](/kv/3.4.0/reference/protocol-buffers/get-bucket-type/)
* [PBC Set Bucket Type](/kv/3.4.0/reference/protocol-buffers/set-bucket-type/)

#### Data Type Operations

* [PBC Data Type Fetch](/kv/3.4.0/reference/protocol-buffers/fetch-data-type/)
* [PBC Data Type Union](/kv/3.4.0/reference/protocol-buffers/union-data-type/)
* [PBC Data Type Store](/kv/3.4.0/reference/protocol-buffers/store-data-type/)
* [PBC Data Type Counter Store](/kv/3.4.0/reference/protocol-buffers/update-counter/)
* [PBC Data Type Set Store](/kv/3.4.0/reference/protocol-buffers/update-set/)
* [PBC Data Type Map Store](/kv/3.4.0/reference/protocol-buffers/update-map/)

[protocol]: #protocol
[whatmakesop]: /kv/3.4.0/reference/protocol-buffers/

## In this section

- [Authentication request with Protocol Buffers](/kv/3.4.0/reference/protocol-buffers/authentication/) — Document the Protocol Buffers contract for this operation, including messages, fields, streaming behavior, examples, and errors.
- [Manage a client identifier with Protocol Buffers](/kv/3.4.0/reference/protocol-buffers/client-id/) — Document the Protocol Buffers contract for this operation, including messages, fields, streaming behavior, examples, and errors.
- [Run coverage queries with Protocol Buffers](/kv/3.4.0/reference/protocol-buffers/coverage-queries/) — Document the Protocol Buffers contract for this operation, including messages, fields, streaming behavior, examples, and errors.
- [Delete an object with Protocol Buffers](/kv/3.4.0/reference/protocol-buffers/delete-object/) — Document the Protocol Buffers contract for this operation, including messages, fields, streaming behavior, examples, and errors.
- [Fetch a data type with Protocol Buffers](/kv/3.4.0/reference/protocol-buffers/fetch-data-type/) — Document the Protocol Buffers contract for this operation, including messages, fields, streaming behavior, examples, and errors.
- [Fetch an object with Protocol Buffers](/kv/3.4.0/reference/protocol-buffers/fetch-object/) — Document the Protocol Buffers contract for this operation, including messages, fields, streaming behavior, examples, and errors.
- [Get bucket properties with Protocol Buffers](/kv/3.4.0/reference/protocol-buffers/get-bucket-properties/) — Document the Protocol Buffers contract for this operation, including messages, fields, streaming behavior, examples, and errors.
- [Get a bucket type with Protocol Buffers](/kv/3.4.0/reference/protocol-buffers/get-bucket-type/) — Document the Protocol Buffers contract for this operation, including messages, fields, streaming behavior, examples, and errors.
- [List buckets with Protocol Buffers](/kv/3.4.0/reference/protocol-buffers/list-buckets/) — Document the Protocol Buffers contract for this operation, including messages, fields, streaming behavior, examples, and errors.
- [List keys with Protocol Buffers](/kv/3.4.0/reference/protocol-buffers/list-keys/) — Document the Protocol Buffers contract for this operation, including messages, fields, streaming behavior, examples, and errors.
- [Run MapReduce with Protocol Buffers](/kv/3.4.0/reference/protocol-buffers/mapreduce/) — Document the Protocol Buffers contract for this operation, including messages, fields, streaming behavior, examples, and errors.
- [Ping with Protocol Buffers](/kv/3.4.0/reference/protocol-buffers/ping/) — Document the Protocol Buffers contract for this operation, including messages, fields, streaming behavior, examples, and errors.
- [Reset bucket properties with Protocol Buffers](/kv/3.4.0/reference/protocol-buffers/reset-bucket-properties/) — Document the Protocol Buffers contract for this operation, including messages, fields, streaming behavior, examples, and errors.
- [Query secondary indexes with Protocol Buffers](/kv/3.4.0/reference/protocol-buffers/secondary-indexes/) — Document the Protocol Buffers contract for this operation, including messages, fields, streaming behavior, examples, and errors.
- [Server information with Protocol Buffers](/kv/3.4.0/reference/protocol-buffers/server-information/) — Document the Protocol Buffers contract for this operation, including messages, fields, streaming behavior, examples, and errors.
- [Set bucket properties with Protocol Buffers](/kv/3.4.0/reference/protocol-buffers/set-bucket-properties/) — Document the Protocol Buffers contract for this operation, including messages, fields, streaming behavior, examples, and errors.
- [Set a bucket type with Protocol Buffers](/kv/3.4.0/reference/protocol-buffers/set-bucket-type/) — Document the Protocol Buffers contract for this operation, including messages, fields, streaming behavior, examples, and errors.
- [Store a data type with Protocol Buffers](/kv/3.4.0/reference/protocol-buffers/store-data-type/) — Document the Protocol Buffers contract for this operation, including messages, fields, streaming behavior, examples, and errors.
- [Store an object with Protocol Buffers](/kv/3.4.0/reference/protocol-buffers/store-object/) — Document the Protocol Buffers contract for this operation, including messages, fields, streaming behavior, examples, and errors.
- [Apply a data type union with Protocol Buffers](/kv/3.4.0/reference/protocol-buffers/union-data-type/) — Document the Protocol Buffers contract for this operation, including messages, fields, streaming behavior, examples, and errors.
- [Update a counter with Protocol Buffers](/kv/3.4.0/reference/protocol-buffers/update-counter/) — Document the Protocol Buffers contract for this operation, including messages, fields, streaming behavior, examples, and errors.
- [Update a map with Protocol Buffers](/kv/3.4.0/reference/protocol-buffers/update-map/) — Document the Protocol Buffers contract for this operation, including messages, fields, streaming behavior, examples, and errors.
- [Update a set with Protocol Buffers](/kv/3.4.0/reference/protocol-buffers/update-set/) — Document the Protocol Buffers contract for this operation, including messages, fields, streaming behavior, examples, and errors.
