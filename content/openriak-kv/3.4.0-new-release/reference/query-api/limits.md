---
title: 'Query API limits and performance'
description: 'Record Query API scanning, filtering, buffering, aggregation, collation, and transformation limits.'
weight: 5
diataxis: 'reference'
product: 'OpenRiak KV'
product_version: '3.4.0'
status: 'editorially-rewritten'
draft: true
audience:
  - 'developers'
  - 'operators'
source_material:
  - 'source-code-release-notes-3.4'
  - 'openriak-quickdocs-3.4'
quickdocs_sources:
  - 'https://openriak.github.io/riak/QueryAPI.html#aggregation-of-combination-queries'
  - 'https://openriak.github.io/riak/QueryAPI.html#buffering'
  - 'https://openriak.github.io/riak/QueryAPI.html#central-collation-of-query-results'
  - 'https://openriak.github.io/riak/QueryAPI.html#filtering'
  - 'https://openriak.github.io/riak/QueryAPI.html#notes-on-implementation'
  - 'https://openriak.github.io/riak/QueryAPI.html#performance-and-efficiency'
  - 'https://openriak.github.io/riak/QueryAPI.html#scanning'
  - 'https://openriak.github.io/riak/QueryAPI.html#setup-and-distribute-the-query'
  - 'https://openriak.github.io/riak/QueryAPI.html#transformation-of-results'
tags: ['diataxis', 'kv', 'reference']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Record Query API scanning, filtering, buffering, aggregation, collation, and transformation limits.

## Details

### Performance and Efficiency

There are multiple stages to producing a query result:

- Setup and distribute the query;
  - parse the API request, validate the request, start a query server, find a coverage plan, initiate snapshots of all vnodes required for the query.
- Scan the index entries (concurrently across vnode backends);
  - read, deserialise and merge blocks of index entries at each level so that index entries within the range can be passed in key order to be evaluated and filtered.
- The filtering of each potential result within the range;
- The buffering and potential deduplication of results at the vnode level.
- the combination of query results using an aggregation expression.
- The collation, aggregation, deduplication and sorting of results at a cluster level.
- The transformation of results (into JSON) and transmission back as the API response.

As queries depend on all these parts, and all these parts are impacted differently by different factors it is not possible to precisely predict query response times.

> In general though, when scanning less than 10K entries and filtering to less than 1K results, most Riak clusters on modern hardware should be able to support **query latency of o(10) ms**.

#### Setup and Distribute the Query

The first stage, setup, is largely a fixed overhead regardless of query type.  The cost of the stage is primarily driven by the Ring Size of the cluster, which determines the number of snapshots that need to be taken in parallel.  A lower Ring Size will reduce the cost of this overhead, but in general a reduced Ring Size has a negative impact on performance - so reducing Ring Size with the intention to reduce query response times is not recommended.

> The latency introduced in the setup phase is generally **less than o(1) ms** for small and mid-sized clusters.

Note though, that requests for snapshots are added to the vnode queue on each vnode.

> On a busy cluster that query latency will be increased the delay of the longest vnode queue in the query coverage plan.

The query coverage plan will distribute the query to at least `RingSize div n_val` vnodes, and the size of the vnode queue is not a factor in the calculation of the plan.  Once the snapshot is taken, all other phases of the query are independent of the vnode queue.

> If there is significant network latency between nodes within a cluster, then that latency will impact the setup phase.  It is recommended to only use the Query API when network latency between cluster members is not significantly greater than 1 ms.

#### Scanning

The scanning stage of the query is in parallel with the filtering, buffering and collation of results.  As results are scanned they are passed into the query pipeline for continuous processing.

> In general a query should be able to scan, merge and select index entries at between **500K and 1M entries per CPU-core per second**.

Assuming there are multiple vnodes per CPU core in the cluster, all CPU cores may be potentially used in the fulfilment of the query.  Fair use of CPU cores is controlled by the Erlang scheduler not through the use of queues within the database.  In most mid-size clusters, 10M to 100M index entries can be scanned per second - however frequent use of queries which scan more than 1M index entries per second may have an impact on overall cluster performance.

Index entries are stored in blocks of around 30 entries, so there is minimal difference between scanning 1 entry per vnode, and scanning 100.  Each block must be decompressed and deserialised every time the block is scanned, there is no caching of deserialised index entries.  The only caching between queries is of a small amount of block metadata and natural promotion of blocks to the file system page cache.

> Spare memory will improve query performance by reducing disk wait times, but no database memory is ring-fenced for caching scanned index entries.

#### Filtering

The filtering stage requires the application of an optional filter, to validate projected attributes overloaded on the index entry to filter the result in or out of the query.  The standard way of filtering projected attributes is through the combination of an `evaluation_expression` (to extract the attributes) and a `filter_expression` (to test the attributes against query conditions).

> The overhead of combining an `evaluation_expression` and a `filter_expression` is normally between 20% and 60% depending on the complexity of the expressions.  Queries with a filter will generally only be able to process between **200K and 500K entries per CPU-core per second**.

