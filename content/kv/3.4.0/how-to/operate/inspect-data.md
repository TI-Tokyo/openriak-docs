---
title: 'Inspect stored data'
description: 'Show operators how to inspect stored objects and backend state without changing data.'
weight: 28
diataxis: 'how-to'
product: 'OpenRiak KV'
product_version: '3.4.0'
status: 'editorially-rewritten'
draft: true
audience:
  - 'operators'
source_material:
  - 'openriak-quickdocs-3.4'
quickdocs_sources:
  - 'https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#accessing-objects'
  - 'https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#data-inspection'
tags: ['diataxis', 'kv', 'how-to']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Show operators how to inspect stored objects and backend state without changing data.

## Before you begin

A healthy cluster, current backups, and access to cluster status and logs. Record the starting state before making an operational change.

## Overview

### Accessing objects

To interrogate the internal representation of an object, it can be fetched from inside of the API using the riak_client module.  To use riak_client, a local_client must first be derived, to pass in as the final argument to riak_client function calls where required e.g.:

```erlang
(dev1@127.0.0.1)1> {ok, C} = riak:local_client().
{ok,{riak_client,['dev1@127.0.0.1',undefined]}}
(dev1@127.0.0.1)2> riak_client:get({<<"BucketType">>, <<"BucketName">>}, <<"KeyName">>, C).
```

The `rp/0` function call can be used to present the full output of any function within the shell, by default outputs will be truncated.  Note that displaying very large outputs fully in the shell may have significant costs and an impact on the usability of the session.

For the full functionality of [riak_client, see the module code](https://github.com/OpenRiak/riak_kv/blob/openriak-3.4/src/riak_client.erl).

#### Data inspection

To understand more about the data being held in the cluster, information can be found using AAE folds. Refer to the [API guide for AAE Fold](/kv/3.4.0/reference/aae-fold-api/) for information on triggering data inspection folds - `find_keys`, `find_tombs`, `list_buckets` and `object_stats`.

## Verify the result

Compare cluster health and workload behaviour with the recorded starting state, and confirm that all affected nodes have converged.
