---
title: Run OpenRiak with persistent Docker storage
description: Keep a Docker node's configuration, data, and logs on persistent storage so that recreating its container
  does not discard its state.
weight: 170
diataxis: how-to
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- operators
source_material:
- live-3.2.5
- proposed-kv
migration_source_root: \\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv
migration_sources:
- \\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv\setup\install\docker\alpine-linux.md
tags:
- diataxis
- kv
- how-to
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- how-to/install/docker.md
related:
- how-to/quick-start/start-a-local-node-with-docker
- how-to/quick-start/start-a-local-cluster-with-docker
- how-to/cluster-lifecycle/back-up-node-data-and-cluster-metadata
- how-to/cluster-lifecycle/upgrade-a-cluster
- foundations/overview/what-openriak-kv-is
- foundations/cluster-architecture/rings-partitions-and-virtual-nodes
---

Keep a Docker node's configuration, data, and logs on persistent storage so that recreating its container does not discard its state.

## Prepare storage

Download the matching Compose and environment files from the image metadata. The published files use bind mounts for configuration, data, and logs; cluster files also share a discovery-control directory.

{{< download-os-picker >}}

{{< docker-downloads >}}

Set the host paths in `.env` to dedicated directories on the intended persistent filesystem. Check ownership, free space, and the service UID/GID settings before startup. Do not point two independent nodes at the same backend data directory.

## Start and verify persistence

Run `docker compose config` and inspect the resolved mounts, image, names, and ports. Start with `docker compose up -d --no-build`, write a test object, and read it back.

Stop the project with `docker compose down`, then start it again using the same files and directories. Verify that the same object and node identity remain available.

## Replace or upgrade the container

Keep the persistent paths stable and follow the cluster upgrade procedure. A new container image does not convert backend data or make arbitrary downgrade paths safe. Back up the required state using the backend's procedure before a change that needs a recovery copy.
