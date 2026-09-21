---
title: Implement a legacy replication hook
description: Implement a callback that filters or supplements objects on an existing legacy `riak_repl` path. These
  hooks do not configure current-generation replication.
weight: 1430
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
migration_source_root: \\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv
migration_sources:
- \\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv\apis-and-clients\APIs\multi-dc-repl.md
legacy_3_2_5_sources:
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\developing\api\repl-hooks.md
tags:
- diataxis
- kv
- how-to
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- how-to/develop/write-replication-hook.md
related:
- reference/extensions-and-specialist-interfaces/replication-hook-interface
- reference/extensions-and-specialist-interfaces/custom-code-and-hook-interfaces
- how-to/legacy-and-specialist-workflows/maintain-legacy-v3-replication
- how-to/application-data/install-and-use-a-commit-hook
- foundations/replication-and-repair/replication-generations-and-compatibility
- foundations/storage-and-performance/storage-backend-trade-offs
---

Implement a callback that filters or supplements objects on an existing legacy `riak_repl` path. These hooks do not configure current-generation replication.

## Implement the contract

Use the callback signatures and return values in [Replication hook interface]({{< product-version-root >}}reference/extensions-and-specialist-interfaces/replication-hook-interface/). Keep the callbacks bounded and avoid recursive writes or blocking external dependencies. Test `ok`, `cancel`, and any additional-object return path separately; filtering can intentionally leave clusters with different data.

## Register and distribute

Compile the module for the target OTP and deploy it to every node that may execute the hook. Register it as a `repl_helper` through the extension registration interface in [Custom code and hook interfaces]({{< product-version-root >}}reference/extensions-and-specialist-interfaces/custom-code-and-hook-interfaces/), and verify that the expected module is loaded before enabling the relationship.

## Test real-time and fullsync paths

Send allowed and blocked sample objects and verify both real-time delivery and a later fullsync. For an additional-object list, confirm the dependency objects arrive before the original object. Test callback errors in an isolated cluster and verify monitoring makes failures visible.

Remove the hook registration before removing its code during rollback. Reconcile or explicitly account for objects previously filtered out.
