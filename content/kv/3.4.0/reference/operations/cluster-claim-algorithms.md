---
title: 'Cluster claim algorithms'
description: 'Compare choose_claim_v2, choose_claim_v3, and choose_claim_v4 inputs, guarantees, and compatibility.'
weight: 100
diataxis: 'reference'
product: 'OpenRiak KV'
product_version: '3.4.0'
status: 'editorially-rewritten'
draft: true
audience:
  - 'operators'
  - 'architects'
source_material:
  - 'openriak-quickdocs-3.4'
quickdocs_sources:
  - 'https://openriak.github.io/riak/BuildAndScaleClusterGuide.html#join-process---choose_claim_v2-default'
  - 'https://openriak.github.io/riak/BuildAndScaleClusterGuide.html#join-process---choose_claim_v3'
  - 'https://openriak.github.io/riak/BuildAndScaleClusterGuide.html#join-process---choose_claim_v4-recommended'
tags: ['diataxis', 'kv', 'reference', 'quickdocs']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Compare choose_claim_v2, choose_claim_v3, and choose_claim_v4 inputs, guarantees, and compatibility.

## Details

### Join process - choose_claim_v2 (default)

The v2 claim is a simple algorithm which achieves a minimal standard of correctness, but only when locations are not defined.  It is the default algorithm.

#### Join process - choose_claim_v3

The v3 claim algorithm which tries to find an optimal solution through a series of random attempts, and returns a plan which is the most optimal it found.  The algorithm is not idempotent, repeated planning may result in different outcomes.  Restoring a previous outcome after re-planning is not possible without expert support.

The v3 algorithm does not support locations, and is considered an experimental feature, but is still in use in large scale production systems.

#### Join process - choose_claim_v4 (recommended)

Available from Riak 3.0.16

The v4 algorithm is a brute-force algorithm which will attempt to solve a sufficient answer, potentially by exhausting all possibilities.  The v4 algorithm is the only effective algorithm for handling locations.  Because it seeks a sufficient answer, rather than an optimal one, the offline `ring_calculator` can be used to determine how far the target inputs can be pushed and still have a viable solution, before running the plan.

Due to the length of time the brute-force algorithm may take, the `plan` command may timeout - however work in progress is cached, so re-running the plan after a short wait should return a plan in a timely manner, as the previous calculations will be reused.
