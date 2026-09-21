---
title: Store and retrieve different content types
description: Store values with a content type that tells clients how to interpret their bytes. OpenRiak stores the
  value; the application remains responsible for serialization and validation.
weight: 430
diataxis: how-to
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- developers
source_material:
- legacy-3.2.5
- live-3.2.5
- proposed-kv
legacy_3_2_5_sources:
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\developing\usage\content-types.md
tags:
- diataxis
- kv
- how-to
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- how-to/develop/use-content-types.md
related:
- how-to/application-data/create-and-store-an-object
- how-to/application-data/update-an-object-with-causal-context
- reference/data-model-contracts/media-types-and-content-encodings
- reference/data-model-contracts/object-metadata
- foundations/data-and-consistency/objects-keys-and-buckets
- foundations/data-and-consistency/bucket-types-and-data-policies
- foundations/data-and-consistency/causality-version-vectors-and-siblings
---

Store values with a content type that tells clients how to interpret their bytes. OpenRiak stores the value; the application remains responsible for serialization and validation.

## Send the intended bytes

For a binary file:

```sh
curl --fail -i -X PUT "$RIAK_HTTP/buckets/files/keys/sample" -H 'Content-Type: application/octet-stream' --data-binary @sample.bin
curl --fail -D sample.headers -o retrieved.bin "$RIAK_HTTP/buckets/files/keys/sample"
cmp sample.bin retrieved.bin
```

Use `--data-binary` so curl preserves file bytes. Use `application/json` for JSON or a more specific registered media type when appropriate. Set a content encoding only when the body actually uses that encoding.

## Verify client behaviour

Check the returned content type and byte equality. Test how the client handles unknown media types, malformed application data, and compressed values. On updates, preserve causal context and metadata as in [Update an object with causal context]({{< product-version-root >}}how-to/application-data/update-an-object-with-causal-context/). Avoid converting arbitrary binary values through a text encoding.
