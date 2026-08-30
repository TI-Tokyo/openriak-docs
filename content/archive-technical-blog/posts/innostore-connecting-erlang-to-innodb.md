---
title: "Innostore — connecting Erlang to InnoDB"
date: "2010-01-26T21:17:13+00:00"
author: "Justin Sheehy"
original_url: "http://basho.com/posts/technical/innostore-connecting-erlang-to-innodb/"
archive_url: "https://web.archive.org/web/20170801120927http://basho.com/posts/technical/innostore-connecting-erlang-to-innodb/"
categories:
  - "Integrations & Plugins"
  - "Erlang & BEAM"
---
*January 26, 2010*

Riak has pluggable storage engines, and so we’re always on the lookout for better ways that users can store their data locally. Recent experiences with some Basho customers managing some large datasets led us to believe that InnoDB might work out very well for them.

To answer that question and fill that need, [Innostore](https://github.com/basho/innostore) was written. It is a standalone Erlang application that provides a simple interface to Embedded InnoDB. So far its performance has been quite good, though InnoDB (with or without the Innostore API) is highly dependent on tuning the local configuration to match the local hardware. Luckily, Dizzy — the author of Innostore — has some heavy-duty experience doing that kind of tuning and as a result we’ve been able to help people meet their performance goals using Innostore.

[-Justin](http://www.twitter.com/justinsheehy)
