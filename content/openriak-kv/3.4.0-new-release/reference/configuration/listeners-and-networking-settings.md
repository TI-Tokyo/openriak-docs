---
title: Listeners and networking settings
description: Listener settings control client endpoints and node networking. Select the intended interfaces explicitly
  and verify access from both permitted clients and cluster peers.
weight: 100
diataxis: reference
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- operators
migration_source_root: \\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv
migration_sources:
- \\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv\configure\networking.md
source_material:
- live-3.2.5
- proposed-kv
- openriak-quickdocs-3.4
quickdocs_sources:
- https://openriak.github.io/riak/BuildAndScaleClusterGuide.html#network
tags:
- diataxis
- kv
- reference
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- reference/configuration/networking.md
related:
- how-to/node-configuration/configure-http-and-protocol-buffers-listeners
- foundations/data-and-consistency/bucket-types-and-data-policies
---

Listener settings control client endpoints and node networking. Select the intended interfaces explicitly and verify access from both permitted clients and cluster peers.

## Settings

Select an operating system, then search by setting name or description. Values shown are the defaults from that release’s settings metadata; explicit configuration overrides take precedence.

{{< configuration-reference-table >}}
^(listener\.|protobuf\.|erlang\.distribution|handoff\.(ip|port))
{{< /configuration-reference-table >}}
