---
title: Cluster, client, and replication compatibility
description: Compatibility must be checked for the exact source and target releases, their Erlang/OTP builds, backend
  formats, and enabled features. Client protocol compatibility alone does not establish cluster upgrade compatibility
weight: 30
diataxis: reference
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- architects
- operators
- developers
source_material:
- source-code-release-notes-3.4
- openriak-discussions
- live-3.2.5
tags:
- diataxis
- kv
- reference
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- reference/releases/version-compatibility.md
related:
- reference/orientation-and-compatibility/platforms-architectures-and-erlang-otp-compatibility
- reference/orientation-and-compatibility/replication-generation-compatibility
- reference/client-libraries/client-compatibility-and-capability-matrix
- how-to/cluster-lifecycle/upgrade-a-cluster
- how-to/cluster-lifecycle/roll-back-a-compatible-cluster-upgrade
- foundations/overview/what-openriak-kv-is
- foundations/replication-and-repair/replication-generations-and-compatibility
- foundations/storage-and-performance/storage-backend-trade-offs
---

Compatibility must be checked for the exact source and target releases, their Erlang/OTP builds, backend formats, and enabled features. Client protocol compatibility alone does not establish cluster upgrade compatibility.

## Cluster and runtime

The previously documented staged family route is 2.2.3 → 2.2.5 → 2.9.x → 3.0.x → 3.2.x → 3.4.x. It is historical guidance, not a validation of every patch, runtime, compression setting, or direct skip between those families.

In particular, Erlang distribution compatibility can prevent nodes built with widely separated OTP releases from participating in one rolling transition. Check the runtime listed with each package and rehearse the exact route with representative data.

## Clients

Use the HTTP or Protocol Buffers contract for the operations the application needs. A library that performs object reads and writes may lack newer data types, conditional operations, or Query API support. Client packages and their runtimes need independent validation.

## Replication and rollback

Next-generation replication and legacy v2/v3 interfaces have distinct compatibility boundaries. A newer binary, persisted format, or activated feature can constrain rollback. Use the upgrade and rollback procedures to record those decisions before changing the cluster.
