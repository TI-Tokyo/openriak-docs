---
title: Read an object and handle missing values
description: Fetch an object and distinguish a value, a missing key, siblings, and a failed request. Use the endpoint,
  bucket type, and credentials expected by the application.
weight: 400
diataxis: how-to
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- developers
legacy_3_2_5_sources:
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\developing\usage\reading-objects.md
source_material:
- legacy-3.2.5
- live-3.2.5
- proposed-kv
- openriak-quickdocs-3.4
quickdocs_sources:
- https://openriak.github.io/riak/ObjectAPI.html#example-get-request
- https://openriak.github.io/riak/ObjectAPI.html#http-api-definition---fetch
tags:
- diataxis
- kv
- how-to
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- how-to/develop/read-object.md
related:
- how-to/application-data/update-an-object-with-causal-context
- how-to/application-data/resolve-concurrent-object-updates
- how-to/troubleshooting/diagnose-client-connection-and-request-failures
- reference/http-api/fetch-object
- foundations/data-and-consistency/objects-keys-and-buckets
- foundations/data-and-consistency/bucket-types-and-data-policies
- foundations/data-and-consistency/causality-version-vectors-and-siblings
---

Fetch an object and distinguish a value, a missing key, siblings, and a failed request. Use the endpoint, bucket type, and credentials expected by the application.

## Fetch headers and body

```sh
curl -sS -D object.headers -o object.body -w '%{http_code}\n' "$RIAK_HTTP/buckets/customers/keys/aiko"
```

Interpret the status before decoding the body:

- `200`: decode the value according to its content type and retain its causal context.
- `300`: retrieve and resolve the sibling values using [Resolve concurrent object updates]({{< product-version-root >}}how-to/application-data/resolve-concurrent-object-updates/).
- `404`: treat the key as missing for this request; preserve deletion context if returned and relevant to a later write.
- Authentication, availability, or timeout errors: report or retry according to the error, not as an empty object.

## Choose acknowledgement requirements

Use the request options in [Object request options]({{< product-version-root >}}reference/http-api/object-request-options/) when the operation requires a particular read policy. A stricter policy can reject requests when too few suitable replicas are available. Do not interpret every `404` during a failure as proof that a value never existed.

## Test the missing path

Request a unique key you have never written, then a known existing key. Confirm the application distinguishes their outcomes from a deliberately unreachable endpoint. Preserve the response context whenever the next operation will update the object.
