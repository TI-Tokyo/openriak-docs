---
title: 'List buckets with the HTTP API'
description: 'Document the complete HTTP contract for this operation, including parameters, representations, examples, and errors.'
weight: 7
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
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\developing\api\http\list-buckets.md'
tags: ['diataxis', 'kv', 'reference']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Document the complete HTTP contract for this operation, including parameters, representations, examples, and errors.

## Details

### HTTP List Buckets

Lists all known buckets (ones that have keys stored in them).

**Not for production use**
Similar to the list keys operation, this requires traversing all keys stored
in the cluster and should not be used in production.

#### Request

```bash
#### Using the default bucket type
GET /buckets?buckets=true

#### Using a non-default bucket type
GET /types/<type>/buckets?buckets=true
```

Required query parameter:

* **buckets=true** - required to invoke the list-buckets functionality

##### Response

Normal status codes:

* `200 OK`

Important headers:

* `Content-Type - application/json`

The JSON object in the response will contain a single entry, "buckets", which
will be an array of bucket names.

##### Example

```curl
$ curl -i http://localhost:8098/buckets?buckets=true
HTTP/1.1 200 OK
Vary: Accept-Encoding
Server: MochiWeb/1.1 WebMachine/1.9.0 (participate in the frantic)
Date: Fri, 30 Sep 2011 15:24:35 GMT
Content-Type: application/json
Content-Length: 21

{"buckets":["files"]}
```
