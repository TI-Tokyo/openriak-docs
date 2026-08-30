---
title: 'Queued Query API results'
description: 'Define disk-backed queue_raw_keys and queue_raw_terms results, batching behavior, retrieval, and lifecycle.'
weight: 7
diataxis: 'reference'
product: 'OpenRiak KV'
product_version: '3.4.1'
status: 'content-specification'
draft: true
audience:
  - 'developers'
source_material:
  - 'source-code-release-notes-3.4'
  - 'openriak-quickdocs-3.4'
tags: ['diataxis', 'kv', 'reference']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Define disk-backed queue_raw_keys and queue_raw_terms results, batching behavior, retrieval, and lifecycle.

> [!NOTE]
> This page is a content specification. Replace the guidance below with tested OpenRiak KV 3.4.1 documentation before publishing it.

## Scope

Define exactly what **Queued Query API results** covers in OpenRiak KV 3.4.1 and what belongs in neighbouring reference pages. State the component, interface, file, command, or data type being documented and the supported context in which it is available.

## Definitions and syntax to add

Provide authoritative names, types, accepted syntax, defaults, allowed ranges, units, and whether each item is required, optional, deprecated, experimental, or version-specific. Use tables where readers need to compare repeated fields.

## Behaviour and constraints

Document precedence rules, interactions with other settings, consistency and failure semantics, security implications, resource limits, and whether a change is dynamic or requires a restart. Avoid procedural advice except for a compact, verifiable example.

## Examples to verify

Add minimal examples for a normal case, an important boundary case, and a representative invalid case. Record exact responses or error forms only after testing them against OpenRiak KV 3.4.1.

## Version notes and sources

Identify what changed from 3.4.0 to 3.4.1, cite the relevant release note or source definition, and distinguish inherited 3.2.5 behaviour from claims independently confirmed for this release.

## Related reference

Link to adjacent commands, configuration keys, APIs, data types, and the how-to guide that demonstrates the most common use.

## In this section

- [Query API accumulation options]({{< product-version-root >}}reference/query-api/accumulation-options/) — Define the 3.4.1 modes for keys, terms, counts, grouped counts, and disk-backed queued results.
- [Query API expression reference]({{< product-version-root >}}reference/query-api/expressions/) — Define supported Query API expressions, operators, composition rules, and Unicode behavior.
- [Query API reference]({{< product-version-root >}}reference/query-api/) — Define Query API endpoints, request expressions, responses, limits, and consistency behavior.
- [Query API limits and performance]({{< product-version-root >}}reference/query-api/limits/) — Record Query API scanning, filtering, buffering, aggregation, collation, and transformation limits.
- [Query API request reference]({{< product-version-root >}}reference/query-api/request/) — Define Query API request paths, JSON fields, defaults, and validation rules.
- [Query API response reference]({{< product-version-root >}}reference/query-api/responses/) — Define Query API response fields, ordering, pagination, and error representations.
