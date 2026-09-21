---
title: Platforms, architectures, and Erlang/OTP compatibility
description: Select the operating system and architecture to see packages and runtime combinations published for
  OpenRiak KV . Availability here comes from the package metadata for this release.
weight: 20
diataxis: reference
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- architects
- operators
legacy_3_2_5_sources:
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\setup\planning\operating-system.md
- Package, platform, installation, upgrade, or downgrade details require release-specific verification for OpenRiak
  KV 3.4.0.
source_material:
- legacy-3.2.5
- source-code-release-notes-3.4
- live-3.2.5
- proposed-kv
- openriak-quickdocs-3.4
quickdocs_sources:
- https://openriak.github.io/riak/InstallAndStartGuide.html#install-erlangotp
- https://openriak.github.io/riak/InstallAndStartGuide.html#using-pre-built-packages
tags:
- diataxis
- kv
- reference
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- reference/releases/supported-platforms.md
related:
- reference/orientation-and-compatibility/cluster-client-and-replication-compatibility
- how-to/installation/install-on-debian-or-ubuntu
- how-to/installation/install-on-rhel-rocky-linux-or-oracle-linux
- how-to/installation/install-on-alpine-linux
- how-to/installation/build-and-install-from-source
- foundations/overview/what-openriak-kv-is
- foundations/replication-and-repair/replication-generations-and-compatibility
- foundations/storage-and-performance/storage-backend-trade-offs
---

Select the operating system and architecture to see packages and runtime combinations published for OpenRiak KV {{< current-version >}}. Availability here comes from the package metadata for this release.

## Published packages

{{< download-os-picker >}}

{{< package-downloads >}}

## Compatibility boundaries

Match the package architecture, distribution release, and Erlang/OTP build to the deployment. An operating system appearing in historical documentation is not evidence that a package exists for this release. A package listing is also distinct from the operating system vendor's maintenance lifecycle.

For upgrades, check cluster and runtime compatibility before mixing builds. Building from source is a separate path with its own toolchain requirements.
