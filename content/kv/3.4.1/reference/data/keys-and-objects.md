---
title: 'Keys and objects'
description: 'Define the fields, limits, supported operations, representations, and compatibility rules for keys and objects.'
weight: 5
diataxis: 'reference'
product: 'OpenRiak KV'
product_version: '3.4.1'
status: 'editorially-rewritten'
draft: true
audience:
  - 'developers'
  - 'operators'
source_material:
  - 'live-3.2.5'
  - 'proposed-kv'
  - 'openriak-quickdocs-3.4'
quickdocs_sources:
  - 'https://openriak.github.io/riak/ObjectAPI.html#object-identifier---the-url'
  - 'https://openriak.github.io/riak/ObjectAPI.html#object-value---the-request-body'
tags: ['diataxis', 'kv', 'reference']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Define the fields, limits, supported operations, representations, and compatibility rules for keys and objects.

## Details

### Object Identifier - the URL

The Riak object Identifier is split into three parts:

- Bucket Type;
- Bucket;
- Key.

Internally within Riak all three elements are binary identifiers.  With the Object HTTP API, these elements are represented within the URL e.g. `/types/<BucketType>/buckets/<Bucket>/keys/<Key>`.

> Although it is possible to use identifiers that are not URL-safe through the Protocol Buffer API, it is important not to do so - as any object using such an identifier may not be accessible via the HTTP API.  Guidelines for the safe use of Unicode in cross-API identifiers, will be clarified in a future Riak release.

The [Bucket Type](/kv/3.4.1/reference/configuration/bucket-properties/) is used to describe the properties of the object.  Properties are associated with a Bucket Type, and all Objects in the Buckets under that type will inherit those properties.

A Bucket Type cannot be used via the API until it has been created and activated, to do this see:

```console
riak admin bucket-type --help
```

The Bucket is a namespace, and a Bucket Type is allowed to have an arbitrary number of Buckets.  A Bucket cannot be moved between Bucket Types, but the properties of an individual Bucket may be changed to override that of the Bucket Type.

Keys are unique identifiers of an object within a Bucket.

#### Object Value - the request body

Within Riak, object values are generally opaque to the database code.  The schema of the value is managed by the application, not by Riak.  Values are normally binaries, but a content-type can be passed via the API and associated with the value (as a standard 'Content-Type' request header in a PUT or POST).  The provided 'Content-Type' will be stored in Riak as object metadata, and returned in future fetch requests as a standard 'Content-Type' response header.  Riak does not validate that the object value is a match for the content type provided.

If a content type is not provided, the value will be assumed to be a binary i.e. `application/octet-stream`.

The size of the values is managed by the application, not the database; there is no auto-sharding of inbound values.  There is a small overhead associated with every object, and so Riak is not optimised for handling large numbers of very small values.  There is no upper limit to the number of unique objects that can be stored - but internal operations, especially inter-cluster reconciliation, have reduced efficiency when the count of objects greatly exceeds 10 billion.

> Typically values stored in Riak are between o(1KB) and o(1MB) in size, but are not constrained by these limits.

In standard Riak operations the database does not require knowledge of the structure of the value, however Riak does have support for [data-types](/kv/3.4.1/reference/specialized-apis/data-type-api/). These types, [also referred to as CRDTs](https://en.wikipedia.org/wiki/Conflict-free_replicated_data_type), are specially formatted values where the handling of conflict is deterministic and managed within the database, so the application does not see siblings even when [`allow_mult` is set to `true`](/kv/3.4.1/reference/configuration/bucket-properties/) and concurrent changes are made to the same object.  The performance and scalability of Riak is improved when values are externally managed, rather than internally constrained through the use of these types.
