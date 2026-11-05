---
title: "Popular Use Cases for Mobile Platforms on Riak"
date: "2013-03-05T06:00:32+00:00"
author: "Basho"
original_url: "http://basho.com/posts/technical/popular-use-cases-for-mobile-platforms-on-riak/"
archive_url: "https://web.archive.org/web/20170801120831http://basho.com/posts/technical/popular-use-cases-for-mobile-platforms-on-riak/"
categories:
  - "Use Cases"
---
*March 5, 2013*

Mobile platforms need to provide always available, low-latency experiences that can scale to millions of users and support highly concurrent access. Riak’s redundant and fault-tolerant design ensures mobile data can be served quickly and reliably, and Riak is run in production by [many popular mobile applications](http://basho.com/riak-users/). For a full overview, check out the whitepaper “[Mobile on Riak: A Technical Introduction](http://info.basho.com/RiakonMobile.html).” Below are a few key mobile use cases and basic approaches to modeling them in Riak:

**User Data:** Storing user accounts, profile information, and events is a common use case for Riak. Mobile apps often store this data in JSON documents, using a UUID or other identifier as the key. Data can be queried through Riak features such as secondary indexes, MapReduce, and full-text search.

**Session Data:** Since session IDs are commonly stored in cookies, or otherwise known at lookup time, they are a natural fit for Riak’s key/value model and Riak can serve these requests at predictably low-latency. Session data can also be encoded in many different ways and evolve without any administrative changes to schema.

**Text & Multimedia Storage:** Since Riak is content agnostic, mobile platforms can easily store a variety of different types of data, including audio, text, photos, video, etc. to power mobile experiences.

**Social Authentication:** Many mobile applications have users sign in via their Facebook or Twitter accounts. Riak’s key/value scheme makes it easy to store both registered accounts and the tokens that make it possible for users to authenticate with their social accounts.

**Global Data Locality:** Riak Enterprise’s multi-datacenter capabilities mean mobile data can be stored in physical proximity to users and served at low-latency no matter where they happen to be.

Here is a chart with possible ways these applications and services can be modeled using Riak’s key/value design. Of course, your application should be structured in a way appropriate to its access and query patterns, among other factors – this is just to get you started. For more information on designing applications with Riak, [check out our documentation](http://docs.basho.com/riak/latest/cookbooks/use-cases/).

![](../images/popular-use-cases-for-mobile-platforms-on-riak/Screen-Shot-2013-03-05-at-4.45.16-PM.png)

To learn more about how mobile platforms can use Riak for their data needs, check out the complete overview, “[Mobile on Riak: A Technical Introduction](http://info.basho.com/RiakonMobile.html).” For more details about Riak and the latest 1.3 release, [sign up for our webcast](http://info.basho.com/IntroToRiakMarch7.html) on March 7th.

[Basho](http://www.twitter.com/basho)
