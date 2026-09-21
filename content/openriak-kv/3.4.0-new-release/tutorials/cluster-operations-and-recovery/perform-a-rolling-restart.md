---
title: Perform a rolling restart
weight: 40
product: OpenRiak KV
product_version: 3.4.0
diataxis: tutorial
draft: true
status: editorially-rewritten
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
description: Restart the five learning nodes one at a time while a sample read continues through another member.
  Complete [[T0]] and use its Compose directory and shell helper.
related:
- how-to/cluster-lifecycle/perform-a-rolling-restart
- how-to/cluster-lifecycle/start-stop-or-restart-a-node
- how-to/monitoring-and-diagnostics/perform-routine-cluster-health-checks
- foundations/cluster-lifecycle/failure-and-recovery
- foundations/cluster-lifecycle/backups-restores-and-disaster-recovery
- foundations/cluster-lifecycle/rolling-maintenance-and-recovery-headroom
previous_page: tutorials/cluster-operations-and-recovery/back-up-and-restore-a-sample-dataset
next_page: tutorials/cluster-operations-and-recovery/inspect-and-repair-a-bounded-data-range
---

Restart the five learning nodes one at a time while a sample read continues through another member. Complete [Build and explore a Docker cluster]({{< product-version-root >}}tutorials/first-cluster/build-and-explore-a-docker-cluster/) and use its Compose directory and shell helper.

## Record the starting condition

{{< cli-example key="shell:riak admin member-status" prefix="kv node1" >}}
{{< cli-example key="shell:riak admin transfers" prefix="kv node1" >}}

Continue only with five valid, reachable members and no pending membership changes. Create a sample:

```sh
curl --fail -X PUT "$RIAK_HTTP/buckets/restart-demo/keys/check" -H 'Content-Type: text/plain' --data-binary 'restart check'
```

## Restart the first node

```sh
docker compose restart node5
docker compose logs --tail=30 node5
curl --fail "$RIAK_HTTP/buckets/restart-demo/keys/check"
```

Expect `restart check`. Wait for node5 to become reachable and for recovery work to settle before moving on. Inspect membership, transfers, and logs; a running container alone is insufficient.

## Repeat with the other nodes

Repeat the same restart and checks for node4, node3, and node2, one at a time. Stop the exercise if a node fails to return or requests become unreliable.

Before restarting node1, direct the test read and administration checks to node2. Restart node1 last, then restore the original endpoint and verify the value through both node1 and node2.

No join, leave, or cluster commit is part of this restart. The returning nodes retain their identities and data. Keep the lab running for the next exercise.
