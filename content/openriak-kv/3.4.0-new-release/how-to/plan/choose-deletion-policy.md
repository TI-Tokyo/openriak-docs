---
title: 'Choose a data deletion policy'
description: 'Show architects how to choose delete mode, tombstone retention, and garbage-collection behavior.'
weight: 5
diataxis: 'how-to'
product: 'OpenRiak KV'
product_version: '3.4.0'
status: 'editorially-rewritten'
draft: true
audience:
  - 'architects'
  - 'operators'
source_material:
  - 'openriak-quickdocs-3.4'
quickdocs_sources:
  - 'https://openriak.github.io/riak/InitialDesignDecisions.html#deleting-data'
  - 'https://openriak.github.io/riak/InitialDesignDecisions.html#deleting-data---making-a-choice'
  - 'https://openriak.github.io/riak/InstallAndStartGuide.html#configuration-of-riak---delete-mode'
tags: ['diataxis', 'kv', 'how-to']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Show architects how to choose delete mode, tombstone retention, and garbage-collection behavior.

## Before you begin

Access to the affected OpenRiak KV environment, the exact product version, a record of the current state, and a safe rollback plan.

## Overview

### Deleting data - making a choice

Reliable deletion of data within eventually consistent databases is non-trivial.  There are two aspects of deletion to be considered, dynamic deletion of individual objects, and the scheduled deletion of expired objects.

The complexity of deletion with eventual consistency is that it is an underlying requirement in a distributed system to compare potentially differing results between different locations for an object (i.e. between vnodes or between clusters).  If location A has an object, and location B doesn't; there is a need to differ between the situation where location B is correct (due to a deletion not being replicated), or location A is correct (due to an insertion not being replicated) - as these circumstances require opposing actions.  There are secondary consequences if keys are reused following deletion, whereby data could be potentially lost if an old deleted object is resurrected and appears to be more recent.

For deletion there are three modes with which a cluster can be run: `keep`, `immediate` and `time-interval`.  For protection against data loss, the safest mode to use is the `keep` based method, especially where the intention is to run multiple inter-connected clusters or where an application may reuse a previous key for a new object.  The `keep` method is a configuration whereby no object is directly deleted, it is replaced instead by a special `tombstone` object that has no value (and will appear as not found when fetched via the Object API).  The tombstone retains a reference to its change history, [the version vector]({{< product-version-root >}}explanation/data-model/version-vectors-and-siblings/), so that it can be correctly assessed for recency when comparing with an undeleted version of the object, and to allow for tracking of causal consistency when replacing tombstones.

Tombstones have no significant cost in terms of disk space, as they have no value, but they exist as a key; and this represents an overhead for background operations and the memory footprint of the store.  It is good practice therefore to periodically reap old tombstones, where the tombstones have existed for a long-enough period to be sure that no lingering problems of stale data exist for that key (e.g. reap tombstones > 1 month old).

[Clearing of old tombstones is a a semi-automated process]({{< product-version-root >}}explanation/operations/garbage-collection/), and so has some ongoing operational overheads.

The `time-interval` method of deletion essentially automates the job of having a delay between the deletion and the reap.  However, for every object between deletion states all nodes hosting a related vnode for the object have to maintain an in-memory timer process for each object awaiting reap.  This limits the practical scale of the time-interval - generally this is used for setting the time-interval in seconds, which is insufficient to fully handle the risks associated with deletion and false recovery of data.  When stopping a node any pending reap timers will be discarded.

The `immediate` configuration ignores the risk of deletion, and does not use tombstones.

It is also possible to manage deletion through the use of a Time To Live.  However, using TTL is impractical when also using anti-entropy, and so this is not recommended unless there is permanent intention never to use anti-entropy or the related services (e.g. inter-cluster reconciliation).

> TTL and anti-entropy will be partially supported as of Riak 3.4 on a per-bucket basis in-conjunction with the [`aae_tree_exclude` bucket property]({{< product-version-root >}}how-to/configure/replication/exclude-bucket-from-aae/)  - so that the disadvantages of not having anti-entropy are limited to those buckets with TTLs.  It is expected that this will be used for buckets which are specifically expected to be short-lived, and not requiring full reliability against data loss i.e. it is expected to be used for exceptional cases within a database, not as a general answer to deletion.

Through operational scheduling of [AAE folds]({{< product-version-root >}}reference/aae-fold-api/), erase and reap jobs can be combined to clear old data, per-bucket, based on the last modified date of the object.  This approach is recommended in preference to the use of TTL, to allow for garbage collection of expired objects.

#### Configuration of Riak - Delete Mode

There are three supported [delete modes in Riak]({{< product-version-root >}}how-to/plan/choose-deletion-policy/): `keep`, an interval or `immediate`.

If delete_mode is set to `keep`, every delete will be an update to a permanent tombstone that will need to be reaped at a later date (i.e. once tombstones have been securely replicated around connected clusters).  This will minimise the chance that values are resurrected through anti-entropy processes.  An interval will automate the reap process, and can be set to the number of milliseconds after the writing of the tombstone; which should be kept to less than 5 minutes.  Setting the delete mode to `immediate` will bypass the tombstone process, and delete directly without first writing a tombstone.

## Verify the result

Confirm the requested outcome, inspect cluster health and logs, and test the relevant client or operational path.
