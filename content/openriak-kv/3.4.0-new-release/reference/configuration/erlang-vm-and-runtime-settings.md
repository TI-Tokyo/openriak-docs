---
title: Erlang VM and runtime settings
weight: 110
product: OpenRiak KV
product_version: 3.4.0
diataxis: reference
draft: true
status: editorially-rewritten
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
description: Erlang runtime settings control process, scheduler, distribution, memory, and shutdown behaviour. Apply
  changes to a measured bottleneck and verify the running service receives them.
related:
- how-to/performance/tune-the-erlang-vm-for-a-measured-bottleneck
- foundations/data-and-consistency/bucket-types-and-data-policies
---

Erlang runtime settings control process, scheduler, distribution, memory, and shutdown behaviour. Apply changes to a measured bottleneck and verify the running service receives them.

## Settings

Select an operating system, then search by setting name or description. Values shown are the defaults from that release’s settings metadata; explicit configuration overrides take precedence.

{{< configuration-reference-table >}}
^(erlang\.|runtime_health\.|max_concurrent_requests|mbox_check_enabled)
{{< /configuration-reference-table >}}
