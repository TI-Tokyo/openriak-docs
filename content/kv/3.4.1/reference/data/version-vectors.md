---
title: 'Version vectors'
description: 'Define the fields, limits, supported operations, representations, and compatibility rules for version vectors.'
weight: 8
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
  - 'https://openriak.github.io/riak/ObjectAPI.html#version-vector'
tags: ['diataxis', 'kv', 'reference']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Define the fields, limits, supported operations, representations, and compatibility rules for version vectors.

## Details

### Version Vector

The Riak [version vector]({{< baseurl >}}kv/3.4.1/explanation/data-model/version-vectors-and-siblings/) is relevant to the database, but generally opaque to the application.  The application should read the version vector (which will be presented base64 encoded), and present the read version vector when updating an object.  The application does not need to understand the contents of the version vector.

The version vector is referred to in the API as a `vector clock` (or `vclock`).  This vector is used internally within Riak to track which content is most up-to-date - to differentiate between content that is superseded (i.e. where an update had seen the content) or genuinely concurrent (the writes were made in parallel).  Parallel writes will lead to unresolvable conflict, and how this is handled is defined within the [bucket properties]({{< baseurl >}}kv/3.4.1/reference/configuration/bucket-properties/).
