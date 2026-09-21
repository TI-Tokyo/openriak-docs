---
title: Node identity, directories, and ring settings
description: Node settings define identity, storage paths, initial ring size, and placement. Set cluster identity
  and ring choices before forming a new cluster.
weight: 90
diataxis: reference
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- operators
source_material:
- live-3.2.5
- proposed-kv
tags:
- diataxis
- kv
- reference
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- reference/configuration/node.md
related:
- how-to/node-configuration/configure-node-identity-directories-and-the-initial-ring
- foundations/data-and-consistency/bucket-types-and-data-policies
---

Node settings define identity, storage paths, initial ring size, and placement. Set cluster identity and ring choices before forming a new cluster.

## Settings

Select an operating system, then search by setting name or description. Values shown are the defaults from that release’s settings metadata; explicit configuration overrides take precedence.

{{< configuration-reference-table >}}
^(nodename|distributed_cookie|platform_.*|ring.*|target_.*|choose_claim_fun|prevent_overlapping_partitions|full_rebalance_onleave|storage_backend)$
{{< /configuration-reference-table >}}
