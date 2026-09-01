---
title: 'Version compatibility'
description: 'Record cluster, client, protocol, and replication compatibility across supported OpenRiak versions.'
weight: 5
diataxis: 'reference'
product: 'OpenRiak KV'
product_version: '3.4.1'
status: 'content-specification'
draft: true
audience:
  - 'architects'
  - 'operators'
  - 'developers'
source_material:
  - 'source-code-release-notes-3.4'
  - 'openriak-discussions'
  - 'live-3.2.5'
tags: ['diataxis', 'kv', 'reference']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Record cluster, client, protocol, and replication compatibility across supported OpenRiak versions.

> [!NOTE]
> This page is a content specification. Replace the guidance below with tested OpenRiak KV {{< current-version >}} documentation before publishing it.

## Scope

Define exactly what **Version compatibility** covers in OpenRiak KV {{< current-version >}} and what belongs in neighbouring reference pages. State the component, interface, file, command, or data type being documented and the supported context in which it is available.

## Definitions and syntax to add

Provide authoritative names, types, accepted syntax, defaults, allowed ranges, units, and whether each item is required, optional, deprecated, experimental, or version-specific. Use tables where readers need to compare repeated fields.

## Behaviour and constraints

Document precedence rules, interactions with other settings, consistency and failure semantics, security implications, resource limits, and whether a change is dynamic or requires a restart. Avoid procedural advice except for a compact, verifiable example.

## Examples to verify

Add minimal examples for a normal case, an important boundary case, and a representative invalid case. Record exact responses or error forms only after testing them against OpenRiak KV {{< current-version >}}.

## Version notes and sources

Identify what changed from {{< previous-version >}} to {{< current-version >}}, cite the relevant release note or source definition, and distinguish inherited 3.2.5 behaviour from claims independently confirmed for this release.

## Related reference

Link to adjacent commands, configuration keys, APIs, data types, and the how-to guide that demonstrates the most common use.

## In this section

- [Deprecated features in OpenRiak KV {{< current-version >}}]({{< product-version-root >}}reference/releases/deprecations/) — List deprecated features carried into {{< current-version >}}, preferred alternatives, compatibility implications, and possible future removal.
- [Downloads]({{< product-version-root >}}downloads/) — List supported OpenRiak packages, checksums, repositories, and source archives by platform and version.
- [Release and compatibility reference]({{< product-version-root >}}reference/releases/) — Provide factual version, platform, package, compatibility, and change information.
- [OpenRiak KV {{< current-version >}} release notes]({{< product-version-root >}}release-notes/) — Summarize the externally visible changes and fixes in OpenRiak KV {{< current-version >}} relative to {{< previous-version >}}.
- [Supported platforms]({{< product-version-root >}}reference/releases/supported-platforms/) — List supported operating systems, architectures, runtimes, and lifecycle dates for this release.
