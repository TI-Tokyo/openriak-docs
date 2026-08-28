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
  - 'No matching OpenRiak KV 3.4.1 package was found in the official 3.4 package index for this platform.'
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

[security index]: /kv/3.4.1/how-to/secure/
[install source erlang]: /kv/3.4.1/how-to/install/source/
[install verify]: /kv/3.4.1/how-to/install/verify-installation/

OpenRiak KV can be installed on Alpine Linux using a binary
package from the Riak repository.

The following steps have been tested to work with OpenRiak KV on:

* Alpine Linux 3.21 using x86_64
* Alpine Linux 3.21 using aarch64

#### Riak 64-bit Installation

To install Riak on Alpine Linux:

1. Add the Riak repository:

* Run `echo https://files.tiot.jp/alpine/v3.21/main >> /etc/apk/repositories`

2. Download and install the Riak repository public key:
   * Run `wget http://files.tiot.jp/alpine/alpine@tiot.jp.rsa.pub -O /etc/apk/keys/alpine@tiot.jp.rsa.pub`
3. Update your list of packages:
   * Run `apk update`
4. Install Riak:
   * For the latest version, run `apk add riak`
   * For version 3.2.5 using OTP 24, run `apk add riak=3.2.5.24-r1`
   * For version 3.2.5 using OTP 25, run `apk add riak=3.2.5.25-r1`

#### Next Steps

Now that Riak is installed, check out [Verifying a Riak Installation][install verify].

> [!WARNING]
> Migration review required: Internal links still refer to the earlier documentation hierarchy and must be retargeted to the Diátaxis paths.

## Verify the result

Confirm the installed version on every node, wait for services and transfers to settle, and run application smoke tests before proceeding.
