---
title: Secondary Indexes
sidebar_label: "2i"
date: 2026-08-18
---
[root site]: [!site]
[root project]: [!project]
[root version]: [!version]

>[!MEMO]OpenRiak includes a Query API to allow you to interact with Secondary Indexes which can be added to OpenRiak objects.
>The API supports range queries, to be run across the sorted terms on an index, but the terms may also contain projected attributes appended to the sort key. The Query API can be passed evaluation and filter expressions: to first evaluate the term to extract the attributes, and then filter the terms by testing the attribute values against query conditions.

Through this combination of querying ranges and filtering on projected attributes, the API can support conjunction queries. The capability and efficiency of these conjunction queries is dependent on work in the application to map the object schema to a set of index terms with a suitable combination of sort keys and attributes. The queries are distributed across the cluster, running in parallel across different partitions of the data (the vnodes); and through that parallelism offer low-latency responses to relatively complex queries, even where significant numbers of index entries are covered by the range of the query.

The Query API isnt just limited to returning lists of object keys, there is also support for different accumulation options. As well as returning object keys, accumulation options can be used to efficiently count results, and group both results and counts by specific projected attributes.

Queries are by default synchronous with the full result-set sent directly back to the requesting process on completion of the query. Queries may be asynchronous, with results queued on-disk (to control memory use) to be consumed in batches by one or more external processes, with results available for consumption prior to the completion of the query.

As well as single queries the API can also handle combination queries. In combination queries, multiple queries are run as part of the same request and the results of each query are combined using a set operation before results are accumulated to construct the response. Those set operations are also distributed across the cluster for efficiency; the application of a set operation happens at the scale of the vnode, not the scale of the cluster. All combination queries are run on a single snapshot per vnode; so the results should always be consistent from the perspective of each potential key in the result set.

# Query Definitions

## API Endpoint

All queries must be sent to the Query endpoint for the Bucket (and Bucket-type if these are used). The two examples below show the endpoint for both Bucket and Bucket-Type options using the `POST` method.

For Bucket-type:

    ```bash
        POST /types/<BucketType>/buckets/Bucket/query
    ```

For untyped/legacy Buckets:

    ```bash
        POST /buckets/<bucketname>/query
    ```

If the accumulation options `queue_raw_keys` or `queue_raw_terms` are used then an opaque reference will be returned as the value of `result_queue` in the JSON response to the query request. Results may be fetched from the same URL, using the `GET` method with the reference to the `result_queue` passed as a query parameter. There is also an optional parameter `max_results` which will put an upper limit on the number of results sent back in the batch, helping to reduce the load per request.
The example below is a `GET` for the `result_queue` output:

    ```bash
        GET types/BucketType/buckets/Bucket/query?result_queue=g2gDdw5kZXYxQDEyNy4wLjAuMVh3DmRldjFAMTI3LjAuMC4xAAAMdwAAAABpPGQWbQAAAARkjfJI?max_results=1000
    ```

>[!NOTE]The `result_queue` reference can be queried and decoded by any node in the cluster. The result requests for queued batches can also be distributed across the cluster to reduce load on individual nodes.

## Query JSON

The query should be in the HTTP request body and sent to the query API for the correct bucket. The JSON you include should have the required keys at the root of the file.

### Parts of a query

Each query contains the following:

* `aggregation_tag` (Optional)
    * Required if an only if an `aggregation_expression` is used
* `index_name` (Required - should be a binary index)
* `start_term` (Required)
* `end_term` (Required)
* `evaluation_expression` (Optional)
    * An expression to extract projected attributes from the term.
* `filter_expression` (Optional)
    * An expression to filter results based on those projected attributes.
    * Must be included if an evaluation_expression is included in the query, but can simply test attribute_exists($key) if no filter is required.
* `regular expression` (Optional)
    * Alternative to using evaluation or filter expressions, which can potentially be used to improve the performance of queries.
    * Must not be included if filter/evaluation expressions form part of the quer

The following are options to be included in the query;

