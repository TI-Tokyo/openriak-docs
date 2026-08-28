---
title: 'Query data with the Query API'
description: 'Show developers how to issue exact, range, wildcard, and combined Query API expressions.'
weight: 19
diataxis: 'how-to'
product: 'OpenRiak KV'
product_version: '3.4.1'
status: 'editorially-rewritten'
draft: true
audience:
  - 'developers'
source_material:
  - 'source-code-release-notes-3.4'
  - 'openriak-quickdocs-3.4'
  - 'openriak-discussions'
quickdocs_sources:
  - 'https://openriak.github.io/riak/QueryAPI.html#secondary-indexes---querying-index-entries-overview'
tags: ['diataxis', 'kv', 'how-to']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Show developers how to issue exact, range, wildcard, and combined Query API expressions.

## Before you begin

A non-production OpenRiak KV cluster, client credentials, and disposable test data that represents the operation you need to implement.

## Overview

### Secondary Indexes - Querying Index Entries Overview

The Query API is intended to provide flexible and performant functionality in the context of a Key-Value store:

> The aim of Riak development is to provide a database that performs efficient, scalable and predictable CRUD operations, and is just-queryable-enough to avoid the need of third party database integration in most use cases.

Riak does support via [an external replication API](/kv/3.4.1/reference/replication-api/), the ability to manage replication and reconciliation to third party query engines (e.g. OpenSearch), should more complex query support be required.  The automation of such integration is outside of the current functional scope of Riak.

## Verify the result

Run the operation against test data, inspect the stored result and response metadata, and exercise the expected failure path.
