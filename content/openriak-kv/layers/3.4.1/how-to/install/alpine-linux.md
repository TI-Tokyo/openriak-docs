---
title: 'Install OpenRiak on Alpine Linux'
description: 'Show operators how to install openriak on alpine linux and confirm that the installation is ready.'
weight: 2
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
  - '\\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv\setup\install\linux\alpine-linux.md'
migration_review:
  - 'Internal links still refer to the earlier documentation hierarchy and must be retargeted to the Diátaxis paths.'
  - 'Release-specific installation, upgrade, downgrade, or quick-start instructions require verification against OpenRiak KV 3.4.1 packages.'
legacy_3_2_5_sources:
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\setup\installing\alpine-linux.md'
  - 'Package, platform, installation, upgrade, or downgrade details require release-specific verification for OpenRiak KV 3.4.1.'
tags: ['diataxis', 'kv', 'how-to']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Show operators how to install openriak on alpine linux and confirm that the installation is ready.

## Before you begin

A supported operating system and package source, verified backups, release notes for the exact target version, and a rolling-change plan for production clusters.

## Overview

### Alpine Linux

[security index]: {{< product-version-root >}}how-to/secure/
[install source erlang]: {{< product-version-root >}}how-to/install/source/
[install verify]: {{< product-version-root >}}how-to/install/verify-installation/

OpenRiak KV can be installed on Alpine Linux using a binary
package from the Riak repository.

The following steps have been tested to work with OpenRiak KV on:

* Alpine Linux 3.21 using x86_64
* Alpine Linux 3.21 using aarch64

#### Install the Alpine package

The Alpine 3.21 repository publishes OpenRiak KV 3.4.1 with OTP 24 and OTP 26
for both `x86_64` and `aarch64`.

1. Add the TI Tokyo Alpine repository:

```sh
echo 'https://files-source.tiot.jp/alpine/v3.21/main' >> /etc/apk/repositories
```

2. Install the repository signing key:

```sh
wget https://files-source.tiot.jp/alpine/alpine@tiot.jp.rsa.pub \
  -O /etc/apk/keys/alpine@tiot.jp.rsa.pub
```

3. Refresh the package index:

```sh
apk update
```

4. Install the package for the required OTP version.

For OTP 26:

```sh
apk add 'riak=3.4.1.26-r1'
```

For OTP 24:

```sh
apk add 'riak=3.4.1.24-r1'
```

Do not use the unversioned `apk add riak` command on a versioned
documentation path, because it may install a later OpenRiak release.

#### Next Steps

Now that Riak is installed, check out [Verifying a Riak Installation][install verify].

> [!WARNING]
> Migration review required: Internal links still refer to the earlier documentation hierarchy and must be retargeted to the Diátaxis paths.

## Verify the result

Confirm the installed version on every node, wait for services and transfers to settle, and run application smoke tests before proceeding.
