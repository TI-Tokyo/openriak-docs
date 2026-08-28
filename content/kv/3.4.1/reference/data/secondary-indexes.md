---
title: 'Secondary indexes'
description: 'Define the fields, limits, supported operations, representations, and compatibility rules for secondary indexes.'
weight: 7
diataxis: 'reference'
product: 'OpenRiak KV'
product_version: '3.4.1'
status: 'editorially-rewritten'
draft: true
audience:
  - 'developers'
  - 'operators'
legacy_3_2_5_sources:
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\using\reference\secondary-indexes.md'
source_material:
  - 'legacy-3.2.5'
  - 'live-3.2.5'
  - 'proposed-kv'
  - 'openriak-quickdocs-3.4'
quickdocs_sources:
  - 'https://openriak.github.io/riak/ObjectAPI.html#index-entries'
  - 'https://openriak.github.io/riak/QueryAPI.html#secondary-indexes---adding-index-entries-to-an-object'
tags: ['diataxis', 'kv', 'reference']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Define the fields, limits, supported operations, representations, and compatibility rules for secondary indexes.

## Details

### Secondary Indexes Reference

[usage bucket types]: /kv/3.4.1/how-to/develop/use-bucket-types/
[use ref strong consistency]: /kv/3.4.1/reference/specialized-apis/strong-consistency-api/

This document provides implementation and other details for OpenRiak's
[secondary indexes](/kv/3.4.1/how-to/develop/query-secondary-indexes/) \(2i) feature.

#### How It Works

Secondary indexes use **document-based partitioning**, a system where
indexes reside with each document, local to the [vnode](/kv/3.4.1/explanation/foundations/glossary/#vnode). This
system is also a local index. Secondary indexes are a list of key/value
pairs that are similar to HTTP headers. At write time, objects are
tagged with index entries consisting of key/value metadata. This
metadata can be queried to retrieve the matching keys.

![Secondary Index](/images/Secondary-index-example.png)

Indexes reside on multiple machines. Since indexes for an object are
stored on the same partition as the object itself, query-time
performance issues might arise. When issuing a query, the system must
read from a "covering" set of partitions and then merge the results.
The system looks at how many replicas of data are stored---the N value
or `n_val`---and determines the minimum number of partitions that it
must examine (1 / `n_val`) to retrieve a full set of results, also
taking into account any offline nodes.

An application can modify the indexes for an object by reading an
object, adding or removing index entries, and then writing the object.
Finally, an object is automatically removed from all indexes when it is
deleted. The object's value and its indexes should be thought of as a
single unit. There is no way to alter the indexes of an object
independently from the value of an object, and vice versa. Indexing is
atomic, and is updated in real time when writing an object. This means
that an object will be present in future index queries as soon as the
write operation completes.

Riak stores 3 replicas of all objects by default, although this can be
changed [using bucket types][usage bucket types], which manage buckets' [replication properties](/kv/3.4.1/explanation/replication/references-and-triggers/). The system is capable of generating a full set of results
from one third of the system’s partitions as long as it chooses the
right set of partitions. The query is sent to each partition, the index
data is read, and a list of keys is generated and then sent back to the
requesting node.

> **Note on 2i and strong consistency**
>
> Secondary indexes do not currently work with the [strong consistency][use ref strong consistency] feature introduced in Riak version 2.0. If you store objects in [strongly consistent buckets](/kv/3.4.1/reference/specialized-apis/strong-consistency-api/) and attach
secondary index metadata to those objects, you can still perform
strongly consistent operations on those objects but the secondary
indexes will be ignored.

#### Index Entries

Index entries consist of multiple index fields, where each index field may have multiple values. The field names must have a suffix of either `_bin` or `_int` - where `_bin` indicates the value will be a binary, and `_int` indicates the value is an integer.  Although the value of an index entry may be a binary type, as it is passed in HTTP headers it is [restricted to visible ASCII text](https://datatracker.ietf.org/doc/html/rfc7230#section-3.2), and field names are required to be handled in a case-insensitive way: so using only lower-case alphanumeric index field names is recommended to avoid future compatibility issues between APIs.

An object will always be presented (in a GET response) with all its index entries, and when updating an object all index entries must be passed - an update requires all entries, not a delta.

If an object results in an unresolved conflict, the index entries for the object within the database will be the union of the index entries for all sibling content items.

#### Secondary Indexes - Adding Index Entries to an Object

Querying in Riak is based around secondary indexes.  A Riak secondary index entry is a combination of a field, a term and an object key: where a field is a name for an index within a bucket, and a term is a sortable binary string that represents a value for a given key on that index, and the object key is the standard result of the query.  All indexes and queries are limited to the scope of a single Bucket.

Indexes are added using [the Object API](/kv/3.4.1/reference/data/secondary-indexes/).

- When an object is PUT into Riak, the PUT should include ALL the index entries for that object - the entirety of the current expected state.  Internally Riak will calculate the delta from the previously stored index entries, and only make the necessary key changes.
- An individual object can have an unlimited number of index entries in total, and an unlimited number of terms on any given field.
- When an object is fetched from Riak using the Object API, it will be returned with all its current Index values.

There is no direct support for schema management within Riak, as Riak is designed to act independently of the format and the content of the application-provided object body.  It is expected that for an application to make use of secondary indexes within Riak, the object-handling logic within the application will require an extension; where that extension will examine the object body, and calculate the required index entries before completing a PUT.  As the schema is managed externally to Riak, schema changes are also required to be managed within the application.  Consideration of how to make such schema changes is the responsibility of the application designer e.g. versioning, rolling updates, querying-planning during transition etc.

The design of secondary indexes in Riak make them best suited to environments where the query demands are relatively predictable in advance, and also the approximate cardinality of the data elements.  The [expected performance of queries is governed by the factors highlighted in the performance section](/kv/3.4.1/explanation/performance/query-execution/), and consideration of those factors is required when defining the indexes and planning the queries to be used.  Riak contains no query planning logic; the optimal path to resolve a query needs to be determined by the application.

Index entries can be made up of simple sort keys:

e.g. `surname_bin: SMITH`

Index terms can be extended by projecting additional attributes onto the sort key, appended to the sort key, e.g. in this case by appending the date of birth to the sort key, separating the two parts using `|` as a delimiter:

e.g. `surnamedob_bin: SMITH|19790613`

There is no pre-defined way to map project attributes onto an index term in Riak; the definition, formatting and appending of projected attributes is the responsibility of the application.  Projected attributes are extracted from index terms at query time, normally using an `evaluation_expression` within the Query API; and so index entries should be added so that the extraction is supported by the [expression language](/kv/3.4.1/reference/query-api/expressions/).

Different extraction functions within the Query API `evaluation_expression` have different costs at query time, but also have differing impacts with regards to flexibility in support of schema change.  For example, using an `index` evaluation function is more efficient than a `kvsplit` function at query time, but when changing the schema the use of `kvsplit` may simplify the management of that change.
