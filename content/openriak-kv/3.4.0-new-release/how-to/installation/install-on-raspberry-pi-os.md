---
title: Install on Raspberry Pi OS
description: Install a published OpenRiak KV package on Raspberry Pi OS. Use a fresh node for a new deployment;
  use [[H78]] when changing a member of an existing cluster.
weight: 160
diataxis: how-to
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- operators
source_material:
- live-3.2.5
- proposed-kv
migration_source_root: \\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv
migration_sources:
- \\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv\setup\install\linux\rapsbian.md
tags:
- diataxis
- kv
- how-to
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- how-to/install/raspbian.md
related:
- how-to/node-configuration/configure-node-identity-directories-and-the-initial-ring
- how-to/node-configuration/configure-http-and-protocol-buffers-listeners
- how-to/installation/verify-an-installation
- how-to/cluster-lifecycle/upgrade-a-cluster
- reference/orientation-and-compatibility/platforms-architectures-and-erlang-otp-compatibility
- foundations/overview/what-openriak-kv-is
- foundations/cluster-architecture/rings-partitions-and-virtual-nodes
---

Install a published OpenRiak KV package on Raspberry Pi OS. Use a fresh node for a new deployment; use [Upgrade an OpenRiak KV cluster]({{< product-version-root >}}how-to/cluster-lifecycle/upgrade-a-cluster/) when changing a member of an existing cluster.

## Select the package

Confirm the installed OS release and architecture with `cat /etc/os-release` and `uname -m`. Select the matching entry below, then choose the OTP variant used by your deployment. If no matching package is listed, use [Build and install from source]({{< product-version-root >}}how-to/installation/build-and-install-from-source/) or choose a listed platform.

{{< download-os-picker >}}
{{< package-downloads >}}

## Install

Check both the OS userspace architecture (`dpkg --print-architecture`) and the device architecture. A 64-bit CPU can run a 32-bit OS, which requires a different package.

Download the package and its published checksum, verify the checksum, then replace `PACKAGE.deb` with the downloaded filename. Let the package manager resolve dependencies from the distribution's configured repositories.

```sh
sudo apt-get update
sudo apt-get install ./PACKAGE.deb
```

Check the package manager's result before continuing. Do not ignore missing dependencies or substitute libraries from an unrelated distribution.

## Configure and start

If installation starts Riak automatically, stop the service before changing an empty node's identity or backend:

{{< service-command action="stop" os="raspbian" >}}

Complete [Configure node identity, directories, and the initial ring]({{< product-version-root >}}how-to/node-configuration/configure-node-identity-directories-and-the-initial-ring/) and [Configure HTTP and Protocol Buffers listeners]({{< product-version-root >}}how-to/node-configuration/configure-http-and-protocol-buffers-listeners/), then validate and start:

{{< cli-example key="shell:riak chkconfig" prefix="sudo" >}}
{{< service-command action="start" os="raspbian" >}}
{{< cli-example key="shell:riak ping" prefix="sudo" >}}

Expect `pong`, then complete [Verify an installation]({{< product-version-root >}}how-to/installation/verify-an-installation/) before joining the cluster or admitting traffic. Containers without a service manager should use their image entrypoint, not the host-service commands above.
