---
title: 'Install OpenRiak on RHEL or Rocky Linux'
description: 'Show operators how to install openriak on rhel or rocky linux and confirm that the installation is ready.'
weight: 7
diataxis: 'how-to'
product: 'OpenRiak KV'
product_version: '3.4.1'
status: 'editorially-rewritten'
draft: true
audience:
  - 'operators'
source_material:
  - 'legacy-3.2.5'
  - 'live-3.2.5'
  - 'proposed-kv'
migration_source_root: '\\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv'
migration_sources:
  - '\\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv\setup\install\linux\rhel.md'
  - '\\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv\setup\install\linux\rocky.md'
migration_review:
  - 'Internal links still refer to the earlier documentation hierarchy and must be retargeted to the Diátaxis paths.'
  - 'Commands or links derived from the 3.2.5 documentation were version-normalized for 3.4.1 and require technical verification.'
  - 'Release-specific installation, upgrade, downgrade, or quick-start instructions require verification against OpenRiak KV 3.4.1 packages.'
legacy_3_2_5_sources:
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\setup\installing\oracle-linux.md'
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\setup\installing\rhel-centos.md'
  - 'Package, platform, installation, upgrade, or downgrade details require release-specific verification for OpenRiak KV 3.4.1.'
tags: ['diataxis', 'kv', 'how-to']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Show operators how to install openriak on rhel or rocky linux and confirm that the installation is ready.

## Before you begin

A supported operating system and package source, verified backups, release notes for the exact target version, and a rolling-change plan for production clusters.

## Overview

### Oracle Linux

[install source index]: {{< product-version-root >}}how-to/install/source/
[install source erlang]: {{< product-version-root >}}how-to/install/source/
[install verify]: {{< product-version-root >}}how-to/install/verify-installation/

#### Installing From Package

If you wish to install the Oracle Linux package by hand, follow these
instructions.

##### Oracle Linux 9 (x86_64)

The published OpenRiak KV {{< current-version >}} package uses OTP 26.

Before installing Riak on Oracle Linux 9, we need to satisfy some Erlang dependencies
from EPEL first by installing the EPEL repository:

```bash
sudo yum install -y epel-release
```

Once EPEL has been installed, install OpenRiak KV using `yum`:

```bash
wget https://files.tiot.jp/riak/kv/3.4/{{< current-version >}}/oracle/9/riak-{{< current-version >}}.OTP26-1.el9.x86_64.rpm
sudo yum install -y riak-{{< current-version >}}.OTP26-1.el9.x86_64.rpm
```

#### Next Steps

Now that Riak is installed, check out [Verifying a Riak Installation][install verify].

### RHEL and CentOS

OpenRiak KV can be installed on RHEL-based systems using a binary package or by
[compiling OpenRiak KV from source code][install source index]. Packages are
published for RHEL 8 and RHEL 9; Rocky Linux users should use the package for
the corresponding RHEL major version.

> **Note on SELinux**
>
> RHEL-compatible systems enable SELinux by default. Keep SELinux enabled unless
> your security policy and troubleshooting results require a different setting.

If you wish to install the RHEL or Rocky Linux packages by hand, follow these
instructions.

#### RHEL 8 or Rocky Linux 8 (x86_64)

Before installing Riak on CentOS 8/RHEL 8, we need to satisfy some Erlang dependencies
from EPEL first by installing the EPEL repository:

Once EPEL has been installed, install the package using `yum`:

```bash
wget https://files.tiot.jp/riak/kv/3.4/{{< current-version >}}/rhel/8/riak-{{< current-version >}}.OTP26-1.el8.x86_64.rpm
sudo yum localinstall -y riak-{{< current-version >}}.OTP26-1.el8.x86_64.rpm
```

Or you can install the `.rpm` package manually:

```bash
wget https://files.tiot.jp/riak/kv/3.4/{{< current-version >}}/rhel/8/riak-{{< current-version >}}.OTP26-1.el8.x86_64.rpm
sudo rpm -Uvh riak-{{< current-version >}}.OTP26-1.el8.x86_64.rpm
```

##### RHEL 9 or Rocky Linux 9 (x86_64)

Install the package using `yum`:

```bash
wget https://files.tiot.jp/riak/kv/3.4/{{< current-version >}}/rhel/9/riak-{{< current-version >}}.OTP26-1.el9.x86_64.rpm
sudo yum localinstall -y riak-{{< current-version >}}.OTP26-1.el9.x86_64.rpm
```

Or install the `.rpm` package manually:

```bash
wget https://files.tiot.jp/riak/kv/3.4/{{< current-version >}}/rhel/9/riak-{{< current-version >}}.OTP26-1.el9.x86_64.rpm
sudo rpm -Uvh riak-{{< current-version >}}.OTP26-1.el9.x86_64.rpm
```

#### Installing From Source

Riak requires an [Erlang](http://www.erlang.org/) installation.
Instructions can be found in [Installing Erlang][install source erlang].

Building from source will require the following packages:

* `gcc`
* `gcc-c++`
* `glibc-devel`
* `make`
* `pam-devel`

You can install these with yum:

```bash
sudo yum install gcc gcc-c++ glibc-devel make git pam-devel
```

Follow [the source installation guide][install source index] to obtain and build
the OpenRiak KV {{< current-version >}} source tree. A successful build creates the release in
the `rel/riak` directory.

#### Next Steps

> [!WARNING]
> Migration review required: Internal links still refer to the earlier documentation hierarchy and must be retargeted to the Diátaxis paths.

## Verify the result

Confirm the installed version on every node, wait for services and transfers to settle, and run application smoke tests before proceeding.
