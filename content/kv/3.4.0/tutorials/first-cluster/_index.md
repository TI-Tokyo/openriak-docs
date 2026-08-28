---
title: 'Learn OpenRiak with a first cluster'
description: 'Introduce supported learning environments for creating a disposable first cluster.'
weight: 1
diataxis: 'tutorial'
product: 'OpenRiak KV'
product_version: '3.4.0'
status: 'editorially-rewritten'
draft: true
audience:
  - 'new-operators'
migration_source_root: '\\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv'
migration_sources:
  - '\\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv\tutorials_howto\quickstart\index.md'
  - '\\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv\use\running-a-cluster.md'
migration_review:
  - 'Release-specific installation, upgrade, downgrade, or quick-start instructions require verification against OpenRiak KV 3.4.0 packages.'
source_material:
  - 'live-3.2.5'
  - 'proposed-kv'
  - 'openriak-quickdocs-3.4'
quickdocs_sources:
  - 'https://openriak.github.io/riak/InstallAndStartGuide.html#local-cluster'
tags: ['diataxis', 'kv', 'tutorial']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Introduce supported learning environments for creating a disposable first cluster.

## Overview

### Local cluster

To create a local development cluster, which is ideal for experimenting with Riak, run `make devclean; make devrel`.  This will clean and rebuild a group of 8 Riak instances in the `dev/dev<n>` folder within the repository clone.

> [!WARNING]
> Migration review required: Release-specific installation, upgrade, downgrade, or quick-start instructions require verification against OpenRiak KV 3.4.0 packages.

## What you will learn

By completing this tutorial, you will build the workflow described above and learn how to validate each stage before moving on.

## Before you begin

Use a disposable OpenRiak KV environment that matches this documentation version, and keep cluster status and logs available while you work.

## Verify the result

Repeat the completed workflow, inspect the stored or operational result, and confirm that the cluster remains healthy.

## Next steps

- [Build a first OpenRiak cluster in the cloud](/kv/3.4.0/tutorials/first-cluster/cloud/)
- [Build a first OpenRiak cluster with Docker](/kv/3.4.0/tutorials/first-cluster/docker/)
- [Build a first OpenRiak cluster on Ubuntu](/kv/3.4.0/tutorials/first-cluster/ubuntu/)

## In this section

- [Build a first OpenRiak cluster in the cloud](/kv/3.4.0/tutorials/first-cluster/cloud/) — Guide a newcomer through deploying and testing a disposable cluster on a supported cloud platform.
- [Build a first OpenRiak cluster with Docker](/kv/3.4.0/tutorials/first-cluster/docker/) — Guide a newcomer from an empty Docker environment to a working cluster and a verified read and write.
- [Build a first OpenRiak cluster on Ubuntu](/kv/3.4.0/tutorials/first-cluster/ubuntu/) — Guide a newcomer through installing, joining, and exercising a small Ubuntu development cluster.
- [Build a first OpenRiak cluster with Vagrant](/kv/3.4.0/tutorials/first-cluster/vagrant/) — Guide a newcomer through creating a repeatable multi-node development cluster with Vagrant.
