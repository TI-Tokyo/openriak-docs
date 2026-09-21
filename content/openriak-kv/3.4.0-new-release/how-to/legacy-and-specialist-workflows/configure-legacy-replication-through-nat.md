---
title: Configure legacy replication through NAT
description: Configure address translation for an existing legacy replication relationship when peers cannot reach
  the addresses advertised inside the source network.
weight: 1410
diataxis: how-to
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- operators
source_material:
- legacy-3.2.5
- live-3.2.5
- proposed-kv
legacy_3_2_5_sources:
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\configuring\v2-multi-datacenter\nat.md
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\configuring\v3-multi-datacenter\nat.md
- Legacy multi-datacenter replication terminology and commands require compatibility review.
tags:
- diataxis
- kv
- how-to
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- how-to/configure/replication/configure-replication-through-nat.md
related:
- how-to/legacy-and-specialist-workflows/maintain-legacy-v2-replication
- how-to/legacy-and-specialist-workflows/maintain-legacy-v3-replication
- how-to/legacy-and-specialist-workflows/secure-legacy-replication-connections
- reference/legacy-and-experimental-features/legacy-aae-and-riak-repl-settings
- reference/orientation-and-compatibility/replication-generation-compatibility
- foundations/replication-and-repair/replication-generations-and-compatibility
- foundations/storage-and-performance/storage-backend-trade-offs
---

Configure address translation for an existing legacy replication relationship when peers cannot reach the addresses advertised inside the source network.

## Map every endpoint

Record internal listener addresses, externally reachable addresses, translated ports, and the direction of each connection. Include cluster-manager discovery and data connections, not only the first bootstrap address. Confirm which legacy replication generation is in use.

## Apply the generation-specific mapping

Use the NAT-related settings and runtime controls in [Legacy AAE and riak_repl settings]({{< product-version-root >}}reference/legacy-and-experimental-features/legacy-aae-and-riak-repl-settings/) and [Legacy riak_repl runtime controls]({{< product-version-root >}}reference/replication-interfaces/legacy-riak-repl-runtime-controls/) for that generation. Configure stable one-to-one mappings where required and apply them consistently to the nodes that advertise peer addresses. Do not reuse these legacy mappings as current-generation `replrtq_sinkpeers` configuration.

## Verify discovery and reconnects

Test from the actual remote network. Confirm initial connection, discovery of all required peers, and reconnection after one peer restarts. Write a sample and observe completed fullsync. If bootstrap succeeds but replication stalls, inspect the later advertised addresses and firewall rules before changing timeouts.
