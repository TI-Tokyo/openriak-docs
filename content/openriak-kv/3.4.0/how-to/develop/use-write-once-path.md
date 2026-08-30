---
title: 'Store immutable data with the write-once path'
description: 'Show developers how to store immutable objects through the write-once path and verify the result.'
weight: 21
diataxis: 'how-to'
product: 'OpenRiak KV'
product_version: '3.4.0'
status: 'editorially-rewritten'
draft: true
audience:
  - 'developers'
source_material:
  - 'openriak-quickdocs-3.4'
quickdocs_sources:
  - 'https://openriak.github.io/riak/OtherAPI.html#write-once-path-api'
tags: ['diataxis', 'kv', 'how-to']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Show developers how to store immutable objects through the write-once path and verify the result.

## Before you begin

A non-production OpenRiak KV cluster, client credentials, and disposable test data that represents the operation you need to implement.

## Overview

### Write Once Path API

The use of the write once path is deprecated in Riak 3.4, and the API will be retired in Riak 4.0.  The write once path was added to improve performance in very specific use cases, but broader changes have reduced the significance of any performance delta previously gained.  The write once path was not feature compatible with other write methods, and the preference of the OpenRiak community in the future is to reduce the number of caveats required to be understood when working with Riak.

The functionality of the Write Once Path is unchanged since Riak 2.2.3, so refer to the [legacy documentation](https://docs.riak.com/riak/kv/2.2.3/developing/app-guide/write-once/index.html) for further information.

## Verify the result

Run the operation against test data, inspect the stored result and response metadata, and exercise the expected failure path.
