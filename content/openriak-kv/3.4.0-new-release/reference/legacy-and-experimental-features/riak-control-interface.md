---
title: Riak Control interface
description: Riak Control is a historical web administration interface whose availability depends on the packaged
  application and configuration. Use the current command reference for operational procedures.
weight: 1330
diataxis: reference
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- operators
source_material:
- legacy-3.2.5
- live-3.2.5
legacy_3_2_5_sources:
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\using\admin\riak-control.md
tags:
- diataxis
- kv
- reference
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- reference/commands/riak-control.md
related:
- reference/commands/riak/admin
- how-to/cluster-lifecycle/plan-and-commit-a-membership-change
- how-to/security/restrict-client-node-and-administrative-network-access
- reference/orientation-and-compatibility/feature-status-and-deprecations
- foundations/replication-and-repair/replication-generations-and-compatibility
- foundations/storage-and-performance/storage-backend-trade-offs
---

Riak Control is a historical web administration interface whose availability depends on the packaged application and configuration. Use the current command reference for operational procedures.

## Configuration

The current settings metadata does not publish configuration entries for this integration. Use the installed component’s own version-matched contract before enabling it; no deployment defaults are implied here.

## Access boundary

If enabled, restrict the interface to the administrative network and verify its authentication separately from application permissions. Do not expose an unauthenticated control interface alongside a public client listener.

## Operational limits

A displayed cluster view can lag an active transition. Confirm membership, planned changes, and transfer completion through the metadata-backed administration commands before decommissioning a member. An absent Control application should not be worked around by copying old web assets into a current release.
