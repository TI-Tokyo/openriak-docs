---
title: Query execution settings
weight: 220
product: OpenRiak KV
product_version: 3.4.0
diataxis: reference
draft: true
status: editorially-rewritten
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
description: Query settings control the published index-query configuration and storage for queued results. Request
  fields, continuations, and delivery-mode behaviour are defined in the Query API reference.
related:
- reference/query-api/endpoints-and-request-schema
- reference/query-api/continuations-and-result-delivery
- how-to/performance/reduce-query-api-cost
- foundations/data-and-consistency/bucket-types-and-data-policies
---

Query settings control the published index-query configuration and storage for queued results. Request fields, continuations, and delivery-mode behaviour are defined in the Query API reference.

## Settings

Select an operating system, then search by setting name or description. Values shown are the defaults from that release’s settings metadata; explicit configuration overrides take precedence.

{{< configuration-reference-table >}}
^(query_|secondary_index_|participate_in_coverage|cluster\.job\..*secondary_index|.*worker_pool.*)
{{< /configuration-reference-table >}}
