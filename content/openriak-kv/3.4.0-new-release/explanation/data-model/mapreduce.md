---
title: 'MapReduce in OpenRiak'
description: 'Explain mapreduce in openriak, its trade-offs, and its effect on application design.'
weight: 7
diataxis: 'explanation'
product: 'OpenRiak KV'
product_version: '3.4.0'
status: 'editorially-rewritten'
draft: true
audience:
  - 'architects'
  - 'developers'
source_material:
  - 'live-3.2.5'
  - 'proposed-kv'
  - 'openriak-quickdocs-3.4'
quickdocs_sources:
  - 'https://openriak.github.io/riak/OtherAPI.html#the-mapreduce-api'
tags: ['diataxis', 'kv', 'explanation']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Explain mapreduce in openriak, its trade-offs, and its effect on application design.

## Overview

### The Map/Reduce API

The use of Map/Reduce API is deprecated in Riak 3.4, and the API will be retired in Riak 4.0.

For using Map/Reduce with Erlang functions, the API is unchanged since Riak 2.2.3, so refer to the [legacy documentation]({{<baseurl>}}openriak-kv/2.2.3/developing/app-guide/advanced-mapreduce/index.html) for further information.  The Map/Reduce API no longer supports JavaScript functions.

> For querying data the [Query API]({{< product-version-root >}}tutorials/query-api/) should be used in preference to the Map/Reduce API.  The Query API is under active development to expand the number of Map/Reduce use cases it covers, in particular the ability to prompt the fetching of multiple objects.
