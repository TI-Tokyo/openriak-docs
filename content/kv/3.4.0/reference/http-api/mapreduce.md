---
title: 'Run MapReduce with the HTTP API'
description: 'Document the complete HTTP contract for this operation, including parameters, representations, examples, and errors.'
weight: 10
diataxis: 'reference'
product: 'OpenRiak KV'
product_version: '3.4.0'
status: 'editorially-rewritten'
draft: true
audience:
  - 'developers'
legacy_3_2_5_sources:
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\developing\api\http\mapreduce.md'
source_material:
  - 'legacy-3.2.5'
  - 'live-3.2.5'
  - 'openriak-quickdocs-3.4'
quickdocs_sources:
  - 'https://openriak.github.io/riak/OtherAPI.html#the-mapreduce-api'
tags: ['diataxis', 'kv', 'reference']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Document the complete HTTP contract for this operation, including parameters, representations, examples, and errors.

## Details

### HTTP MapReduce

[MapReduce]({{< baseurl >}}kv/3.4.0/how-to/develop/run-mapreduce/) is a generic way to query Riak by specifying inputs and constructing a set of map, reduce, and link phases through which data will flow.

#### Request

```bash
POST /mapred
```

Important headers:
* `Content-Type` - must always be `application/json`.  The format of the request body is described in detail on the [MapReduce]({{< baseurl >}}kv/3.4.0/how-to/develop/run-mapreduce/) page.

Optional query parameters:
* `chunked` - when set to `true`, results will be returned as they are received in `multipart/mixed` format using chunked-encoding.

_+This request must include an entity (body), which is the JSON form of the MapReduce query.+_

#### Response

Normal status codes:
* `200 OK`

Typical error codes:
* `400 Bad Request` - if an invalid job is submitted.
* `500 Internal Server Error` - if there was an error in processing a map or reduce function
* `503 Service Unavailable` - if the job timed out before it could complete

Important headers:
* `Content-Type` - `application/json` when `chunked` is not true, otherwise `multipart/mixed` with `application/json` sections.

#### Example

```curl
$ curl -v -d '{"inputs":"test", "query":[{"link":{"bucket":"test"}},{"map":{"language":"javascript","name":"Riak.mapValuesJson"}}]}' -H "Content-Type: application/json" http://127.0.0.1:8098/mapred
* About to connect() to 127.0.0.1 port 8098 (#0)
*   Trying 127.0.0.1... connected
* Connected to 127.0.0.1 (127.0.0.1) port 8098 (#0)
> POST /mapred HTTP/1.1
> User-Agent: curl/7.19.4 (universal-apple-darwin10.0) libcurl/7.19.4 OpenSSL/0.9.8l zlib/1.2.3
> Host: 127.0.0.1:8098
> Accept: */*
> Content-Type: application/json
> Content-Length: 117
>
< HTTP/1.1 200 OK
< Server: MochiWeb/1.1 WebMachine/1.9.0 (participate in the frantic)
< Date: Fri, 30 Sep 2011 15:24:35 GMT
< Content-Type: application/json
< Content-Length: 30
<
* Connection #0 to host 127.0.0.1 left intact
* Closing connection #0
[{"foo":"bar"},{"riak":"CAP"}]
```

#### The Map/Reduce API

The use of Map/Reduce API is deprecated in Riak 3.4, and the API will be retired in Riak 4.0.

For using Map/Reduce with Erlang functions, the API is unchanged since Riak 2.2.3, so refer to the [legacy documentation](https://docs.riak.com/riak/kv/2.2.3/developing/app-guide/advanced-mapreduce/index.html) for further information.  The Map/Reduce API no longer supports JavaScript functions.

> For querying data the [Query API]({{< baseurl >}}kv/3.4.0/tutorials/query-api/) should be used in preference to the Map/Reduce API.  The Query API is under active development to expand the number of Map/Reduce use cases it covers, in particular the ability to prompt the fetching of multiple objects.
