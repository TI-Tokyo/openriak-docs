---
title: TicTac anti-entropy settings
description: TicTac settings control the current anti-entropy stores, tree rebuilds, exchanges, and repair pacing.
  Legacy anti-entropy settings are listed separately.
weight: 160
diataxis: reference
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- operators
source_material:
- legacy-3.2.5
- source-code-release-notes-3.4
- live-3.2.5
- proposed-kv
legacy_3_2_5_sources:
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\configuring\active-anti-entropy.md
tags:
- diataxis
- kv
- reference
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- reference/configuration/active-anti-entropy.md
related:
- how-to/replication-and-reconciliation/enable-tictac-anti-entropy
- reference/legacy-and-experimental-features/legacy-aae-and-riak-repl-settings
- foundations/data-and-consistency/bucket-types-and-data-policies
---

TicTac settings control the current anti-entropy stores, tree rebuilds, exchanges, and repair pacing. Legacy anti-entropy settings are listed separately.

## Settings

Select an operating system, then search by setting name or description. Values shown are the defaults from that release’s settings metadata; explicit configuration overrides take precedence.

{{< configuration-reference-table >}}
^(tictacaae_|aae_|legacyformat_tictacaae_tree)
{{< /configuration-reference-table >}}
