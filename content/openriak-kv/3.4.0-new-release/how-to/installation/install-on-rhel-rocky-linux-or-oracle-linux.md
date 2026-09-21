---
title: Install on RHEL, Rocky Linux, or Oracle Linux
description: Install a published OpenRiak KV package on RHEL, Rocky Linux, or Oracle Linux. Use a fresh node for
  a new deployment; use [[H78]] when changing a member of an existing cluster.
weight: 130
diataxis: how-to
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- operators
source_material:
- legacy-3.2.5
- live-3.2.5
- proposed-kv
migration_source_root: \\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv
migration_sources:
- \\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv\setup\install\linux\rhel.md
- \\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv\setup\install\linux\rocky.md
legacy_3_2_5_sources:
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\setup\installing\oracle-linux.md
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\setup\installing\rhel-centos.md
- Package, platform, installation, upgrade, or downgrade details require release-specific verification for OpenRiak
  KV 3.4.0.
tags:
- diataxis
- kv
- how-to
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- how-to/install/rhel-rocky.md
related:
- how-to/node-configuration/configure-node-identity-directories-and-the-initial-ring
- how-to/node-configuration/configure-http-and-protocol-buffers-listeners
- how-to/installation/verify-an-installation
- how-to/cluster-lifecycle/upgrade-a-cluster
- reference/orientation-and-compatibility/platforms-architectures-and-erlang-otp-compatibility
- foundations/overview/what-openriak-kv-is
- foundations/cluster-architecture/rings-partitions-and-virtual-nodes
---

Install a published OpenRiak KV package on RHEL, Rocky Linux, or Oracle Linux. Use a fresh node for a new deployment; use [Upgrade an OpenRiak KV cluster]({{< product-version-root >}}how-to/cluster-lifecycle/upgrade-a-cluster/) when changing a member of an existing cluster.

## Select the package

Confirm the installed OS release and architecture with `cat /etc/os-release` and `uname -m`. Select the matching entry below, then choose the OTP variant used by your deployment. If no matching package is listed, use [Build and install from source]({{< product-version-root >}}how-to/installation/build-and-install-from-source/) or choose a listed platform.

{{< download-os-picker >}}
{{< package-downloads >}}

## Install

Choose the exact distribution and release shown in the catalogue. Do not assume an RPM for one distribution is validated for another merely because their package format matches.

Download the package and its published checksum, verify the checksum, then replace `PACKAGE.rpm` with the downloaded filename. Let the package manager resolve dependencies from the distribution's configured repositories.

```sh
sudo dnf install ./PACKAGE.rpm
```

Check the package manager's result before continuing. Do not ignore missing dependencies or substitute libraries from an unrelated distribution.

## Configure and start

If installation starts Riak automatically, stop the service before changing an empty node's identity or backend:

{{< service-command action="stop" os="rhel" >}}

Complete [Configure node identity, directories, and the initial ring]({{< product-version-root >}}how-to/node-configuration/configure-node-identity-directories-and-the-initial-ring/) and [Configure HTTP and Protocol Buffers listeners]({{< product-version-root >}}how-to/node-configuration/configure-http-and-protocol-buffers-listeners/), then validate and start:

{{< cli-example key="shell:riak chkconfig" prefix="sudo" >}}
{{< service-command action="start" os="rhel" >}}
{{< cli-example key="shell:riak ping" prefix="sudo" >}}

Expect `pong`, then complete [Verify an installation]({{< product-version-root >}}how-to/installation/verify-an-installation/) before joining the cluster or admitting traffic. Containers without a service manager should use their image entrypoint, not the host-service commands above.
