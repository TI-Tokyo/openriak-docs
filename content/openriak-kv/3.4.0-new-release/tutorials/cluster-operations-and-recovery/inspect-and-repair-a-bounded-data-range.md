---
title: Inspect and repair a bounded data range
weight: 50
product: OpenRiak KV
product_version: 3.4.0
diataxis: tutorial
draft: true
status: editorially-rewritten
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
description: Inspect and request repair for three sample keys without scanning unrelated buckets. Use the Docker
  lab from [[T0]] with TicTac AAE active and its initial trees built.
related:
- how-to/data-inspection-and-repair/run-and-retrieve-a-long-running-aae-fold
- how-to/data-inspection-and-repair/measure-object-sizes-and-sibling-distributions
- how-to/data-inspection-and-repair/repair-a-selected-key-range
- how-to/data-inspection-and-repair/control-repair-impact-during-application-traffic
- reference/aae-fold-api/repair-keys-in-a-range
- foundations/cluster-lifecycle/failure-and-recovery
- foundations/cluster-lifecycle/backups-restores-and-disaster-recovery
- foundations/cluster-lifecycle/rolling-maintenance-and-recovery-headroom
previous_page: tutorials/cluster-operations-and-recovery/perform-a-rolling-restart
next_page: tutorials/cluster-operations-and-recovery/practise-a-backend-migration
---

Inspect and request repair for three sample keys without scanning unrelated buckets. Use the Docker lab from [Build and explore a Docker cluster]({{< product-version-root >}}tutorials/first-cluster/build-and-explore-a-docker-cluster/) with TicTac AAE active and its initial trees built.

## Write the sample range

```sh
for key in item-001 item-002 item-003; do
  curl --fail -X PUT "$RIAK_HTTP/buckets/repair-demo/keys/$key" -H 'Content-Type: text/plain' --data-binary "$key"
done
```

Open the Erlang remote console interactively. The `kvi` helper from `learning-env.sh` allocates the interactive terminal required by the console:

{{< cli-example key="shell:riak remote_console" prefix="kvi node1" >}}

## Inspect the selected keys

At the Erlang prompt, run:

{{< cli-example key="erlang:riak_client:aae_fold:object_stats" args=`{object_stats, <<"repair-demo">>, {<<"item-001">>, <<"item-003">>}, all}` >}}

Expect a successful result containing a total count of three. The interval is inclusive. If the trees or parallel store are still building, wait and retry before interpreting an incomplete result.

## Request repair for that range

{{< cli-example key="erlang:riak_client:aae_fold:repair_keys_range" args=`{repair_keys_range, <<"repair-demo">>, {<<"item-001">>, <<"item-003">>}, all, all}` >}}

The result reports work submitted, not proof that every repair has completed. Observe the reader queue and logs, then repeat the statistics request and read each key over HTTP. In a healthy lab there may be no divergent replicas to change; the purpose of this exercise is to bound and observe the operation, not to damage a store artificially.

Detach with `Ctrl-G`, then `q`. Do not call `q()` or `init:stop()` in the node's Erlang shell: those stop the VM.
