---
title: 'Object request options'
description: 'Define common OpenRiak Object API GET and PUT parameters, defaults, and response behavior.'
weight: 27
diataxis: 'reference'
product: 'OpenRiak KV'
product_version: '3.4.0'
status: 'editorially-rewritten'
draft: true
audience:
  - 'developers'
source_material:
  - 'openriak-quickdocs-3.4'
quickdocs_sources:
  - 'https://openriak.github.io/riak/ObjectAPI.html#get-and-put-options'
tags: ['diataxis', 'kv', 'reference', 'quickdocs']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Define common OpenRiak Object API GET and PUT parameters, defaults, and response behavior.

## Details

### GET and PUT Options

The GET and PUT API allow for options to be passed in the HTTP API via [HTTP query parameters appended to the URI](https://www.rfc-editor.org/rfc/rfc3986#section-3.4).

It is recommended that the options supported in the Object API should be set via [bucket properties](/kv/3.4.0/reference/configuration/bucket-properties/) wherever possible (except where the option is a per-request option rather than a property e.g. `vtag`).  It is best practice to define the expectations for managing a request within the properties of the type, and only use options in exceptional cases to override those definitions.

The most common options used are:

- `vtag`; to be added to a read request from an object in a sibling state, where the value is the `vtag` of one of the sibling objects.
- `notfound_ok`; should be set to `false` if the application is expecting an object.  Only valid for read requests.
- `node_confirms`; can be set to a number 1..N where N is the `n_val` for that object, and used to indicate how many unique nodes must contribute to the quorum when handling the request.  Can be set on either store or read requests.
- Available from Riak 3.0.8`sync_on_write`; can be set to `one`, `all` or `backend` and is used to indicate whether it is necessary to flush the write to disk before confirming a request.  Generally all backends should be set not to flush pre-request (for performance), and where required the setting of `one` or `all` may be used where data-loss protection in catastrophic failure scenarios is of elevated importance.  Only valid for store requests.
- `pr`; can be set to 1..N where N is the `n_val` for that object.  Stipulates how many primary vnodes must be involved in providing consensus before returning an object.  Should be set to `1`.  Only valid for read requests.
- `pw`; can be set to 1..N where N is the `n_val` for that object.  Stipulates how many primary vnodes must have acknowledged acceptance of a store request before returning a positive response to the client.  Only valid for write requests.
- `return_body`; should the updated object be returned in response to a store request.  Only valid for write requests.
- `deleted_vclock`; if an object is not_found, but is in fact a tombstone, should the version vector of the tombstone be returned, to be used if it is required to update the deleted object with a new object.  Only valid for read requests.
- `timeout`; the maximum time (in milliseconds) to wait for a response from Riak before returning a timeout error.

There are four other potential PUT and GET options related to the balance between consistency, performance and availability: `w`, `r`, `sloppy_quorum` and `dw`; but changing of these defaults on a per-request basis is not recommended.
