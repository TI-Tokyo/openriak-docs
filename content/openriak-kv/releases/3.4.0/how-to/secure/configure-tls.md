---
title: 'Configure TLS certificates and ciphers'
description: 'Show security engineers how to configure tls certificates and ciphers and test the resulting controls.'
weight: 2
diataxis: 'how-to'
product: 'OpenRiak KV'
product_version: '3.4.0'
status: 'editorially-rewritten'
draft: true
audience:
  - 'security-engineers'
  - 'operators'
source_material:
  - 'live-3.2.5'
  - 'proposed-kv'
  - 'openriak-quickdocs-3.4'
quickdocs_sources:
  - 'https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#tls-enablement'
tags: ['diataxis', 'kv', 'how-to']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Show security engineers how to configure tls certificates and ciphers and test the resulting controls.

## Before you begin

Secure administrative access, an inventory of identities and certificates involved, and a tested rollback path that will not lock operators out.

## Overview

### TLS Enablement

In Riak 3.4, support is provided for TLS 1.2 only.

The process for enabling TLS differs between the HTTP and PB interfaces.  For HTTP, there are two steps to enabling TLS on the API:

- Configure a listener on HTTPS within `riak.conf` - `listener.https.internal = <ip>:<port>`.
- Configure file paths within `riak.conf` to valid [`PEM` files](https://en.wikipedia.org/wiki/Privacy-Enhanced_Mail) for three components:
  - `ssl.certfile = <file_path>`;
    - the pem file for the server certificate to be used by the Riak node in TLS negotiation.
  - `ssl.keyfile = <file_path>`;
    - the private key for the server certificate, which may be the same file as the `ssl.certfile`.
  - `ssl.cacertfile = <file_path>`;
    - the CA certificate that signed the server certificate.

The configuration will start a HTTPS listener, and any HTTP client will be able to send any supported HTTP request via TLS using that listener.

For the PB interface, it is not possible to enable TLS in isolation without [adding further security measures]({{< product-version-root >}}how-to/secure/enable-security/).  The configuration of file paths to certificate and key files is required as a prerequisite for applying those measures.  No independent listener is used for PB when security is enabled, the standard listener will expect TLS negotiation if and only if security is enabled.

> Riak does not support any automated certificate management, or notification on pending certificate expiry.

## Verify the result

Test permitted and denied access separately, validate certificate and identity details, and review security-related logs.
