---
title: 'Version vectors and siblings'
description: 'Explain version vectors and siblings, its trade-offs, and its effect on application design.'
weight: 9
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
  - 'https://openriak.github.io/riak/ObjectAPI.html#version-vector'
  - 'https://openriak.github.io/riak/QueryAPI.html#siblings'
  - 'https://openriak.github.io/riak/RiakTheoryGuide.html#version-vectors'
tags: ['diataxis', 'kv', 'explanation']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Explain version vectors and siblings, its trade-offs, and its effect on application design.

## Overview

### Version Vector

The Riak [version vector]({{< product-version-root >}}foundations/data-model/version-vectors-and-siblings/) is relevant to the database, but generally opaque to the application.  The application should read the version vector (which will be presented base64 encoded), and present the read version vector when updating an object.  The application does not need to understand the contents of the version vector.

The version vector is referred to in the API as a `vector clock` (or `vclock`).  This vector is used internally within Riak to track which content is most up-to-date - to differentiate between content that is superseded (i.e. where an update had seen the content) or genuinely concurrent (the writes were made in parallel).  Parallel writes will lead to unresolvable conflict, and how this is handled is defined within the [bucket properties]({{< product-version-root >}}reference/configuration/bucket-properties/).

#### Siblings

Riak supports the `allow_mult = true` state, whereby the history of changes to an object is retained when concurrent updates are made to the same object.  In the sibling state, all index entries on all versions of the object are active from a query perspective.

#### Version vectors

The default mechanism for tracking causal consistency on Riak objects is Dotted Version Vectors.

> Within Riak documentation and within the APIs, the name vector clock is used to refer to both the current recommended approach (dotted version vectors), and the previous legacy approach (loosely based on logical clocks).

A dotted version vector has two parts:

- A list of actors, and count of changes which have been coordinated by that actor (a per-actor sequence number);
- A dot attached to each content value, where the dot is the actor and actor-specific sequence number with which that change was introduced.

If there are two objects, one can be considered to be dominant (or more advanced) if within the version vector all the sequence numbers on all the actors are either equal to, or greater than, those on the other object (and at least one is greater than).  An update being dominant within the version vectors allows it to be updated in the backend without the need for a comparison and merge between the objects.

If there are two versions of an object, and neither version vector is dominant, then their contents are potentially siblings: the causal consistency cannot determine which is the more advanced value.  However, it may be possible to determine from the "dot" on a given value that the conflict is unrelated to that particular value, because either:

- Both changes see this as a replaced content value, or;
- The content value has the same dot, and so can be assumed to be the same value (a value cannot be a sibling of itself).

These two characteristics are important to avoid sibling explosion, which might otherwise result when multiple application processes are concurrently trying to update the same object (and correct the sibling state).  It is also important to the pruning of version vectors.

> The actors within the version vectors are the unique vnode IDs that have coordinated change on an object.  The number of actors will grow over time as as an object is updated by different vnodes in a preflist, via different cluster preflists and as the membership of a preflist is changed by the promotion of fallbacks during failure or the reshuffling of vnodes on cluster change.

As the list of actors in the version vector will grow over time, the version vector needs to support pruning.  Pruning is not coordinated, and happens independently on each vnode (and on each cluster) for that object key, when the vector exceeds a configured size limit.  Pruning of old information from version vectors will lead to false conflicts between version vectors: but this is highly unlikely to cause siblings, as the "dot" of the content can be used to confirm that the current object was not related to the portion of the version vector in conflict (i.e. it was not coordinated by a pruned actor).

Detailed information on the implementation of dotted version vectors in Riak can be found in the [original evaluation](https://asc.di.fct.unl.pt/~nmp/pubs/inforum-2011-2.pdf).
