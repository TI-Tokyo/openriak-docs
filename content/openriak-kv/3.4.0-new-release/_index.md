---
title: OpenRiak KV 3.4.0
description: Learn, deploy, operate, and integrate OpenRiak KV.
weight: 1
diataxis: explanation
product: OpenRiak KV
product_version: 3.4.0
release_baseline: true
status: editorially-rewritten
draft: true
audience:
- all-readers
legacy_3_2_5_sources:
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\index.md
source_material:
- legacy-3.2.5
- source-code-release-notes-3.4
- openriak-quickdocs-3.4
- live-3.2.5
- proposed-kv
quickdocs_sources:
- https://openriak.github.io/riak/#openriak-quickdocs-34
tags:
- diataxis
- kv
- explanation
editorial_review: complete
technical_review: required
last_reviewed: '2026-08-28'
review_scope: editorial-and-site-integration
layout: single
related:
- tutorials/first-cluster/build-and-explore-a-docker-cluster
- reference/configuration/all-configuration-settings-and-defaults
- reference/commands
- how-to/monitoring-and-diagnostics/perform-routine-cluster-health-checks
---

OpenRiak KV is a distributed key-value database for applications that need to store and retrieve data across several servers. Its replica policies and conflict handling let applications make explicit choices about availability and consistency.

## Start learning

New to OpenRiak? Read [What OpenRiak KV is]({{< product-version-root >}}foundations/overview/what-openriak-kv-is/), then follow [Build and explore a Docker cluster]({{< product-version-root >}}tutorials/first-cluster/build-and-explore-a-docker-cluster/) to build a disposable cluster and make your first request.

## Choose your next task

- [Foundations]({{< product-version-root >}}foundations/): understand the data model, architecture, and operational trade-offs.
- [Tutorials]({{< product-version-root >}}tutorials/): work through guided exercises with observable results.
- [How-to]({{< product-version-root >}}how-to/): complete a specific installation, application, maintenance, or recovery task.
- [Reference]({{< product-version-root >}}reference/): find settings, commands, API fields, and compatibility limits.

## Download and install

Choose the package that matches your operating system and architecture on the [downloads page]({{< product-version-root >}}downloads/). Existing deployments should follow [Upgrade an OpenRiak KV cluster]({{< product-version-root >}}how-to/cluster-lifecycle/upgrade-a-cluster/) before changing a cluster member's package.
