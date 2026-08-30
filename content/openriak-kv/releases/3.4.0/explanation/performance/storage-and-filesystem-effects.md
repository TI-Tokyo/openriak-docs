---
title: 'Storage and filesystem effects'
description: 'Explain storage and filesystem effects and how its trade-offs influence measurement and tuning decisions.'
weight: 5
diataxis: 'explanation'
product: 'OpenRiak KV'
product_version: '3.4.0'
status: 'editorially-rewritten'
draft: true
audience:
  - 'performance-engineers'
  - 'architects'
  - 'operators'
source_material:
  - 'live-3.2.5'
  - 'openriak-quickdocs-3.4'
quickdocs_sources:
  - 'https://openriak.github.io/riak/ObjectAPI.html#notes-on-implementation'
  - 'https://openriak.github.io/riak/ObjectAPI.html#performance-and-efficiency'
  - 'https://openriak.github.io/riak/ObjectAPI.html#performance-expectations'
tags: ['diataxis', 'kv', 'explanation']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Explain storage and filesystem effects and how its trade-offs influence measurement and tuning decisions.

## Overview

### Notes on Implementation

When a request is made to PUT an object in Riak, the PUT is sent to an available primary to coordinate the change.  A Primary vnode is considered available when the node on which it resides is reachable and reported as active by intra-cluster health-checks.  The coordination of a change is the updating of the version history of the object (the version vector), storing the object and prompting replication to other clusters where required. The PUT is then sent to the remaining available primaries (or fallbacks should there be a failure), to be stored at those vnodes if the version history indicates this change is more recent that the currently stored object.

Handling a forwarded PUT is marginally less expensive than coordinating a PUT.

When a request is made to GET an object in Riak, the metadata (containing the vector of the version history) for that object is fetched from each vnode in the preflist.  The first vnode to respond is tasked with fetching the value, and the remaining responses are used to determine whether the fetched value represents the most recent version (and if it is it may be returned to the client as the response).  If a replacement (later) version is available, then that is fetched as the value instead.  If analysis of the version vector and the version of the values, cannot determine which value is up-to-date the full history of unreconciled values is returned as "siblings".

> As of Riak 3.4, the bitcask backend does not support the handling of HEAD requests.  Each vnode will respond to the original request with the whole object, and no race is invoked.  Support for HEAD requests is available only in the leveled backend.

Handling the value fetch on vnode is an order of magnitude more expensive than simply handling the request for metadata.

Each vnode has a single queue through which all requests are received.  There is no priority on this queue, a request cannot be processed until all previous requests have been handled.  Latency on a very busy OpenRiak cluster is generally governed by the vnode queue sizes.  The GET and PUT process are designed to ensure that request performance is never governed by the pace of the longest queue.  Activity can proceed with a quorum of answers, and work is dynamically reduced so that vnodes with longer queues do less work until those queues realign with other vnodes.

#### Performance Expectations

Within the object API load distribution is first based on consistent hashing (to find the preflist of vnodes), but the race to support the value fetch in `GET` operations, and also the selection of the coordinator of a `PUT` operation is designed to try and rebalance load discrepancies within a preflist of vnodes.

The Object API is designed to be the most efficient of all the Riak APIs; it is assumed that requests to the Object API will occur with at least an order of magnitude of frequency greater than requests to other APIs.

> The primary target of Riak is not to minimise response times in normal conditions, but to provide predictable response times in extreme conditions with resource contention, device failure and device recovery.

In summary, the performance targets for the Object API are:

- With high-speed infrastructure, a 1ms mean response time should be achievable assuming small object sizes and a limited number of index entries per object.
- Without contention and under healthy conditions, for objects of o(100KB) in size with o(10) index entries per object (via the HTTP API) into a store with > 100M records, as measured from the application;
  - 3ms per GET (mean).
  - 7ms per PUT (mean).
- Under contention, and within failure scenarios, for o(10ms) 99th percentile response times to Object API requests.
  - It should be possible to maintain controlled response times as the failure is recovered (including repair of lost data), as well as when the failure occurs.
  - In general the 99th percentile should be less than twice the mean.
- As object sizes grow, the growth is response times should be logarithmic not linear - and stability of tail latency should not be impacted
  - As the differential between the cost of a HEAD request and a GET request expands with the size of objects, the stability of tail latency may actually improve with larger objects.

In Riak, an object of o(1KB) in size is considered to be small, and an object of o(1MB) in size is considered to be large.  For very large objects overall performance will be improved by the sharding of objects within the application.
