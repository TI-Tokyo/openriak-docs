---
title: HTTP conventions, authentication, and errors
description: The HTTP API addresses resources under the configured HTTP or HTTPS listener. Examples use `RIAK_HTTP`
  for that base URL; replace it with the deployment's actual endpoint.
weight: 410
diataxis: reference
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- developers
migration_source_root: \\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv
migration_sources:
- \\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv\apis-and-clients\APIs\http-https\http-https.md
legacy_3_2_5_sources:
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\developing\api\http.md
source_material:
- legacy-3.2.5
- openriak-quickdocs-3.4
- live-3.2.5
- proposed-kv
quickdocs_sources:
- https://openriak.github.io/riak/ObjectAPI.html#object-identifier---the-url
- https://openriak.github.io/riak/ObjectAPI.html#riak-kv---object-api
tags:
- diataxis
- kv
- reference
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- reference/http-api/_index.md
related:
- reference/http-api/fetch-object
- reference/http-api/store-object
- reference/http-api/delete-object
- reference/http-api/conditional-requests-and-latch-objects
- reference/http-api/distributed-data-type-operations
- reference/query-api/endpoints-and-request-schema
- how-to/security/authenticate-an-application-client
- foundations/data-and-consistency/objects-keys-and-buckets
- foundations/data-and-consistency/quorums-availability-and-durability
---

The HTTP API addresses resources under the configured HTTP or HTTPS listener. Examples use `RIAK_HTTP` for that base URL; replace it with the deployment's actual endpoint.

## Requests

Encode type, bucket, key, and index terms as separate URL components. Set the body media type explicitly and preserve opaque context and continuation values. Use HTTPS and the configured credentials when security is enabled. A proxy must preserve request headers and response status semantics.

## Common outcomes

Successful status depends on the operation: fetches return content, stores may return a body or an empty acknowledgement, and deletes acknowledge removal. `300` can represent siblings; `304` is a conditional-read result; `404` represents a missing resource for the request; `412` is a failed precondition. Authentication, validation, and availability failures require separate handling.

## Retry and consistency limits

A timed-out write may already have taken effect. Retry according to the application's idempotency and context rules, not solely the HTTP transport error. Requests across keys do not form a transaction, and a query followed by object fetches need not see one snapshot.

## Interfaces

Use the object, bucket, datatype, and secondary-index pages in this section for exact endpoints. The current Query API and AAE fold API have their own reference sections. Legacy listing, counters, link walking, and MapReduce are labelled separately.
