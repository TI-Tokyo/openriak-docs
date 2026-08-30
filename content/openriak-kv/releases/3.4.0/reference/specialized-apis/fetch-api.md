---
title: 'Fetch API reference'
description: 'Define Fetch API requests, responses, options, compatibility, and errors.'
weight: 2
diataxis: 'reference'
product: 'OpenRiak KV'
product_version: '3.4.0'
status: 'editorially-rewritten'
draft: true
audience:
  - 'developers'
source_material:
  - 'openriak-quickdocs-3.4'
quickdocs_sources:
  - 'https://openriak.github.io/riak/OtherAPI.html#the-fetch-api'
tags: ['diataxis', 'kv', 'reference']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Define Fetch API requests, responses, options, compatibility, and errors.

## Details

### The Fetch API

The fetch API supports three requests: the GET of a membership request, the GET from a queue and the POST to a queue.

| URL | Request parameters | Method | Description |
|:--------------|:--------------|:--------------|:--------------|
| `/membership_request` | n/a | GET | Return a list of IP listeners and ports for members of the cluster |
| `/queuename/<QueueName>` | `object_format = internal\|internal_aaehash` | GET | Consume the next object on queue referred to by Queue Name.  Object response may include segment ID and AAE hash of Key/VC if `internal_aaehash` chosen |
| `/queuename/<QueueName>` | n/a | POST | Push a list of Keys and clocks onto the queue so that those objects may be fetched by a consumer of the queue |

The fetch API is for internal use only in Riak 3.4.  The definition of the API may change in future releases.
