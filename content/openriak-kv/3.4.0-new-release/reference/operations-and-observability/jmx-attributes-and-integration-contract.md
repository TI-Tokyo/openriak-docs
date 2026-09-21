---
title: JMX attributes and integration contract
description: JMX integration depends on a compatible monitoring bridge; the Erlang node is not itself a Java VM.
  Treat bridge attributes and their mapping to Riak statistics as a separate versioned contract.
weight: 1110
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
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\using\reference\jmx.md
tags:
- diataxis
- kv
- reference
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- reference/operations/jmx.md
related:
- reference/http-api/status-and-statistics
- reference/operations-and-observability/node-and-cluster-metrics
- how-to/monitoring-and-diagnostics/perform-routine-cluster-health-checks
- how-to/security/restrict-client-node-and-administrative-network-access
- foundations/storage-and-performance/latency-queues-and-resource-contention
- foundations/cluster-lifecycle/failure-and-recovery
---

JMX integration depends on a compatible monitoring bridge; the Erlang node is not itself a Java VM. Treat bridge attributes and their mapping to Riak statistics as a separate versioned contract.

## Attribute mapping

Record the bridge version, exposed object names, attribute types, polling interval, and underlying Riak statistic for each dashboard or alert. Distinguish counters, gauges, and latency observations, and account for restart resets.

## Compatibility boundary

The presence of an old JMX integration guide does not establish that its Java bridge is packaged or validated for this release. Verify the deployed bridge and compare its values with `/stats` on the same node and interval. Use the direct statistics interface when no compatible bridge has been established.

Restrict remote management access and test authentication independently from Riak's client API credentials.
