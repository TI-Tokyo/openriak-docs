---
title: Security boundaries and trust
description: OpenRiak security separates client authentication and permissions from trust in the host, cluster network,
  and administrative environment. Each exposed interface needs a deliberate access boundary.
weight: 380
diataxis: explanation
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- security-engineers
- architects
- operators
source_material:
- live-3.2.5
- proposed-kv
tags:
- diataxis
- kv
- explanation
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- foundations/security/security-model.md
related:
- foundations/security/identities-authentication-and-permissions
- foundations/security/tls-and-certificate-trust
- how-to/security/enable-authentication-and-authorization
- how-to/security/restrict-client-node-and-administrative-network-access
- how-to/security/audit-deployment-security
- reference/configuration/authentication-authorization-and-tls-settings
---

OpenRiak security separates client authentication and permissions from trust in the host, cluster network, and administrative environment. Each exposed interface needs a deliberate access boundary.

## Client access

Authentication establishes an identity; authorization controls the operations that identity may perform. Protecting the transport with TLS addresses another question: whether peers can establish trust and whether traffic is protected in transit.

## Administrative access

Access to the service account, node configuration, or an Erlang console can expose much broader control than an application's bucket permissions. Treat node-to-node connectivity and Erlang distribution credentials as cluster administration capabilities.

## Network boundaries

Bind and filter interfaces according to the intended clients and peers. A secure application listener does not automatically protect another listener, replication endpoint, or operating-system login path. Include load balancers and intermediate systems in the trust model.

## Failure behaviour

Test rejected access as well as successful access. A configuration that lets the intended application connect may still admit a wider source range or permission set than intended. Administrative recovery access should be planned before changing authentication or certificates.
