---
title: Bucket properties and defaults
description: Bucket defaults supply the initial policy for ordinary object requests. A bucket type, bucket override,
  or request option can change the effective policy; data-type and lifecycle restrictions still apply.
weight: 130
diataxis: reference
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- developers
- operators
source_material:
- openriak-quickdocs-3.4
quickdocs_sources:
- https://openriak.github.io/riak/InitialDesignDecisions.html#data-distribution-guarantees
- https://openriak.github.io/riak/InstallAndStartGuide.html#configuration-of-riak---bucket-properties
- https://openriak.github.io/riak/InstallAndStartGuide.html#property---aae_tree_exclude
- https://openriak.github.io/riak/InstallAndStartGuide.html#property---allow_mult
- https://openriak.github.io/riak/InstallAndStartGuide.html#property---backend
- https://openriak.github.io/riak/InstallAndStartGuide.html#property---dvv_enabled
- https://openriak.github.io/riak/InstallAndStartGuide.html#property---general-readwrite-parameters
- https://openriak.github.io/riak/InstallAndStartGuide.html#property---last_write_wins
- https://openriak.github.io/riak/InstallAndStartGuide.html#property---n_val
- https://openriak.github.io/riak/InstallAndStartGuide.html#property---node_confirms
- https://openriak.github.io/riak/InstallAndStartGuide.html#property---notfound_ok
- https://openriak.github.io/riak/InstallAndStartGuide.html#property---pr-and-pw
- https://openriak.github.io/riak/InstallAndStartGuide.html#property---small_vclock
- https://openriak.github.io/riak/InstallAndStartGuide.html#property---sync_on_write
tags:
- diataxis
- kv
- reference
- quickdocs
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- reference/configuration/bucket-properties.md
related:
- how-to/application-data/create-and-activate-bucket-types
- reference/http-api/object-request-options
- foundations/data-and-consistency/bucket-types-and-data-policies
---

Bucket defaults supply the initial policy for ordinary object requests. A bucket type, bucket override, or request option can change the effective policy; data-type and lifecycle restrictions still apply.

## Settings

Select an operating system, then search by setting name or description. Values shown are the defaults from that release’s settings metadata; explicit configuration overrides take precedence.

{{< configuration-reference-table >}}
^buckets\.default\.
{{< /configuration-reference-table >}}
