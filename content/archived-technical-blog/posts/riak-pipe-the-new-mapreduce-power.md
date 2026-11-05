---
title: "Riak Pipe – the New MapReduce Power"
date: "2011-09-19T01:29:15+00:00"
author: "Bryan Fink"
original_url: "http://basho.com/posts/technical/riak-pipe-the-new-mapreduce-power/"
archive_url: "https://web.archive.org/web/20170801115150http://basho.com/posts/technical/riak-pipe-the-new-mapreduce-power/"
categories:
  - "Search & Analytics"
---
*September 19, 2011*

A few months ago, I [announced](http://lists.basho.com/pipermail/riak-users_lists.basho.com/2011-June/004550.html) the opening of [Riak Pipe](https://github.com/basho/riak_pipe), as well as two goals for the project. With the upcoming 1.0 release of Riak, we have achieved the first goal: new clusters will use Riak Pipe to power their MapReduce processing. Existing clusters will also be able to migrate to using Riak Pipe, with no changes needed from the client perspective.

There are a few reasons you should be excited about running your MapReduce queries on Riak Pipe. First and foremost, Riak Pipe is designed as a work distribution system, and as such, **it is** **better able to take advantage of the parallel resources available in****the cluster**. One small example of how Riak Pipe achieves this is simply by splitting the “map” phase processing into two steps: fetching the object from Riak KV, and transforming it. This allows the work of each step to happen in parallel; the next input will be fetched while the transformation of the last one is in progress.

Riak Pipe also recognizes that a cluster’s resources are finite, and that sometimes it’s better to delay one pile of work in order to make progress on another. Processing phases in Riak Pipe, called *fittings*, provide **backpressure to fittings** **upstream** from them by means of limiting the sizes of their input queues. The upstream fittings pause their processing when the downstream queues are full, **freeing up system** **resources** (or at least not increasing their consumption) to allow those downstream processes a chance to catch up.

Input queues are another example of Riak Pipe’s parallel resource use. **Inter-phase results are delivered directly** from a vnode running one stage to the vnode that will process them for the next stage. Since they are **not forced through a single,** **central process**, the memory of the entire cluster can be used to move them around, instead of requiring a single machine’s memory to handle them.

The KV-object fetching stage of the new Riak Pipe MapReduce system is also **much more of a well-behaved KV user**. That is, the requests it makes are much more fairly balanced with respect to regular Riak KV operations (get, put, etc.). This means MapReduce on Riak Pipe should have **much less impact on the** **performance** of rest of your Riak use.

Using Riak Pipe MapReduce is simple. Make sure that the setting `{mapred_system, pipe}` is in the `riak_kv` section of your cluster’s `app.config`, and then … just send MapReduce queries over HTTP or Protocol Buffers as you always have. The results should be the same. There are a few knobs you can tweak, which control batching of reduce phase evaluation, but the goal of this release was a **100% compatible implementation of the** **existing MapReduce functionality**.

There is much more on the horizon for Riak Pipe, including more efficiency gains and exposing some of the new processing statistics it tracks, not to mention exposing more of its functionality beyond Riak KV’s MapReduce. We’re very excited about the future.

If you would like to learn more about Riak Pipe, in general, and get involved, I recommend paging through [the README](https://github.com/basho/riak_pipe/blob/master/README.org) to get an idea of its structure, and then browsing [the new Riak KV MapReduce code](https://github.com/basho/riak_kv/blob/master/src/riak_kv_mrc_pipe.erl) for some examples.

–[Bryan](http://twitter.com/hobbyist)
