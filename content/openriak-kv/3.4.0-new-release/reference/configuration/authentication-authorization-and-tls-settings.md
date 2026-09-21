---
title: Authentication, authorization, and TLS settings
description: Security settings configure certificate files, TLS controls, listener restrictions, and transport trust.
  User, group, source, and permission records are managed through the security commands.
weight: 190
diataxis: reference
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- operators
source_material:
- live-3.2.5
- proposed-kv
tags:
- diataxis
- kv
- reference
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- reference/configuration/security.md
related:
- reference/commands/riak/admin/security
- how-to/security/configure-and-rotate-tls-certificates
- foundations/data-and-consistency/bucket-types-and-data-policies
---

Security settings configure certificate files, TLS controls, listener restrictions, and transport trust. User, group, source, and permission records are managed through the security commands.

## Settings

Select an operating system, then search by setting name or description. Values shown are the defaults from that release’s settings metadata; explicit configuration overrides take precedence.

{{< configuration-reference-table >}}
^(ssl\.|tls_protocols\.|handoff\.ssl\.|repl_(cacert|cert|key|username)|check_crl|honor_cipher_order|permit_insecure_http_ops|secure_referer_check)
{{< /configuration-reference-table >}}
