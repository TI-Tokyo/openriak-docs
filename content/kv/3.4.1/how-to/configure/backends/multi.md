---
title: 'Configure multiple backends'
description: 'Show operators how to configure multiple backends without losing access to required data.'
weight: 7
diataxis: 'how-to'
product: 'OpenRiak KV'
product_version: '3.4.1'
status: 'editorially-rewritten'
draft: true
audience:
  - 'operators'
migration_source_root: '\\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv'
migration_sources:
  - '\\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv\configure\backends\configure-multi.md'
migration_review:
  - 'The multi backend is deprecated in OpenRiak KV 3.4 unless every configured backend is Bitcask.'
source_material:
  - 'proposed-kv'
  - 'openriak-quickdocs-3.4'
quickdocs_sources:
  - 'https://openriak.github.io/riak/InitialDesignDecisions.html#multi-backend'
tags: ['diataxis', 'kv', 'how-to']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Show operators how to configure multiple backends without losing access to required data.

## Before you begin

Administrative access to the nodes you will change; a copy of the current configuration; and a maintenance window if the setting requires a restart.

## Overview

### Multi-backend

The multi-backend has the following characteristics and features:

- Allows different data buckets to be mapped to different backends, so that different buckets can use the different capabilities of those backends.
- Generally only recommended for production use when running multiple bitcask backends (e.g. with different TTL, or storage paths).

Testing of Riak is focused on single-backend solutions, but multi-backend (bitcask) is a combination well-tested within large-scale production deployments.

> [!WARNING]
> Migration review required: The multi backend is deprecated in OpenRiak KV 3.4 unless every configured backend is Bitcask.

## Verify the result

Confirm that the intended setting is active on every affected node, then check cluster health and the relevant logs for warnings.
