---
title: Practise conditional updates
weight: 170
product: OpenRiak KV
product_version: 3.4.0
diataxis: tutorial
draft: true
status: editorially-rewritten
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
description: Observe a successful conditional creation and a rejected attempt to create the same object again. Use
  the active `docs` type from the previous exercise.
related:
- tutorials/data-and-concurrency/create-and-resolve-concurrent-updates
- tutorials/data-and-concurrency/build-a-shared-counter-and-collection
- how-to/application-data/make-conditional-reads-and-writes
- how-to/application-data/coordinate-an-update-with-a-latch-object
- reference/http-api/conditional-requests-and-latch-objects
- foundations/data-and-consistency/objects-keys-and-buckets
- foundations/data-and-consistency/causality-version-vectors-and-siblings
- foundations/data-and-consistency/conflict-free-replicated-data-types
previous_page: tutorials/data-and-concurrency/create-and-resolve-concurrent-updates
next_page: tutorials/data-and-concurrency/build-a-shared-counter-and-collection
---

Observe a successful conditional creation and a rejected attempt to create the same object again. Use the active `docs` type from the previous exercise.

## Claim a fresh key

```sh
key="claim-$(date +%s)"
url="$RIAK_HTTP/types/docs/buckets/learning/keys/$key"
curl -i -X PUT "$url" -H 'If-None-Match: *'   -H 'Content-Type: text/plain' --data-binary 'worker-a'
curl -i -X PUT "$url" -H 'If-None-Match: *'   -H 'Content-Type: text/plain' --data-binary 'worker-b'
```

The first request succeeds. The second should return `412 Precondition Failed`. These requests intentionally omit `--fail` so both statuses remain visible.

## Inspect the result

```sh
curl --fail "$url"
```

Confirm that the stored value is `worker-a`. Repeat with a new key to check that the rejected response was caused by the existing object, rather than by a malformed request.

## Interpret the boundary

This exercise demonstrates the ordinary precondition path. It does not establish a formal distributed-lock guarantee under partitions, maintenance, or independent writers that omit conditions. Use the conditional-update explanation before building a coordination workflow.

## Cleanup

Delete the claim object. Keep the cluster and bucket type for later exercises.
