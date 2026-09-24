---
title: TLS and certificate trust
description: TLS protects a connection only when the client and server use an appropriate trust chain and verify
  the peer they intended to reach. Encryption without identity verification leaves an important part of that contract
  unme
weight: 400
diataxis: explanation
product: OpenRiak KV
product_version: 3.4.0
status: Reviewed
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
technical_review: complete
last_reviewed: '2026-09-24'
review_scope: content changes
review-by: TI Tokyo/JOM
restructured_from:
- foundations/security/tls-model.md
related:
- how-to/security/configure-and-rotate-tls-certificates
- how-to/security/authenticate-an-application-client
- tutorials/security/make-an-authenticated-tls-client-connection
- tutorials/security/rotate-a-certificate-in-a-learning-environment
- reference/configuration/authentication-authorization-and-tls-settings
---

TLS protects a connection only when the client and server use an appropriate trust chain and verify the peer they intended to reach. Encryption without identity verification leaves an important part of that contract unmet.

## Certificates and trust

A certificate binds an identity to a public key. A trust store identifies the issuers a peer accepts. The private key must remain available to its service and protected from unrelated users. Endpoint names, certificate names, validity periods, and chains must agree with the actual connection.

## TLS and application permissions

A trusted transport does not itself grant access to every bucket. Authentication and authorization still apply according to the configured method and interface. Client-certificate authentication also requires a deliberate mapping from the verified certificate to an accepted identity.

## Rotation

Rotation changes the trust material while connections and applications may still use the old material. An overlap period can allow clients to accept the new chain before the old one is removed. The sequence depends on the listener, client library, and authentication method.

Verify both trusted and untrusted connections after a change, and test name verification rather than suppressing it to make a connection succeed.
