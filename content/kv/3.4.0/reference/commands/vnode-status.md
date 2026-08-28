---
title: 'vnode-status command'
description: 'Define the syntax, output fields, scope, and operational cautions for riak admin vnode-status.'
weight: 15
diataxis: 'reference'
product: 'OpenRiak KV'
product_version: '3.4.0'
status: 'content-specification'
draft: true
audience:
  - 'operators'
source_material:
  - 'openriak-quickdocs-3.4'
quickdocs_sources:
  - 'https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#vnode-status'
tags: ['diataxis', 'kv', 'reference', 'quickdocs']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Define the syntax, output fields, scope, and operational cautions for riak admin vnode-status.

> [!NOTE]
> This page is a content specification. Replace the guidance below with tested OpenRiak KV 3.4.0 documentation before publishing it.

## Scope

Define exactly what **vnode-status command** covers in OpenRiak KV 3.4.0 and what belongs in neighbouring reference pages. State the component, interface, file, command, or data type being documented and the supported context in which it is available.

## Definitions and syntax to add

Provide authoritative names, types, accepted syntax, defaults, allowed ranges, units, and whether each item is required, optional, deprecated, experimental, or version-specific. Use tables where readers need to compare repeated fields.

## Behaviour and constraints

Document precedence rules, interactions with other settings, consistency and failure semantics, security implications, resource limits, and whether a change is dynamic or requires a restart. Avoid procedural advice except for a compact, verifiable example.

## Examples to verify

Add minimal examples for a normal case, an important boundary case, and a representative invalid case. Record exact responses or error forms only after testing them against OpenRiak KV 3.4.0.

## Version notes and sources

Identify what changed from 3.4.0 to 3.4.1, cite the relevant release note or source definition, and distinguish inherited 3.2.5 behaviour from claims independently confirmed for this release.

## Related reference

Link to adjacent commands, configuration keys, APIs, data types, and the how-to guide that demonstrates the most common use.

## In this section

- [AAE command reference]({{< baseurl >}}kv/3.4.0/reference/commands/aae/) — List 3.4.0 command-line operations for AAE status, tree rebuilding, fold execution, and result retrieval.
- [Command reference]({{< baseurl >}}kv/3.4.0/reference/commands/) — Define command syntax, options, output fields, exit behavior, and required privileges.
- [riak admin command reference]({{< baseurl >}}kv/3.4.0/reference/commands/riak-admin/) — List every supported riak admin command with syntax, options, output, and safety notes.
- [Riak Control reference]({{< baseurl >}}kv/3.4.0/reference/commands/riak-control/) — List Riak Control capabilities, configuration, access requirements, and operational constraints.
- [riak command reference]({{< baseurl >}}kv/3.4.0/reference/commands/riak/) — List every supported riak command with syntax, options, output, and exit behavior.
