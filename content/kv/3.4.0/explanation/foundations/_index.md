---
title: 'OpenRiak foundations'
description: 'Introduce the ideas that shape OpenRiak behavior and appropriate use.'
weight: 1
diataxis: 'explanation'
product: 'OpenRiak KV'
product_version: '3.4.0'
status: 'editorially-rewritten'
draft: true
audience:
  - 'architects'
  - 'operators'
  - 'developers'
legacy_3_2_5_sources:
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\learn.md'
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\learn\concepts.md'
source_material:
  - 'legacy-3.2.5'
  - 'openriak-quickdocs-3.4'
  - 'live-3.2.5'
quickdocs_sources:
  - 'https://openriak.github.io/riak/#openriak-quickdocs-34'
  - 'https://openriak.github.io/riak/RiakTheoryGuide.html#riak-kv---theory-guide'
tags: ['diataxis', 'kv', 'explanation']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Introduce the ideas that shape OpenRiak behavior and appropriate use.

## Overview

### Learn About OpenRiak KV

[learn why riak]: ./why-riak-kv/
[learn use cases]: ./use-cases/
[learn new nosql]: ./new-to-nosql/
[glossary]: ./glossary/
[concepts]: ./concepts/

#### In This Section

##### [Why OpenRiak KV?][learn why riak]

An overview of OpenRiak KV and when to use it.

[Learn More >>][learn why riak]

###### [Use Cases][learn use cases]

Details use cases and applications in which OpenRiak KV excels.

[Learn More >>][learn use cases]

###### [Glossary][glossary]

A list of terms relating to Riak used throughout the documentation.

[Learn More >>][glossary]

###### [Concepts][concepts]

Provides definitions for, insight into, and high level information about the various parts of OpenRiak KV

[Learn More >>][concepts]

### Concepts

[concept aae]: /kv/3.4.0/explanation/replication/active-anti-entropy/
[concept buckets]: /kv/3.4.0/explanation/data-model/keys-objects-and-buckets/
[concept cap neg]: /kv/3.4.0/explanation/foundations/capability-negotiation/
[concept causal context]: /kv/3.4.0/explanation/data-model/causal-context/
[concept clusters]: /kv/3.4.0/explanation/foundations/clusters-rings-and-partitions/
[concept crdts]: /kv/3.4.0/explanation/data-model/distributed-data-types/
[concept eventual consistency]: /kv/3.4.0/explanation/consistency/eventual-consistency/
[concept keys objects]: /kv/3.4.0/explanation/data-model/keys-objects-and-buckets/
[concept replication]: /kv/3.4.0/explanation/replication/
[concept strong consistency]: /kv/3.4.0/reference/specialized-apis/strong-consistency-api/
[concept vnodes]: /kv/3.4.0/explanation/foundations/virtual-nodes/
[config index]: /kv/3.4.0/how-to/configure/
[plan index]: /kv/3.4.0/how-to/plan/
[use index]: /kv/3.4.0/how-to/operate/

OpenRiak KV has many great features, functions, and guiding principles that inform how the product works. This section provides definitions for, insight into, and high level information about the various parts of OpenRiak KV you will encounter as you [plan][plan index], [configure][config index], and [use][use index] Riak.

Learn more about:

* [Active Anti-Entropy (AAE)][concept aae]
* [Buckets][concept buckets]
* [Capability Negotiation][concept cap neg]
* [Causal Context][concept causal context]
* [Clusters][concept clusters]
* [Convergent Replicated Data Types (CRDTs)][concept crdts]
* [Eventual Consistency][concept eventual consistency]
* [Keys and Objects][concept keys objects]
* [Replication][concept replication]
* [Virtual Nodes (vnodes)][concept vnodes]

### [OpenRiak QuickDocs 3.4](https://openriak.github.io/riak/)

#### OpenRiak QuickDocs 3.4

This site provides overview documentation for the OpenRiak community release of Riak.

#### OpenRiak KV - Theory Guide

This guide provides insight into the underlying theories and processes which underpin the function of an OpenRiak cluster.  Understanding this theory will be helpful to understand the design, setup and operation of an OpenRiak cluster.

- [The ring and how data is distributed in Riak](/kv/3.4.0/explanation/foundations/clusters-rings-and-partitions/)
- [Eventual consistency](/kv/3.4.0/explanation/consistency/eventual-consistency/)
- [Background processes](/kv/3.4.0/explanation/operations/)
- [Backend design](/kv/3.4.0/explanation/storage/)
