---
title: Grammar and spelling review
linkTitle: Grammar and spelling review
description: Grammar and spelling findings in documentation added or changed for OpenRiak KV 3.4.1.
weight: -5
product: OpenRiak KV
product_version: 3.4.1
draft: true
hide_provenance: true
features: []
concepts: ["documentation"]
---

This is the grammar and spelling review for documentation **added or changed in OpenRiak KV 3.4.1**, updated on **6 November 2026**. The reviewed source documentation has not been changed as part of this update.

The target is **UK English with a professional, friendly tone for IT readers**. Familiar technical terms, concise instructions, contractions, and short headings are acceptable.

## Scope

This review compares 3.4.1's authored pages and generated reference text with 3.4.0. It lists findings in the new or changed content only. Unchanged pages and unchanged wording inherited from 3.4.0 are excluded; their findings remain in the [3.4.0 review]({{< product-version-root version="3.4.0" >}}to-do/grammar-and-spelling-review/).

This refresh checks the release-specific page content and generated command descriptions, examples and help against 3.4.0. Shared wording, including the truncated page descriptions listed in the 3.4.0 review, is not repeated here. The previous finding against “all ongoing partition repair” has been withdrawn: “repair” can describe the activity, so that wording does not require a grammar correction.

## Errors in command example prose

These findings concern the explanatory text supplied with command examples, not the literal output captured from a command.

| Page and location | Existing wording | Finding |
| --- | --- | --- |
| [riak admin backup — example title]({{< product-version-root >}}reference/commands/riak/admin/backup/) | Backup an empty test cluster | “Backup” is a noun or adjective. The action in this example title needs the two-word verb “back up”. |

## UK English consistency in command example prose

These findings are specific to the examples exposed in 3.4.1. As in the 3.4.0 review, `-ize` forms are treated as consistency findings rather than universally incorrect British English.

| Page and location | Existing wording | UK form used for this review |
| --- | --- | --- |
| [resync_bucket — example title and description]({{< product-version-root >}}reference/commands/erlang/riak-client/resync-bucket/) | Resynchronize an empty bucket; Resynchronize cli_reference_empty | “Resynchronise”. Keep the bucket identifier unchanged. The example is also embedded in [Reconcile selected buckets]({{< product-version-root >}}how-to/replication-and-reconciliation/reconcile-selected-buckets/). |
| [resync_bucket — error remedy]({{< product-version-root >}}reference/commands/erlang/riak-client/resync-bucket/) | before resynchronizing a bucket | “resynchronising”. |
| [riak repl — full-sync example description]({{< product-version-root >}}reference/commands/riak/repl/) | An acknowledgment alone does not establish replication. | “acknowledgement”. |

## Errors reproduced from upstream reference text

These findings occur in generated command help. Any later correction should be made upstream or clearly annotated, then regenerated; literal excerpts should continue to match their source. No captured output or generated JSON has been edited.

| Page and location | Existing wording | Finding |
| --- | --- | --- |
| [riak admin stat — captured command-group usage]({{< product-version-root >}}reference/commands/riak/admin/stat/) | Two kinds of wildcard are suppored | Spelling mistake: “supported”. |
| [riak admin vnode-status — help text]({{< product-version-root >}}reference/commands/riak/admin/vnode-status/) | as a json object | The acronym JSON is incorrectly lower-cased. |
