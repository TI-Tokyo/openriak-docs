---
title: "Clocks Are Bad, Or, Welcome to the Wonderful World of Distributed Systems"
date: "2013-11-12T17:53:58+00:00"
author: "John Daily"
original_url: "http://basho.com/posts/technical/clocks-are-bad-or-welcome-to-distributed-systems/"
archive_url: "https://web.archive.org/web/20170722130253http://basho.com/posts/technical/clocks-are-bad-or-welcome-to-distributed-systems"
categories:
  - "Architecture & Distributed Systems"
---
*November 12, 2013*

A [recent email thread](http://lists.basho.com/pipermail/riak-users_lists.basho.com/2013-October/013747.html) on the [Riak users](http://lists.basho.com/pipermail/riak-users_lists.basho.com/) mailing list highlighted one of the key weaknesses of distributed systems: clock consistency.

The first email:

> Occasionally, riak seems to not store an object I try to save. I have run tcpdump on the node receiving the request to ensure it is receiving the http packets with the correct JSON from the client. When the issue occurs the node is in fact receiving the request with the correct JSON.

Riak is designed to accommodate server and network failures without **ever** losing committed writes, so this led to a quick response from Basho’s engineers.

After some discussion, a vital piece of information was revealed:

> One other thing that might be worth mentioning here is the writes I’m mentioning are actually updates to existing objects. The object exists, an attempt to write an update for the object appears to be received by a node, but the object maintains it’s original value.

Riak was dropping *updates* rather than writes, which is a horse of a different color. To see why updates are much more problematic for any distributed database, read on.

## Concurrent Updates

In a database that runs on a single server, setting aside any complications introduced by transactions or locks, the second of two updates to the same record will overwrite the first. Last write wins.

With Riak’s simplest conflict resolution behavior, the second of two updates to the same object may or may not overwrite the first, even if those two updates are spaced far apart. Last write wins, **except when it doesn’t**, but even then it does.

Confused yet?

The problem is simple: there is no reliable definition of “last write”; because system clocks across multiple servers are going to drift.

On a single server, there’s one canonical clock, regardless of accuracy. The system can always tell which write occurred in which order (assuming that the clock is always increasing; setting a clock backwards can cause all sorts of bad behavior).

So, back to our original problem with lost updates:

> The nodes were a bit out of synch (up to 30 seconds… looking into why ntp wasn’t working!). So far it appears this was the issue.

If two updates to the same object occur within 30 seconds in such an environment, the end result is unpredictable.

## Taming the Beast

The conclusion drawn from the discussion was to implement (and, hopefully, to monitor) time synchronization. This is a step in the right direction, and one that every distributed system should implement, but there are more powerful and instructive lessons to impart.

## Background Reading

Some of this discussion requires awareness of siblings, vector clocks, and related arcana. If you wish to read more about these topics, Basho’s earlier blog post [Understanding Riak’s Configurable Behaviors: Part 1](http://basho.com/understanding-riaks-configurable-behaviors-part-1/) provides sufficient context. (You can find links in [the epilogue](http://basho.com/riaks-config-behaviors-epilogue/) to the full series, but part 1 covers the necessary background for this post.)

If instead you decide you’d like to avoid reading about and dealing with such complexities entirely, skip over the **Nitty Gritty** section to **The Land of Milk and Honey**.

# Nitty Gritty

## Vector Clocks

One approach that should generally be employed when writing Riak applications is to supply vector clocks with each update. It’s not clear in this particular scenario that it would have helped, but it certainly can’t hurt. Giving Riak more information to track causal history is never a bad thing.

~~See our documentation on vector clocks~~ for more information. And although the details are a bit dated, our blog post [Why Vector Clocks are Easy](http://basho.com/why-vector-clocks-are-easy/) makes for a nice overview of the concept.

## Forcing the Last Write to Win

A rather non-obvious approach is to take the default *last write wins* conflict resolution one step further.

As discussed in [part 1 of the configurable behaviors blog series](http://basho.com/understanding-riaks-configurable-behaviors-part-1/), there are two closely-related configuration parameters that determine how Riak approaches conflict resolution: `allow_mult` and `last_write_wins`. The former indicates whether Riak should keep all conflicts for the client to resolve; the latter is our concern at the moment.

If `allow_mult` is set to `false`, setting `last_write_wins` to `true` will instruct Riak to **always** overwrite existing objects, ignoring the timestamps stored with them.

So, nominally, this achieves what we earlier implied to be impossible: the last write truly does win, regardless of clock consistency.

The problem is that we’ve just punted the problem down the road a bit. Yes, all servers that receive an object will blindly write it, but any servers that **don’t** receive it due to network partition or server failure will still retain an older value, and depending on clock consistency the older value may still win once the network or server failure is corrected.

Broadly speaking, if you’re going to have data consistency problems, it’s best for that to be obvious and easily detectable during testing stages. This “solution’; would have made the situation much harder to recognize before production.

## Stopping Last Write Wins

At least in part to limit the complexity of developing applications, Basho decided to specify Riak’s default configuration as `allow_mult=false`, which requires the database to resolve conflicting writes internally.

As we’ve seen, Riak isn’t exactly a genius at resolving conflicting writes. Beyond the challenges of clock consistency, Riak treats objects as opaque and has no awareness of business logic.

It’s almost always better to bite the bullet: instruct Riak to retain all conflicting updates as siblings (via `allow_mult=true`) and write your application to deal with them appropriately.

**Note:** We are planning to change the default setting for `allow_mult` to `true` in Riak 2.0, but please check the documentation and your configuration before assuming either behavior.

# The Land of Milk and Honey

## Distributed data types

Creating data types that can survive network partitions and self-heal has long been a goal for our engineers. With Riak 1.4, Basho introduced [distributed counters](http://basho.com/counters-in-riak-1-4/); with 2.0, Riak will have a larger suite of distributed data types that can resolve conflicts internally, notably including sets and maps.

Although 2.0 is not yet released, a [technical preview is available](http://basho.com/introducing-riak-2-0/).

It is also possible to define such Riak Data Types (known formally as CRDTs) at the application layer. See the two-part blog series [Index for Fun and for Profit](http://basho.com/index-for-fun-and-for-profit/) and [Indexing the Zombie Apocalypse With Riak](http://basho.com/indexing-the-zombie-apocalypse-with-riak/) for more information.

## Strong Consistency

Also with 2.0, Riak will include the option of designating certain data as strongly consistent, meaning that the servers that hold a piece of data will have to agree on any updates to that data.

As appealing as that may sound, it is impossible to guarantee strong consistency without introducing coordination overhead and constraining Riak’s ability to continue to allow for requests when servers or networks have failed.

And aren’t low latency and high availability the reasons you’re using Riak?

## The Silver(\*) Bullet: Immutability

(\* or at least stainless steel)

The rise of “big data” is linked to a resurgence of interest in functional programming, which is particularly well-suited for processing large data sets. (See Dean Wampler’s Lambda Jam talk [Copious Data](http://www.infoq.com/presentations/big-data-functional-programming) for an interesting exposition of this idea.)

One of the key tenets of functional programming is that data is *immutable*, meaning that destructive updates are not (typically) allowed.

The relational data model does not offer much (any?) support for immutable data, but it is a powerful concept. At Basho’s [inaugural RICON conference](http://ricon.io/archive/2012/west.html) Pat Helland gave a talk entitled [Immutability Changes Everything](http://vimeo.com/52831373) which goes into more detail.

While it isn’t necessarily true that immutability *solves* everything with distributed systems, it’s a great start. Without data updates, there are no conflicts.

See [the configurable behaviors epilogue](http://basho.com/riaks-config-behaviors-epilogue/) (specifically, the discussion of Datomic) for a discussion of configuration tweaks to Riak to take better advantage of immutable data for low latency.

# TL;DR

If your distributed system isn’t explicitly dealing with data conflicts, any correct behavior it exhibits is more a matter of good luck than of good design.

If your distributed database relies on clocks to pick a winner, you’d better have rock-solid time synchronization, and even then, it’s unlikely your business needs are served well by blindly selecting the last write that happens to arrive.

Riak provides powerful tools for helping address the inherent challenges of distributed data, but they have to be used to be useful.

[John Daily](https://twitter.com/macintux)
