---
title: Add and remove cluster members
description: Practise removing a healthy member and joining it again while a small dataset remains available. Use
  only the disposable five-node cluster from [[T0]].
weight: 10
diataxis: tutorial
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- new-operators
source_material:
- legacy-3.2.5
- proposed-kv
migration_source_root: \\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv
migration_sources:
- \\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv\admin\ring-changes.md
- \\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv\tutorials_howto\tutorials\add-remove-node.md
legacy_3_2_5_sources:
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\using\cluster-operations\adding-removing-nodes.md
tags:
- diataxis
- kv
- tutorial
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- tutorials/operations/change-cluster-membership.md
related:
- how-to/cluster-lifecycle/plan-and-commit-a-membership-change
- how-to/cluster-lifecycle/add-nodes-to-a-cluster
- how-to/cluster-lifecycle/remove-a-node-from-a-cluster
- how-to/cluster-lifecycle/monitor-and-control-handoffs
- foundations/cluster-lifecycle/failure-and-recovery
- foundations/cluster-lifecycle/backups-restores-and-disaster-recovery
- foundations/cluster-lifecycle/rolling-maintenance-and-recovery-headroom
next_page: tutorials/cluster-operations-and-recovery/observe-a-node-failure-and-recovery
---

Practise removing a healthy member and joining it again while a small dataset remains available. Use only the disposable five-node cluster from [Build and explore a Docker cluster]({{< product-version-root >}}tutorials/first-cluster/build-and-explore-a-docker-cluster/).

## Establish the starting state

Source `learning-env.sh` in the Compose directory. Confirm five valid members and no pending ownership changes:

{{< cli-example key="shell:riak admin member-status" prefix="kv node1" >}}
{{< cli-example key="shell:riak admin transfers" prefix="kv node1" >}}

Write a value through node1 and read it through node2:

```sh
curl --fail -X PUT "$RIAK_HTTP/buckets/membership/keys/check" -H 'Content-Type: text/plain' --data-binary 'still here'
curl --fail http://127.0.0.1:18198/buckets/membership/keys/check
```

Copy node5's exact Erlang node name from the membership output. The container service name and Erlang node name are different identifiers.

## Stage a graceful leave

On node5, stage its own departure:

{{< cli-example key="shell:riak admin cluster leave" prefix="kv node5" >}}
{{< cli-example key="shell:riak admin cluster plan" prefix="kv node1" >}}

The plan should remove only node5 and distribute its partitions among the other four members. If it includes any unexpected change, clear the staged plan before proceeding:

{{< cli-example key="shell:riak admin cluster clear" prefix="kv node1" >}}

After clearing, stage the leave again. When the plan contains exactly the intended leave, commit:

{{< cli-example key="shell:riak admin cluster commit" prefix="kv node1" >}}

Repeat the transfers and membership checks. Wait until four members are valid and handoffs have finished. Read the sample through node2 again; expect `still here`.

## Rejoin the empty member

Wait for node5 to complete its departure before restarting its container. Do not erase its files while it is still transferring ownership. Restart node5 if it has stopped:

```sh
docker compose restart node5
```

Copy node1's exact Erlang name from the current membership output and substitute it for `riak@EXISTING_NODE`:

{{< cli-example key="shell:riak admin cluster join" prefix="kv node5" args="riak@EXISTING_NODE" >}}

Plan and commit on node1 using the commands above. Wait for five valid members and no outstanding transfers. Read the same key through both nodes once more. You have changed ownership without changing the application's key or endpoint format.
