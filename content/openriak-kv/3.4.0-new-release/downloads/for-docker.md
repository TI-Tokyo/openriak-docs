---
title: 'For Docker'
linkTitle: 'For Docker'
description: 'Download tested OpenRiak KV Dockerfiles, Compose files, and example environment files by operating system.'
weight: 1
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

{{< download-os-picker >}}
{{< docker-downloads >}}

{{< collapsable-section title="All Docker Files" level="2" id="all-docker-files" >}}
OpenRiak KV {{< current-version >}} can run in Docker for testing and development purposes.

For each supported OS, you can download:
- A Dockerfile to build the base image. This can be customised for your own custom images.
- A Docker Compose file to run a single-node cluster. This is great for local development and testing.
- A Docker Compose file to run a 5-node cluster, which is useful for integration and failover tests.
- An example .env file showing what settings can be changed easily.
{{< all-docker-downloads >}}
{{< /collapsable-section >}}
