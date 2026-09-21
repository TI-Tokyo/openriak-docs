---
title: Build and query a people-search index
description: Load three people, find their keys by surname, and fetch a matching profile. Use the Leveled learning
  cluster and active `docs` bucket type from the earlier exercises. You also need Python 3.
weight: 210
diataxis: tutorial
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- developers
source_material:
- openriak-quickdocs-3.4
quickdocs_sources:
- https://openriak.github.io/riak/QueryAPI.html#example-1---a-simple-people-search-index
- https://openriak.github.io/riak/QueryAPI.html#example-1---finding-an-exact-match
- https://openriak.github.io/riak/QueryAPI.html#example-1---inexact-match
- https://openriak.github.io/riak/QueryAPI.html#example-1---inexact-match-of-given-name
- https://openriak.github.io/riak/QueryAPI.html#example-1---more-extensible-index-schema
- https://openriak.github.io/riak/QueryAPI.html#example-1---simple-range-query
- https://openriak.github.io/riak/QueryAPI.html#example-1---wildcards-within-terms
- https://openriak.github.io/riak/QueryAPI.html#example-2---an-alternative-people-search
- https://openriak.github.io/riak/QueryAPI.html#example-2---simple-variations-and-limitations
- https://openriak.github.io/riak/QueryAPI.html#example-3---reporting-index
- https://openriak.github.io/riak/QueryAPI.html#example-3---simple-variations-and-limitations
- https://openriak.github.io/riak/QueryAPI.html#secondary-indexes---adding-index-entries-to-an-object
tags:
- diataxis
- kv
- tutorial
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- tutorials/query-api/build-search-index.md
related:
- tutorials/indexes-and-querying/search-projected-attributes
- how-to/indexes-and-queries/add-and-query-secondary-indexes
- reference/data-model-contracts/secondary-index-terms-and-projected-attributes
- reference/query-api/endpoints-and-request-schema
- foundations/indexes-and-querying/secondary-indexes-and-projected-attributes
- foundations/indexes-and-querying/how-distributed-queries-execute
- foundations/indexes-and-querying/query-cost-and-result-delivery
next_page: tutorials/indexes-and-querying/search-projected-attributes
previous_page: tutorials/data-and-concurrency/estimate-unique-activity-with-hyperloglog
---

Load three people, find their keys by surname, and fetch a matching profile. Use the Leveled learning cluster and active `docs` bucket type from the earlier exercises. You also need Python 3.

## Load the people

Download [people.py]({{< baseurl >}}openriak-kv/examples/people.py) into your working directory. The fixture contains Aiko Ng in Tokyo, Sam Ng in Osaka, and Wei Li in Tokyo. Their ages are deliberately chosen sample values: 29, 34, and 41.

```sh
export RIAK_HTTP=http://127.0.0.1:18098
python3 people.py
```

Each printed key should have a successful write status. The script stores full objects plus surname, city, and projected-attribute index terms. On reruns it preserves the context it reads rather than blindly overwriting an existing object.

## Find a surname

Create `query.json` with:

```json
{
  "accumulation_option":"keys",
  "query_list":[{"index_name":"family_bin","start_term":"Ng","end_term":"Ng"}]
}
```

Submit it:

```sh
curl --fail -H 'Content-Type: application/json' --data-binary @query.json   "$RIAK_HTTP/types/docs/buckets/people/query"
```

The result contains the keys `aiko` and `sam`. Do not depend on a guessed ordering. Change both boundaries to `Li` and check that only `wei` matches.

## Fetch the object

```sh
curl --fail "$RIAK_HTTP/types/docs/buckets/people/keys/aiko"
```

You now have the profile body rather than just an index match. Keep the three records for the next four lessons. If the query reports an unsupported operation, verify that every participating node uses Leveled and that the cluster has finished starting.
