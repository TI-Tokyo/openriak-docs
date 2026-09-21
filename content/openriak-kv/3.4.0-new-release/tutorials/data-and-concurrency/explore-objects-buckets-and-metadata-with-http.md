---
title: Explore objects, buckets, and metadata with HTTP
weight: 140
product: OpenRiak KV
product_version: 3.4.0
diataxis: tutorial
draft: true
status: editorially-rewritten
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
description: Store a JSON object, inspect its metadata, update it with the context returned by a read, and delete
  it. Start with the Docker learning cluster running.
related:
- tutorials/first-cluster/build-and-explore-a-docker-cluster
- tutorials/data-and-concurrency/apply-different-policies-with-bucket-types
- reference/http-api/fetch-object
- reference/http-api/store-object
- foundations/data-and-consistency/objects-keys-and-buckets
- foundations/data-and-consistency/causality-version-vectors-and-siblings
- foundations/data-and-consistency/conflict-free-replicated-data-types
next_page: tutorials/data-and-concurrency/apply-different-policies-with-bucket-types
previous_page: tutorials/first-cluster/build-and-explore-a-docker-cluster
---

Store a JSON object, inspect its metadata, update it with the context returned by a read, and delete it. Start with the Docker learning cluster running.

## Choose the endpoint

In a terminal on the Docker host, set the example endpoint:

```sh
export RIAK_HTTP=http://127.0.0.1:18098
```

## Store and inspect a profile

```sh
curl --fail -i -X PUT "$RIAK_HTTP/buckets/learning/keys/person-1"   -H 'Content-Type: application/json'   -H 'X-Riak-Meta-Lesson: objects'   --data-binary '{"name":"Aiko","city":"Tokyo"}'
curl --fail -D person.headers -o person.json   "$RIAK_HTTP/buckets/learning/keys/person-1"
cat person.json
cat person.headers
```

The body contains Aiko's profile. The headers include the media type, your lesson metadata, and the object's causal context in `X-Riak-Vclock`. Header names are case-insensitive.

## Update with the returned context

```sh
context=$(awk 'tolower($1)=="x-riak-vclock:" {gsub("\r", "", $2); print $2}' person.headers)
test -n "$context"
curl --fail -i -X PUT "$RIAK_HTTP/buckets/learning/keys/person-1"   -H 'Content-Type: application/json' -H "X-Riak-Vclock: $context"   --data-binary '{"name":"Aiko","city":"Osaka"}'
curl --fail "$RIAK_HTTP/buckets/learning/keys/person-1"
```

Check that the city is now Osaka. Supplying the context identifies the version you updated; the concurrency lesson explores what happens with competing writers.

## Delete and check

```sh
curl --fail -i -X DELETE "$RIAK_HTTP/buckets/learning/keys/person-1"
curl -i "$RIAK_HTTP/buckets/learning/keys/person-1"
```

The final request should report a missing object. The missing-object check intentionally omits `--fail` so you can inspect its error response. Remove `person.headers` and `person.json` when finished.
