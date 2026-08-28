---
title: 'Data Type API reference'
description: 'Define endpoints, request and response formats, options, and constraints for OpenRiak distributed data types.'
weight: 101
diataxis: 'reference'
product: 'OpenRiak KV'
product_version: '3.4.1'
status: 'editorially-rewritten'
draft: true
audience:
  - 'developers'
source_material:
  - 'openriak-quickdocs-3.4'
quickdocs_sources:
  - 'https://openriak.github.io/riak/OtherAPI.html#the-data-type-api'
tags: ['diataxis', 'kv', 'reference', 'quickdocs']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Define endpoints, request and response formats, options, and constraints for OpenRiak distributed data types.

## Details

### The Data Type API

Riak supports Conflict-Free Replicated Data-Types (CRDTs); specific object formats that can be merged within the database on conflict between versions, so that the application will not see siblings.

There are four basic data-types supported:

- counters;
- grow-only sets;
- sets;
- maps,
  - combinations of the above three types, with support for two additional types - registers and flags.

Support for these data types is unchanged since Riak 2.2.3, so refer to the [legacy documentation](https://docs.riak.com/riak/kv/2.2.3/learn/concepts/crdts/index.html) for further information.

Before using data-types, there are important caveats within the current implementation to consider:

- All CRDTs implement "Action At a Distance", that is to say the application does not provide an identity of the actor making the request.  Due to this, other than for grow-only sets, CRDT updates are not idempotent.
  - The correct handling of failure of an individual request is not presently defined.
- Riak is designed for the storing of many keys, where the load of object requests is spread roughly evenly across the key-space; this is also true for CRDTs.  Do not use individual counters, for example a single hit counter for an application, that may create a __hot__ key that is accessed much more frequently than other keys.
- Both sets and maps have specific constraints in Riak 3.4 where the growth of components within an object is not handled efficiently.
- There is no in-built support for querying data within data-types, the Data Type API is incompatible with the [Query API]({{< baseurl >}}kv/3.4.1/tutorials/query-api/).

> The approach to supporting data types is expected to be evolved significantly in future Riak releases; which may result in significant changes to both sets and maps, and change the use of those data types in those releases.
