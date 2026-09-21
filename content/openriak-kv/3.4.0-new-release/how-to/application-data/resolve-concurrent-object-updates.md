---
title: Resolve concurrent object updates
description: Resolve concurrent versions using an application rule, then write the merged value with the combined
  causal context. Do not discard siblings merely to obtain a single convenient response.
weight: 440
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
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\developing\usage\conflict-resolution.md
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\developing\usage\conflict-resolution\csharp.md
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\developing\usage\conflict-resolution\golang.md
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\developing\usage\conflict-resolution\java.md
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\developing\usage\conflict-resolution\nodejs.md
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\developing\usage\conflict-resolution\php.md
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\developing\usage\conflict-resolution\python.md
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\developing\usage\conflict-resolution\ruby.md
tags:
- diataxis
- kv
- how-to
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- how-to/develop/resolve-conflicts.md
related:
- tutorials/data-and-concurrency/create-and-resolve-concurrent-updates
- how-to/application-data/update-an-object-with-causal-context
- reference/http-api/fetch-object
- foundations/data-and-consistency/causality-version-vectors-and-siblings
- foundations/data-and-consistency/resolving-concurrent-updates
---

Resolve concurrent versions using an application rule, then write the merged value with the combined causal context. Do not discard siblings merely to obtain a single convenient response.

## Fetch every version

For HTTP, request `Accept: multipart/mixed` when a read reports siblings. Parse each part's content type, value, and metadata, and retain the context supplied for the sibling set. A client library may expose the siblings directly.

## Apply the application's merge rule

Merge values according to their meaning: preserve independent changes, combine collections where valid, or request user intervention for incompatible edits. A wall-clock timestamp alone is not a safe general conflict rule. See [Resolving concurrent updates]({{< product-version-root >}}foundations/data-and-consistency/resolving-concurrent-updates/) for the choices.

## Write and verify

Send the resolved value with the context from the complete read, preserving required indexes and metadata. Read again and confirm that the resulting value matches the merge. Another concurrent update may create new siblings, so the resolution path must be repeatable and must not assume one attempt always finishes.

Exercise the procedure with two clients updating from the same starting context before deploying it. [Create and resolve concurrent updates]({{< product-version-root >}}tutorials/data-and-concurrency/create-and-resolve-concurrent-updates/) provides a small reproducible HTTP example.