Filtering results will reduce the cost of downstream processes significantly, especially deduplication, sorting and deserialisation.  These costs though are dependent on the `accumulation_option`, but only the `raw_count` option has minimal downstream costs.

> When using any `accumulation_option` other than `raw_count`, being more specific in the evaluation and filter of index entries will probably improve performance - regardless of the complexity of the required expressions.

#### Buffering

Once a result has been filtered it is added to the local per-vnode buffer for that query.  The buffer will aggregate results, and then for large queries periodically (based on the count of results added to the buffer) send interim result sets back to the query server - the process collating results across the cluster.  The query buffer will wait to receive a reply from the server before proceeding.

> The number of concurrent CPU cores that may be used by a query will be constrained by the delay awaiting an acknowledgement from the query server.  This delay will depend on network latency within the cluster and the work required in the collation phase for the chosen `accumulation_option`.  Lower latency clusters returning `raw_count` should normally scale to make use of **o(100) CPU cores per query**.  Higher latency clusters using `keys`, `count` or `term_with_keys` may not scale beyond **o(10) CPU cores per query**.

If `keys`, or `count` or `term_with_count` are used as the `accumulation_option` there is a need to deduplicate the results.  For `keys` this deduplication will occur centrally at the query_server; but this will have a significant impact on query performance as the number of filtered results grows.

For `count` and `term_with_count`, there is an optimisation to deduplicate results at the vnode level. However, even with this optimisation, for large numbers of post-filter results the overhead of deduplication may become a dominant factor in overall query cost and latency.

> At 10K filtered results per vnode, the deduplication overhead will typically be 10%, at 100K filtered results per vnode it will be around 50%, and at over 1M results per vnode the overhead may be an order of magnitude.

For each `accumulation_option` option there is a `raw` option that does not deduplicate the results.  Always use the `raw` option for large result sets if deduplication is not necessary.  For instance; if the application enforces cardinality rules so that each object may only have one entry on the index, or duplicate results can be handled by the application.

> A mid-size cluster should be able to `raw_count` **100M unfiltered index entries in less than 10 seconds**; however the `count` of such a result set could take o(100) seconds.

If using the `raw` option is not possible and a large result set is expected, then dividing the query into multiple sub-queries by range and accepting the increased per-query overhead is generally a better option than using the non-`raw` option.  The need for a `raw` option is unnecessary if combined result set sizes are less than 100K keys.

Partitioning of results is best done by breaking up the sort key range; the `max_results` option cannot be used on `count`-like queries.

The `max_results` (and then `continuation`) option may be used to partition results into multiple queries, but this is [only supported with the `terms` and `raw_keys` accumulation option]({{< product-version-root >}}reference/query-api/request/).

> When setting `max_results` with a `raw_keys` query, a `terms` query will be run internally, and the terms stripped before sending the keys in the response.  Setting `max_results` on a `raw_keys` query will therefore lead to the performance overheads of a `terms` query i.e. extra data transmitted within the cluster, and a sorting overhead at the query server.

#### Aggregation of Combination Queries

For combination queries, each query is run in-turn, and is always run.  Once all queries have been run the `aggregation_expression` is applied to the result set at the vnode level.

> In most scenarios, the distributed running of the `aggregation_expression` means that latency of that aggregation is not significant in overall query latency, as the set operations are performed on vnode-sized sets not cluster-sized sets.

If the `aggregation_expression` is based on `INTERSECT` there may be situations where the result set of latter queries are going to be intersected with an empty set, and therefore running the latter query is unnecessary:

> There is presently no optimisation that would not run queries based on partial completion of the `aggregation_expression`.

Aggregation queries, which use set expressions to combine results across multiple queries, do not use the query buffer until all queries are complete and the `aggregation_expression` has been applied on that vnode's results.

> As the query buffer is bypassed a cancelled query will not terminate early for combination queries.

Support for `aggregation_expression`s in Riak 3.4 is a work in progress and may [be optimised in future releases]({{< product-version-root >}}foundations/data-model/query-api/).

#### Central Collation of Query Results

The query server which prompted the setup of the query, will also be responsible for collation of results.  This server will always reside on the node which received the query request.

> It is important to distribute query requests evenly across a cluster due to the overheads of collation, and if necessary mark down nodes with specific temporary overheads within the load-balancer's active configuration.

The query server will acknowledge results received in batches, but for `count`, `term_with_count` and `term_with_rawcount` queries only a `ping` will be sent for acknowledgement.  For these queries partial result sets are not collated, just the final result for the vnode.

The `keys` and `term_with_keys` result set both require sorting on the query server.  The sorting takes place in parallel to vnode querying and batches of results arrive, but may delay the query server in acknowledging results.  The vnode queries cannot outrun the centralised sorting process.

#### Transformation of Results

The final stage of handling the request is the formation of the response into a JSON message.  The cost of this stage is directly linked to the size of the final result set, although this is normally a minority of the overall cost.

There is no protection against overloading memory with the results of an individual query.

> The node handling the request must have enough memory to hold all the results in memory, and during transformation the memory overhead may be doubled.  Consideration of this is required, especially when running non-`count` queries that return o(10m) results or greater.
