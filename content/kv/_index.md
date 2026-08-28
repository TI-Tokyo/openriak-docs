---
title: 'OpenRiak KV documentation'
description: 'Choose the documentation version that matches the OpenRiak KV release deployed in your environment.'
weight: 1
url: '/kv/'
page_kind: 'version-selector'
versions:
  - '3.4.1'
  - '3.4.0'
diataxis: 'reference'
product: 'OpenRiak KV'
product_version: 'all'
status: 'content-specification'
draft: true
audience:
  - 'all-readers'
source_material:
  - 'source-code-release-notes-3.4'
  - 'openriak-quickdocs-3.4'
  - 'live-3.2.5'
  - 'proposed-kv'
tags: ['diataxis', 'kv', 'reference']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Choose the documentation version that matches the OpenRiak KV release deployed in your environment.

> [!NOTE]
> This page is a content specification. Replace the guidance below with tested, version-specific OpenRiak KV documentation before publishing it.

## Choose a version

Use the documentation version that exactly matches the OpenRiak KV release deployed in the target environment. Commands, defaults, configuration keys, and operational cautions must not be assumed to be interchangeable between releases.

- [OpenRiak KV 3.4.0]({{< baseurl >}}kv/3.4.0/) — Orient readers to OpenRiak KV and route them to learning, task, lookup, or conceptual documentation.
- [OpenRiak KV 3.4.1]({{< baseurl >}}kv/3.4.1/) — Orient readers to OpenRiak KV and route them to learning, task, lookup, or conceptual documentation.

## What this page still needs

Before publication, add the supported-version policy, links to release and upgrade guidance, and a concise explanation of how readers can identify the version running on every node in a cluster.

## Review requirements

Verify every version link in a built site, confirm that unsupported or unreleased versions are not listed, and make the default or latest version explicit without silently redirecting readers away from older documentation.
