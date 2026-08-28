---
title: 'Object merge strategies'
description: 'Explain how merge strategies resolve concurrent object versions and where application policy is required.'
weight: 13
diataxis: 'explanation'
product: 'OpenRiak KV'
product_version: '3.4.1'
status: 'editorially-rewritten'
draft: true
audience:
  - 'architects'
  - 'developers'
source_material:
  - 'openriak-discussions'
  - 'openriak-quickdocs-3.4'
quickdocs_sources:
  - 'https://openriak.github.io/riak/ObjectAPI.html#accessing-legacy-objects'
tags: ['diataxis', 'kv', 'explanation']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Explain how merge strategies resolve concurrent object versions and where application policy is required.

## Overview

### Accessing Legacy Objects

As well as typed buckets, Riak offers support for untyped buckets for backwards compatibility.  Using the HTTP API for such buckets is the same as using typed buckets, except that the URI for keys in untyped buckets is `buckets/Bucket/keys/Key` (i.e. as before but without the prefix of `types\TypedBucket`).
