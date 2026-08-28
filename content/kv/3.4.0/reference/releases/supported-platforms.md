---
title: 'Supported platforms'
description: 'List supported operating systems, architectures, runtimes, and lifecycle dates for this release.'
weight: 4
diataxis: 'reference'
product: 'OpenRiak KV'
product_version: '3.4.0'
status: 'editorially-rewritten'
draft: true
audience:
  - 'architects'
  - 'operators'
legacy_3_2_5_sources:
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\setup\planning\operating-system.md'
  - 'Package, platform, installation, upgrade, or downgrade details require release-specific verification for OpenRiak KV 3.4.0.'
source_material:
  - 'legacy-3.2.5'
  - 'source-code-release-notes-3.4'
  - 'live-3.2.5'
  - 'proposed-kv'
  - 'openriak-quickdocs-3.4'
quickdocs_sources:
  - 'https://openriak.github.io/riak/InstallAndStartGuide.html#install-erlangotp'
  - 'https://openriak.github.io/riak/InstallAndStartGuide.html#using-pre-built-packages'
tags: ['diataxis', 'kv', 'reference']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

List supported operating systems, architectures, runtimes, and lifecycle dates for this release.

## Details

### Operating System Support

[downloads]: /kv/3.4.0/reference/releases/downloads/

We recommend deploying OpenRiak KV on a mainstream Unix-like operating system.
Mainstream distributions have larger support communities, making
solutions to common problems easier to find.

Basho provides [binary packages][downloads] of OpenRiak KV for the following distributions:

* **Red Hat based:** Red Hat Enterprise Linux, CentOS, Fedora Core
* **Debian based:** Debian, Ubuntu
* **Solaris based:** Sun Solaris, OpenSolaris

#### Install Erlang/OTP

Installation guides for different OTP versions are available via erlang.org:

- [OTP 24 Installation Guide](https://www.erlang.org/docs/24/installation_guide/install);
- [OTP 26 Installation Guide](https://www.erlang.org/docs/26/installation_guide/install).

For convenience [`kerl` may be used to simplify the installation of Erlang/OTP](https://github.com/kerl/kerl).

Some points to note when installing Erlang:

- If using OTP 24 take note of [CVE-2022-37026](https://nvd.nist.gov/vuln/detail/CVE-2022-37026).
- Of the optional dependencies for OTP, only OpenSSL is required for Riak.
- The OpenSSL 3.0 integration in OTP 24 is not currently considered to be production-ready and stable.
- If using OpenRiak KV 3.0.16 and OTP 22.3, Riak does not support Erlang/OTP running in [HIPE mode](https://www.erlang.org/docs/22/man/hipe_app).  HIPE is retired as of OTP 24.
- There are significant performance advantages in running Riak on OTP 26, when compared with OTP 24.3.
- The Erlang/OTP team are only committed to fixing issues in the three most recent major versions of Erlang.  Although Erlang 24.3 is mature and very stable, migrating forward to a Riak release running on a presently supported Erlang version is recommended.
- It is not possible to [migrate directly using a rolling restart](/kv/3.4.0/how-to/operate/upgrade-cluster/) from OpenRiak KV 3.0 to OpenRiak KV 3.4 due to breaking changes in the Erlang distribution protocol.  Migrating directly between these versions with zero down-time can only be managed using [the cluster migration strategy](/kv/3.4.0/how-to/configure/replication/migrate-cluster/).

#### Using pre-built packages

> The OpenRiak community currently provides Riak as **source-only**, and does not directly provide pre-built packages of Riak.

Organisations within the OpenRiak community do offer pre-built packages as part of their service offering, and these are [freely available](https://files.tiot.jp/riak/).  The use of pre-built packages is _not_ recommended by the OpenRiak community where end-to-end assurance of the software supply-chain is required.  The building of packages in a customer-specific secure environment is the preferred approach.
