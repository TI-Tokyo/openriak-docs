---
title: Custom code and hook interfaces
description: Custom Erlang code must match the release's OTP, object representations, and callback contracts. Code
  installation and hook registration are separate from ordinary object writes.
weight: 1230
diataxis: reference
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- operators
legacy_3_2_5_sources:
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\using\reference\custom-code.md
source_material:
- legacy-3.2.5
- live-3.2.5
- proposed-kv
- openriak-quickdocs-3.4
quickdocs_sources:
- https://openriak.github.io/riak/ObjectAPI.html#commit-hooks
tags:
- diataxis
- kv
- reference
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- reference/operations/custom-code.md
related:
- how-to/application-data/install-and-use-a-commit-hook
- how-to/legacy-and-specialist-workflows/implement-a-legacy-replication-hook
- reference/extensions-and-specialist-interfaces/backend-callback-interface
- reference/extensions-and-specialist-interfaces/replication-hook-interface
- reference/configuration/bucket-properties-and-defaults
- foundations/storage-and-performance/storage-backend-trade-offs
---

Custom Erlang code must match the release's OTP, object representations, and callback contracts. Code installation and hook registration are separate from ordinary object writes.

## Code loading

Compile modules for the target runtime and place them in a configured code path available to every node that can invoke them. Verify the loaded module version and avoid replacing a module while incompatible processes are using its old state. Preserve the artifact and source revision with deployment configuration.

## Commit hooks

An Erlang pre-commit hook is called as `Module:Function(Object)`. Return the accepted or transformed `riak_object`, `fail`, or `{fail, Reason}`. Returning an invalid object or raising an exception also rejects the write. Hooks run in list order; the accepted object from one pre-commit hook is passed to the next. An Erlang post-commit hook is called as `Module:Function(Object)` after the write has succeeded. Its return value does not transform the stored object or roll back the write. `fail`, `{fail, Reason}`, and exceptions are recorded as hook failures. Do not recursively update the same key without a guard. Hook lists use module/function entries in the bucket policy; their names and defaults are in [Bucket properties and defaults]({{< product-version-root >}}reference/configuration/bucket-properties-and-defaults/).

Hooks execute in the request path and can affect latency or availability. External notifications need an application strategy for retries and duplicate effects; hook invocation is not a general exactly-once transaction with another system.

An Erlang hook entry uses this JSON form (example module and function names):

```json
{"mod":"customer_validation","fun":"validate"}
```

Place the entry in the `precommit` or `postcommit` array. The callback handling is defined in the release's `riak_kv_put_fsm` module.

## Other extension interfaces

Legacy replication helper callbacks use [Replication hook interface]({{< product-version-root >}}reference/extensions-and-specialist-interfaces/replication-hook-interface/). Backend implementations use [Backend callback interface]({{< product-version-root >}}reference/extensions-and-specialist-interfaces/backend-callback-interface/). These contracts are separate and must not be inferred from a similarly named command-line function.
