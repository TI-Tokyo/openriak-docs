---
title: Build and install from source
description: Build a release from its pinned source and dependencies when a suitable package is unavailable or you
  need a development build. Build in an isolated environment matching the intended deployment.
weight: 180
diataxis: how-to
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- operators
legacy_3_2_5_sources:
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\setup\installing\source.md
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\setup\installing\source\erlang.md
- Package, platform, installation, upgrade, or downgrade details require release-specific verification for OpenRiak
  KV 3.4.0.
source_material:
- legacy-3.2.5
- live-3.2.5
- proposed-kv
- openriak-quickdocs-3.4
quickdocs_sources:
- https://openriak.github.io/riak/InstallAndStartGuide.html#generating-a-package
- https://openriak.github.io/riak/InstallAndStartGuide.html#install-erlangotp
- https://openriak.github.io/riak/InstallAndStartGuide.html#local-cluster
- https://openriak.github.io/riak/InstallAndStartGuide.html#local-release
- https://openriak.github.io/riak/InstallAndStartGuide.html#make-riak
- https://openriak.github.io/riak/InstallAndStartGuide.html#starting-riak-by-make-method
tags:
- diataxis
- kv
- how-to
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- how-to/install/source.md
related:
- reference/orientation-and-compatibility/platforms-architectures-and-erlang-otp-compatibility
- reference/orientation-and-compatibility/cluster-client-and-replication-compatibility
- how-to/installation/verify-an-installation
- how-to/cluster-lifecycle/upgrade-a-cluster
- foundations/overview/what-openriak-kv-is
- foundations/cluster-architecture/rings-partitions-and-virtual-nodes
---

Build a release from its pinned source and dependencies when a suitable package is unavailable or you need a development build. Build in an isolated environment matching the intended deployment.

## Choose the release and toolchain

Check [Platforms, architectures, and Erlang/OTP compatibility]({{< product-version-root >}}reference/orientation-and-compatibility/platforms-architectures-and-erlang-otp-compatibility/) for the release's OTP compatibility. Install the compiler, build tools, Git, and native development libraries required by the repository's release-specific build instructions. Use the same OTP major version for build and runtime unless the release explicitly supports another combination.

Clone the OpenRiak release repository and check out the exact release tag, verifying that it exists before building:

```sh
git clone https://github.com/OpenRiak/riak.git
cd riak
git tag --list
```

Select the tag for OpenRiak KV {{< current-version >}}. Record the resulting commit with `git rev-parse HEAD`. Do not build a moving branch and label it as a released package.

## Build and inspect

Follow the checked-out repository's `README` and `Makefile` for the release target and dependency installation. Preserve its pinned dependency revisions. Record compiler and OTP versions, the commit, and the build output alongside the resulting artifact.

Inspect the generated release's `bin`, `etc`, and `lib` directories. Run the configuration check against a dedicated empty data directory, then start the release under a non-root service account with the required directory ownership.

## Verify before deployment

Complete [Verify an installation]({{< product-version-root >}}how-to/installation/verify-an-installation/) and run the application's integration tests on the built artifact. Package or archive the release with its configuration and provenance; do not copy a partially built source tree over a running node. Follow [Upgrade an OpenRiak KV cluster]({{< product-version-root >}}how-to/cluster-lifecycle/upgrade-a-cluster/) for deployment into an existing cluster.
