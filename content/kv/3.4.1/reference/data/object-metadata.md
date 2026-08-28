---
title: 'Object metadata'
description: 'Define the fields, limits, supported operations, representations, and compatibility rules for object metadata.'
weight: 6
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
  - 'https://openriak.github.io/riak/ObjectAPI.html#object-meta-content---the-request-and-response-headers'
  - 'https://openriak.github.io/riak/ObjectAPI.html#object-metadata'
  - 'https://openriak.github.io/riak/ObjectAPI.html#user-metadata'
tags: ['diataxis', 'kv', 'reference']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Define the fields, limits, supported operations, representations, and compatibility rules for object metadata.

## Details

### Object Meta Content - the request and response headers

There are four object components that make use of HTTP headers:

- Version vector;
- User Metadata;
- Object Metadata;
- Index Entries.

#### User Metadata

User Metadata is arbitrary pairs of binary Keys and Values that form part of the content.  The user metadata is opaque to the database.  Internally, and via the protocol buffer API then the Keys and Values may be any binary - but for presentation and use via the HTTP API they keys must be url safe and case insensitive, and the values must be visible ascii.

#### Object Metadata

Riak carries metadata about an object, primarily:

- the last modified date;
  - internally within Riak this is a timestamp to microsecond accuracy,
  - when presented via the HTTP API the accuracy is truncated to a second.
- the deleted status (does the object represent a current value or a record of deletion).
- the ["dot" for each content item](/kv/3.4.1/reference/data/version-vectors/) - this is not returned via the API;
- the content type
  - the content type is never validated, it may be added to an update, and will be returned as-is regardless of the nature of the value.
