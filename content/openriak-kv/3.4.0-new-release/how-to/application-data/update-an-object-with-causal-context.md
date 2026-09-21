---
title: Update an object with causal context
description: Update a fetched object while preserving its causal context. Sending an ordinary replacement without
  the context can create a concurrent version.
weight: 410
diataxis: how-to
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- developers
legacy_3_2_5_sources:
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\developing\usage\updating-objects.md
source_material:
- legacy-3.2.5
- live-3.2.5
- proposed-kv
- openriak-quickdocs-3.4
quickdocs_sources:
- https://openriak.github.io/riak/ObjectAPI.html#example-put-request
- https://openriak.github.io/riak/ObjectAPI.html#http-api-definition---store
tags:
- diataxis
- kv
- how-to
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- how-to/develop/update-object.md
related:
- how-to/application-data/read-an-object-and-handle-missing-values
- how-to/application-data/resolve-concurrent-object-updates
- how-to/application-data/make-conditional-reads-and-writes
- reference/data-model-contracts/causal-context-and-version-vector-representations
- foundations/data-and-consistency/objects-keys-and-buckets
- foundations/data-and-consistency/bucket-types-and-data-policies
- foundations/data-and-consistency/causality-version-vectors-and-siblings
---

Update a fetched object while preserving its causal context. Sending an ordinary replacement without the context can create a concurrent version.

## Fetch the current value

```sh
curl --fail -D object.headers -o object.json "$RIAK_HTTP/buckets/customers/keys/aiko"
VCLOCK=$(awk 'tolower($1)=="x-riak-vclock:" {gsub("\r", "", $2); print $2}' object.headers)
test -n "$VCLOCK"
```

Handle siblings before proceeding. Keep the context opaque; do not decode or construct a replacement vector clock in application code.

## Send the changed value

```sh
curl --fail -i -X PUT "$RIAK_HTTP/buckets/customers/keys/aiko" -H "X-Riak-Vclock: $VCLOCK" -H 'Content-Type: application/json' --data-binary '{"name":"Aiko","city":"Osaka"}'
```

Preserve indexes and other metadata the application still needs; a replacement object must carry the intended metadata, not only its new body.

## Verify and handle races

Read the object again and check its body, metadata, and context. Another writer may have updated it concurrently, so retain the application's sibling-resolution path. Use [Make conditional reads and writes]({{< product-version-root >}}how-to/application-data/make-conditional-reads-and-writes/) when the operation should fail if the fetched version has changed, and handle that failure by refetching rather than blindly retrying the old request.
