---
title: Backend capability matrix
weight: 60
product: OpenRiak KV
product_version: 3.4.0
diataxis: reference
draft: true
status: editorially-rewritten
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
description: Backend capabilities vary by release and are not interchangeable. The matrix below records the capabilities
  declared by the installed release's backend implementations.
related:
- how-to/planning-a-deployment/choose-a-storage-backend
- reference/configuration/bitcask-settings
- reference/configuration/leveled-settings
- reference/legacy-and-experimental-features/legacy-leveldb-settings
- reference/legacy-and-experimental-features/memory-backend-settings
- foundations/overview/what-openriak-kv-is
- foundations/replication-and-repair/replication-generations-and-compatibility
- foundations/storage-and-performance/storage-backend-trade-offs
---

Backend capabilities vary by release and are not interchangeable. The matrix below records the capabilities declared by the installed release's backend implementations.

## Capabilities

{{< configuration-reference-table reference="backends" >}}{{< /configuration-reference-table >}}

Secondary-index support does not by itself imply support for the newer Query API. Data-type policy and expiration controls have additional constraints; check their API and backend settings before choosing a combination.

The presence of a backend implementation is not a production support promise. Bitcask and Leveled are the principal choices described for current deployments; legacy engines and routing remain separately documented for existing installations.
