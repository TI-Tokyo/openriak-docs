---
title: 'Build a search index with the Query API'
description: 'Guide a developer through designing, loading, querying, and evaluating a small Query API search index.'
weight: 2
diataxis: 'tutorial'
product: 'OpenRiak KV'
product_version: '3.4.0'
status: 'editorially-rewritten'
draft: true
audience:
  - 'developers'
source_material:
  - 'openriak-quickdocs-3.4'
quickdocs_sources:
  - 'https://openriak.github.io/riak/QueryAPI.html#example-1---a-simple-people-search-index'
  - 'https://openriak.github.io/riak/QueryAPI.html#example-1---finding-an-exact-match'
  - 'https://openriak.github.io/riak/QueryAPI.html#example-1---inexact-match'
  - 'https://openriak.github.io/riak/QueryAPI.html#example-1---inexact-match-of-given-name'
  - 'https://openriak.github.io/riak/QueryAPI.html#example-1---more-extensible-index-schema'
  - 'https://openriak.github.io/riak/QueryAPI.html#example-1---simple-range-query'
  - 'https://openriak.github.io/riak/QueryAPI.html#example-1---wildcards-within-terms'
  - 'https://openriak.github.io/riak/QueryAPI.html#example-2---an-alternative-people-search'
  - 'https://openriak.github.io/riak/QueryAPI.html#example-2---simple-variations-and-limitations'
  - 'https://openriak.github.io/riak/QueryAPI.html#example-3---reporting-index'
  - 'https://openriak.github.io/riak/QueryAPI.html#example-3---simple-variations-and-limitations'
  - 'https://openriak.github.io/riak/QueryAPI.html#secondary-indexes---adding-index-entries-to-an-object'
tags: ['diataxis', 'kv', 'tutorial']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Guide a developer through designing, loading, querying, and evaluating a small Query API search index.

## Overview

### Secondary Indexes - Adding Index Entries to an Object

Querying in Riak is based around secondary indexes.  A Riak secondary index entry is a combination of a field, a term and an object key: where a field is a name for an index within a bucket, and a term is a sortable binary string that represents a value for a given key on that index, and the object key is the standard result of the query.  All indexes and queries are limited to the scope of a single Bucket.

Indexes are added using [the Object API]({{< baseurl >}}kv/3.4.0/reference/data/secondary-indexes/).

- When an object is PUT into Riak, the PUT should include ALL the index entries for that object - the entirety of the current expected state.  Internally Riak will calculate the delta from the previously stored index entries, and only make the necessary key changes.
- An individual object can have an unlimited number of index entries in total, and an unlimited number of terms on any given field.
- When an object is fetched from Riak using the Object API, it will be returned with all its current Index values.

There is no direct support for schema management within Riak, as Riak is designed to act independently of the format and the content of the application-provided object body.  It is expected that for an application to make use of secondary indexes within Riak, the object-handling logic within the application will require an extension; where that extension will examine the object body, and calculate the required index entries before completing a PUT.  As the schema is managed externally to Riak, schema changes are also required to be managed within the application.  Consideration of how to make such schema changes is the responsibility of the application designer e.g. versioning, rolling updates, querying-planning during transition etc.

The design of secondary indexes in Riak make them best suited to environments where the query demands are relatively predictable in advance, and also the approximate cardinality of the data elements.  The [expected performance of queries is governed by the factors highlighted in the performance section]({{< baseurl >}}kv/3.4.0/explanation/performance/query-execution/), and consideration of those factors is required when defining the indexes and planning the queries to be used.  Riak contains no query planning logic; the optimal path to resolve a query needs to be determined by the application.

Index entries can be made up of simple sort keys:

e.g. `surname_bin: SMITH`

Index terms can be extended by projecting additional attributes onto the sort key, appended to the sort key, e.g. in this case by appending the date of birth to the sort key, separating the two parts using `|` as a delimiter:

e.g. `surnamedob_bin: SMITH|19790613`

There is no pre-defined way to map project attributes onto an index term in Riak; the definition, formatting and appending of projected attributes is the responsibility of the application.  Projected attributes are extracted from index terms at query time, normally using an `evaluation_expression` within the Query API; and so index entries should be added so that the extraction is supported by the [expression language]({{< baseurl >}}kv/3.4.0/reference/query-api/expressions/).