1. `aggregation_expression` (Optional)
    * If multiple queries are to be run, the aggregation expression is used to inform the database how those results should be combined, using $1, $2 etc to refer to the numeric `aggregation_tag` for each query - with the key words UNION, INTERSECT and SUBTRACT to show how the sets of results are to be combined. Parenthesis may be used for clarity. e.g. ($1 INTERSECT $2) UNION ($3 SUBTRACT $1)

2. `accumulation_option` (Optional - default = keys)

There are multiple options for accumulating the results from a single query:

    * `keys`; return a list of keys that matched in the query, where the keys have been deduplicated and sorted.
    * `raw_keys`; return a list of keys that matched in the query, but in no specific order and where multiple matches for the same key will result in that key appearing multiple times within the results.
    * `queue_raw_keys` Available from OpenRiak 3.4.1; return a reference to a queue, where the results will be streamed to be consumed in batches of keys from any node by one of more external processes. The results will be the same as `raw_keys`, the only difference is the method of returning the results.
    * `terms`; returns a list of term/key pairs, ordered by term.
    * `raw_terms`; return a list of term/key pairs, unsorted.
    * `queue_raw_keys` Available from Riak 3.4.1; return a reference to a queue, where the results will be streamed to be consumed in batches of term/key pairs from any node by one of more external processes. The results will be as in raw_terms, the only difference is the method of returning the results.
    * `count`; return a count of unique keys that matched the query.
    * `raw_count`; return a count of matches against the query (i.e. unlike count if an object key appears against multiple terms matched within the query, with raw_count that key will be counted multiple times).
    * `term_with_count`; return a count of unique key matches by term (where term is specified by the accumulation_term) in no specific order.
    * `term_with_rawcount`; return a count of key matches by term (where term is specified by the `accumulation_term`) in no specific order, where a key which appears multiple times under that term will be counted multiple times.

In some circumstances, there are constraints on the `accumulation_option` which can be used:

    * If an `aggregation_expression` is added to the query (i.e. it is a combination query), only `raw_keys` and `raw_count` are valid accumulation options.
    * If a `max_results` setting is added to the query, then only `terms` and `raw_keys` are valid accumulation options.

3. `accumulation_term` (optional - default = `$term`)

When using an accumulation option of `terms`, `raw_terms`, `term_with_rawcount` or `term_with_count`; the `accumulation_term` is the projected attribute returned from the evaluation function to be used as the term in the accumulator. The default is `$term` - the whole term.

4. `max_results` (Optional)

The potential to limit the number of results returned by the query, to the first `N` results. The query will stop once enough results have been returned, and a `continuation` term will be returned along with the results, which can be passed into a subsequent query to return the next set of results after this point. This allows for pagination of results.

    * The Max results option is only supported with an `accumulation_option` of `terms` or `raw_keys`.
        * Only the `terms` accumulator is able to make a reliable continuation point.
        * Internally if using `raw_keys` with `max_results`, then the query will run as a terms query, with the terms being stripped immediately prior to returning a response.

>[!NOTE]Note on paging queries
>As queries are distributed, and there is minimal difference to performance for fetching 1 or 10K results, then pagination will not be efficient for user-facing page sizes (e.g. small batches of 10). Instead, it is normally more efficient to fetch larger batches of results and cache them within the application.

5. `continuation` (Optional)

A string returned from a previous query constrained by `max_results`, this is used to indicate the starting point for the next page of results.

6. `substitution` (Optional)

An array of key/value pairs that can be used inside filter or evaluation expressions. When an expression includes a substitution key (prefixed by :), that key is replaced with its corresponding value before the query process parses the expression.

For example, you could pass:

    ```bash
    {"low_dob": "19550301", "high_dob": "19560630"} 
    ```

As substitutions to evaluate:

    ```bash
        $dob BETWEEN ":low_dob" AND ":high_dob"`
    ```

All substitution values should be all strings.

7. `timeout` (Optional)

The amount of time to wait for the query to complete, before returning a timeout error in seconds.

>[!NOTE]Note on timeouts
>This is the timeout used by the server, other HTTP timeouts may exist on the path to OpenRiak, in particular in the OpenRiak client. You should ensure those timeouts are noted to avoid confusion.

8. `query_list` (Required)

A list of one or more queries. This should be a list of just one query unless an `aggregation_expression` has been included in the main query block.