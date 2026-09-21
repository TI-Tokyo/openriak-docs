---
title: Create and resolve concurrent updates
weight: 160
product: OpenRiak KV
product_version: 3.4.0
diataxis: tutorial
draft: true
status: editorially-rewritten
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
description: Create two concurrent values for one object, read the siblings, and resolve them into one value. Complete
  the bucket-type exercise first.
related:
- tutorials/data-and-concurrency/apply-different-policies-with-bucket-types
- tutorials/data-and-concurrency/practise-conditional-updates
- how-to/application-data/resolve-concurrent-object-updates
- reference/data-model-contracts/causal-context-and-version-vector-representations
- foundations/data-and-consistency/objects-keys-and-buckets
- foundations/data-and-consistency/causality-version-vectors-and-siblings
- foundations/data-and-consistency/conflict-free-replicated-data-types
previous_page: tutorials/data-and-concurrency/apply-different-policies-with-bucket-types
next_page: tutorials/data-and-concurrency/practise-conditional-updates
---

Create two concurrent values for one object, read the siblings, and resolve them into one value. Complete the bucket-type exercise first.

## Make independent writes

Use a fresh key in the sibling-preserving `docs` type. The writes deliberately omit causal context:

```sh
key="conflict-$(date +%s)"
url="$RIAK_HTTP/types/docs/buckets/learning/keys/$key"
curl --fail -i -X PUT "$url" -H 'Content-Type: text/plain' --data-binary 'red'
curl --fail -i -X PUT "$url" -H 'Content-Type: text/plain' --data-binary 'blue'
curl -D siblings.headers -H 'Accept: multipart/mixed' "$url"
```

Expect a multiple-values response with both contents. Inspect the multipart sections; do not treat the multipart envelope itself as the value to save.

## Resolve the object

For this exercise the application rule combines the two colours into the text `red,blue`. Preserve the context returned with the sibling response:

```sh
context=$(awk 'tolower($1)=="x-riak-vclock:" {gsub("\r", "", $2); print $2}' siblings.headers)
test -n "$context"
curl --fail -i -X PUT "$url" -H 'Content-Type: text/plain'   -H "X-Riak-Vclock: $context" --data-binary 'red,blue'
curl --fail "$url"
```

The read should now contain one value. This merge rule is chosen only for the lesson; a real application's rule must preserve the meaning of its data.

## Cleanup

Delete `$url` and remove `siblings.headers`. Keep the type for the next exercise. If siblings remain, check that you used the combined response context and that no other writer is modifying the key.
