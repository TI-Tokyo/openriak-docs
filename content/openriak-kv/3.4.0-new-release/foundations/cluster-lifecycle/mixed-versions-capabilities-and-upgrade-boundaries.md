---
title: Mixed versions, capabilities, and upgrade boundaries
description: A rolling upgrade creates a period in which nodes run different software. Compatibility must cover
  their communication, stored data, negotiated capabilities, and Erlang/OTP runtimes.
weight: 370
diataxis: explanation
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- operators
- architects
source_material:
- live-3.2.5
- proposed-kv
- openriak-quickdocs-3.4
quickdocs_sources:
- https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#upgrading-a-node
tags:
- diataxis
- kv
- explanation
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- foundations/operations/upgrade-and-downgrade.md
- foundations/foundations/capability-negotiation.md
related:
- reference/orientation-and-compatibility/cluster-client-and-replication-compatibility
- reference/orientation-and-compatibility/feature-status-and-deprecations
- how-to/cluster-lifecycle/upgrade-a-cluster
- how-to/cluster-lifecycle/roll-back-a-compatible-cluster-upgrade
- reference/configuration/all-configuration-settings-and-defaults
---

A rolling upgrade creates a period in which nodes run different software. Compatibility must cover their communication, stored data, negotiated capabilities, and Erlang/OTP runtimes.

## Capability negotiation

Nodes can negotiate features that require cluster-wide agreement. A feature available on the new binary may remain inactive until the participating nodes support it. Negotiation is a compatibility mechanism, not proof that every historical version can join every newer cluster.

## Persistent changes matter

A newer release can write data or metadata that older software cannot interpret. Enabling a feature may therefore change the available rollback path. Reinstalling an old package alone is not a general downgrade procedure.

## Runtime and backend boundaries

Erlang distribution compatibility and backend file formats constrain the route between releases. Review the exact source and target versions, package runtime, compression choices, and activated features. Do not skip intermediate steps merely because the application protocol appears unchanged.

## Configuration during an upgrade

A preserved configuration file can retain explicit old values when package defaults change. Compare the installed configuration with the release's generated settings, and record deliberate overrides separately. Validate the upgrade and recovery path against representative data before advancing through the production cluster.
