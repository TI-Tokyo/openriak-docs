---
title: 'Build a first OpenRiak cluster on Ubuntu'
description: 'Guide a newcomer through installing, joining, and exercising a small Ubuntu development cluster.'
weight: 4
diataxis: 'tutorial'
product: 'OpenRiak KV'
product_version: '3.4.0'
status: 'editorially-rewritten'
draft: true
audience:
  - 'new-operators'
source_material:
  - 'proposed-kv'
migration_source_root: '\\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv'
migration_sources:
  - '\\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv\tutorials_howto\quickstart\ubuntu.md'
migration_review:
  - 'Internal links still refer to the earlier documentation hierarchy and must be retargeted to the Diátaxis paths.'
  - 'Commands or links derived from the 3.2.5 documentation were version-normalized for 3.4.0 and require technical verification.'
  - 'Release-specific installation, upgrade, downgrade, or quick-start instructions require verification against OpenRiak KV 3.4.0 packages.'
  - 'Legacy version text or MDX syntax remains and requires editorial review.'
tags: ['diataxis', 'kv', 'tutorial']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Guide a newcomer through installing, joining, and exercising a small Ubuntu development cluster.

## Overview

> [!WARNING]
> Migration review required: Internal links still refer to the earlier documentation hierarchy and must be retargeted to the Diátaxis paths.

## What you will learn

By completing this tutorial, you will build the workflow described above and learn how to validate each stage before moving on.

## Before you begin

Use a disposable OpenRiak KV environment that matches this documentation version, and keep cluster status and logs available while you work.

## Verify the result

Repeat the completed workflow, inspect the stored or operational result, and confirm that the cluster remains healthy.

## Next steps

- [Build a first OpenRiak cluster in the cloud](/kv/3.4.0/tutorials/first-cluster/cloud/)
- [Build a first OpenRiak cluster with Docker](/kv/3.4.0/tutorials/first-cluster/docker/)
- [Build a first OpenRiak cluster with Vagrant](/kv/3.4.0/tutorials/first-cluster/vagrant/)
