---
title: Observe a node failure and recovery
weight: 20
product: OpenRiak KV
product_version: 3.4.0
diataxis: tutorial
draft: true
status: editorially-rewritten
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
description: Observe how the learning cluster serves data while one node is stopped, then brings that node back.
  This exercise uses a graceful container stop; it does not simulate disk loss or prove tolerance of every failure
  pattern
related:
- how-to/troubleshooting/recover-a-failed-node-or-choose-replacement
- how-to/data-inspection-and-repair/repair-a-vnode-or-node-from-surviving-replicas
- how-to/monitoring-and-diagnostics/monitor-anti-entropy-progress
- foundations/cluster-lifecycle/failure-and-recovery
- foundations/cluster-lifecycle/backups-restores-and-disaster-recovery
- foundations/cluster-lifecycle/rolling-maintenance-and-recovery-headroom
next_page: tutorials/cluster-operations-and-recovery/back-up-and-restore-a-sample-dataset
previous_page: tutorials/cluster-operations-and-recovery/add-and-remove-cluster-members
---

Observe how the learning cluster serves data while one node is stopped, then brings that node back. This exercise uses a graceful container stop; it does not simulate disk loss or prove tolerance of every failure pattern.

## Prepare a value

Complete [Build and explore a Docker cluster]({{< product-version-root >}}tutorials/first-cluster/build-and-explore-a-docker-cluster/), source `learning-env.sh`, and check that all five members are valid. Use the ordinary untyped bucket, whose replication policy has not been changed in this lab.

```sh
curl --fail -X PUT "$RIAK_HTTP/buckets/failure-demo/keys/check" -H 'Content-Type: text/plain' --data-binary 'before stop'
curl --fail http://127.0.0.1:18198/buckets/failure-demo/keys/check
```

## Stop one member

```sh
docker compose stop node5
```

{{< cli-example key="shell:riak admin member-status" prefix="kv node1" >}}

Node5 remains a cluster member but is unavailable. Do not issue a leave or replacement: this exercise expects the same node and its data to return.

Update through node1 and read through node2:

```sh
curl --fail -D failure.headers -o failure.value "$RIAK_HTTP/buckets/failure-demo/keys/check"
VCLOCK=$(awk 'tolower($1)=="x-riak-vclock:" {gsub("\r", "", $2); print $2}' failure.headers)
curl --fail -X PUT "$RIAK_HTTP/buckets/failure-demo/keys/check" -H "X-Riak-Vclock: $VCLOCK" -H 'Content-Type: text/plain' --data-binary 'while node5 was stopped'
curl --fail http://127.0.0.1:18198/buckets/failure-demo/keys/check
```

Expect the new value. If requests fail, inspect the actual membership and request errors before stopping any other member. Success here depends on the lab's surviving replicas and acknowledgement policy.

## Bring the member back

```sh
docker compose start node5
```

Repeat the membership and transfer checks until the node is available and pending handoffs finish:

{{< cli-example key="shell:riak admin transfers" prefix="kv node1" >}}

Read through node5's HTTP endpoint, `http://127.0.0.1:18498`, until it returns `while node5 was stopped`. A successful read through a node does not prove that every local replica has already been repaired; also inspect anti-entropy progress when assessing recovery.
