---
title: 'Install OpenRiak on Debian or Ubuntu'
description: 'Show operators how to install openriak on debian or ubuntu and confirm that the installation is ready.'
weight: 4
diataxis: 'how-to'
product: 'OpenRiak KV'
product_version: '3.4.0'
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
  - '\\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv\setup\install\linux\debian.md'
  - '\\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv\setup\install\linux\ubuntu.md'
migration_review:
  - 'Internal links still refer to the earlier documentation hierarchy and must be retargeted to the Diátaxis paths.'
  - 'Commands or links derived from the 3.2.5 documentation were version-normalized for 3.4.0 and require technical verification.'
  - 'Release-specific installation, upgrade, downgrade, or quick-start instructions require verification against OpenRiak KV 3.4.0 packages.'
legacy_3_2_5_sources:
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\setup\installing\debian-ubuntu.md'
  - 'Package, platform, installation, upgrade, or downgrade details require release-specific verification for OpenRiak KV 3.4.0.'
tags: ['diataxis', 'kv', 'how-to']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Show operators how to install openriak on debian or ubuntu and confirm that the installation is ready.

## Before you begin

A supported operating system and package source, verified backups, release notes for the exact target version, and a rolling-change plan for production clusters.

## Overview

### Debian and Ubuntu

[install source index]: {{< baseurl >}}kv/3.4.0/how-to/install/source/
[security index]: {{< baseurl >}}kv/3.4.0/how-to/secure/
[install source erlang]: {{< baseurl >}}kv/3.4.0/how-to/install/source/
[install verify]: {{< baseurl >}}kv/3.4.0/how-to/install/verify-installation/

OpenRiak KV can be installed on Debian or Ubuntu-based systems using a binary
package or by compiling from source code.

Binary packages for OpenRiak KV 3.4.0 are published for:

- Ubuntu 22.04 on AMD64
- Ubuntu 24.04 on AMD64 and ARM64
- Debian 12 on AMD64

#### Installing From Package

If you wish to install the deb packages by hand, follow these
instructions.

##### PAM Library Requirement for Ubuntu

One dependency that may be missing on your machine is the `libpam0g-dev`
package used for Pluggable Authentication Module (PAM) authentication,
associated with [Riak security][security index].

To install:

```bash
sudo apt-get install libpam0g-dev
```
OpenRiak KV 3.4.0 packages are available with OTP 24 and OTP 26. Select the
package that matches the OTP version required by your deployment.

###### Ubuntu 22.04 Jammy (AMD64, OTP 26)

```bash
wget https://files.tiot.jp/riak/kv/3.4/3.4.0/ubuntu/jammy64/riak_3.4.0-OTP26_amd64.deb
sudo dpkg -i riak_3.4.0-OTP26_amd64.deb
```

For OTP 24, download and install
[`riak_3.4.0-OTP24_amd64.deb`](https://files.tiot.jp/riak/kv/3.4/3.4.0/ubuntu/jammy64/riak_3.4.0-OTP24_amd64.deb).

###### Ubuntu 24.04 Noble (AMD64, OTP 26)

```bash
wget https://files.tiot.jp/riak/kv/3.4/3.4.0/ubuntu/noble64/riak_3.4.0-OTP26_amd64.deb
sudo dpkg -i riak_3.4.0-OTP26_amd64.deb
```

For OTP 24, download and install
[`riak_3.4.0-OTP24_amd64.deb`](https://files.tiot.jp/riak/kv/3.4/3.4.0/ubuntu/noble64/riak_3.4.0-OTP24_amd64.deb).

###### Ubuntu 24.04 Noble (ARM64, OTP 26)

```bash
wget https://files.tiot.jp/riak/kv/3.4/3.4.0/ubuntu/noble64/riak_3.4.0-OTP26_arm64.deb
sudo dpkg -i riak_3.4.0-OTP26_arm64.deb
```

For OTP 24, download and install
[`riak_3.4.0-OTP24_arm64.deb`](https://files.tiot.jp/riak/kv/3.4/3.4.0/ubuntu/noble64/riak_3.4.0-OTP24_arm64.deb).

###### Debian 12 Bookworm (AMD64, OTP 26)

```bash
wget https://files.tiot.jp/riak/kv/3.4/3.4.0/debian/12/riak_3.4.0-OTP26_amd64.deb
sudo dpkg -i riak_3.4.0-OTP26_amd64.deb
```

For OTP 24, download and install
[`riak_3.4.0-OTP24_amd64.deb`](https://files.tiot.jp/riak/kv/3.4/3.4.0/debian/12/riak_3.4.0-OTP24_amd64.deb).

#### Next Steps

Now that Riak is installed, check out [Verifying a Riak Installation][install verify].

> [!WARNING]
> Migration review required: Internal links still refer to the earlier documentation hierarchy and must be retargeted to the Diátaxis paths.

## Verify the result

Confirm the installed version on every node, wait for services and transfers to settle, and run application smoke tests before proceeding.
