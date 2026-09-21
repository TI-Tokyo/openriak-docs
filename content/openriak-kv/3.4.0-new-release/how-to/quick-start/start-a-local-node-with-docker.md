---
title: Start a local node with Docker
weight: 10
product: OpenRiak KV
product_version: 3.4.0
diataxis: how-to
draft: true
status: editorially-rewritten
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
description: Start one local OpenRiak node with a published Docker Compose file, then verify an HTTP write and read.
  This is a disposable development environment.
related:
- tutorials/first-cluster/build-and-explore-a-docker-cluster
- how-to/quick-start/start-a-local-cluster-with-docker
- how-to/installation/run-openriak-with-persistent-docker-storage
- reference/http-api/ping
---

Start one local OpenRiak node with a published Docker Compose file, then verify an HTTP write and read. This is a disposable development environment.

## Before you begin

Install Docker Engine or Docker Desktop with Compose, and have `curl` available. Create an empty working directory. Keep it separate from any existing cluster data.

## Download and start

Select an operating system below. Download its **Single Node Compose File** and **Example Environment File** into the working directory. Save them as `compose.yaml` and `.env`.

{{< download-os-picker >}}

{{< docker-downloads >}}

For this example, set `OPENRIAK_HTTP_PORT=127.0.0.1:18098` and `OPENRIAK_PB_PORT=127.0.0.1:18087` in `.env`. These are deliberate local port bindings. Use a unique container name if another copy of the same Compose project exists.

```sh
docker compose config
docker compose pull
docker compose up -d --no-build
docker compose logs --tail=50 node
```

Wait for startup to finish, then check:

```sh
curl --fail http://127.0.0.1:18098/ping
curl --fail -i -X PUT http://127.0.0.1:18098/buckets/quickstart/keys/hello   -H 'Content-Type: text/plain' --data-binary 'Hello OpenRiak'
curl --fail http://127.0.0.1:18098/buckets/quickstart/keys/hello
```

The ping returns `OK`; the final read returns `Hello OpenRiak`. If startup fails, inspect the container logs and verify that the chosen host ports and bind-mount directories are available.

## Stop

```sh
docker compose down
```

The published Compose file uses bind-mounted data directories. Stopping the project retains those directories; restarting with them resumes the node. Remove only this exercise's directories if you want a completely fresh environment.
