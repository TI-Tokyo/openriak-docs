---
title: 'Query API accumulation options'
description: 'Define the 3.4.0 Query API modes for returning keys, terms, counts, and counts by attribute.'
weight: 6
diataxis: 'reference'
product: 'OpenRiak KV'
product_version: '3.4.0'
status: 'editorially-rewritten'
draft: true
audience:
  - 'developers'
source_material:
  - 'source-code-release-notes-3.4'
  - 'openriak-quickdocs-3.4'
quickdocs_sources:
  - 'https://openriak.github.io/riak/QueryAPI.html#accumulation_option-optional---default--keys'
  - 'https://openriak.github.io/riak/QueryAPI.html#accumulation_term-optional---default--term'
tags: ['diataxis', 'kv', 'reference']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Define the {{< current-version >}} Query API modes for returning keys, terms, counts, and counts by attribute.

## Details

### accumulation_option (optional - default = keys)

- There are multiple options for accumulating the results from a single query:
  - `keys`; return a list of keys that matched in the query, where the keys have been deduplicated and sorted.
  - `raw_keys`; return a list of keys that matched in the query, but in no specific order and where multiple matches for the same key will result in that key appearing multiple times within the results.
  - `terms`; return a list of term/key pairs, ordered by term.
  - `raw_terms`; return a list of term/key pairs, unsorted.
  - `count`; return a count of unique keys that matched the query.
  - `raw_count`; return a count of matches against the query (i.e. unlike `count` if an object key appears against multiple terms matched within the query, with `raw_count` that key will be counted multiple times).
  - `term_with_count`; return a count of unique key matches by term (where term is specified by the `accumulation_term`) in no specific order.
  - `term_with_rawcount`; return a count of key matches by term (where term is specified by the `accumulation_term`) in no specific order, where a key which appears multiple times under that term will be counted multiple times.

In some circumstances, there are constraints on the `accumulation_option` which can be used:

- If an `aggregation_expression` is added to the query (i.e. it is a combination query), only `raw_keys` and `raw_count` are valid accumulation options.
- If a `max_results` setting is added to the query, then only `terms` and `raw_keys` are valid accumulation options.

#### accumulation_term (optional - default = $term)

When using an accumulation option of `terms`, `raw_terms`, `term_with_rawcount` or `term_with_count`; the `accumulation_term` is the projected attribute returned from the evaluation function to be used as the term in the accumulator. The default is $term - the whole term.
