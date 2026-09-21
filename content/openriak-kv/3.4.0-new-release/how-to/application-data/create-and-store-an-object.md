---
title: Create and store an object
description: Create an object at an application-selected key and check the result. Set `RIAK_HTTP` to your endpoint
  and include the required authentication and TLS options.
weight: 390
diataxis: how-to
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- developers
legacy_3_2_5_sources:
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\developing\usage\creating-objects.md
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
- how-to/develop/create-object.md
related:
- how-to/application-data/read-an-object-and-handle-missing-values
- how-to/application-data/update-an-object-with-causal-context
- how-to/application-data/resolve-concurrent-object-updates
- how-to/application-data/make-conditional-reads-and-writes
- reference/http-api/store-object
- foundations/data-and-consistency/objects-keys-and-buckets
- foundations/data-and-consistency/bucket-types-and-data-policies
- foundations/data-and-consistency/causality-version-vectors-and-siblings
---

Create an object at an application-selected key and check the result. Set `RIAK_HTTP` to your endpoint and include the required authentication and TLS options.

## Choose the address and value

Select the active bucket type, bucket, and key. This example uses the untyped `customers` bucket and the key `aiko`; use a unique test key when trying it against a shared environment.

```sh
curl --fail -i -X PUT "$RIAK_HTTP/buckets/customers/keys/aiko" -H 'Content-Type: application/json' --data-binary '{"name":"Aiko","city":"Tokyo"}'
```

A normal successful PUT without a returned body gives `204`. For a typed bucket, insert `/types/TYPE` before `/buckets`. To require creation only when no value exists, use [Make conditional reads and writes]({{< product-version-root >}}how-to/application-data/make-conditional-reads-and-writes/) instead of treating an ordinary PUT as a create-only operation.

## Verify and preserve context

```sh
curl --fail -D object.headers -o object.json "$RIAK_HTTP/buckets/customers/keys/aiko"
cat object.json
```

Check the value and content type. Save the returned causal context for later updates. If you receive siblings, resolve them rather than selecting an arbitrary response body. A timeout can leave the write outcome uncertain; read and reconcile before retrying a non-idempotent application operation.
