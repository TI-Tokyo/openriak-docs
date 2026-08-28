---
title: 'vnode-status command'
description: 'Define the syntax, output fields, scope, and operational cautions for riak admin vnode-status.'
weight: 6
diataxis: 'reference'
product: 'OpenRiak KV'
product_version: '3.4.1'
status: 'editorially-rewritten'
draft: true
audience:
  - 'operators'
source_material:
  - 'source-code-release-notes-3.4'
  - 'openriak-quickdocs-3.4'
quickdocs_sources:
  - 'https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#vnode-status'
tags: ['diataxis', 'kv', 'reference']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Define the syntax, output fields, scope, and operational cautions for riak admin vnode-status.

## Details

### Vnode Status

**Available from OpenRiak KV 3.4.1.**

A significant proportion of the work within Riak takes places within the vnode.  To see the status of each vnode in the cluster, and see available statistics from the backend:  `riak admin vnode-status | sed -n 1p | json_pp`

To look at the statistics from specific nodes or partitions see: `riak admin vnode-status --help`.
