---
title: Back up and restore a sample dataset
weight: 30
product: OpenRiak KV
product_version: 3.4.0
diataxis: tutorial
draft: true
status: editorially-rewritten
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
description: Take an offline backup of the learning cluster, change a value, then restore the saved state. All nodes
  will be stopped together. Keep this exercise isolated from applications and other clusters.
related:
- how-to/cluster-lifecycle/back-up-node-data-and-cluster-metadata
- how-to/cluster-lifecycle/restore-node-data-from-a-backup
- reference/operations-and-observability/runtime-files-and-backup-contents
- foundations/cluster-lifecycle/failure-and-recovery
- foundations/cluster-lifecycle/backups-restores-and-disaster-recovery
- foundations/cluster-lifecycle/rolling-maintenance-and-recovery-headroom
previous_page: tutorials/cluster-operations-and-recovery/observe-a-node-failure-and-recovery
next_page: tutorials/cluster-operations-and-recovery/perform-a-rolling-restart
---

Take an offline backup of the learning cluster, change a value, then restore the saved state. All nodes will be stopped together. Keep this exercise isolated from applications and other clusters.

## Save a recognisable value

Use the five-node Docker lab from [Build and explore a Docker cluster]({{< product-version-root >}}tutorials/first-cluster/build-and-explore-a-docker-cluster/). Stop any other lesson clients or replication consumers before starting.

```sh
curl --fail -X PUT "$RIAK_HTTP/buckets/backup-demo/keys/check" -H 'Content-Type: text/plain' --data-binary 'saved version'
curl --fail "$RIAK_HTTP/buckets/backup-demo/keys/check"
docker compose config > backup-compose.yaml
docker compose stop
```

Confirm that every service is stopped with `docker compose ps --all`.

## Copy the complete stopped state

In `.env` and `backup-compose.yaml`, identify every node's bind-mounted configuration and data directory, plus the control directory. Create an archive outside those directories. For example, if all lab node directories and the control directory are under `lab-state`, run:

```sh
sudo tar -cpf learning-backup.tar lab-state
sudo tar -tf learning-backup.tar
sha256sum learning-backup.tar > learning-backup.sha256
```

Replace `lab-state` with the actual directory names from your Compose configuration. Preserve ownership and permissions. Include the ring and cluster metadata, not only the backend files. Keep `.env`, both Compose files, the image tag or digest, and this archive together.

## Create a later state

Restart all services, wait for healthy membership, fetch the vector clock, and update the same key to `later version`. Follow the context-preserving update in [Explore objects, buckets, and metadata with HTTP]({{< product-version-root >}}tutorials/data-and-concurrency/explore-objects-buckets-and-metadata-with-http/). Read it back to confirm the change, then stop every service again.

## Restore the saved files

Check the archive before using it:

```sh
sha256sum --check learning-backup.sha256
```

Move the current lab-state directories aside into a separate recovery directory. Restore the archive into the original parent directory with `sudo tar -xpf learning-backup.tar`. Do not merge a backup into existing backend directories. Preserve the original node names, paths, and image.

Start all five services, wait for membership and transfers to settle, and read the key. Expect `saved version`. Read through a second node as well. If any node was left running with the later state, replication can restore that later state; stop and correct the isolation before repeating.

## Finish

Retain the saved state until you have verified the recovery. This full-stop lab procedure is intentionally different from a rolling production backup or a Leveled hot backup; use [Back up node data and cluster metadata]({{< product-version-root >}}how-to/cluster-lifecycle/back-up-node-data-and-cluster-metadata/) to choose the production procedure.
