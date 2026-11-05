---
title: "The Release Riak 0.8 and JavaScript Map/Reduce"
date: "2010-02-03T21:54:40+00:00"
author: "Basho"
original_url: "http://basho.com/posts/technical/the-release-riak-0-8-and-javascript-mapreduce/"
archive_url: "https://web.archive.org/web/20170716204850http://basho.com/posts/technical/the-release-riak-0-8-and-javascript-mapreduce/"
categories:
  - "Releases"
  - "Search & Analytics"
---
*February 3, 2010*

We are happy to announce the release of Riak 0.8 available for [download](http://docs.basho.com/riak/latest/downloads/) immediately. Riak 0.8 features a number of enhancements to the core map/reduce machinery that will make Riak more accessible to a wider audience. The biggest enhancement is the ability to write map/reduce queries in JavaScript. We’re using our [erlang\_js](https://github.com/basho/erlang_js) project to integrate Mozilla’s Spidermonkey engine directly into Riak to keep overhead to a minimum.

We’ve also built a spiffy REST API for submitting map/reduce queries. Queries are described in JSON and POST-ed to the Riak server. Results are sent back as JSON for your processing pleasure. And, the REST interface supports streaming results for large result sets, too.

To kick it all off, we’ve put together a short screencast demonstrating how to use Riak’s flashy new features. You can watch it below, or [view it on Vimeo.](http://vimeo.com/9188550) There’s also a slew of bug fixes and optimizations included in Riak 0.8. See [the release notes](http://lists.basho.com/pipermail/riak-users_lists.basho.com/2010-February/000387.html) for all the juicy details.

Download and enjoy!

[View on Vimeo](http://vimeo.com/9188550)
