---
title: 'Downloads'
linkTitle: 'Downloads'
description: 'List supported OpenRiak KV packages, checksums, repositories, and source archives by platform and version.'
weight: -10
layout: 'downloads'
hide_reading_time: true
diataxis: 'reference'
product: 'OpenRiak KV'
product_version: '3.4.0'
status: 'ready-for-external-review'
draft: false
audience:
  - 'operators'
source_material:
  - 'live-3.2.5'
  - 'proposed-kv'
  - 'openriak-quickdocs-3.4'
quickdocs_sources:
  - 'https://openriak.github.io/riak/InstallAndStartGuide.html#download-riak'
tags: ['diataxis', 'kv', 'reference']
editorial_review: 'complete'
technical_review: 'complete'
last_reviewed: '2026-09-01'
review_scope: 'editorial-and-site-integration'
---

## Recommended Downloads

Pick the OS release you intend to run OpenRiak KV {{< current-version >}} on. The documentation will also update to show any configuration values specific to that OS release.

> [!Docker] Docker
> For Docker images and Compose files, see [Downloads For Docker](for-docker/).

{{< download-os-picker >}}
{{< package-downloads >}}

{{< collapsable-section title="Source code" level="2">}}

Riak is [available to clone on GitHub](https://github.com/OpenRiak/riak).

The tag for the OpenRiak KV {{< current-version >}} is `riak-{{< current-version >}}` and can be accessed [here](https://github.com/OpenRiak/riak/tree/riak-{{< current-version >}}).

> [!NOTE]
> Tagged releases contain a `rebar.lock` file which ensures all major dependencies are fetched from the precise commit made at the point of release.

Each major release has an associated branch which represents current development activity.  For Riak {{< current-version format="major-minor" >}} this is `openriak-{{< current-version format="major-minor" >}}` and can be accessed [here](https://github.com/OpenRiak/riak/tree/openriak-{{< current-version format="major-minor" >}}). Building from these branches may contain unreleased changes.

{{< /collapsable-section >}}

{{< collapsable-section title="All Packages" level="2" id="all-downloads" >}}
Download the package to install OpenRiak KV {{< current-version >}} on any supported OS.
{{< all-package-downloads >}}
{{< /collapsable-section >}}
