---
title: 'Storage architecture'
description: 'Introduce storage engine design, workload fit, capacity implications, and backend trade-offs.'
weight: 1
diataxis: 'explanation'
product: 'OpenRiak KV'
product_version: '3.4.1'
status: 'editorially-rewritten'
draft: true
audience:
  - 'architects'
  - 'operators'
source_material:
  - 'openriak-quickdocs-3.4'
  - 'live-3.2.5'
  - 'proposed-kv'
quickdocs_sources:
  - 'https://openriak.github.io/riak/RiakTheoryGuide.html#backend-design'
tags: ['diataxis', 'kv', 'explanation']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Introduce storage engine design, workload fit, capacity implications, and backend trade-offs.

## Overview

### Backend Design

For Riak 3.4, there are two backends recommended for use in production systems:

- the bitcask backend;
- the leveled backend.

## In this section

- [How Bitcask stores data]({{< baseurl >}}kv/3.4.1/explanation/storage/bitcask/) — Explain how bitcask stores data, its constraints, and the workloads for which it is appropriate.
- [Storage capacity planning]({{< baseurl >}}kv/3.4.1/explanation/storage/capacity-planning/) — Explain storage capacity planning, its constraints, and the workloads for which it is appropriate.
- [Choosing a storage backend]({{< baseurl >}}kv/3.4.1/explanation/storage/choosing-backend/) — Explain choosing a storage backend, its constraints, and the workloads for which it is appropriate.
- [How LevelDB stores data]({{< baseurl >}}kv/3.4.1/explanation/storage/leveldb/) — Explain how leveldb stores data, its constraints, and the workloads for which it is appropriate.
- [How Leveled stores data]({{< baseurl >}}kv/3.4.1/explanation/storage/leveled/) — Explain how leveled stores data, its constraints, and the workloads for which it is appropriate.
- [How the Memory backend stores data]({{< baseurl >}}kv/3.4.1/explanation/storage/memory/) — Explain how the memory backend stores data, its constraints, and the workloads for which it is appropriate.
- [How multiple backends work]({{< baseurl >}}kv/3.4.1/explanation/storage/multi-backend/) — Explain how multiple backends work, its constraints, and the workloads for which it is appropriate.
- [How Prefix Multi routing works]({{< baseurl >}}kv/3.4.1/explanation/storage/prefix-multi/) — Explain how prefix multi routing works, its constraints, and the workloads for which it is appropriate.
