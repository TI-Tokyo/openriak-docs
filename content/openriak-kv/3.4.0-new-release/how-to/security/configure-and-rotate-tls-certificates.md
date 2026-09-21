---
title: Configure and rotate TLS certificates
description: Install or rotate the server certificate, private key, and CA chain used by the client listeners. Use
  certificates whose identities match the hostnames clients verify.
weight: 1140
diataxis: how-to
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- security-engineers
- operators
source_material:
- live-3.2.5
- proposed-kv
- openriak-quickdocs-3.4
quickdocs_sources:
- https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#tls-enablement
tags:
- diataxis
- kv
- how-to
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- how-to/secure/configure-tls.md
related:
- how-to/security/enable-authentication-and-authorization
- how-to/security/authenticate-an-application-client
- how-to/cluster-lifecycle/perform-a-rolling-restart
- tutorials/security/rotate-a-certificate-in-a-learning-environment
- reference/configuration/authentication-authorization-and-tls-settings
- foundations/security/security-boundaries-and-trust
- foundations/security/identities-authentication-and-permissions
- foundations/security/tls-and-certificate-trust
next_page: how-to/security/create-update-and-remove-users
---

Install or rotate the server certificate, private key, and CA chain used by the client listeners. Use certificates whose identities match the hostnames clients verify.

## Prepare and validate files

Check the certificate's validity period, subject alternative names, issuer chain, and matching private key. Install PEM files with permissions that let the Riak service read them while restricting private-key access.

{{< configuration-reference-table >}}
^ssl\.
^listener\.https\.
{{< /configuration-reference-table >}}

For HTTPS, configure a named HTTPS listener and the certificate paths. For PB, configure those paths and enable security using [Enable authentication and authorization]({{< product-version-root >}}how-to/security/enable-authentication-and-authorization/); PB does not use a separate HTTPS listener.

## Rotate without losing trust

Distribute any new trust anchor to clients before switching the server certificate. Retain the old trust chain for the required overlap period. Replace the files and restart nodes in a controlled sequence so active listeners load the intended material.

## Verify the served certificate

From the client network, perform a hostname-verified TLS connection and an authenticated operation. Check the served serial number and expiry, not only the files on disk. Test an untrusted certificate or wrong hostname to confirm verification is active. Remove obsolete keys and trust anchors after the overlap and rollback period ends.
