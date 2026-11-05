---
title: "Counters in Riak 1.4"
date: "2013-07-29T20:41:10+00:00"
author: "Basho"
original_url: "http://basho.com/posts/technical/counters-in-riak-1-4/"
archive_url: "https://web.archive.org/web/20170309194557http://basho.com/posts/technical/counters-in-riak-1-4/"
categories:
  - "Data Modeling"
  - "Releases"
---
*July 29, 2013*

For those of you who are up on your [RICON](http://ricon.io/) history, you’ll remember that last year, Basho Hackers Russell Brown and Sean Cribbs gave a talk called “[Data Structures in Riak](https://speakerdeck.com/basho/data-structures-in-riak)” (video can be viewed [here](https://vimeo.com/52414903)). Russell and Sean detailed the approach that Basho was taking to add eventually consistent data structures to Riak. The highlight of the presentation was a demonstration of incrementing and decrementing a counter using a sample app built with [riak\_dt](https://github.com/basho/riak_dt). A simple counter was incremented. During this, nodes were killed, network partitions were introduced, and despite all that, counts converged once the cluster healed.

It was one of the more memorable moments of the entire conference.

We believe developers can build robust applications utilizing a simple key/value API. GETs, PUTs, and DELETEs can work wonders when utilized correctly. But this doesn’t let you build everything on Riak, and we’ve seen a fair amount of applications that outsource things – like data type operations – to other storage or caching systems. Especially when porting apps from Redis to Riak, we often hear that counters are one feature that Riak lacks. Basho is firmly in the “right-technology-for-the-right-job” camp but we’re aggressively adding functionality that doesn’t break Riak’s design goals of availability and fault-tolerance.

As of the [Riak 1.4 release](http://basho.com/basho-announces-availability-of-riak-1-4/), counters are officially supported. Specifically, a data type known as a PN-Counter, which can be both incremented and decremented. This is the first of a suite of data types we’re planning to add (more on this in a moment) that give developers the ability to build more complex functionality on top of data stored as keys and values.

## Use Cases

Using counters, you can increment and decrement a count associated with a named object in a given bucket. This sounds easy, but in a system like Riak where writes aren’t serialized and all updates are asynchronous, determining the last actor in a series of updates to an object is non-trivial. Riak’s counters should be used (in their current state) to count things that can tolerate eventual consistency. With that in mind, here are a few apps and types of functionality that could be implemented with Riak’s Counters:

- Facebook Like Button
- Youtube Views and Likes
- Hacker News Votes
- Twitter Followers and Favorites

The thing to remember here is that these counts can tolerate slight, brief imprecision. When your follower count fluctuates between 1000 and 1010 before finally settling on 1009, Twitter continues to work as expected. Riak 2.0 will feature work that enables you to enforce consistency around designated buckets which will solve this problem (with the necessary tradeoffs). Until then, use counters in Riak for things that can tolerate eventual consistency.

Even with this caveat, counters are a huge addition to Riak and we’re excited to see the new suite of applications and functionality they make possible.

## Usage & Getting Started

To make use of counters we’ve introduced new endpoints and request types for the HTTP and Protocol Buffers APIs, respectively.

### HTTP

The complete documentation for the HTTP interface is [here](http://docs.basho.com/riak/latest/dev/references/http/counters/). Here are the basics using CURL:

That’s it.

### PBC

Usage documentation for this is still in the works, but here’s the relevant message (as seen in [riak\_pb](https://github.com/basho/riak_pb/blob/1.4.0.7/src/riak_kv.proto#L234-L262)):

We’re working on implementing these in all of Basho supported client libraries. Keep an eye [on these](http://docs.basho.com/riak/latest/dev/using/libraries/) for details and timelines around availability. We currently support counters in the following libraries across the following protocols:

- Python – HTTP and PB
- Java – HTTP and PB
- Erlang – PB

In addition to the docs and code, Basho Hacker Sam Elliot has started a [Riak CRDT cookbook](https://github.com/basho/riak_crdt_cookbook/blob/master/counters/README.md). The first section walks you through using counters in a few different ways, and even shows you how to simulate failure events. Take it for a spin and send Sam some feedback.

## Future Data Types

In addition to counters, we have big plans for more data types in Riak. Sets and maps are on the short list, and the goal is to have these ready for Riak 2.0. Russell posted an [extensive RFC](https://github.com/basho/riak/issues/354) on the Riak GitHub repo for those interested. Comments, critiques, and contributions are all encouraged.

## Related Work and Additional Reading

- [A simple way to store a PN-Counter in a riak\_object](https://github.com/basho/riak_kv/pull/536)
- [Release Notes on Counters](https://github.com/basho/riak/blob/master/RELEASE-NOTES.md#data-types)
- [CRDT paper from Shapiro et al. at INRIA](http://hal.upmc.fr/docs/00/55/55/88/PDF/techreport.pdf)
- [riak\_dt](https://github.com/basho/riak_dt)

Enjoy and see you at [RICON West](http://ricon.io/west.html) in October.

[Mark](http://twitter.com/pharkmillups) and [The Basho Team](http://twitter.com/basho)
