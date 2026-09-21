---
title: Configure node identity, directories, and the initial ring
description: Configure an empty node's stable identity, storage paths, and initial ring before joining it to a cluster.
  For a populated node, use the dedicated rename or migration procedure instead.
weight: 200
diataxis: how-to
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- operators
migration_source_root: \\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv
migration_sources:
- \\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv\configure\basics.md
- \\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv\configure\guides\basic-configuration.md
legacy_3_2_5_sources:
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\configuring\basic.md
source_material:
- legacy-3.2.5
- live-3.2.5
- proposed-kv
- openriak-quickdocs-3.4
quickdocs_sources:
- https://openriak.github.io/riak/InstallAndStartGuide.html#configuration-of-riak---key-riakconf-changes
tags:
- diataxis
- kv
- how-to
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- how-to/configure/basic-node-settings.md
related:
- how-to/planning-a-deployment/choose-a-ring-size
- how-to/planning-a-deployment/choose-a-storage-backend
- how-to/node-configuration/configure-http-and-protocol-buffers-listeners
- how-to/cluster-lifecycle/add-nodes-to-a-cluster
- how-to/cluster-lifecycle/change-node-names-addresses-or-cluster-identity
- reference/configuration/node-identity-directories-and-ring-settings
- foundations/cluster-architecture/rings-partitions-and-virtual-nodes
- foundations/cluster-architecture/the-lifecycle-of-a-read-and-a-write
next_page: how-to/node-configuration/configure-http-and-protocol-buffers-listeners
---

Configure an empty node's stable identity, storage paths, and initial ring before joining it to a cluster. For a populated node, use the dedicated rename or migration procedure instead.

## Record the cluster-wide choices

Use the same distribution cookie, initial ring size, and compatible placement policy on every member. Assign each node a unique Erlang node name whose host portion remains resolvable from the other members. Do not clone a populated data directory to create another member.

{{< configuration-reference-table >}}
^(nodename|distributed_cookie|ring_size|platform_.*_dir)$
{{< /configuration-reference-table >}}

## Set the node configuration

Stop the service and edit its `riak.conf`. Set the node name, cookie, and chosen backend. Place data and logs on the intended persistent filesystems, ensuring the Riak service account can create and update files there. Keep secrets and private keys readable only by the required accounts.

Configure client listeners using [Configure HTTP and Protocol Buffers listeners]({{< product-version-root >}}how-to/node-configuration/configure-http-and-protocol-buffers-listeners/). For hosts with multiple interfaces, confirm which address other members will resolve and use; client listeners and Erlang distribution are separate connections.

## Validate and join

{{< cli-example key="shell:riak chkconfig" >}}

Start the node, confirm its reported identity and local directories, then follow [Add nodes to a cluster]({{< product-version-root >}}how-to/cluster-lifecycle/add-nodes-to-a-cluster/). Review the plan before committing membership. If the identity is wrong after the node contains data, stop and use [Change node names, addresses, or cluster identity]({{< product-version-root >}}how-to/cluster-lifecycle/change-node-names-addresses-or-cluster-identity/) rather than editing names and deleting ring files.
