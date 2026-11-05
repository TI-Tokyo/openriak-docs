---
title: "BashoChats 001 – Erlang and DTrace; Storm and Distributed RPC"
date: "2011-12-21T02:27:40+00:00"
author: "Mark Phillips"
original_url: "http://basho.com/posts/technical/bashochats-001-erlang-and-dtrace-storm-and-distributed-rpc/"
archive_url: "https://web.archive.org/web/20170801120851http://basho.com/posts/technical/bashochats-001-erlang-and-dtrace-storm-and-distributed-rpc/"
categories:
  - "Erlang & BEAM"
  - "Community & Events"
---
*December 21, 2011*

The [inaugural BashoChats](http://www.meetup.com/BashoChats/events/43849732) was held just under a week ago at BashoWest in San Francisco. About 30 local developers came out to have a few beers on Basho’s tab and discuss distributed systems and databases. If you’re local to the Bay Area and/or want to keep an eye on what we have planned, [join the group](http://www.meetup.com/BashoChats). There are some great talks in the pipeline…

Most importantly I’m happy to report that both talks from the evening are now online for your viewing pleasure.

Enjoy. Hope to see you next month.

[Mark](https://twitter.com/#!/pharkmillups)

**DTrace and the Erlang VM**

[Andy Gross](https://twitter.com/#!/argv0) opened up the evening with just under 30 minutes on the current work happening at Basho and a few other companies to bring [DTrace](http://en.wikipedia.org/wiki/DTrace) to Erlang VM. He starts off with some general information on both components and then goes in-depth on how they can be used to profile a running Riak installation.

Repo [here on GitHub](https://github.com/argv0/dtrace-erlang-bashochat-12142011) with the code he used for the examples in his presentation.

**Computing Reach Using Storm Distributed RPC**

After Andy concluded, [Nathan Marz](http://nathanmarz.com/about/) gave an overview of [Storm](https://github.com/nathanmarz/storm), a framework he and his team at BackType built for distributed and fault tolerant realtime computation. He takes us through some Storm basics and then demonstrates how it is used to compute reach using distributed RPC.
