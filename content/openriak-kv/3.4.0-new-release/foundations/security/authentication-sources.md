---
title: 'Authentication sources and trust'
description: 'Explain authentication sources and trust and the security decisions administrators must make.'
weight: 2
diataxis: 'explanation'
product: 'OpenRiak KV'
product_version: '3.4.0'
status: 'content-specification'
draft: true
audience:
  - 'security-engineers'
  - 'architects'
  - 'operators'
source_material:
  - 'live-3.2.5'
  - 'proposed-kv'
tags: ['diataxis', 'kv', 'explanation']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Explain authentication sources and trust and the security decisions administrators must make.

> [!NOTE]
> This page is a content specification. Replace the guidance below with tested OpenRiak KV {{< current-version >}} documentation before publishing it.

## Purpose and context

Explain the question that **Authentication sources and trust** answers for architects, developers, or operators using OpenRiak KV {{< current-version >}}. Establish the problem and vocabulary before describing the mechanism, and keep task instructions in linked how-to guides.

## Concepts and mental model

Introduce the participating components, data or control flow, important states, and invariants. Add a diagram or worked narrative when relationships would otherwise be difficult to follow, and define all terms used by the rest of the page.

## How it works

Describe the mechanism from input to observable outcome, including distribution, coordination, persistence, and failure behaviour where relevant. Separate guaranteed behaviour from implementation detail and identify assumptions that depend on configuration.

## Trade-offs and operational implications

Explain what the design optimises, what it costs, and how workload, scale, topology, consistency requirements, and failure modes affect the choice. Connect these trade-offs to decisions readers actually make without turning the page into a procedure.

## Worked example to add

Provide a version-correct scenario that traces one request or state transition through the mechanism. Show the normal path and one failure or concurrency case, then connect the result back to the mental model.

## Boundaries and related topics

State what this explanation does not cover, note differences from earlier releases, and link to relevant tutorials, how-to guides, and authoritative reference material.

## In this section

- [Security concepts]({{< product-version-root >}}foundations/security/) — Introduce the OpenRiak security model, trust boundaries, identities, and authorization decisions.
- [The OpenRiak security model]({{< product-version-root >}}foundations/security/security-model/) — Explain the openriak security model and the security decisions administrators must make.
- [TLS identities and certificate trust]({{< product-version-root >}}foundations/security/tls-model/) — Explain tls identities and certificate trust and the security decisions administrators must make.
- [Users, groups, and permissions]({{< product-version-root >}}foundations/security/users-groups-and-permissions/) — Explain users, groups, and permissions and the security decisions administrators must make.
