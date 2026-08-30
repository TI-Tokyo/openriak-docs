---
title: 'List keys with the HTTP API'
description: 'Document the complete HTTP contract for this operation, including parameters, representations, examples, and errors.'
weight: 8
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
legacy_3_2_5_sources:
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\developing\api\http\list-keys.md'
tags: ['diataxis', 'kv', 'reference']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Document the complete HTTP contract for this operation, including parameters, representations, examples, and errors.

## Details

### HTTP List Keys

Lists keys in a bucket.

**Not for production use**
This operation requires traversing all keys stored in the cluster and should
not be used in production.

#### Request

```bash
#### Using the default bucket type
GET /buckets/bucket/keys?keys=true    # List all keys
GET /buckets/bucket/keys?keys=stream  # Stream keys to the client

#### Using a non-default bucket type
GET /types/<type>/buckets/bucket/keys?keys=true
GET /types/<type>/buckets/bucket/keys?keys=stream
```

Required query parameters:

* `keys` - defaults to `false`. When set to `true` all keys will be returned in
a single payload.  When set to `stream`, keys will be returned in
chunked-encoding.

##### Response

Normal response codes:

* `200 OK`

Important headers:

* `Content-Type` - `application/json`
* `Transfer-Encoding` - `chunked` when the `keys` query parameter is set to
`stream`.

The JSON object in the response will contain up to two entries,
`"props"` and `"keys"` which are present or missing according to the
query parameters and format used.  If `keys=stream` in the query
parameters, multiple JSON objects in chunked-encoding will be returned
containing `"keys"` entries.

##### Example

```curl
$ curl -i http://localhost:8098/buckets/jsconf/keys?keys=true
HTTP/1.1 200 OK
Vary: Accept-Encoding
Server: MochiWeb/1.1 WebMachine/1.9.0 (participate in the frantic)
Date: Fri, 30 Sep 2011 15:24:35 GMT
Content-Type: application/json
Content-Length: 239

{"keys":["challenge.jpg","puddi.png","basho.gif","puddikid.jpg","yay.png","
thinking.png","victory.gif","slides","joyent.png","seancribbs-small.jpg","
trollface.jpg","riak_logo_animated1.gif","victory.jpg","challenge.png","
team_cribbs.png"]}
```
