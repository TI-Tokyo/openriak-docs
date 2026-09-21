---
title: Upgrade an OpenRiak KV cluster
description: Upgrade an existing cluster in a rehearsed rolling sequence, preserving data and configuration on every
  member. Read the exact source and target release notes before selecting a package.
weight: 790
diataxis: how-to
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- operators
migration_source_root: \\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv
migration_sources:
- \\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv\admin\upgrade\upgrade-checklist.md
- \\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv\admin\upgrade\upgrading.md
legacy_3_2_5_sources:
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\setup\upgrading.md
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\setup\upgrading\checklist.md
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\setup\upgrading\cluster.md
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\setup\upgrading\multi-datacenter.md
- Package, platform, installation, upgrade, or downgrade details require release-specific verification for OpenRiak
  KV 3.4.0.
source_material:
- legacy-3.2.5
- live-3.2.5
- proposed-kv
- openriak-quickdocs-3.4
quickdocs_sources:
- https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#upgrading-a-node
tags:
- diataxis
- kv
- how-to
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- how-to/operate/upgrade-cluster.md
related:
- how-to/cluster-lifecycle/perform-a-rolling-restart
- how-to/cluster-lifecycle/roll-back-a-compatible-cluster-upgrade
- how-to/installation/verify-an-installation
- reference/orientation-and-compatibility/platforms-architectures-and-erlang-otp-compatibility
- reference/orientation-and-compatibility/cluster-client-and-replication-compatibility
- reference/orientation-and-compatibility/feature-status-and-deprecations
- foundations/cluster-lifecycle/mixed-versions-capabilities-and-upgrade-boundaries
---

Upgrade an existing cluster in a rehearsed rolling sequence, preserving data and configuration on every member. Read the exact source and target release notes before selecting a package.

## Check compatibility

Confirm the supported upgrade path, OTP version, backend formats, client compatibility, and replication relationships in [Cluster, client, and replication compatibility]({{< product-version-root >}}reference/orientation-and-compatibility/cluster-client-and-replication-compatibility/). Inventory deprecated features and custom Erlang modules. Keep target-only features disabled while older members remain unless compatibility is explicitly documented.

Download the target packages from that version's package catalogue and verify their checksums. Save the installed package versions, effective configuration, and recovery plan. Rehearse the application workload and a pilot-node recovery before production deployment.

## Upgrade a pilot member

Drain one node, stop it gracefully, preserve the required backup, and install the target package without replacing its data or identity. Merge configuration changes deliberately; compare generated settings with the saved values and validate before startup.

## Observe, then continue

Start the node and verify version, membership, transfers, AAE, replication, and representative client operations. Observe a workload cycle appropriate to the change. Continue one member at a time using [Perform a rolling restart]({{< product-version-root >}}how-to/cluster-lifecycle/perform-a-rolling-restart/) only after the pilot and each subsequent member pass.

## Complete the transition

Confirm every node runs the intended release and configuration. Recheck cluster and inter-cluster convergence before enabling new features. Retain the rollback artifacts until the agreed verification period ends; use [Roll back a compatible cluster upgrade]({{< product-version-root >}}how-to/cluster-lifecycle/roll-back-a-compatible-cluster-upgrade/) only when the earlier release can read the resulting state.
