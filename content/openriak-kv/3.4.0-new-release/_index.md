---
title: 'OpenRiak KV 3.4.0'
description: 'Orient readers to OpenRiak KV and route them to learning, task, lookup, or conceptual documentation.'
weight: 1
diataxis: 'explanation'
product: 'OpenRiak KV'
product_version: '3.4.0'
release_baseline: true
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
layout: single
---
[Downloads]: {{< product-version-root >}}downloads/
[QuickStart]: {{< product-version-root >}}how-tos/quick-start/
[QuickDocs]: https://openriak.github.io/riak/
[SectionReference]: {{< product-version-root >}}refernce/
[SectionTutorials]: {{< product-version-root >}}tutorials/
[SectionHowTos]: {{< product-version-root >}}how-tos/
[SectionFoundations]: {{< product-version-root >}}foundations/

## Overview

OpenRiak KV {{< current-version >}} is a distributed NoSQL database designed to deliver maximum data availability by distributing data across multiple servers. As long as your OpenRiak KV client can reach one Riak server, it should be able to write data.

### Supported Operating Systems

{{< download-os-picker >}}

{{% button-link link="[Downloads]" %}}Go to Downloads{{% /button-link %}}

## Quick Start

If you're new to OpenRiak KV, start with our [Quick Start guides][QuickStart] to create your first OpenRiak KV node and cluster.

## How to use the documentation

The site is split into four sections:

### **Reference**

This contains authoritative details of the configuration options, the CLI commands, APIs, clients, and compatibility across versions. Great for finding a specific piece of information.

{{% button-link link="[SectionReference]" padding="small" %}}Go to Reference{{% /button-link %}}

### **Tutorials**

Guided explanations of how to install, configure, manage and maintain OpenRiak KV. Contains detailed guides for using different features of OpenRiak.

{{% button-link link="[SectionTutorials]" padding="small" %}}Go to Tutorials{{% /button-link %}}

### **How-Tos**

Go here for in depth guides for a specific task. Great for quickly solving a problem.

{{% button-link link="[SectionHowTos]" padding="small" %}}Go to How-Tos{{% /button-link %}}

### **Foundations**

Explains the concepts, architecture, rationale, and trade-offs of OpenRiak. Superb for in-depth understanding.

{{% button-link link="[SectionFoundations]" padding="small" %}}Go to Foundations{{% /button-link %}}

## Other Documentation

- [OpenRiak QuickDocs][QuickDocs]