Different extraction functions within the Query API `evaluation_expression` have different costs at query time, but also have differing impacts with regards to flexibility in support of schema change.  For example, using an `index` evaluation function is more efficient than a `kvsplit` function at query time, but when changing the schema the use of `kvsplit` may simplify the management of that change.

#### Example (1) - A Simple People Search Index

In this example, the database contains people whose records are stored under a unique individual identifier (the primary Key used in Riak).  There is also a requirement to search for people to find potential matches where the unique identifier is not known, and in these searches the following criteria can be provided to the query:

- Date Of birth (required).
- Current family name (optional).
- All known given names (optional).
- Current home [postal code](https://en.wikipedia.org/wiki/Postal_code) (optional).

For all queryable attributes approximate entries are allowed.  The Date of Birth can be a range rather than a specific date, the names and post codes require a minimal prefix (the first two characters), but wildcards may be provided for unknown parts.

For this example, a single index per record is constructed to support these queries, whereby the Date Of Birth would be the sort key, the current family name, given names and current home postcode could be added as projected attributes - with `|` used as a delimiter between the types of attributes and `.` used as a delimiter between the individual attributes of a given type (which in this case is only for given names).

So a sample person:

- born on 1st May 1965;
- with current family name of SMITH;
- known by given names of ANNE, MARIE & ANNE-MARIE;
- and has registered a home Postal Code (LS9 0TW).

They would then be represented by the following index entry:

`peoplefinder_bin: 19650501|SMITH|ANNE.MARIE.ANNE-MARIE|LS9_0TW`

#### Example (1) - Simple Range Query

To find all the people with a given date of birth, a simple range query could be used:

```json
    {
        "query_list" :
            [
                {
                    "index_name" : "peoplefinder_bin",
                    "start_term" : "19650501",
                    "end_term"   : "19650502"
                }
            ]
    }
```

This is the equivalent to finding all those born on "19650501" in "YYYYMMDD" format.  As all index entries have additional information appended, the `end_term` "19650502" is lexicographically before any of the index entries for those born on "19650502" e.g. `"19650502" < "19650502|...."`.  As no `accumulation_option` has been set, this will return a list of keys for those people born on that day.

#### Example (1) - Finding an Exact Match

To find an exact match on a subset of the provided data (e.g. Date Of Birth = 19650501, FamilyName = SMITH, GivenName = ANNE), the following query could be used:

```json
    {
        "substitutions" : {"dl1" : "|", "dl2" : ".", "qfn" : "SMITH", "qgn" : "ANNE"},
        "query_list" :
            [
                {
                    "index_name" : "peoplefinder_bin",
                    "start_term" : "19650501",
                    "end_term"   : "19650501~",
                    "evaluation_expression" : "delim($term, :dl1, ($dob, $fn, $gn, $pc)) | split($gn, :dl2, $gn)",
                    "filter_expression" : "($fn = :qfn ) AND (:qgn IN $gn)"
                }
            ]
    }
```

This query defines some `substitutions`, of the delimiters (to simplify escaping required when passing text into the expressions), and of the actual terms to be queried (which can make it easier within the application to transpose user input into standard query templates).  The substitutions are referred to within expressions by prefixing the substitution name with `:`.

e.g. the substitution of `{"qfn", : "SMITH", "qgn", "ANNE"}` will translate the `filter_expression` `"($fn = :qfn ) AND (:qgn IN $gn)"` into `"($fn = SMITH ) AND (ANNE IN $gn)"`.

The query list in this case contains only one query, and that identifies the index field (`index_name`), and the start and end terms (`start_term` snd `end_term`).  Note that as the projected attributes are appended the sort key, although the query is for an exact sort key it must be range query which covers all possible projected attributes (in this case by appending to the end_term a character `~` that has a value higher than the delimiter `|` in the ascii table).

The evaluation expression is a pipeline of evaluation functions to be applied to each index term.  The first evaluation function `delim($term, :dl1, ($dob, $fn, $gn, $pc))` instructs the query to split the query term using the delimiter identified by the substitution `dl1` (i.e. `|`) and then up to four elements will be placed in the projected attributes maps as `$dob`, `$fn`, `$gn` and `$pc` respectively.  The second evaluation function `split($gn, :dl2, $gn)` is used to take the value of the attribute `$gn` and create a new attribute `$gn` which is a list obtained by splitting the attribute value on the delimiter identified by the substitution `dl2` (i.e. `.`).

So in this term there are two delimiters, one `|` which splits up a fixed number of attributes, and this is evaluated with the `delim` function which outputs elements directly into the map of attributes.  There is then a second delimiter `.` which splits one of those attributes, the given name attribute, into individual given names.  As there is a variable number of given names supported, the `split` function is used to output an attribute whose value is a list.  In this case the output name of the attribute `$gn` is the same as the input, so this alters the value in the attribute map rather than creating a new one.

After applying the `evaluation_expression`, the `filter_expression` will receive a map of projected attributes like this (for this specific index entry):

```erlang
    #{
        <<"$dob">> => "19650501",
        <<"$fn">> => "SMITH",
        <<"$gn">> => ["ANNE", "MARIE", "ANNE-MARIE"],
        <<"$pc">> => "LS9_0TW"
    }
```

The filter does not need to qualify the date of birth, as this is already qualified by the range.  However, it needs to check that the current Family Name is as expected `($fn = :qfn)` and that the query given name is in the list of given names produced `(:gqn IN $gn)`.

Note that, in this particular case, there would be a significant performance improvement by rewriting the query as:

```json
    {
        "substitutions" : {"dl1" : "|", "dl2" : ".", "qgn" : "ANNE"},
        "query_list" :
            [
                {
                    "index_name" : "peoplefinder_bin",
                    "start_term" : "19650501|SMITH|",
                    "end_term"   : "19650501|SMITH|~",
                    "evaluation_expression" : "delim($term, :dl1, ($dob, $fn, $gn, $pc)) | split($gn, :dl2, $gn)",
                    "filter_expression" : "(:qgn IN $gn)"
                }
            ]
    }
```

The optimisation will reduce the number of results that need to be scanned and processed, by requesting a more specific range.  To exploit such optimisations, there is a need for design effort to correctly order the projected attributes in the index term.

> The potential for such optimisations is a key driver to using an append-then-evaluate approach to adding projected attributes to index entries; rather than keeping projected attributes in an unordered array separate to the sort key.

The query _may_ be further optimised using a regular expression.  Some functionality may be harder to implement in regular expressions - in this case it will also hit a match on a given name that includes the letters ANNE rather than match only on a given name that is entirely ANNE.  Regular expressions make handling range checks on projected attributes much more difficult:

```json
    {
        "query_list" :
            [
                {
                    "index_name" : "peoplefinder_bin",
                    "start_term" : "19650501|SMITH|",
                    "end_term"   : "19650501|SMITH|~",
                    "regular_expression" : "[^\\|]*\\|[^\\|]*\\|[^\\|]*ANNE"
                }
            ]
    }
```

This regular expression based query is not guaranteed to be quicker than using the filter and evaluation expressions in the previous example.  Further, even if it does improve performance, building such optimisations into queries can add significant complications to application code, and add to the complexity of testing that application code.

#### Example (1) - Inexact Match

If for the same query it is required to have an inexact match (e.g. Born between between 1965 and 1970, birthday of 1st May, Family name of SM*, Given name of ANNE), the following query could be used:

```json
    {
        "substitutions" : {"dl1" : "|", "dl2" : ".", "qfn_begins" : "SM", "qgn" : "ANNE", "qbd" : "0501"},
        "query_list" :
            [
                {
                    "index_name" : "peoplefinder_bin",
                    "start_term" : "19650101",
                    "end_term"   : "19691231~",
                    "evaluation_expression" : "delim($term, :dl1, ($dob, $fn, $gn, $pc)) | split($gn, :dl2, $gn) | index($dob, 4, 4, $birthday)",
                    "filter_expression" : "begins_with($fn, :qfn_begins ) AND (:qgn IN $gn) AND ($birthday = :qbd)"
                }
            ]
    }
```

The evaluation expression is extended to output the birthday by taking the last 4 characters of the date of birth.  The filter expression checks an inexact match by looking only at the start of the family name.

Alternative approaches would be possible:

- `ends_with($dob, :qbd)` could be used for the birthday check avoiding the additional pipeline function in the evaluation expression.
- `index($fn, 0, 2, $fn)` could be used in the evaluation expression to slim the $fn to the first two characters for equality checking.
- Also, because of the birthday check, the range start and end terms could also be tighter, and reduce the number of index terms to be processed by about 20%.

#### Example (1) - Inexact Match of Given Name

The evaluation expression language supports flexible comparisons on exact terms; but when a term has been broken into a sub-list (as with the Given Names in the above example), it is only possible to look for an exact match within the sub-list.

There are three possible alternatives should a more complex match be required on such a sub-list:

- Use the alternative `accumulation_option` of `terms` to the default (which is `keys`), and this will return a list of term/key tuples to filter in the application (rather than just a list of object keys).  By default the whole term will be returned, but a specific projected attribute can be returned using the `accumulation_term` option, as long as the value of that attribute is a string.
  - Filtering in the database is generally quicker than filtering in the application though - due to the increased parallelism of the database filter, and the reduced serialisation and sorting costs.
- Use an alternative representation and the `contains` evaluation function - e.g. storing given names with a preceding and succeeding delimiter `.ANNE.MARIE.ANNE-MARIE.`, would allow for: `contains($gn, "ANNE")` to find any mention of ANNE in any part of any given name; `contains($gn, ".ANNE.")` to find only where the whole given name is ANNE; `contains($gn, ".ANNE") OR contains($gn, "ANNE.")` to find where the given name either begins or ends with ANNE.
- Use a regular expression filter rather than an evaluation and filter expression, which may in this case be considered a more natural approach to wildcard matching on strings.

#### Example (1) - Wildcards within terms

Wildcard style queries against individual string attributes are only supported directly using the regular expression filter type.

When using evaluation and filter expressions, the `filter_expression` functions `begins_with`, `ends_with` and `between` are to be used to support internal wildcards within terms.  For example to match on family names of `SM*KOWSKI` where `*` represents one or more characters - a `filter_expression` of `begins_with($fn, "SM") AND ends_with($fn, "KOWSKI") NOT ($fn = "SMKOWSKI)` would be required.

There exists a regex based evaluation function that can be used as a pseudo filter function, where the power of regular expressions is required in a specific part of the query.  The regex evaluation function extracts matches, but only when the expected number of matches is found - so non-matching regular expressions will result in attributes not existing in the projected attribute map.

This query should filter family names based on a "fn_regex" provided in the substitutions.

```json
    {
        "substitutions" : {"dl1" : "|", "dl2" : ".", "qgn" : "ANNE", "fn_regex" : "(?P<fn_match>SM[A-Z]+KOWSKI)"},
        "query_list" :
            [
                {
                    "index_name" : "peoplefinder_bin",
                    "start_term" : "19650501",
                    "end_term"   : "19650501~",
                    "evaluation_expression" : "delim($term, :dl1, ($dob, $fn, $gn, $pc)) | regex($fn, :fn_regex, ($fn_match)) | split($gn, :dl2, $gn)",
                    "filter_expression" : "attribute_exists($fn_match) AND (:qgn IN $gn)"
                }
            ]
    }
```

#### Example (1) - More Extensible Index Schema

It is possible to reduce the pre-defined structure in an index entry by using KV pairs in the index entry.

For example, the above index entry could be stored in a Key=Value form, and note that we here differentiate for extra clarity between the primary given name (`pgn`), and the secondary given names (`sgn`):

`peoplefinder_bin: 19650501|fn=SMITH#pgn=ANNE#sgn=MARIE.ANNE-MARIE#pc=LS9_0TW`

This evaluation expression can then be used: `delim($term, :dl1, ($dob, $kvs)) | kvsplit($kvs, "#", "=") | split($sgn, :dl2, $sgn)`

To produce this set of projected attributes to be passed to the filter:

```erlang
    #{
        <<"$dob">> => "19650501",
        <<"$fn">> => "SMITH",
        <<"$pgn">> => "ANNE",
        <<"$sgn">> => ["MARIE", "ANNE-MARIE"],
        <<"$pc">> => "LS9_0TW"
    }
```

#### Example (2) - An Alternative People Search

An alternative strategy to option (1), would be to use multiple indexes, with the Date Of Birth as a projected attribute.  Further, in this example the concept of effective dates is introduced, where certain attributes (in particular Postal Code) are relevant only to certain timeframes.  Appending effective date ranges as projected attributes then supports a search for records based on both the present information, or potentially the information at a given date in the past.

In this example there will be three indexes:

- `familyname_bin : <FAMILYNAME>|<DOB>|<EFFECTIVE_STARTDATE><EFFECTIVE_ENDDATE>`
- `givenname_bin : <GIVENNAME>|<DOB>|<EFFECTIVE_STARTDATE><EFFECTIVE_ENDDATE>`
- `postalcode_bin : <POSTCODE>|<DOB>|<EFFECTIVE_STARTDATE><EFFECTIVE_ENDDATE>`

The start date and end dates will be of fixed YYYYMMDD format, with current information being given an artificial end date of `99999999`.

So for a sample person, the index entries could be:

- `familyname_bin: SMITH|19650501|19895060499999999, JONES|19650501|19650501198950604`
- `givenname_bin: ANNE|19650501|1965050199999999, MARIE|19650501|1965050199999999, ANNE-MARIE|19650501|1965050199999999`
- `postcode_bin: LS9_0TW|19650501|1990080199999999, LS9_1GH|19650501|1965050119900801`

This strategy requires more index entries, but potentially simpler and more powerful querying.

```json
    {
        "substitutions" : {"dl1" : "|", "low_dob" : "19650101", "high_dob" : "19650531"},
        "query_list" :
            [
                {
                    "index_name" : "familyname_bin",
                    "start_term" : "SMITH|",
                    "end_term"   : "SMITH~",
                    "evaluation_expression" : "delim($term, :dl1, ($fn, $dob, $edates))",
                    "filter_expression" : "$dob BETWEEN :low_dob AND :high_dob"
                }
            ]
    }
```

The query definition above will search for every SMITH born in the first 6 months of 1964.  Note that the delimiter chosen (`|`) is after all the standard text characters in the ASCII table (char 124), so that this will match on only the complete name SMITH, whereas `"start_term" : "SMITH"` would also match on any surname starting SMITH.

```json
    {
        "substitutions" : {"dl1" : "|", "low_dob" : "19650101", "high_dob" : "19650531", "effective_date" : "19800101"},
        "query_list" :
            [
                {
                    "index_name" : "postcode_bin",
                    "start_term" : "LS9_",
                    "end_term"   : "LS9_~",
                    "evaluation_expression" : "delim($term, :dl1, ($pc, $dob, $edates)) | index($edates, 0, 8, $start_date) | index($edates, 8, 8, $end_date)",
                    "filter_expression" : "($dob BETWEEN :low_dob AND :high_dob) AND (:effective_date BETWEEN $start_date AND $end_date)"
                }
            ]
    }
```

The query definition above will search for anyone who was born in the first 6 months of 1964, and was living in the LS9 postal area on 1st January 1980.

To query across both indexes, a combination query is required.  The following query could be managed on a single query with the [previous strategy]({{< baseurl >}}kv/3.4.0/tutorials/query-api/build-search-index/), however, in this strategy the family name and address information is split across different indexes. Multiple queries combined through an aggregation expression are now required to search for only the SMITHs that meet the address criteria.

```json
    {
        "aggregation_expression" : "$1 INTERSECT $2",
        "substitutions" : {"dl1" : "|", "low_dob" : "19650101", "high_dob" : "19650531", "effective_date" : "19800101"},
        "query_list" :
            [
                {
                    "aggregation_tag" : 1,
                    "index_name" : "postcode_bin",
                    "start_term" : "LS9_",
                    "end_term"   : "LS9_~",
                    "evaluation_expression" : "delim($term, :dl1, ($pc, $dob, $edates)) | index($edates, 0, 8, $start_date) | index($edates, 8, 8, $end_date)",
                    "filter_expression" : "($dob BETWEEN :low_dob AND :high_dob) AND (:effective_date BETWEEN $start_date AND $end_date)"
                },
                {
                    "aggregation_tag" : 2,
                    "index_name" : "familyname_bin",
                    "start_term" : "SMITH|",
                    "end_term"   : "SMITH~",
                    "evaluation_expression" : "delim($term, :dl1, ($fn, $dob, $edates))",
                    "filter_expression" : "$dob BETWEEN :low_dob AND :high_dob"
                }
            ]
    }
```

#### Example (2) - Simple Variations and Limitations

It is possible to combine strategies (1) and (2) by using separate indices and overloading each term with all additional information.  The application would then need a query planning strategy to determine which index to use based on the information provided - i.e. the strategy would need to determine based on the query details which index would likely lead to the fewest number of index entries being scanned, and use that index and sort key combination.  Designing such a strategy would require up-front knowledge of how the data is distributed.

#### Example (3) - Reporting index

As well as returning keys, and term/key tuples; when using single queries it is also possible to return counts, and counts by term.  These alternative accumulators are commonly used to support report-style queries.

For this example it is assumed all the people in the store exist in a hierarchy.  Each person is assigned to a GP Provider, and every GP Provider belongs to a Strategic Health Authority (and these are represented by fixed-width codes).  People have a Date of Birth (from which we can calculate age), but also a series of characteristics which can be expressed in single character flags (e.g. administrative gender code, smoking status, death status, alcohol dependency etc).  This information is then required to do organisation, and population level reporting.

For this a single index is used:

- `healthreport_bin : <SHA><GP><DOB><STATUS_FLAGS>`

So a test record may have an entry like:

- `healthreport_bin: SHA0001GP00000119650501FYNNY`

So if today's date is 30 May 2025, to count all the female smokers over the age of 60 registered in SHA001

```json
    {
        "accumulation_option" : "raw_count",
        "query_list" :
            [
                {
                    "index_name" : "healthreport_bin",
                    "start_term" : "SHA0001",
                    "end_term"   : "SHA0001~",
                    "evaluation_expression" : "index($term, 15, 8, $dob) | index($term, 23, 1, $agc) | index($term, 24, 1, $smoker)",
                    "filter_expression" : "($dob <= \"19650530\") AND ($agc = \"F\") AND ($smoker = \"Y\")"
                }
            ]
    }
```

If the same results are required, but this time a count by age at today's date (30th May 2025):

```json
    {
        "substitutions" : {"current_date" : "0530"},
        "accumulation_option" : "term_with_rawcount",
        "accumulation_term" : "$age",
        "query_list" :
            [
                {
                    "index_name" : "healthreport_bin",
                    "start_term" : "SHA0001",
                    "end_term"   : "SHA0001~",
                    "evaluation_expression" : "index($term, 15, 8, $dob) | index($term, 23, 1, $agc) | index($term, 24, 1, $smoker) | index($dob, 0, 4, $yob) | to_integer($yob, $yob) | index($dob, 4, 4, $birthday) | map($birthday, <=, ((:current_date, 2025)), 2024, $yoc) | subtract($yoc, $yob, $age) | to_string($age, $age)",
                    "filter_expression" : "($dob <= \"19650530\") AND ($agc = \"F\") AND ($smoker = \"Y\")"
                }
            ]
    }
```

#### Example (3) - Simple Variations and Limitations

In using report-style queries, counting results or grouping counts by a projected attribute - the type of `accumulation_option` used is important.  There is support for both `raw` and non-`raw` forms of each `accumulation_option`.  The `raw` form of each accumulator [will be significantly more efficient when covering large result sets]({{< baseurl >}}kv/3.4.0/explanation/performance/query-execution/), but it will not deduplicate the result set by object key before counting.

## What you will learn

By completing this tutorial, you will build the workflow described above and learn how to validate each stage before moving on.

## Before you begin

Use a disposable OpenRiak KV environment that matches this documentation version, and keep cluster status and logs available while you work.

## Verify the result

Repeat the completed workflow, inspect the stored or operational result, and confirm that the cluster remains healthy.

## Next steps

- Continue with the section index and choose the next task for your role.
