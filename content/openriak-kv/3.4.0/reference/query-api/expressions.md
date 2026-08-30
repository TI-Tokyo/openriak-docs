---
title: 'Query API expression reference'
description: 'Define supported Query API expressions, operators, composition rules, and Unicode behavior.'
weight: 3
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
  - 'https://openriak.github.io/riak/QueryAPI.html#aggregation_expression-optional'
  - 'https://openriak.github.io/riak/QueryAPI.html#evaluation-expression---definition'
  - 'https://openriak.github.io/riak/QueryAPI.html#filter-expression---definition'
  - 'https://openriak.github.io/riak/QueryAPI.html#query-json---expressions'
  - 'https://openriak.github.io/riak/QueryAPI.html#unicode-support'
tags: ['diataxis', 'kv', 'reference']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Define supported Query API expressions, operators, composition rules, and Unicode behavior.

## Details

### aggregation_expression (optional)

- If multiple queries are to be run, the aggregation expression is used to inform the database how those results should be combined, using $1, $2 etc to refer to the numeric `aggregation_tag` for each query - with the key words `UNION`, `INTERSECT` and `SUBTRACT` to show how the sets of results are to be combined.  Parenthesis may be used for clarity. e.g. `($1 INTERSECT $2) UNION ($3 SUBTRACT $1)`

#### Query Json - Expressions

There are two parts to using expressions in a Riak query: an evaluation expression (to convert the term into projected attributes), and a filter expression (to filter the results in or out by matching on the values of projected attributes).

#### Evaluation Expression - Definition

The evaluation pipeline receives a map of projected attributes containing two Identifier/Value pairs - $term, $key.  The $term is the index term that has been matched (as it is within the sorted key range for the given index field and bucket), and the $key is the value of the Key.  Both $term and $key will be strings.

The `evaluation_expression` is a pipeline of individual functions, joined using the `|` operator.  All pipeline functions will update the map, potentially adding new projected attributes, or adjusting the value for existing attributes - and the map will be forwarded onto the next stage for processing.

Values of the projected attributes in the map always start as strings in the pipeline, but may be explicitly converted to lists of strings, or to an integer - and in the case of an integer can also be converted back to a string.  Functions in the pipeline that receive inputs of the wrong type are skipped.

The functions that can be used in a pipeline are:

`delim ( IN_ID identifier , DELIM string , OUT_ID_LIST identifier_list )`

- take a value associated with IN_ID and split it using the delimiter DELIM.  The parts are matched to the identifiers in OUT_ID_LIST.  If there are only N values following the application of the delimiter where N is less than the length of the OUT_ID_LIST, then only then only the first N identifiers in OUT_ID_LIST are assigned a value.  Any overhanging elements (i.e. where N is greater than the length of the OUT_ID_LIST) are ignored.

`join ( IN_ID_LIST identifier_list , DELIM string , OUT_ID identifier )`

- a concatenation function that takes each value associated with an identifier in IN_ID_LIST in turn, and concatenates them together using the DELIM as a separator.  The output is given as the value of OUT_ID.  In effect `join` is the reverse of the `delim` function.
- this is generally used with term-based aggregators in queries (e.g. to create a combined term to count by).

`split ( IN_ID identifier , DELIM string , OUT_ID identifier )`

- works as with the `delim` function, but the output (a list of strings) is assigned to a single OUT_ID identifier.

`slice ( IN_ID identifier , LENGTH pos_integer , OUT_ID identifier )`

- slice a string into a list of multiple strings assuming each sub-string is of fixed length e.g. if the value of IN_ID is a string containing 2-character values, slicing with a length 2 will assign a list of 2-character strings to OUT_ID.

`index ( IN_ID identifier , POSITION non_neg_integer , LENGTH pos_integer , OUT_ID identifier )`

- take a single slice from a string mapped to the IN_ID identifier, from character position POSITION of length LENGTH and assign the output to OUT_ID.  If there are insufficient characters in the string value of IN_ID to take a string of that position and length, then the function will be skipped.

