---
title: 'Reconciliation scope'
description: 'Explain all-cluster, per-bucket, time-window, and key-range reconciliation trade-offs.'
weight: 13
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
quickdocs_sources:
  - 'https://openriak.github.io/riak/ReplicationGuide.html#replication-scope'
tags: ['diataxis', 'kv', 'explanation']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Explain all-cluster, per-bucket, time-window, and key-range reconciliation trade-offs.

## Overview

### Replication scope

Replication in Riak between clusters is limited in scope to objects only.  Cluster metadata, including bucket type configurations, bucket properties and authentication credentials are not replicated.  When enabling bucket types, the enablement must be triggered on each and every cluster that may receive an object for that bucket type.
