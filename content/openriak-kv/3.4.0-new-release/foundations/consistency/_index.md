---
title: 'Consistency concepts'
description: 'Introduce how OpenRiak balances availability, convergence, and stronger consistency guarantees.'
weight: 1
diataxis: 'explanation'
product: 'OpenRiak KV'
product_version: '3.4.0'
status: 'editorially-rewritten'
draft: true
audience:
  - 'architects'
  - 'developers'
  - 'operators'
source_material:
  - 'openriak-quickdocs-3.4'
  - 'live-3.2.5'
quickdocs_sources:
  - 'https://openriak.github.io/riak/QueryAPI.html#consistency'
tags: ['diataxis', 'kv', 'explanation']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Introduce how OpenRiak balances availability, convergence, and stronger consistency guarantees.

## Overview

### Consistency

Index changes are not deferred to an async process, at a vnode level all index changes are made as a transaction with the object change.  Outside of failure scenarios, secondary index queries will almost always immediately reflect the results of any changes in the object (with caveats related to unreliable latency across intra-cluster networking communication).

In failure and recovery scenarios, false negatives are possible (i.e. results may be missing until anti-entropy mechanisms correct) but results will be eventually consistent.  The query uses a coverage plan which will check only one (of N) potential copies of the data, and so should a vnode be temporarily incorrect, the entropy is not detected as part of the query.  The `participate_in_coverage` configuration option (which can be applied at run-time) is used to mitigate this - this can be used to prevent a node with a known entropy issue from being involved in queries.

## In this section

- [Conditional requests]({{< product-version-root >}}foundations/consistency/conditional-requests/) — Explain how validators and conditional operations reduce races, bandwidth, and unnecessary object reads.
- [Eventual consistency]({{< product-version-root >}}foundations/consistency/eventual-consistency/) — Explain eventual consistency, convergence, quorums, and the application behaviors they produce.
- [Read and write quorums]({{< product-version-root >}}foundations/consistency/read-write-quorums/) — Explain how quorum choices affect latency, availability, durability, and stale reads.
- [Strong consistency]({{< product-version-root >}}foundations/consistency/strong-consistency/) — Explain strong consistency guarantees, limitations, costs, and suitable workloads.
