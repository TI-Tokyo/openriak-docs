---
title: 'Eventual consistency'
description: 'Explain eventual consistency, convergence, quorums, and the application behaviors they produce.'
weight: 2
diataxis: 'explanation'
product: 'OpenRiak KV'
product_version: '3.4.0'
status: 'editorially-rewritten'
draft: true
audience:
  - 'architects'
  - 'developers'
  - 'operators'
legacy_3_2_5_sources:
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\learn\concepts\eventual-consistency.md'
source_material:
  - 'legacy-3.2.5'
  - 'live-3.2.5'
  - 'openriak-quickdocs-3.4'
quickdocs_sources:
  - 'https://openriak.github.io/riak/RiakTheoryGuide.html#eventual-consistency'
tags: ['diataxis', 'kv', 'explanation']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Explain eventual consistency, convergence, quorums, and the application behaviors they produce.

## Overview

### Eventual Consistency

[concept buckets]: /kv/3.4.0/explanation/data-model/keys-objects-and-buckets/
[concept causal context vc]: /kv/3.4.0/explanation/data-model/causal-context/#vector-clocks
[concept clusters]: /kv/3.4.0/explanation/foundations/clusters-rings-and-partitions/
[concept replication]: /kv/3.4.0/explanation/replication/
[glossary node]: /kv/3.4.0/explanation/foundations/glossary/#node
[glossary read rep]: /kv/3.4.0/explanation/foundations/glossary/#read-repair
[usage bucket types]: /kv/3.4.0/how-to/develop/use-bucket-types/
[usage conflict resolution]: /kv/3.4.0/how-to/develop/resolve-conflicts/

In a distributed and fault-tolerant system like Riak, server and network
failures are expected. Riak is designed to respond to requests even when
[nodes][glossary node] are offline or the cluster is experiencing
a network partition.

Riak handles this problem by enabling conflicting copies of data stored
in the same location, as specified by [bucket type][concept buckets], bucket, and key, to exist at the same time in the cluster. This
gives rise to the problem of **data inconsistency**.

#### Data Inconsistency

