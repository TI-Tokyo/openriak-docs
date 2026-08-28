---
title: 'Choose a storage backend'
description: 'Show architects how to select a storage backend from durability, query, memory, compaction, and operational requirements.'
weight: 36
diataxis: 'how-to'
product: 'OpenRiak KV'
product_version: '3.4.1'
status: 'editorially-rewritten'
draft: true
audience:
  - 'architects'
  - 'operators'
source_material:
  - 'openriak-quickdocs-3.4'
quickdocs_sources:
  - 'https://openriak.github.io/riak/InitialDesignDecisions.html#database-backend'
  - 'https://openriak.github.io/riak/InitialDesignDecisions.html#database-backend---making-a-choice'
tags: ['diataxis', 'kv', 'how-to', 'quickdocs']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Show architects how to select a storage backend from durability, query, memory, compaction, and operational requirements.

## Before you begin

Access to the affected OpenRiak KV environment, the exact product version, a record of the current state, and a safe rollback plan.

## Overview

### Database backend - making a choice

A Riak database cluster is a collection of smaller databases (known as vnodes).  Each vnode has a backend which is responsible for storing, and providing access to the data.  What backends are to Riak, are what storage engines are to MySQL.  The choice of backend is important to the performance of the solution, but also critical to the features which are available to use.

The following choices exist:

- **leveled** (recommended for Riak 3.4)
- **bitcask** (default)
- eleveldb (deprecated as of Riak 3.4)
- in-memory (deprecated as of Riak 3.4)
- **multi-backend** (supported only in limited use cases, specifically as a multi-bitcask backend)

> In most common deployment scenarios, the best choice when the full functionality of Riak is required, is to use the leveled backend.

The bitcask backend may be used, especially if

- there is no potential future need for querying of data using the Query API, and;
- objects are largely immutable, and especially if also;
- read-repair is sufficient to meet the application anti-entropy requirements,
  - noting that anti-entropy is still supported with bitcask, just with additional overheads.

Sometimes, even in those situations, the leveled backend may be more efficient at present. There are ongoing plans within the OpenRiak community to continue to invest in bitcask improvements, and there are pending changes which have been shown to improve Riak/bitcask performance by 30% to 50% in some use cases.

> The bitcask backend is the preferred long-term solution for immutable, unsorted, data storage in Riak.

Use of multi-backend should generally be avoided, unless as a multi-bitcask backend (e.g. for tiered storage).  It may also be used to manage multiple expiry schedules across multiple bitcask backends through the backend TTL support; but not if anti-entropy requirements exist beyond read-repair or if inter-cluster reconciliation is required.  In these cases managing expiry [through the use of the eraser process is preferred]({{< baseurl >}}kv/3.4.1/how-to/plan/choose-deletion-policy/).

## Verify the result

Confirm the requested outcome, inspect cluster health and logs, and test the relevant client or operational path.
