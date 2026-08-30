---
title: 'Delete an object with the HTTP API'
description: 'Document the complete HTTP contract for this operation, including parameters, representations, examples, and errors.'
weight: 3
diataxis: 'reference'
product: 'OpenRiak KV'
product_version: '3.4.0'
status: 'editorially-rewritten'
draft: true
audience:
  - 'developers'
legacy_3_2_5_sources:
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\developing\api\http\delete-object.md'
source_material:
  - 'legacy-3.2.5'
  - 'live-3.2.5'
  - 'openriak-quickdocs-3.4'
quickdocs_sources:
  - 'https://openriak.github.io/riak/ObjectAPI.html#http-api-definition---delete'
tags: ['diataxis', 'kv', 'reference']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Document the complete HTTP contract for this operation, including parameters, representations, examples, and errors.

## Details

### HTTP Delete Object

Deletes an object from the specified bucket / key.

#### Request

```
DELETE /types/type/buckets/bucket/keys/key
DELETE /buckets/bucket/keys/key
```

Optional query parameters:

* `rw` - quorum for both operations (get and put) involved in deleting an
object (default is set at the bucket level)
* `r` - (read quorum) how many replicas need to agree when retrieving the object
* `pr` - (primary read quorum) works like `r` but requires that the nodes
read from are not fallback nodes
* `w` - (write quorum) how many replicas must confirm receiving writes before returning a successful response
* `dw` - (durable write quorum) how many replicas to commit to durable storage
before returning a successful response
* `pw` - (primary write quorum) how many replicas to commit to primary nodes
before returning a successful response

#### Response

Normal response codes:

* `204 No Content`
* `404 Not Found`

Typical error codes:

* `400 Bad Request` - e.g. when rw parameter is invalid (> N)

`404` responses are "normal" in the sense that DELETE operations are idempotent
and not finding the resource has the same effect as deleting it.

#### Example

```curl
$ curl -v -X DELETE http://127.0.0.1:8098/buckets/test/keys/test2
* About to connect() to 127.0.0.1 port 8098 (#0)
*   Trying 127.0.0.1... connected
* Connected to 127.0.0.1 (127.0.0.1) port 8098 (#0)
> DELETE /buckets/test/keys/test2 HTTP/1.1
> User-Agent: curl/7.19.4 (universal-apple-darwin10.0) libcurl/7.19.4 OpenSSL/0.9.8l zlib/1.2.3
> Host: 127.0.0.1:8098
> Accept: */*
>
< HTTP/1.1 204 No Content
< Vary: Accept-Encoding
< Server: MochiWeb/1.1 WebMachine/1.9.0 (participate in the frantic)
< Date: Fri, 30 Sep 2011 15:24:35 GMT
< Content-Type: application/json
< Content-Length: 0
<
* Connection #0 to host 127.0.0.1 left intact
* Closing connection #0
```

#### HTTP API Definition - Delete

Delete requests should be sent using the DELETE method.  As with PUT requests, DELETE requests should include the `x-riak-vclock` header with the value of the entry that was read.

Without providing version information, the delete will first read the current version of the object, and then attempt to delete the object using that discovered version information.  This may not be the same version of the object that prompted the delete request.  DELETE with no `x-riak-vclock` is "delete regardless", whereas with a `x-riak-vclock` it is a request to delete only the object at that version.

Supported HTTP request headers for DELETE:

- `x-riak-vclock`; see above.
- `x-riak-if-not-modified`; optional, for conditional requests.
- `if-none-match: *`; optional, for conditional requests.
- `authorization`; optional, for tls-protected requests only when Riak security is enabled.
