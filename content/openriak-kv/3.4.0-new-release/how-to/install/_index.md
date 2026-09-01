---
title: 'Install and verify OpenRiak'
description: 'Introduce installation procedures and their common verification outcome.'
weight: 1
diataxis: 'how-to'
product: 'OpenRiak KV'
product_version: '3.4.0'
status: 'editorially-rewritten'
draft: true
audience:
  - 'operators'
migration_source_root: '\\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv'
migration_sources:
  - '\\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv\setup\install\index.md'
migration_review:
  - 'Release-specific installation, upgrade, downgrade, or quick-start instructions require verification against OpenRiak KV 3.4.0 packages.'
legacy_3_2_5_sources:
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\setup.md'
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\setup\installing.md'
  - 'Package, platform, installation, upgrade, or downgrade details require release-specific verification for OpenRiak KV 3.4.0.'
source_material:
  - 'legacy-3.2.5'
  - 'openriak-quickdocs-3.4'
  - 'live-3.2.5'
  - 'proposed-kv'
quickdocs_sources:
  - 'https://openriak.github.io/riak/InstallAndStartGuide.html#installation'
  - 'https://openriak.github.io/riak/InstallAndStartGuide.html#riak-kv---install-and-start'
  - 'https://openriak.github.io/riak/InstallAndStartGuide.html#using-pre-built-packages'
tags: ['diataxis', 'kv', 'how-to']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Introduce installation procedures and their common verification outcome.

## Before you begin

A supported operating system and package source, verified backups, release notes for the exact target version, and a rolling-change plan for production clusters.

## Overview

### Setup OpenRiak KV

[plan index]: {{< product-version-root >}}how-to/plan/
[install index]: {{< product-version-root >}}how-to/install/
[upgrade index]: {{< product-version-root >}}how-to/operate/upgrade-cluster/
[downgrade]: {{< product-version-root >}}how-to/operate/downgrade-cluster/

#### In This Section

##### [Planning][plan index]

Information on planning your OpenRiak KV cluster including software & hardware recommendations.

[Learn More >>][plan index]

###### [Installing][install index]

Step-by-step tutorials on installing OpenRiak KV.

[Learn More >>][install index]

###### [Upgrading][upgrade index]

Guides on upgrading your OpenRiak KV cluster.

[Learn More >>][upgrade index]

###### [Downgrading][downgrade]

A guide on downgrading your OpenRiak KV cluster.

[Learn More >>][downgrade]

### Installing OpenRiak KV

[install aws]: {{< product-version-root >}}how-to/install/amazon-linux/
[install alpine]: {{< product-version-root >}}how-to/install/alpine-linux/
[install debian & ubuntu]: {{< product-version-root >}}how-to/install/debian-ubuntu/
[install raspbian]: {{< product-version-root >}}how-to/install/debian-ubuntu/#raspbian-bullseye
[install rhel & centos]: {{< product-version-root >}}how-to/install/rhel-rocky/
[install oracle linux]: {{< product-version-root >}}how-to/install/rhel-rocky/
[install source index]: {{< product-version-root >}}how-to/install/source/
[upgrade index]: {{< product-version-root >}}how-to/operate/upgrade-cluster/

#### Supported Platforms

Riak is supported on numerous popular operating systems and virtualized
environments. The following information will help you to
properly install or upgrade Riak in one of the supported environments:

* [Amazon Web Services][install aws]
  * [Alpine Linux][install alpine]
  * [Debian & Ubuntu][install debian & ubuntu]
  * [Raspbian][install raspbian]
  * [Oracle Linux][install oracle linux]
  * [RHEL & CentOS][install rhel & centos]

#### Building from Source

If your platform isn’t listed above, you may be able to build Riak from source. See [Installing Riak from Source][install source index] for instructions.

#### Community Projects

Check out [Community Projects][community projects] for installing with tools such as [Chef](https://www.chef.io/chef/), [Ansible](http://www.ansible.com/), or [Cloudsoft](http://www.cloudsoftcorp.com/).

#### Upgrading

For information on upgrading an existing cluster see [Upgrading OpenRiak KV][upgrade index].

#### Installation

Riak is built on the Erlang/OTP platform.  Only the even numbered major versions of Erlang/OTP are fully tested for operating Riak.  For each major version of Riak, the major version is initially released supporting two major OTP versions, where the lower version is common with the previous Riak major release.  Once a Riak major release has been in production for 12 months, future minor releases may only support the higher of the two Erlang/OTP versions.

The mappings for current and planned releases are:

|Riak Release| Supported OTP Version
|:------------|:------------:|
| OpenRiak KV 3.0.16 | OTP 22.3 |
| OpenRiak KV 3.2.6 | OTP 24.3 |
| OpenRiak KV {{< current-version >}} | OTP 24.3 or OTP 26.2 (recommended) |
| OpenRiak KV 4.0 (planned) | OTP 26.2 or OTP 28.3 |

Any updates to this mappings will be announced on the [Riak discussion forum](https://github.com/orgs/OpenRiak/discussions).

Riak can be potentially built on most Unix-flavour systems, including OSX for development machines; but is primarily run in production on up-to-date versions of CentOS or Ubuntu.

#### Using pre-built packages

> The OpenRiak community currently provides Riak as **source-only**, and does not directly provide pre-built packages of Riak.

Organisations within the OpenRiak community do offer pre-built packages as part of their service offering, and these are [freely available](https://files.tiot.jp/riak/).  The use of pre-built packages is _not_ recommended by the OpenRiak community where end-to-end assurance of the software supply-chain is required.  The building of packages in a customer-specific secure environment is the preferred approach.

> [!WARNING]
> Migration review required: Release-specific installation, upgrade, downgrade, or quick-start instructions require verification against OpenRiak KV {{< current-version >}} packages.

## Verify the result

Confirm the installed version on every node, wait for services and transfers to settle, and run application smoke tests before proceeding.
