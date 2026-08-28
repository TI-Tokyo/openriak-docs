---
title: 'Grant and revoke permissions'
description: 'Show security engineers how to grant and revoke permissions and test the resulting controls.'
weight: 5
diataxis: 'how-to'
product: 'OpenRiak KV'
product_version: '3.4.0'
status: 'editorially-rewritten'
draft: true
audience:
  - 'security-engineers'
  - 'operators'
source_material:
  - 'live-3.2.5'
  - 'proposed-kv'
  - 'openriak-quickdocs-3.4'
quickdocs_sources:
  - 'https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#granting-permissions-for-specific-actions'
tags: ['diataxis', 'kv', 'how-to']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Show security engineers how to grant and revoke permissions and test the resulting controls.

## Before you begin

Secure administrative access, an inventory of identities and certificates involved, and a tested rollback path that will not lock operators out.

## Overview

### Granting permissions for specific actions

There are specific actions within the API, to which specific permissions can be granted - restrictions both on the action alone, and constraints on performing the action by bucket type.

The actions supported by permission grants are:

- [`riak_kv.get`](/kv/3.4.0/reference/http-api/fetch-object/)
- [`riak_kv.put`](/kv/3.4.0/reference/http-api/store-object/)
- [`riak_kv.delete`](/kv/3.4.0/reference/http-api/delete-object/)
- [`riak_kv.list_keys`](/kv/3.4.0/reference/specialized-apis/list-api/)
- [`riak_kv.list_buckets`](/kv/3.4.0/reference/specialized-apis/list-api/)
- [`riak_kv.mapreduce`](/kv/3.4.0/reference/http-api/mapreduce/)
- `riak_kv.index`;
  - used to control both the [legacy query api](/kv/3.4.0/reference/specialized-apis/legacy-query-api/) and the [Query API](/kv/3.4.0/tutorials/query-api/).

For all other API endpoints, only `source` protection is applied.

> With the PB API, authentication is provided at the start of a connection, and grants are assessed and cached for that connection to be used against each request.  On the HTTP API, each request on a connection is authenticated and has grant checks made independently on a per-request basis.

Further information on the granting of permissions can be found in the [legacy documentation](https://docs.riak.com/riak/kv/latest/using/security/basics/index.html).

## Verify the result

Test permitted and denied access separately, validate certificate and identity details, and review security-related logs.
