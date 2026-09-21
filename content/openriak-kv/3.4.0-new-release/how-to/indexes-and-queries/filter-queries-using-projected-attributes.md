---
title: Filter queries using projected attributes
weight: 560
product: OpenRiak KV
product_version: 3.4.0
diataxis: how-to
draft: true
status: editorially-rewritten
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
description: Filter a Query API index range using attributes projected into each term. Prepare a small dataset whose
  expected matches you can calculate independently.
related:
- reference/query-api/endpoints-and-request-schema
- reference/query-api/expression-grammar-and-operators
- tutorials/indexes-and-querying/search-projected-attributes
- foundations/indexes-and-querying/secondary-indexes-and-projected-attributes
- foundations/indexes-and-querying/how-distributed-queries-execute
- foundations/indexes-and-querying/query-cost-and-result-delivery
---

Filter a Query API index range using attributes projected into each term. Prepare a small dataset whose expected matches you can calculate independently.

## Define the projection

Choose a term encoding with stable ordering and an unambiguous separator or format. Write the projected attributes alongside the object and verify the stored index metadata on representative objects.

## Add evaluation and filtering

Start with a working exact or range query. Add an `evaluation_expression` that extracts the desired attributes, then a `filter_expression` that tests them. Use the expression reference for the grammar and use `substitutions` for supplied values instead of concatenating unescaped input into expressions.

Keep the accumulation explicit. First return keys or terms so you can inspect the matches before changing the query to counts.

## Verify

Include a matching record, a nonmatching record, a boundary value, and a malformed or missing projected attribute. Compare the returned keys to that known set. Update one object and its index together and repeat the check.

If a selective filter remains slow, reduce the range scanned or redesign the leading term rather than assuming the small result makes the query cheap.
