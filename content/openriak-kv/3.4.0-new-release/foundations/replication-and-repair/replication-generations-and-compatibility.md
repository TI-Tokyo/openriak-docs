---
title: Replication generations and compatibility
description: OpenRiak documentation covers more than one replication implementation. Next-generation replication,
  legacy v3 replication, and legacy v2 replication must be identified explicitly when configuring or diagnosing
  a deploym
weight: 260
diataxis: explanation
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- architects
- operators
legacy_3_2_5_sources:
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\using\reference\v2-multi-datacenter.md
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\using\reference\v3-multi-datacenter.md
- Legacy multi-datacenter replication terminology and commands require compatibility review.
source_material:
- legacy-3.2.5
- source-code-release-notes-3.4
- openriak-discussions
- live-3.2.5
- proposed-kv
- openriak-quickdocs-3.4
quickdocs_sources:
- https://openriak.github.io/riak/ReplicationGuide.html#legacy-replication---riak_repl
tags:
- diataxis
- kv
- explanation
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- foundations/replication/v2-and-v3-replication.md
- foundations/replication/legacy-aae.md
related:
- reference/orientation-and-compatibility/replication-generation-compatibility
- reference/replication-interfaces/next-generation-replication-runtime-controls
- reference/replication-interfaces/legacy-riak-repl-runtime-controls
- how-to/replication-and-reconciliation/connect-clusters-with-next-generation-replication
- how-to/legacy-and-specialist-workflows/maintain-legacy-v2-replication
- how-to/legacy-and-specialist-workflows/maintain-legacy-v3-replication
---

OpenRiak documentation covers more than one replication implementation. Next-generation replication, legacy v3 replication, and legacy v2 replication must be identified explicitly when configuring or diagnosing a deployment.

## Next-generation replication

The current source/queue/sink design uses its own queue, consumer, and reconciliation controls. Its TicTac-based comparisons do not imply that legacy replication settings or transports are interchangeable.

## Legacy generations

Legacy v2 and v3 belong to the `riak_repl` family. They have their own listeners, connection establishment, fullsync mechanisms, and compatibility requirements. A command containing the word “fullsync” is not sufficient to identify which implementation it controls.

## Migration boundaries

Changing generation is a data-movement and cutover exercise. Check wire compatibility, data policies, existing filters, conflict handling, and the route used for deletions. Verify convergence before switching applications, and retain a recovery path while both systems can still be compared.

## Reading older examples

Use the generation labels in Reference and the legacy workflow section. Historical references to Riak Enterprise describe the origin and applicability of that material; they do not establish a current package, support policy, or next-generation configuration.