`kvsplit ( IN_ID identifier , PAIR_DELIM string , KV_DELIM string )`

- take a string value associated with IN_ID, where the string contains a delimited (by PAIR_DELIM) list of Key/Value pairs - where the Key and Value and separated by KV_DELIM.  The output will add each Key/Value pair to the map of projected attributes.

`regex ( IN_ID identifier , REGEX string , OUT_ID_LIST identifier_list )`

- use a regular expression to extract new projected attributes as Key/Value pairs, where the REGEX must match the value of IN_ID and extract named capture groups that align with the attribute keys in the OUT_ID_LIST.  All expected captures must exist in the input value for the projected attributes to be updated, otherwise the function will pass on the map of projected attributes unchanged.

`map ( IN_ID identifier , COMP comparator , MAP_LIST mappings_list , DEFAULT operand , OUT_ID identifier )`

- to classify the value of a projected attribute the map function is used.  The MAP_LIST is a list of pairs, where the first element of the pair is a value to compare with, and the second element is a classification for a match against this  pair (the output value).  The comparison between the value and the first element is done using the comparator COMP.  If no element of the MAP_LIST returns a match against the input value, then the DEFAULT classification is used as the output value.  The output value is added to the projected attributes using the OUT_ID identifier as the key.
- this is generally used with term-based aggregators in queries (e.g. to create a combined term to count by).

`to_integer ( IN_ID identifier , OUT_ID identifier )`

- convert a string to an integer where IN_ID has a string value, and is mapped after integer-conversion to the projected attribute with an OUT_ID identifier.  The pipeline stage is skipped when the value does not convert to an integer.
- note that if IN_ID and OUT_ID are the same identifier, the type of the value of OUT_ID is dependent on the success of the conversion.

`to_string ( IN_ID identifier , OUT_ID identifier )`

- convert an integer back to a string where IN_ID has an integer value, and is mapped after string-conversion to the projected attribute with an OUT_ID identifier.  If the input value is already a string, the mapping will still occur without the conversion.

`subtract ( X math_operand , Y math_operand , OUT_ID identifier )`

- subtract Y from X and map the output to the OUT_ID identifier of the map of projected attributes.  X and Y can either be an integer provided as an input, or an identifier of an existing projected attribute which has been converted to an integer.  If either X or Y are not integers, then the function will be skipped.

`add ( X math_operand , Y math_operand , OUT_ID identifier )`

- add X to Y and map the output to the OUT_ID identifier of the map of projected attributes.  X and Y can either be an integer provided as an input, or an identifier of an existing projected attribute which has been converted to an integer.  If either X or Y are not integers, then the function will be skipped.

The final map of projected attributes will be passed as the input to the Filter Expression.

#### Filter Expression - Definition

The Filter expression takes the projected attributes as an input, and the output is either `true` (the term is a match) or `false`.

In the definition an `operand` can either be a `key` of a projected attribute (where the value of that attribute will be used when applying the expression), or a fixed value provided within the expression.

```
condition-expression ::=
      operand comparator operand
    | operand BETWEEN operand AND operand
    | operand IN operand
    | operand IN (',' operand )
    | function
    | condition AND condition
    | condition OR condition
    | NOT condition
    | ( condition )

comparator ::=
    =
    | <>
    | <
    | <=
    | >
    | >=

function ::=
    attribute_exists (key)
    | attribute_not_exists (key)
    | attribute_empty (key)
    | begins_with (key, substr)
    | ends_with (key, substr)
    | contains (key, substr)
```

#### Unicode support

Testing is only undertaken on ascii-based index terms in Riak 3.4, although filter and evaluation expressions have been designed to support unicode.

There are potential issues with unicode support, not least with support for unicode in HTTP headers, so significant additional work may be required to provide a comprehensive and well-tested solution with Unicode support in a future Riak release.
