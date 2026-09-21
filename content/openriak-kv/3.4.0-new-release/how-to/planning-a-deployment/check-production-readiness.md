---
title: Check production readiness
description: Check a deployment before sending production traffic. Keep the evidence with the release and infrastructure
  configuration so the checks can be repeated after changes.
weight: 110
diataxis: how-to
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- architects
- operators
migration_source_root: \\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv
migration_sources:
- \\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv\setup\plan\Choosing-a-backend\best-practices.md
legacy_3_2_5_sources:
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\setup\planning\best-practices.md
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\setup\planning\future.md
source_material:
- legacy-3.2.5
- live-3.2.5
- proposed-kv
- openriak-quickdocs-3.4
quickdocs_sources:
- https://openriak.github.io/riak/BuildAndScaleClusterGuide.html#choosing-infrastructure
tags:
- diataxis
- kv
- how-to
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- how-to/plan/production-readiness-checklist.md
related:
- how-to/installation/verify-an-installation
- how-to/monitoring-and-diagnostics/perform-routine-cluster-health-checks
- how-to/security/audit-deployment-security
- how-to/performance/benchmark-a-representative-workload
- how-to/cluster-lifecycle/back-up-node-data-and-cluster-metadata
- how-to/troubleshooting/recover-a-failed-node-or-choose-replacement
- foundations/cluster-architecture/replica-placement-and-failure-domains
- foundations/storage-and-performance/storage-backend-trade-offs
- foundations/storage-and-performance/capacity-and-growth
---

Check a deployment before sending production traffic. Keep the evidence with the release and infrastructure configuration so the checks can be repeated after changes.

## Confirm the deployment

- Verify package versions, OTP variants, architecture, and backend on every member.
- Confirm unique stable node identities, compatible ring settings, and the intended membership and ownership plan.
- Check that data directories survive process and host restarts and have sufficient capacity for recovery.
- Restrict client, distribution, and administrative access to the intended networks and identities.

## Exercise the application

Run representative create, read, update, delete, index, and conflict-resolution operations. Verify timeout and retry behaviour, missing-object handling, and causal-context preservation. Test with the actual authentication and TLS configuration.

## Prove operational recovery

Rehearse a rolling restart, a failed-node recovery, and a restore in an isolated environment. If replication is used, pause and resume a consumer and prove reconciliation. Confirm that monitoring detects unavailable nodes, growing queues, disk pressure, and elevated request latency.

## Record the operating limits

Document measured capacity, expansion triggers, backup retention, recovery targets, and who can execute administrative changes. Resolve failed checks before enabling traffic; repeat the relevant checks when the package, workload, or infrastructure changes.
