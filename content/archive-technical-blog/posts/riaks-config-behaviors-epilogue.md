---
title: "Understanding Riak’s Configurable Behaviors Epilogue"
date: "2013-05-22T17:19:23+00:00"
author: "John Daily"
original_url: "http://basho.com/posts/technical/riaks-config-behaviors-epilogue/"
archive_url: "https://web.archive.org/web/20170801120859http://basho.com/posts/technical/riaks-config-behaviors-epilogue/"
categories:
  - "Architecture & Distributed Systems"
  - "Operations"
---
*May 22, 2013*

Basho recently held its second distributed systems conference, ~~RICON East~~ in New York City. Months of preparation led to two days of concentrated learning, with community members from academia and industry sharing where we’ve been and where we’re going.

By design, many of the presentations had little direct relationship to Riak: RICON is a marketplace for ideas, not for product. However, two of the speakers tackled topics I discussed recently in my blog series on the subtleties of Riak configuration.

- [Part 1](http://basho.com/understanding-riaks-configurable-behaviors-part-1/)
- [Part 2](http://basho.com/riaks-config-behaviors-part-2/)
- [Part 3](http://basho.com/riaks-config-behaviors-part-3/)
- [Part 4](http://basho.com/riaks-config-behaviors-part-4/)

This is a follow-up to that series to examine those talks. I won’t repeat earlier content in any significant detail.

# Rich Hickey, Using Datomic with Riak

[Datomic](http://www.datomic.com) is a very different take on databases, more akin to a version control system than a traditional RDBMS. In Datomic, records (“facts”) are never changed, but rather can be replaced as needed.

The notion of immutable facts leads to a conceptually simple distributed model that allows for transactions: a view into the database is simply a checkpoint of the facts. It’s always possible that a client may be reading an old checkpoint, but the facts at that checkpoint will be consistent regardless of what further updates have been applied.

Riak is one of several backends that can be used with Datomic.

## How Datomic queries Riak

Because Datomic keeps a record of all keys in the system, and because the values for those keys **never change**, reads can be expedited by setting `R=1`.

However, as you’ll recall, `R=1` has an important complication: if the first vnode to respond does not have a copy of that key (perhaps there’s a sloppy quorum in play due to a node failure) the request will “successfully” complete with a `notfound` message.

This default behavior can be changed by setting `notfound_ok=false` so that the coordinating node will await an actual value before reporting it back to the client, and in fact this is how Datomic operates.

# Kyle Kingsbury, Call Me Maybe: Carly Rae Jepsen and the Perils of Network Partitions

Kyle conducted extensive testing of various distributed databases in the face of network partition. Specifically, he wanted to see whether writes were successful (and properly retained) during and after the partition.

His testing of Riak with `allow_mult=false` (the default) revealed **91%** of writes were lost after the partition healed.

Riak is, however, the only database that retained 100% of writes during a partition, but only when `allow_mult` was set to `true` in order to allow sibling resolution on the client side after the partition.

Without `allow_mult=true`, there is no way (currently) for Riak to resolve conflicting writes other than to accept the last value written.

**Important**: Riak would also do a perfectly good job of preserving all writes under the Datomic model of creating immutable key/value pairs. It may seem like all databases should handle that scenario properly, but in fact some will throw away all writes on one side of the partition.

Kyle emphasizes what I mentioned in [part 1](http://basho.com/understanding-riaks-configurable-behaviors-part-1/) of this series: if you can’t create immutable objects, and don’t want to handle conflict resolution via the client, [CRDTs](https://github.com/basho/riak_dt) will allow for automatic resolution in the future, so long as you can make your data fit that model.

Kyle has [expanded his talk into a blog series](http://aphyr.com/tags/jepsen).

# RICON

Basho will be hosting two more [RICON conferences](http://ricon.io) this year, in San Francisco and London. As was true in New York City in May and San Francisco last fall, the talks will be streamed live over the Internet and would be well worth your time.

However, speaking from personal experience, the talks are just a portion of the overall value offered by RICON. It is difficult to convey the atmosphere during and between sessions, but even the afterparty was replete with technical discussions.

If you’ve not experienced it, you can [browse the #riconeast tag at Twitter](https://twitter.com/search/realtime?q=%23riconeast) for a feel for the reactions of those present (and those not) to the RICON experience, and please consider joining us next time.

RICON East videos should be available soon; the [album of RICON 2012 videos](http://vimeo.com/album/2258285) is recommended.

[John R. Daily](https://twitter.com/macintux)
