---
title: 'Run an AAE fold from the command line'
description: 'Show operators how to start a long-running AAE fold and write its completed results to disk.'
weight: 11
diataxis: 'how-to'
product: 'OpenRiak KV'
product_version: '3.4.0'
status: 'editorially-rewritten'
draft: true
audience:
  - 'operators'
source_material:
  - 'source-code-release-notes-3.4'
  - 'openriak-quickdocs-3.4'
quickdocs_sources:
  - 'https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#running-aae-folds'
  - 'https://openriak.github.io/riak/OtherAPI.html#aae-folds-via-the-command-line'
tags: ['diataxis', 'kv', 'how-to']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Show operators how to start a long-running AAE fold and write its completed results to disk.

## Before you begin

A healthy cluster, current backups, and access to cluster status and logs. Record the starting state before making an operational change.

## Overview

### Running AAE Folds

Refer to the [API guide for AAE Fold]({{< product-version-root >}}reference/aae-fold-api/) for information on triggering an AAE fold from `riak remote_console`.

#### AAE Folds via the Command Line

**Available from OpenRiak KV {{< current-version >}}.**

AAE folds can be triggered via the command line using `riak admin tictacaae fold`:

```console
riak admin tictacaae fold list-buckets NVAL
riak admin tictacaae fold find-keys BUCKET KEY_RANGE MODIFIED_RANGE sibling_count=COUNT|object_size=BYTES
riak admin tictacaae fold find-keys BUCKET KEY_RANGE MODIFIED_RANGE sibling_count=COUNT|object_size=BYTES
riak admin tictacaae fold find|count-tombstones KEY_RANGE SEGMENTS MODIFIED_RANGE
riak admin tictacaae fold reap-tombstones KEY_RANGE SEGMENTS MODIFIED_RANGE CHANGE_METHOD
riak admin tictacaae fold object-stats BUCKET KEY_RANGE MODIFIED_RANGE
riak admin tictacaae fold erase-keys BUCKET KEY_RANGE SEGMENTS MODIFIED_RANGE CHANGE_METHOD
riak admin tictacaae fold repair-keys BUCKET KEY_RANGE MODIFIED_RANGE
```

Each of these fold commands will call the corresponding aae_fold operation and write the results in JSON format in a file named `aaefold-%o-results-%t.json`, where `%o` will be substituted with the operation being performed, and `%t`, with the current datetime string, or to a file explicitly specified with option `-o`.

> The outcome is written to the file only when the fold is completed; so if using `find_keys` the node must be able to hold all keys found in memory at least twice (as the result set needs to be copied between processes).

> It is recommended that the output file be specified, including the full file path, using the `-o` option; rather than being left to the default.  The file path should be writable by the `riak` user.

## Verify the result

Compare cluster health and workload behaviour with the recorded starting state, and confirm that all affected nodes have converged.
