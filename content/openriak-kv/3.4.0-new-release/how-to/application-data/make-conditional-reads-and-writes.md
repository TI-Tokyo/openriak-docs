---
title: Make conditional reads and writes
description: Use conditional requests when an operation should depend on the version the client observed or on a
  key being absent. Conditions reduce unwanted overwrites but do not make ordinary objects a general transaction
  system.
weight: 450
diataxis: how-to
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- developers
source_material:
- source-code-release-notes-3.4
- openriak-quickdocs-3.4
quickdocs_sources:
- https://openriak.github.io/riak/ObjectAPI.html#conditional-requests
- https://openriak.github.io/riak/ObjectAPI.html#use-of-request-header---if-none-match
- https://openriak.github.io/riak/ObjectAPI.html#use-of-request-header---x-riak-if-not-modified-non-standard-riak-header
tags:
- diataxis
- kv
- how-to
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- how-to/develop/send-conditional-object-request.md
related:
- tutorials/data-and-concurrency/practise-conditional-updates
- how-to/application-data/coordinate-an-update-with-a-latch-object
- reference/http-api/conditional-requests-and-latch-objects
- foundations/data-and-consistency/conditional-updates-and-latch-objects
---

Use conditional requests when an operation should depend on the version the client observed or on a key being absent. Conditions reduce unwanted overwrites but do not make ordinary objects a general transaction system.

## Read conditionally

Keep the ETag from a successful read and send `If-None-Match` on a later GET when the client already has that representation. Handle `304` without trying to decode a new object body.

## Create or update conditionally

Use `If-None-Match: *` for a create-if-absent HTTP request. For an update based on a fetched version, retain its causal context and use the conditional form documented in [Conditional requests and latch objects]({{< product-version-root >}}reference/http-api/conditional-requests-and-latch-objects/). Select the bucket's token/condition policy according to the required behaviour during failure and ownership changes; inspect the settings in [Bucket properties and defaults]({{< product-version-root >}}reference/configuration/bucket-properties-and-defaults/).

```sh
curl -i -X PUT "$RIAK_HTTP/buckets/conditional-demo/keys/new" -H 'If-None-Match: *' -H 'Content-Type: text/plain' --data-binary 'created once'
```

Run the create twice with a fresh test key. The second attempt should fail its condition rather than overwrite the first value.

## Handle failure explicitly

Distinguish a rejected condition from an unavailable replica or an uncertain timeout. Refetch and reconsider the operation after a condition failure. Do not blindly retry a stale update or treat a timeout as proof that nothing was written. Use [Practise conditional updates]({{< product-version-root >}}tutorials/data-and-concurrency/practise-conditional-updates/) to rehearse the success and failure paths.
