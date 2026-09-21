---
title: Object expiration and reclamation settings
weight: 210
product: OpenRiak KV
product_version: 3.4.0
diataxis: reference
draft: true
status: editorially-rewritten
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
description: Expiration and reclamation settings govern different stages of the data lifecycle. Expiry, deletion-marker
  retention, erasure, and reaping are not interchangeable operations.
related:
- how-to/planning-a-deployment/choose-a-deletion-and-retention-policy
- how-to/data-inspection-and-repair/schedule-erasure-and-tombstone-reaping
- foundations/data-and-consistency/bucket-types-and-data-policies
---

Expiration and reclamation settings govern different stages of the data lifecycle. Expiry, deletion-marker retention, erasure, and reaping are not interchangeable operations.

## Settings

Select an operating system, then search by setting name or description. Values shown are the defaults from that release’s settings metadata; explicit configuration overrides take precedence.

{{< configuration-reference-table >}}
(^delete_mode$|expiry|expiration|^memory_backend\.ttl$|^eraser_|^reaper_|^tombstone_pause$|^repl_reap$)
{{< /configuration-reference-table >}}
