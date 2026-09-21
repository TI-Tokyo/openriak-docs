---
title: Retrieve a larger result set
weight: 250
product: OpenRiak KV
product_version: 3.4.0
diataxis: tutorial
draft: true
status: editorially-rewritten
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
description: Retrieve all three people using secondary-index continuations and verify the combined result.
related:
- tutorials/indexes-and-querying/produce-counts-and-grouped-results
- reference/query-api/continuations-and-result-delivery
- reference/query-api/accumulation-modes
- how-to/indexes-and-queries/retrieve-paginated-or-asynchronous-query-results
- foundations/indexes-and-querying/secondary-indexes-and-projected-attributes
- foundations/indexes-and-querying/how-distributed-queries-execute
- foundations/indexes-and-querying/query-cost-and-result-delivery
previous_page: tutorials/indexes-and-querying/produce-counts-and-grouped-results
---

Retrieve the three people in small pages, preserving the continuation between requests. Continue with the dataset from the preceding index lessons. This exercise uses the secondary-index HTTP endpoint and needs Python 3 on your workstation.

## Fetch one key at a time

Save this as `page_people.py`. The page size of one is deliberately small so you can see the continuation change.

```python
import json
import os
from urllib.parse import urlencode
from urllib.request import urlopen

endpoint = os.environ["RIAK_HTTP"].rstrip("/") + "/types/docs/buckets/people/index/family_bin/A/Z~"
continuation = None
keys = []
while True:
    parameters = {"max_results": 1}
    if continuation:
        parameters["continuation"] = continuation
    with urlopen(endpoint + "?" + urlencode(parameters), timeout=30) as response:
        result = json.load(response)
    print(result)
    keys.extend(result["keys"])
    continuation = result.get("continuation")
    if not continuation:
        break
assert sorted(keys) == ["aiko", "sam", "wei"], keys
print("Retrieved all three people")
```

Run the saved program:

```sh
python3 page_people.py
```

You should see the keys spread across responses, followed by `Retrieved all three people`. A final empty page is harmless if it has no continuation.

## Inspect the continuation

The program passes the opaque token back to the same endpoint using URL encoding. Keep the bucket, index, and range unchanged between requests. Do not edit the token or treat it as a bookmark that survives arbitrary query changes.

## Choose a delivery interface

The secondary-index endpoint returns its continuation in the JSON body. The Query API has a separate `X-Riak-Continuation` response header and request contract; the tokens are not interchangeable. See [Continuations and result delivery]({{< product-version-root >}}reference/query-api/continuations-and-result-delivery/) before adapting this exercise to the Query API.

## Cleanup

Delete the three known keys under `/types/docs/buckets/people/keys/` when finished, and remove `page_people.py`. Keep the cluster if continuing with operations lessons.
