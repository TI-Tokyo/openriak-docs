---
title: 'Start, stop, or restart a node'
description: 'Show operators how to start, stop, or restart a node with prechecks, verification, and recovery guidance.'
weight: 16
diataxis: 'how-to'
product: 'OpenRiak KV'
product_version: '3.4.1'
status: 'editorially-rewritten'
draft: true
audience:
  - 'operators'
source_material:
  - 'live-3.2.5'
  - 'proposed-kv'
  - 'openriak-quickdocs-3.4'
quickdocs_sources:
  - 'https://openriak.github.io/riak/InstallAndStartGuide.html#local-release-or-cluster'
  - 'https://openriak.github.io/riak/InstallAndStartGuide.html#package-deployment'
  - 'https://openriak.github.io/riak/InstallAndStartGuide.html#starting-riak'
  - 'https://openriak.github.io/riak/InstallAndStartGuide.html#starting-riak-by-make-method'
tags: ['diataxis', 'kv', 'how-to']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Show operators how to start, stop, or restart a node with prechecks, verification, and recovery guidance.

## Before you begin

A healthy cluster, current backups, and access to cluster status and logs. Record the starting state before making an operational change.

## Overview

### Starting Riak by Make Method

Starting Riak changes depending on how Riak was made - a [local release](/kv/3.4.1/how-to/install/source/) or [local development cluster](/kv/3.4.1/tutorials/first-cluster/), or through [package deployment](/kv/3.4.1/how-to/operate/start-stop-restart-node/).  In all cases Riak is released using [the relx release generator](https://rebar3.org/docs/deployment/releases/), and inherits the control commands from the `relx` extended start script; but the location and method for accessing that script will vary.

#### Local Release or Cluster

For locally deployed instances (i.e. via `make rel` for a single node or `make devrel` for a development cluster), nodes can be controlled using the `bin/riak` script:

```console
bin/riak daemon
bin/riak ping
bin/riak stop
```

The location of the `bin` directory will depend on whether `make rel` or `make devrel` has been used to create the Riak release.  By default `make rel` will copy the release into the `rel/riak` folder in the base folder to which Riak was cloned - so the control script can be found at `rel/riak/bin/riak`.  For clusters generated with `make devrel`, the make process will create `n` multiple nodes under `dev/dev{n}/riak` in the base folder.  Those nodes are independent until [they are joined into a cluster](/kv/3.4.1/how-to/operate/add-node/).

> Under `riak`, there should be `bin`, `data`, `log` and `etc` folders.  The location of the `data` and `log` folders can be changed using the `platform.data_dir` and `platform.log_dir` in `etc/riak.conf`.

> The `bin/riak start` command which was used in Riak 3.0 and earlier releases is now deprecated.
>
> From Riak 3.2.0 use `daemon` to start Riak, or `foreground` to start with output redirected to `stdout`.

Help for further console activities can be found via:

```console
bin/riak --help
bin/riak admin --help
bin/riak admin cluster --help
```

#### Package Deployment

For instances deployed through packages, startup and shutdown should be controlled using `systemd` e.g.:

```console
service riak start
service riak ping
service riak stop
```

Help for further console activities can be found by using the standard `riak` script e.g. `sudo riak admin --help`.

> The default location of `bin`, `data`, `log` and `etc` folders following package deployment, should follow standard conventions for that operating system.  For example, on Ubuntu the configuration can be found in `/etc/riak/riak.conf`, and other paths are described within that file.

## Verify the result

Compare cluster health and workload behaviour with the recorded starting state, and confirm that all affected nodes have converged.
