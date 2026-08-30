---
title: 'Latch objects'
description: 'Explain how latch objects support conditional requests and which concurrency guarantees they provide.'
weight: 10
diataxis: 'explanation'
product: 'OpenRiak KV'
product_version: '3.4.0'
status: 'editorially-rewritten'
draft: true
audience:
  - 'architects'
  - 'developers'
source_material:
  - 'openriak-quickdocs-3.4'
quickdocs_sources:
  - 'https://openriak.github.io/riak/ObjectAPI.html#conditional-requests-and-latch-objects'
tags: ['diataxis', 'kv', 'explanation']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Explain how latch objects support conditional requests and which concurrency guarantees they provide.

## Overview

### Conditional requests and latch objects

There may be circumstances where it is necessary to prevent multiple application processes working on the same set of objects concurrently - e.g. where there are two processes for batching objects, and only one should be batching at a time so the batches don't overlap.  Although conditional requests are intended to provide consensus over individual objects, the application developer may define individual objects in such a way so that they can be used as part of a system to provide broader pseudo-serialisation of activity.
