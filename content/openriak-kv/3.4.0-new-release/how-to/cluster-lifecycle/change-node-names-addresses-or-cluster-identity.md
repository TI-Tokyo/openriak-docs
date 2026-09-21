---
title: Change node names, addresses, or cluster identity
description: Change a node's network address or identity without discarding its ownership metadata. Distinguish
  a client-listener change from an Erlang node-name change before proceeding.
weight: 780
diataxis: how-to
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- operators
source_material:
- legacy-3.2.5
- live-3.2.5
- proposed-kv
legacy_3_2_5_sources:
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\using\cluster-operations\changing-cluster-info.md
tags:
- diataxis
- kv
- how-to
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- how-to/operate/change-cluster-information.md
related:
- how-to/node-configuration/configure-node-identity-directories-and-the-initial-ring
- how-to/node-configuration/configure-http-and-protocol-buffers-listeners
- how-to/cluster-lifecycle/replace-nodes-without-stopping-the-cluster
- how-to/cluster-lifecycle/back-up-node-data-and-cluster-metadata
- reference/configuration/node-identity-directories-and-ring-settings
- foundations/cluster-architecture/membership-gossip-and-handoff
- foundations/cluster-lifecycle/failure-and-recovery
- foundations/cluster-lifecycle/rolling-maintenance-and-recovery-headroom
---

Change a node's network address or identity without discarding its ownership metadata. Distinguish a client-listener change from an Erlang node-name change before proceeding.

## Keep identity stable when possible

For a client endpoint change, update listeners, firewall rules, certificates, and proxy targets using [Configure HTTP and Protocol Buffers listeners]({{< product-version-root >}}how-to/node-configuration/configure-http-and-protocol-buffers-listeners/). A stable resolvable hostname can avoid changing the Erlang identity when an underlying address changes.

## Prepare a rename

Record the old and new full node names, ring directory, cluster name, and the affected configuration. Take a stopped-state backup of the metadata. Rehearse the exact release's offline rename command on a copy first:

{{< cli-example key="shell:riak admin reip_manual" >}}

Use its metadata help for the required arguments and stopped-node preconditions. Do not delete a populated node's ring files as a shortcut to renaming it, and do not allow both identities to serve the same storage concurrently.

## Apply and verify

Stop the node, update the persistent identity and required offline ring metadata using the documented command, and start it. Check membership from another member, logs, transfers, and application reads. Update monitoring and replication peers that refer to the old address. If the rename cannot be validated, retain the original state and use a planned replacement instead.
