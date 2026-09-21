---
title: Search projected attributes
weight: 220
product: OpenRiak KV
product_version: 3.4.0
diataxis: tutorial
draft: true
status: editorially-rewritten
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
description: Search a projected city and age without fetching every candidate profile. Continue with the three-person
  dataset from the previous lesson.
related:
- tutorials/indexes-and-querying/build-and-query-a-people-search-index
- tutorials/indexes-and-querying/combine-query-conditions
- reference/query-api/expression-grammar-and-operators
- how-to/indexes-and-queries/filter-queries-using-projected-attributes
- foundations/indexes-and-querying/secondary-indexes-and-projected-attributes
- foundations/indexes-and-querying/how-distributed-queries-execute
- foundations/indexes-and-querying/query-cost-and-result-delivery
previous_page: tutorials/indexes-and-querying/build-and-query-a-people-search-index
next_page: tutorials/indexes-and-querying/combine-query-conditions
---

Search a projected city and age without fetching every candidate profile. Continue with the three-person dataset from the previous lesson.

## Inspect the projection

The fixture writes `person_bin` terms in the form `family|city|age`. For Aiko the term is `Ng|Tokyo|29`. The encoding and all values are choices made by this exercise.

## Evaluate and filter

Replace `query.json` with:

```json
{
  "accumulation_option":"keys",
  "substitutions":{"separator":"|","city":"Tokyo"},
  "query_list":[{
    "index_name":"person_bin",
    "start_term":"Ng|",
    "end_term":"Ng~",
    "evaluation_expression":"delim($term, :separator, ($family, $city, $age)) | to_integer($age, $age)",
    "filter_expression":"$city = :city AND $age < 30"
  }]
}
```

Submit the file to the same query endpoint:

```sh
curl --fail -H 'Content-Type: application/json' --data-binary @query.json   "$RIAK_HTTP/types/docs/buckets/people/query"
```

Only `aiko` should match. The range includes the `Ng|` projection terms; evaluation splits the term and converts age before filtering.

## Change one condition

Change the city substitution to `Osaka` and the age bound to `40`. Run it again and expect `sam`. Set the bound back to `30` and expect no match. These checks distinguish the city predicate from the numeric age predicate.

Keep the dataset for the next lesson. No object changes were needed for these query changes.
