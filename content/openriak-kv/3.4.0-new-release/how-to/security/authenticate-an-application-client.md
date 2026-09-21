---
title: Authenticate an application client
description: Connect an application using the authentication method and trust policy configured for its identity.
  Keep credentials out of source code and command histories used for production operations.
weight: 1160
diataxis: how-to
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- developers
source_material:
- legacy-3.2.5
- live-3.2.5
- proposed-kv
legacy_3_2_5_sources:
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\developing\usage\security.md
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\developing\usage\security\erlang.md
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\developing\usage\security\java.md
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\developing\usage\security\php.md
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\developing\usage\security\python.md
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\developing\usage\security\ruby.md
tags:
- diataxis
- kv
- how-to
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- how-to/develop/authenticate-client.md
related:
- how-to/security/configure-authentication-sources
- how-to/security/grant-and-revoke-permissions
- how-to/security/configure-and-rotate-tls-certificates
- tutorials/security/make-an-authenticated-tls-client-connection
- reference/http-api/http-conventions-authentication-and-errors
- reference/protocol-buffers-api/authentication-messages
- foundations/security/security-boundaries-and-trust
- foundations/security/identities-authentication-and-permissions
- foundations/security/tls-and-certificate-trust
previous_page: how-to/security/enable-authentication-and-authorization
---

Connect an application using the authentication method and trust policy configured for its identity. Keep credentials out of source code and command histories used for production operations.

## Match the interface

For HTTP, use HTTPS with a trusted CA and hostname verification. For PB, use a client that supports Riak's security handshake, credentials or client certificate, and CA verification. Do not send plain PB frames to a listener that expects the security handshake.

## Supply credentials securely

Load passwords and private-key paths through the application's secret mechanism. For certificate authentication, verify that the certificate identity matches the configured Riak user and source rule. Configure the narrowest grants needed by the application.

## Test the complete policy

Make a permitted operation against a known key, a forbidden operation, a request with invalid credentials, and a connection with an untrusted server certificate. Verify the application reports each failure correctly and does not retry authentication failures indefinitely.

Reopen long-lived connections when testing source or grant changes. Rehearse credential and certificate rotation before expiry; [Make an authenticated TLS client connection]({{< product-version-root >}}tutorials/security/make-an-authenticated-tls-client-connection/) gives a disposable HTTPS exercise, while [Authentication messages]({{< product-version-root >}}reference/protocol-buffers-api/authentication-messages/) specifies the PB authentication exchange.
