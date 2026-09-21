---
title: Secure legacy replication connections
description: Protect an existing legacy replication relationship using its generation-specific TLS configuration.
  Keep the previous working files and a recovery path during certificate changes.
weight: 1420
diataxis: how-to
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- operators
legacy_3_2_5_sources:
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\configuring\v2-multi-datacenter\ssl.md
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\configuring\v3-multi-datacenter\ssl.md
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\using\security\v2-v3-ssl-ca.md
- Legacy multi-datacenter replication terminology and commands require compatibility review.
source_material:
- legacy-3.2.5
- live-3.2.5
- proposed-kv
- openriak-quickdocs-3.4
quickdocs_sources:
- https://openriak.github.io/riak/ReplicationGuide.html#security-configuration
tags:
- diataxis
- kv
- how-to
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- how-to/configure/replication/secure-replication.md
related:
- how-to/legacy-and-specialist-workflows/maintain-legacy-v3-replication
- how-to/legacy-and-specialist-workflows/configure-legacy-replication-through-nat
- how-to/security/configure-and-rotate-tls-certificates
- reference/legacy-and-experimental-features/legacy-aae-and-riak-repl-settings
- reference/orientation-and-compatibility/replication-generation-compatibility
- foundations/replication-and-repair/replication-generations-and-compatibility
- foundations/storage-and-performance/storage-backend-trade-offs
---

Protect an existing legacy replication relationship using its generation-specific TLS configuration. Keep the previous working files and a recovery path during certificate changes.

## Prepare identities and trust

Record the identities and trust roots expected at both ends. Check certificate names, validity, matching private keys, and readable PEM paths. Do not assume the current-generation `repl_*` certificate settings configure `riak_repl`.

## Configure the legacy transport

Use [Legacy AAE and riak_repl settings]({{< product-version-root >}}reference/legacy-and-experimental-features/legacy-aae-and-riak-repl-settings/) for the available legacy TLS settings and [Legacy riak_repl runtime controls]({{< product-version-root >}}reference/replication-interfaces/legacy-riak-repl-runtime-controls/) for any required runtime controls. Apply the peer-name and trust policy consistently, then reload or restart according to the supported mechanism for the installed release.

## Verify both authentication and delivery

Confirm a connection with the trusted peer, rejection of an untrusted certificate, and delivery of a new sample object. Recheck fullsync after the transport change. Monitor expiry independently; do not assume Riak will renew certificates automatically.

During rotation, deploy new trust before changing peer certificates and remove old trust only after all peers have moved and the rollback interval has ended.
