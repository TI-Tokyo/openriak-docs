---
title: 'Capability negotiation'
description: 'Explain capability negotiation and why it matters when designing or operating OpenRiak systems.'
weight: 3
diataxis: 'explanation'
product: 'OpenRiak KV'
product_version: '3.4.0'
status: 'editorially-rewritten'
draft: true
audience:
  - 'architects'
  - 'operators'
  - 'developers'
source_material:
  - 'legacy-3.2.5'
  - 'live-3.2.5'
legacy_3_2_5_sources:
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\learn\concepts\capability-negotiation.md'
tags: ['diataxis', 'kv', 'explanation']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Explain capability negotiation and why it matters when designing or operating OpenRiak systems.

## Overview

### Capability Negotiation

[glossary vnode]: {{< product-version-root >}}explanation/foundations/glossary/#vnode
[upgrade cluster]: {{< product-version-root >}}how-to/operate/upgrade-cluster/
[usage mapreduce]: {{< product-version-root >}}how-to/develop/run-mapreduce/

In early versions of OpenRiak KV, [rolling upgrades][upgrade cluster] from an older version to a newer involved (a) disabling all new features associated with the newer version, and then (b) re-enabling those features once all nodes in the cluster were upgraded.

Rolling upgrades no longer require you to disable and then re-enable features due to the *capability negotiation* subsystem that automatically manages the addition of new features. Using this subsystem, nodes negotiate with each other to automatically determine which versions are supported on which nodes, which allows clusters to maintain normal operations even when divergent versions of OpenRiak KV are present in the cluster.

**Note on Mixed Versions**
The capability negotiation subsystem is used to manage mixed versions of OpenRiak KV within a cluster ONLY during rolling upgrades. We strongly recommend not running mixed versions during normal operations.
