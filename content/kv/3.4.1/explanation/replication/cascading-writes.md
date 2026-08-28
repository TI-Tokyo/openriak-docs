---
title: 'Cascading replication writes'
description: 'Explain cascading replication writes, its data flow, failure behavior, and operational trade-offs.'
weight: 3
diataxis: 'explanation'
product: 'OpenRiak KV'
product_version: '3.4.1'
status: 'editorially-rewritten'
draft: true
audience:
  - 'architects'
  - 'operators'
source_material:
  - 'legacy-3.2.5'
  - 'live-3.2.5'
  - 'proposed-kv'
legacy_3_2_5_sources:
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\using\reference\v3-multi-datacenter\cascading-writes.md'
  - 'Legacy multi-datacenter replication terminology and commands require compatibility review.'
tags: ['diataxis', 'kv', 'explanation']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Explain cascading replication writes, its data flow, failure behavior, and operational trade-offs.

## Overview

### Cascading Realtime Writes

#### Introduction

Riak includes a feature that cascades realtime writes across
multiple clusters.

Cascading Realtime Writes is enabled by default on new clusters running
Riak. It will need to be manually enabled on existing clusters.

Cascading realtime requires the `{riak_repl, rtq_meta}` capability to
function.

**Note on cascading tracking**
Cascading tracking is a simple list of where an object has been written. This
works well for most common configurations. Larger installations, however, may
have writes cascade to clusters to which other clusters have already written.

```
+---+     +---+     +---+
| A | <-> | B | <-> | C |
+---+     +---+     +---+
  ^                   ^
  |                   |
  V                   V
+---+     +---+     +---+
| F | <-> | E | <-> | D |
+---+     +---+     +---+
```

In the diagram above, a write at cluster A will begin two cascades. One
goes to B, C, D, E, and finally F; the other goes to F, E, D, C, and
finally B. Each cascade will loop around to A again, sending a
replication request even if the same request has already occurred from
the opposite direction, creating 3 extra write requests.

This can be mitigated by disabling cascading in a cluster. If cascading
were disabled on cluster D, a write at A would begin two cascades. One
would go through B, C, and D, the other through F, E, and D. This
reduces the number of extraneous write requests to 1.

A different topology can also prevent extra write requests:

```
+---+                     +---+
| A |                     | E |
+---+                     +---+
 ^  ^                     ^  ^
 |   \  +---+     +---+  /   |
 |    > | C | <-> | D | <    |
 |   /  +---+     +---+  \   |
 V  V                     V  V
+---+                     +---+
| B |                     | F |
+---+                     +---+
```

A write at A will cascade to C and B. B will not cascade to C because
A will have already added C to the list of clusters where the write has
occurred. C will then cascade to D. D then cascades to E and F. E and F
see that the other was sent a write request (by D), and so they do not
cascade.

#### Usage

Riak Cascading Writes can be enabled and disabled using the
`riak repl` command. Please see the [Version 3 Operations guide](/kv/3.4.1/reference/replication-api/runtime-controls/) for more information.

To show current the settings:

`riak repl realtime cascades`

To enable cascading:

`riak repl realtime cascades always`

To disable cascading:

`riak repl realtime cascades never`
