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

This is the grammar and spelling review for documentation **added or changed in OpenRiak KV 3.4.1**, scoped on **5 November 2026**. No corrections have been applied to the reviewed documentation.

The target is **UK English with a professional, friendly tone for IT readers**. Familiar technical terms, concise instructions, contractions, and short headings are acceptable.

## Scope

This review compares 3.4.1's authored pages and generated reference text with 3.4.0. It lists findings in the new or changed content only. Unchanged pages and unchanged wording inherited from 3.4.0 are excluded; their findings remain in the [3.4.0 review](/docs/openriak-kv/3.4.0/to-do/grammar-and-spelling-review/).

The previously flagged authored prose and configuration descriptions are unchanged from 3.4.0, so they are not repeated here. The findings below concern command help newly exposed or expanded in the 3.4.1 documentation.

## Errors reproduced from upstream reference text

These findings occur in generated command help. Any later correction should be made upstream or clearly annotated, then regenerated; literal excerpts should continue to match their source. No captured output or generated JSON has been edited.

| Page and location | Existing wording | Finding |
| --- | --- | --- |
| [riak admin stat — help text]({{< product-version-root >}}reference/commands/riak/admin/stat/) | Two kinds of wildcard are suppored | Spelling mistake: “supported”. |
| [riak admin node repair stop — help text]({{< product-version-root >}}reference/commands/riak/admin/node/repair/stop/) | all ongoing partition repair | “All” is paired with a singular countable operation here; the wording needs plural “repairs” or an explicit mass noun such as “repair work”. |
| [riak admin vnode-status — help text]({{< product-version-root >}}reference/commands/riak/admin/vnode-status/) | as a json object | The acronym JSON is incorrectly lower-cased. |
