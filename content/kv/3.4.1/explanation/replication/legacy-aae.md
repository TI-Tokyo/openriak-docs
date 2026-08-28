---
title: 'Legacy active anti-entropy'
description: 'Explain legacy active anti-entropy, its data flow, failure behavior, and operational trade-offs.'
weight: 4
diataxis: 'explanation'
product: 'OpenRiak KV'
product_version: '3.4.1'
status: 'editorially-rewritten'
draft: true
audience:
  - 'architects'
  - 'operators'
source_material:
  - 'source-code-release-notes-3.4'
  - 'live-3.2.5'
  - 'proposed-kv'
  - 'openriak-quickdocs-3.4'
quickdocs_sources:
  - 'https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#monitoring-legacy-aae'
tags: ['diataxis', 'kv', 'explanation']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Explain legacy active anti-entropy, its data flow, failure behavior, and operational trade-offs.

## Overview

### Monitoring legacy AAE

If using the non-tictac AAE process, [information on the management and monitoring of AAE can be found in the legacy documentation](https://docs.riak.com/riak/kv/latest/using/cluster-operations/active-anti-entropy/index.html).
