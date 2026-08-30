---
title: "Where To Start With Riak Core"
date: "2011-04-12T21:54:14+00:00"
author: "Mark Phillips"
original_url: "http://basho.com/posts/technical/where-to-start-with-riak-core/"
archive_url: "https://web.archive.org/web/20170427133143http://basho.com/posts/technical/where-to-start-with-riak-core"
categories:
  - "Architecture & Distributed Systems"
---
*April 12, 2011*

There has been a lot of buzz as of late around “riak\_core” in various venues, so much so that we are having trouble producing enough resources and content to keep the community at bay ([though we most-certainly have plans to](http://lists.basho.com/pipermail/riak-users_lists.basho.com/2011-April/003744.html)). While we hustle to catch up, here is the rundown on what is currently available for those of you who want to learn about, look at, and play with riak\_core.

(TL;DR – riak\_core is the distributed systems framework that underpins Riak and is, in our opinion, what makes Riak the best and most-robust distributed datastore available today. If you want so see it in action, go [download Riak](http://info.basho.com/Riak-Open-Source-Download.html) and put it through its paces.)

**Blogs**

If you know nothing about riak\_core (or are in the mood for a refresher), start with the [Introducing Riak Core](http://basho.com/posts/business/introducing-riak-core/) blog post that appeared on the Basho Blog a while back. This will introduce you, at a very high-level, to what riak\_core is and how it works.

**Slides and Videos**

There are varying degrees of overlap in each of these slides and videos, but they all address riak\_core primarily.

- [“Building Distributed Systems With Riak and Riak Core”](http://www.slideshare.net/argv0/riak-coredevnation)
- [Riak Core: An Erlang Distributed Systems Toolkit Slides](http://www.erlang-factory.com/upload/presentations/372/AndyGross-RiakCore-EFSFBay2011.pdf) and [Video](http://vimeo.com/21772889)
- [Masterless Distributed Computing with Riak Core Slides](http://www.slideshare.net/rklophaus/masterless-distributed-computing-with-riak-core-euc-2010) and [Video](http://vimeo.com/18758206)
- Riak Core: Dynamo Building Blocks (PDF) (Note, link no longer active)
- [Riak From The Inside](http://www.erlang-factory.com/upload/presentations/255/RiakInside.pdf)
- [Riak’s Distributed Storage Architecture](http://vimeo.com/17146260)

**Code**

- [riak\_core repo on GitHub](https://github.com/basho/riak_core)
- Basho Banjo – Sample application that uses Riak Core to play distributed music (Note, link no longer active)
- [Try Try Try](https://github.com/rzezeski/try-try-try) – Ryan Zezeski’s working blog that is taking an in depth look at various aspects of riak\_core
- [rebar\_riak\_core](https://github.com/websterclay/rebar_riak_core) – Rebar templates for riak\_core apps from the awesome team at Webster/Clay

**Getting Involved With Riak and Riak Core**

We are very much as the beginning of what Riak Core can be as a stand-alone platform for distributed applications, so if you want to get in at the ground floor of something that we feel is truly innovative and unparalleled, now is the time. The best way to join the conversation and to help with the development of Riak Core is to join the [Riak Mailing list](http://lists.basho.com/mailman/listinfo/riak-users_lists.basho.com) where you can start asking questions and sharing code.

If you want to see riak\_core in action, look no further than [Riak](https://github.com/basho/riak), [Riak Search](https://github.com/basho/riak_search), and [Luwak](https://github.com/basho/luwak). The distribution and scaling components for all of these projects if handled by riak\_core.

Also, make sure to follow the Basho Team on Twitter as we spend way too much time talking about this stuff.

[Mark](https://twitter.com/pharkmillups)
