---
title: SNMP objects and integration contract
description: SNMP integration exposes selected runtime and database counters through the installed MIB and agent
  configuration. It is a specialist monitoring interface; metric availability depends on the packaged components
  and confi
weight: 1100
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
- proposed-kv
legacy_3_2_5_sources:
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\using\reference\snmp.md
tags:
- diataxis
- kv
- reference
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- reference/operations/snmp.md
related:
- how-to/monitoring-and-diagnostics/perform-routine-cluster-health-checks
- reference/http-api/status-and-statistics
- reference/operations-and-observability/node-and-cluster-metrics
- how-to/security/restrict-client-node-and-administrative-network-access
- foundations/storage-and-performance/latency-queues-and-resource-contention
- foundations/cluster-lifecycle/failure-and-recovery
---

SNMP integration exposes selected runtime and database counters through the installed MIB and agent configuration. It is a specialist monitoring interface; metric availability depends on the packaged components and configuration.

## Contract

Use the MIB shipped with the selected release as the authority for object identifiers, types, and access modes. Preserve the node identity and collection timestamp. Counters can reset on restart, and a gauge must not be interpreted as a cumulative counter.

## Configuration and scope

The current settings metadata does not publish configuration entries for this integration. Use the installed component’s own version-matched contract before enabling it; no deployment defaults are implied here.

Restrict the management listener to the monitoring network and configure its authentication/access model deliberately. Verify an actual walk against a known node and compare selected values with the HTTP statistics endpoint before depending on the integration.
