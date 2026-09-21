---
title: Diagnostic commands
weight: 320
product: OpenRiak KV
product_version: 3.4.0
diataxis: reference
draft: true
status: editorially-rewritten
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
description: Diagnostic interfaces expose different parts of node and cluster state. A successful health command
  does not by itself verify every replica, backend, or application request.
related:
- how-to/monitoring-and-diagnostics/inspect-node-and-cluster-health
- how-to/monitoring-and-diagnostics/inspect-vnode-and-backend-status
- how-to/monitoring-and-diagnostics/collect-diagnostic-evidence
- reference/operations-and-observability/node-and-cluster-metrics
---

Diagnostic interfaces expose different parts of node and cluster state. A successful health command does not by itself verify every replica, backend, or application request.

## Node and cluster checks

- {{< cli key="shell:riak ping" >}} checks whether the local node responds.
- {{< cli key="shell:riak admin status" >}} reports node statistics and status.
- {{< cli key="shell:riak admin member-status" >}} reports membership.
- {{< cli key="shell:riak admin ring-status" >}} reports ring state.
- {{< cli key="shell:riak admin transfers" >}} reports transfers.
- {{< cli key="shell:riak admin vnode-status" >}} exposes vnode and backend details.
- {{< cli key="shell:riak admin cluster-info" >}} collects diagnostic information.

Use the linked generated entries for arguments and help. Interpret the output together with logs, client responses, and recent membership or configuration changes.
