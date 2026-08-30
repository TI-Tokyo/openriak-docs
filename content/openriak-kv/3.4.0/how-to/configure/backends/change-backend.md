---
title: 'Change the backend of an existing node'
description: 'Show operators how to change the backend of an existing node without losing access to required data.'
weight: 3
diataxis: 'how-to'
product: 'OpenRiak KV'
product_version: '3.4.0'
status: 'editorially-rewritten'
draft: true
audience:
  - 'operators'
legacy_3_2_5_sources:
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\using\cluster-operations\backend.md'
source_material:
  - 'legacy-3.2.5'
  - 'proposed-kv'
  - 'openriak-quickdocs-3.4'
quickdocs_sources:
  - 'https://openriak.github.io/riak/InitialDesignDecisions.html#database-backend---changing-the-choice'
tags: ['diataxis', 'kv', 'how-to']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Show operators how to change the backend of an existing node without losing access to required data.

## Before you begin

Administrative access to the nodes you will change; a copy of the current configuration; and a maintenance window if the setting requires a restart.

## Overview

### Backend

**TODO: Add content**

#### Database backend - changing the choice

The database backend configuration is local to a node.  Migrating the database backend will require a [rolling replacement]({{< product-version-root >}}how-to/operate/rolling-replacement/) of one or more nodes at a time.  For example, a multi-backend configuration with bitcask and in-memory backends and parallel-mode Tictac AAE, can be upgraded to a single leveled backend with native Tictac AAE (assuming the TTL capability requirement is not being utilised).

> A rolling replacement is a safe and reliable process even when a cluster is under application load; although it would be normal in a large-scale production OpenRiak cluster for a complete rolling replacement to take days and not hours.

Where different backends support different cluster-wide features (e.g. support of the [Riak Query API]({{< product-version-root >}}tutorials/query-api/)), then the feature will only be usable when all nodes have updated.

## Verify the result

Confirm that the intended setting is active on every affected node, then check cluster health and the relevant logs for warnings.
