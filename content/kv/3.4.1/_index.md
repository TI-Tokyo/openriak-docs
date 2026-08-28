---
title: 'OpenRiak KV 3.4.1'
description: 'Orient readers to OpenRiak KV and route them to learning, task, lookup, or conceptual documentation.'
weight: 1
url: '/kv/3.4.1/'
diataxis: 'explanation'
product: 'OpenRiak KV'
product_version: '3.4.1'
status: 'editorially-rewritten'
draft: true
audience:
  - 'all-readers'
legacy_3_2_5_sources:
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\index.md'
source_material:
  - 'legacy-3.2.5'
  - 'source-code-release-notes-3.4'
  - 'openriak-quickdocs-3.4'
  - 'live-3.2.5'
  - 'proposed-kv'
quickdocs_sources:
  - 'https://openriak.github.io/riak/#openriak-quickdocs-34'
tags: ['diataxis', 'kv', 'explanation']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Orient readers to OpenRiak KV and route them to learning, task, lookup, or conceptual documentation.

## Overview

### OpenRiak KV 3.2.5

[aboutenterprise]: https://www.tiot.jp/en/about-us/contact-us/
[config index]: {{< baseurl >}}kv/3.4.1/how-to/configure/
[downloads]: {{< baseurl >}}kv/3.4.1/reference/releases/downloads/
[install index]: {{< baseurl >}}kv/3.4.1/how-to/install/
[plan index]: {{< baseurl >}}kv/3.4.1/how-to/plan/
[perf open files]: {{< baseurl >}}kv/3.4.1/how-to/tune/set-open-files-limit/
[install debian & ubuntu]: {{< baseurl >}}kv/3.4.1/how-to/install/debian-ubuntu/
[getting started]: {{< baseurl >}}kv/3.4.1/tutorials/first-application/
[dev client libraries]: {{< baseurl >}}kv/3.4.1/reference/client-libraries/

OpenRiak KV is a distributed NoSQL database designed to deliver maximum data availability by distributing data across multiple servers. As long as your OpenRiak KV client can reach one Riak server, it should be able to write data.

This release is tested with OTP 20, OTP 21 and OTP 22; but optimal performance is likely to be achieved when using OTP 22.

#### Supported Operating Systems

- Alpine Linux 3.21
- Amazon Linux 2023
- CentOS 8
- CentOS 9
- Debian 10.0 ("Buster")
- Debian 11.0 ("Bullseye")
- Debian 12.0 ("Bookworm")
- Oracle Linux 9
- Red Hat Enterprise Linux 8
- Red Hat Enterprise Linux 9
- Raspbian Bullseye
- Ubuntu 20.04.4 ("Focal Fossa")
- Ubuntu 22.04 ("Jammy Jellyfish")
- Ubuntu 24.04 ("Noble Numbat")

#### Getting Started

Are you brand new to OpenRiak KV? Start by [downloading][downloads] OpenRiak KV, and then follow the below pages to get started:

1. [Install OpenRiak KV][install index]
2. [Plan your OpenRiak KV setup][plan index]
3. [Configure OpenRiak KV for your needs][config index]

**Developing with OpenRiak KV**
If you are looking to integrate OpenRiak KV with your existing tools, check out the [Developing with OpenRiak KV]({{< baseurl >}}kv/3.4.1/how-to/develop/) docs. They provide instructions and examples for languages such as: Java, Ruby, Python, Go, Haskell, NodeJS, Erlang, and more.

#### Popular Docs

1. [Open Files Limit][perf open files]
2. [Installing on Debian-Ubuntu][install debian & ubuntu]
3. [Developing with OpenRiak KV: Getting Started][getting started]
4. [Developing with OpenRiak KV: Client Libraries][dev client libraries]

### [OpenRiak QuickDocs 3.4](https://openriak.github.io/riak/)

#### OpenRiak QuickDocs 3.4

This site provides overview documentation for the OpenRiak community release of Riak.

## In this section

- [Explanation]({{< baseurl >}}kv/3.4.1/explanation/) — Route readers to concepts, architecture, rationale, trade-offs, and operational mental models.
- [How-to guides]({{< baseurl >}}kv/3.4.1/how-to/) — Route practitioners to focused procedures for installing, configuring, operating, securing, and troubleshooting OpenRiak.
- [Reference]({{< baseurl >}}kv/3.4.1/reference/) — Route readers to authoritative configuration, command, API, data, client, and compatibility facts.
- [Tutorials]({{< baseurl >}}kv/3.4.1/tutorials/) — Introduce the guided learning paths and state what readers will build in each one.
