---
title: 'Use counters with the HTTP API'
description: 'Document the complete HTTP contract for this operation, including parameters, representations, examples, and errors.'
weight: 2
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
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\developing\api\http\counters.md'
tags: ['diataxis', 'kv', 'reference']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Document the complete HTTP contract for this operation, including parameters, representations, examples, and errors.

## Details

### HTTP Counters

Riak counters are a CRDT (convergent replicated data type) that (eventually)
converge to the correct total. You merely increment the counter with some
integer, and any potential conflicts will be automatically resolved by Riak.

#### Setup

Riak counters can only be used if the bucket has the `allow_mult` property
set to `true`.

```
curl -XPUT localhost:8098/buckets/BUCKET/props \
  -H "Content-Type: application/json" \
  -d "{\"props\" : {\"allow_mult\": true}}"
```

If you attempt to use counters without setting the above, you'll get this
message:

```
Counters require bucket property 'allow_mult=true'
```

#### Request

To insert just POST an integer value using the `/counters` resource. This will
increment that keyed value by the given amount.

```
POST /buckets/BUCKET/counters/KEY
```

To receive the current value is a GET using `/counters`

```
GET /buckets/BUCKET/counters/KEY
```

#### Response

The regular POST/PUT ([HTTP Store Object](/kv/3.4.0/reference/http-api/store-object/)) and GET ([HTTP Fetch Object](/kv/3.4.0/reference/http-api/fetch-object/)) responses apply here.

Caveats: Counters have no support for Secondary Indexes (2i), Links or Custom HTTP Metadata.

#### Example

The body must be an integer (positive or negative).

```
curl -XPOST http://localhost:8098/buckets/my_bucket/counters/my_key -d "1"

curl http://localhost:8098/buckets/my_bucket/counters/my_key
1

curl -XPOST http://localhost:8098/buckets/my_bucket/counters/my_key -d "100"

curl http://localhost:8098/buckets/my_bucket/counters/my_key
101

curl -XPOST http://localhost:8098/buckets/my_bucket/counters/my_key -d "-1"
100
```
