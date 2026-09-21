---
title: Secure next-generation replication connections
weight: 690
product: OpenRiak KV
product_version: 3.4.0
diataxis: how-to
draft: true
status: editorially-rewritten
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
description: Secure the transport used by a next-generation replication sink and its source. Configure an authenticated
  path before admitting application data to it.
related:
- how-to/replication-and-reconciliation/connect-clusters-with-next-generation-replication
- how-to/security/configure-and-rotate-tls-certificates
- reference/configuration/next-generation-replication-settings
- foundations/replication-and-repair/read-repair-and-tictac-anti-entropy
- foundations/replication-and-repair/replication-sources-queues-and-sinks
- foundations/replication-and-repair/real-time-replication-and-fullsync
---

Secure the transport used by a next-generation replication sink and its source. Configure an authenticated path before admitting application data to it.

## Establish the endpoint and identity

Identify the source protocol, listener, sink identity, and destination queue. Check which security controls apply to that transport; settings for legacy `riak_repl` listeners do not secure the next-generation path.

## Configure trust material

Install the trusted CA chain, certificate, and private key with permissions appropriate to the service account. Configure the replication credentials and the endpoint using the generated settings below.

{{< configuration-reference-table >}}
^repl_(cacert_filename|cert_filename|key_filename|username)$
^replrtq_sinkpeers$
^ttaaefs_peer
{{< /configuration-reference-table >}}

Create the corresponding source-side identity and least-privilege access needed for the selected interface. Validate the effective configuration before restarting or reconnecting consumers.

## Verify accepted and rejected connections

Deliver a test write and deletion through the intended queue. Then test an untrusted certificate, an incorrect identity, and a blocked origin in the learning environment. Confirm that both real-time delivery and reconciliation use the intended protected path.

Monitor failures and queue growth during certificate rotation, and retain the old trust material only for the planned transition period.
