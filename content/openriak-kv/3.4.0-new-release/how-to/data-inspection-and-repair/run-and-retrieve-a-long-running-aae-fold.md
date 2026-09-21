---
title: Run and retrieve a long-running AAE fold
description: Run an AAE fold with a bounded scope and retain its completed result outside an interactive terminal.
  Enable TicTac AAE and wait for usable stores before submitting the fold.
weight: 940
diataxis: how-to
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- operators
source_material:
- source-code-release-notes-3.4
- openriak-quickdocs-3.4
quickdocs_sources:
- https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#running-aae-folds
- https://openriak.github.io/riak/OtherAPI.html#aae-folds-via-the-command-line
tags:
- diataxis
- kv
- how-to
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- how-to/operate/aae-fold/run-from-command-line.md
related:
- how-to/data-inspection-and-repair/inventory-buckets-using-aae-folds
- how-to/data-inspection-and-repair/find-oversized-objects-or-excessive-siblings
- how-to/data-inspection-and-repair/count-objects-in-a-selected-scope
- how-to/data-inspection-and-repair/repair-a-selected-key-range
- reference/aae-fold-api/fold-invocation-and-result-conventions
- reference/aae-fold-api/fold-filters
- foundations/replication-and-repair/targeted-reconciliation-and-aae-folds
- foundations/replication-and-repair/read-repair-and-tictac-anti-entropy
---

Run an AAE fold with a bounded scope and retain its completed result outside an interactive terminal. Enable TicTac AAE and wait for usable stores before submitting the fold.

## Choose the operation and bounds

Select the fold in [Fold invocation and result conventions]({{< product-version-root >}}reference/aae-fold-api/fold-invocation-and-result-conventions/) and record its bucket, key or modified-time interval, and whether it only reads or also queues changes. Prefer a count before a potentially large key listing. Some folds collect the full result in memory before writing it.

## Submit through the CLI

{{< cli-command key="shell:riak admin tictacaae fold" >}}

Choose the documented sub-operation and use `-o` to specify an explicit result path writable by the Riak service account. Use a unique filename for each run and keep it outside sensitive configuration directories.

## Retrieve the completed result

Wait for the fold to finish and the result file to be written. Preserve the submitted scope, node, start/end times, and errors alongside the JSON. An empty or absent file is not a successful zero count. Copy the completed file through your normal administrative channel and validate its JSON before processing it.

For a repair, erase, reap, or replication fold, also monitor the consumer queues: the returned count usually describes work submitted, not every side effect completed.
