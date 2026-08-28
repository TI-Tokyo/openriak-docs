---
title: 'Security concepts'
description: 'Introduce the OpenRiak security model, trust boundaries, identities, and authorization decisions.'
weight: 1
diataxis: 'explanation'
product: 'OpenRiak KV'
product_version: '3.4.1'
status: 'content-specification'
draft: true
audience:
  - 'security-engineers'
  - 'architects'
  - 'operators'
source_material:
  - 'openriak-quickdocs-3.4'
  - 'live-3.2.5'
  - 'proposed-kv'
tags: ['diataxis', 'kv', 'explanation']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Introduce the OpenRiak security model, trust boundaries, identities, and authorization decisions.

> [!NOTE]
> This page is a content specification. Replace the guidance below with tested OpenRiak KV 3.4.1 documentation before publishing it.

## Purpose and context

Explain the question that **Security concepts** answers for architects, developers, or operators using OpenRiak KV 3.4.1. Establish the problem and vocabulary before describing the mechanism, and keep task instructions in linked how-to guides.

## Concepts and mental model

Introduce the participating components, data or control flow, important states, and invariants. Add a diagram or worked narrative when relationships would otherwise be difficult to follow, and define all terms used by the rest of the page.

## How it works

Describe the mechanism from input to observable outcome, including distribution, coordination, persistence, and failure behaviour where relevant. Separate guaranteed behaviour from implementation detail and identify assumptions that depend on configuration.

## Trade-offs and operational implications

Explain what the design optimises, what it costs, and how workload, scale, topology, consistency requirements, and failure modes affect the choice. Connect these trade-offs to decisions readers actually make without turning the page into a procedure.

## Worked example to add

Provide a version-correct scenario that traces one request or state transition through the mechanism. Show the normal path and one failure or concurrency case, then connect the result back to the mental model.

## Boundaries and related topics

State what this explanation does not cover, call out 3.4.0 versus 3.4.1 differences, and link to relevant tutorials, how-to guides, and authoritative reference material.

## In this section

- [Authentication sources and trust]({{< baseurl >}}kv/3.4.1/explanation/security/authentication-sources/) — Explain authentication sources and trust and the security decisions administrators must make.
- [The OpenRiak security model]({{< baseurl >}}kv/3.4.1/explanation/security/security-model/) — Explain the openriak security model and the security decisions administrators must make.
- [TLS identities and certificate trust]({{< baseurl >}}kv/3.4.1/explanation/security/tls-model/) — Explain tls identities and certificate trust and the security decisions administrators must make.
- [Users, groups, and permissions]({{< baseurl >}}kv/3.4.1/explanation/security/users-groups-and-permissions/) — Explain users, groups, and permissions and the security decisions administrators must make.