Conflicts between replicas of an object are inevitable in
highly-available, [clustered][concept clusters] systems like Riak because there
is nothing in those systems to guarantee so-called [ACID
transactions](http://en.wikipedia.org/wiki/ACID). Because of this, these
systems need to rely on some form of conflict-resolution mechanism.

One of the things that makes OpenRiak's eventual consistency model powerful
is that Riak does not dictate how data resolution takes place. While
Riak does ship with a set of defaults regarding how data is
[replicated](#replication-properties-and-request-tuning) and how
[conflicts are resolved][usage conflict resolution], you can override these
defaults if you want to employ a different strategy.

Among those strategies, you can enable Riak to resolve object conflicts
automatically, whether via internal [vector clocks][concept causal context vc], timestamps, or
special eventually consistent [Data Types](/kv/3.4.0/reference/data/distributed-data-types/), or you can resolve those
conflicts on the application side by employing a use case-specific logic
of your choosing. More information on this can be found in our guide to
[conflict resolution][usage conflict resolution].

This variety of options enables you to manage OpenRiak's eventually
consistent behavior in accordance with your application's [data model
or models](/kv/3.4.0/how-to/plan/map-data-to-objects/).

#### Replication Properties and Request Tuning

In addition to providing you different means of resolving conflicts,
Riak also enables you to fine-tune **replication properties**, which
determine things like the number of nodes on which data should be stored
and the number of nodes that are required to respond to read, write, and
other requests.

An in-depth discussion of these behaviors and how they can be
implemented on the application side can be found in our guides to
[replication properties][concept replication] and [conflict resolution][usage conflict resolution].

In addition to our official documentation, we also recommend checking
out the [Understanding OpenRiak's Configurable
Behaviors](http://basho.com/understanding-riaks-configurable-behaviors-part-1/)
series from [the Basho blog](https://riak.com/blog/).

#### A Simple Example of Eventual Consistency

Let's assume for the moment that a sports news application is storing
all of its data in Riak. One thing that the application always needs to
be able to report to users is the identity of the current manager of
Manchester United, which is stored in the key `manchester-manager` in
the bucket `premier-league-managers`. This bucket has `allow_mult` set
to `false`, which means that Riak will resolve all conflicts by itself.

Now let's say that a node in this cluster has recently recovered from
failure and has an old copy of the key `manchester-manager` stored in
it, with the value `Alex Ferguson`. The problem is that Sir Ferguson
stepped down in 2013 and is no longer the manager. Fortunately, the
other nodes in the cluster hold the value `David Moyes`, which is
correct.

Shortly after the recovered node comes back online, other cluster
members recognize that it is available. Then, a read request for
`manchester-manager` arrives from the application. Regardless of which
order the responses arrive to the node that is coordinating this
request, `David Moyes` will be returned as the value to the client,
because `Alex Ferguson` is recognized as an older value.

Why is this? How does Riak make this decision? Behind the scenes, after
`David Moyes` is sent to the client, a [read repair][glossary read rep] mechanism will occur on the cluster to fix the
older value on the node that just came back online. Because Riak tags
all objects with versioning information, it can make these kinds of
decisions on its own, if you wish.

##### R=1

Let's say that you keep the above scenario the same, except you tweak
the request and set R to 1, perhaps because you want faster responses to
the client. In this case, it _is_ possible that the client will receive
the outdated value `Alex Ferguson` because it is only waiting for a
response from one node.

However, the read repair mechanism will kick in and fix the value, so
the next time someone asks for the value of `manchester-manager`, `David
Moyes` will indeed be the answer.

##### R=1, sloppy quorum

Let's take the scenario back in time to the point at which our unlucky
node originally failed. At that point, all 3 nodes had `Alex Ferguson`
as the value for `manchester-manager`.

When a node fails, OpenRiak's *sloppy quorum* feature kicks in and another
node takes responsibility for serving its requests.

The first time we issue a read request after the failure, if `R` is set
to 1, we run a significant risk of receiving a `not found` response from
Riak. The node that has assumed responsibility for that data won't have
a copy of `manchester-manager` yet, and it's much faster to verify a
missing key than to pull a copy of the value from disk, so that node
will likely respond fastest.

If `R` is left to its default value of 2, there wouldn't be a problem
because 1 of the nodes that still had a copy of `Alex Ferguson` would
also respond before the client got its result. In either case, read
repair will step in after the request has been completed and make
certain that the value is propagated to all the nodes that need it.

##### PR, PW, sloppy quorum

Thus far, we've discussed settings that permit sloppy quorums in the
interest of allowing Riak to maintain as high a level of availability as
possible in the presence of node or network failure.

It is possible to configure requests to ignore sloppy quorums in order
to limit the possibility of older data being returned to a client. The
tradeoff, of course, is that there is an increased risk of request
failures if failover nodes are not permitted to serve requests.

In the scenario we've been discussing, for example, the possibility of a
node for the `manchester-manager` key having failed, but to be more
precise, we've been talking about a *primary* node, one that when the
cluster is perfectly healthy would bear responsibility for that key.

When that node failed, using `R=2` as we've discussed or even `R=3` for
a read request would still work properly: a failover node (sloppy quorum
again) would be tasked to take responsibility for that key, and when it
receives a request for it, it would reply that it doesn't have any such
key, but the two surviving primary nodes still know who the
`manchester-manager` is.

However, if the PR (primary read) value is specified, only the two
surviving primary nodes are considered valid sources for that data.

So, setting PR to 2 works fine, because there are still 2 such nodes,
but a read request with PR=3 would fail because the 3rd primary node is
offline, and no failover node can take its place *as a primary*.

The same is true of writes: W=2 or W=3 will work fine with the primary
node offline, as will PW=2 (primary write), but PW=3 will result in an
error.

>**Note: Errors and Failures**
>
>It is important to understand the difference between an error and a
failure.
>
>The `PW=3` request in this scenario will result in an error,
but the value will still be written to the two surviving primary
nodes.
>
>By specifying `PW=3` the client indicated that 3 primary
nodes must respond for the operation to be considered successful, which
it wasn't, but there's no way to tell without performing another read
whether the operation truly failed.

#### Further Reading

* [Understanding OpenRiak's Configurable Behaviors blog series](http://basho.com/understanding-riaks-configurable-behaviors-part-1/)
* Werner Vogels, et. al.: [Eventually Consistent - Revisited](http://www.allthingsdistributed.com/2008/12/eventually_consistent.html)

#### Eventual Consistency

Riak is designed to be eventually consistent, in that it is:

- Permissive about accepting updates, ensuring data is stored securely on behalf of the application, even when the current state of the data relative to the update cannot be guaranteed;
  - either because some state may be in geographically diverse location, and waiting for verification of the present state would cause an unacceptable increase in response time,
  - or because failure of individual components has limited the visibility of the current state.
- Definitive that all changes will eventually be visible;
  - not just because data is replicated between nodes and between clusters,
  - but also because it is continuously reconciled, with background process that efficiently analyse the overall system for discrepancies and proactively heal those deltas without operator intervention,
  - where that continuous reconciliation occurs both within and between clusters.

It should be noted that Riak offers the same guarantees of zero-intervention eventual-consistency for both multi-cluster environments as well as single cluster environments.  However, within a cluster it is possible to enforce conditions on writes to make Riak less permissive, but less likely to result in conflict e.g. through the use of [conditional PUTs with token-based consensus](/kv/3.4.0/reference/http-api/conditional-requests/).

Care may be taken by the Riak user to avoid conflict; but inevitably there will be some object values that eventually end-up in conflict.  When in a conflicted state, an object may have two values where the database cannot determine which is the most current, often as updates were made concurrently by two different application instances.

Not being eventually consistent in a database, is likely to increase the operational processes required during failure scenarios: e.g. static fail-overs between primary and standby clusters, intervention to recover from replication failures between regions.  With eventual consistency: the gain in operational simplicity and reduced operational intervention, is a trade-off against the developer overhead of considering conflict.

> Handling an object where the value is in doubt, adds cognitive load to the application developer - it is the key trade-off between the operator and the developer to accept when adopting Riak.  At small-scale, and when downtime is acceptable; it is almost always preferable to favour the application developer in the trade-off.  Riak is an answer to exceptional use cases with demanding non-functional requirements, not a general purpose data-storage solution.

It is possible to craft objects whereby the situation can always be resolved, known as conflict-free replicated data-types.  However, designing a system based only on those data types is another type of cognitive load for the application developer.

In general, most applications that depend on Riak evolve strategies to restrict and manage conflict scenarios:

- Separating immutable and mutable data into different objects.
- Using application conditions to direct updates to clusters to avoid conflicting cross-cluster updates on the same object.
- Use sharding within the application or Riak's conditional PUT controls to avoid intra-cluster conflicts.
  - Potentially adopt an event sourcing CQRS-type pattern, to first secure capture of the data and then retry updates to queryable stores, so that refusing a write downstream will not lead to a risk of data-loss.
- Adding metadata to objects to allow deterministic resolution in either all cases, or just common cases.
