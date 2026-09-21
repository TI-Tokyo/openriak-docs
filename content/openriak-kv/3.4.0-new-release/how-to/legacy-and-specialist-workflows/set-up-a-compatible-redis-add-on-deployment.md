---
title: Set up a compatible Redis add-on deployment
description: Prepare an isolated compatibility test before deploying the historical Redis add-on with this OpenRiak
  release. A verified add-on package and compatibility matrix are not included in the current release metadata.
weight: 1460
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
legacy_3_2_5_sources:
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\add-ons\redis\set-up-rra.md
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\add-ons\redis\set-up-rra\deployment-models.md
tags:
- diataxis
- kv
- how-to
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- how-to/redis-add-on/set-up.md
related:
- how-to/legacy-and-specialist-workflows/use-and-monitor-the-redis-add-on
- how-to/legacy-and-specialist-workflows/develop-an-application-using-the-redis-add-on
- reference/extensions-and-specialist-interfaces/redis-add-on-commands-and-configuration
- reference/client-libraries/client-compatibility-and-capability-matrix
- foundations/replication-and-repair/replication-generations-and-compatibility
- foundations/storage-and-performance/storage-backend-trade-offs
---

Prepare an isolated compatibility test before deploying the historical Redis add-on with this OpenRiak release. A verified add-on package and compatibility matrix are not included in the current release metadata.

## Establish a reproducible candidate

Record the add-on source revision or package, Redis version, OTP version, and OpenRiak package. Check that the candidate supports the intended bucket-type and security interfaces. Do not install an old binary or obsolete distribution repository merely because a historical guide used it.

## Isolate the test

Keep Redis, the add-on, and OpenRiak on a private test network with disposable data. Configure authentication, resource limits, cache bounds, and the add-on's connection settings using that candidate's own version-matched instructions. Use [Verify an installation]({{< product-version-root >}}how-to/installation/verify-an-installation/) to verify OpenRiak independently before introducing the proxy.

## Accept or reject compatibility

Run the read-through, write, delete, expiry, sibling, and outage checks in [Use and monitor the Redis add-on]({{< product-version-root >}}how-to/legacy-and-specialist-workflows/use-and-monitor-the-redis-add-on/) and [Develop an application using the Redis add-on]({{< product-version-root >}}how-to/legacy-and-specialist-workflows/develop-an-application-using-the-redis-add-on/). Record the exact versions and results. Until these checks pass, use the normal OpenRiak client interface for the deployment.
