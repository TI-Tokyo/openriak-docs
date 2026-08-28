---
title: 'Get bucket properties with the HTTP API'
description: 'Document the complete HTTP contract for this operation, including parameters, representations, examples, and errors.'
weight: 5
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
legacy_3_2_5_sources:
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\developing\api\http\get-bucket-props.md'
tags: ['diataxis', 'kv', 'reference']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Document the complete HTTP contract for this operation, including parameters, representations, examples, and errors.

## Details

### HTTP Get Bucket Properties

Reads the bucket or bucket type properties.

#### Request

```bash
GET /buckets/bucket/props
```

Or, to read bucket properties from a bucket in a bucket type:

```bash
GET /types/type/buckets/bucket/props
```

Optional query parameters (only valid for the old format):

* `props` - whether to return the bucket properties (`true` is the default)
* `keys` - whether to return the keys stored in the bucket. (`false` is the
default). See also [HTTP List Keys](/kv/3.4.1/reference/http-api/list-keys/).

#### Response

Normal status codes:

* `200 OK`

Important headers:

* `Content-Type` - `application/json`

The JSON object in the response will contain up to two entries, `"props"` and
`"keys"`, which are present or missing, according to the optional query
parameters.  The default is for only `"props"` to be present.

See [HTTP Set Bucket Properties](/kv/3.4.1/reference/http-api/set-bucket-properties/) for more information about the available
bucket properties. See [Managing Bucket Types Through the Command Line](/kv/3.4.1/reference/data/buckets-and-bucket-types/#managing-bucket-types-through-the-command-line) for more details about reading bucket types using  the `riak admin bucket-type` interface.

#### Example

```curl
$ curl -v http://127.0.0.1:8098/buckets/test/props
* About to connect() to 127.0.0.1 port 8098 (#0)
*   Trying 127.0.0.1... connected
* Connected to 127.0.0.1 (127.0.0.1) port 8098 (#0)
> GET /buckets/test/props HTTP/1.1
> User-Agent: curl/7.19.7 (universal-apple-darwin10.0) libcurl/7.19.7
OpenSSL/0.9.8l zlib/1.2.3
> Host: 127.0.0.1:8098
> Accept: */*
>
< HTTP/1.1 200 OK
< Vary: Accept-Encoding
< Server: MochiWeb/1.1 WebMachine/1.9.0 (participate in the frantic)
< Date: Fri, 30 Sep 2011 15:24:35 GMT
< Content-Type: application/json
< Content-Length: 368
<
* Connection #0 to host 127.0.0.1 left intact
* Closing connection #0
{"props":{"name":"test","n_val":3,"allow_mult":false,"last_write_wins":false,"
precommit":[],"postcommit":[],"chash_keyfun":{"mod":"riak_core_util","fun":"
chash_std_keyfun"},"linkfun":{"mod":"riak_kv_wm_link_walker","fun":"
mapreduce_linkfun"},"old_vclock":86400,"young_vclock":20,"big_vclock":50,"
small_vclock":10,"r":"quorum","w":"quorum","dw":"quorum","rw":"quorum"}}
```
