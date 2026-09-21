---
title: Install and use a commit hook
description: Deploy an Erlang commit hook and associate it with the intended bucket policy. Test the hook's return
  contract and failure behaviour before allowing application writes through it.
weight: 530
diataxis: how-to
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- developers
legacy_3_2_5_sources:
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\developing\usage\commit-hooks.md
source_material:
- legacy-3.2.5
- live-3.2.5
- proposed-kv
- openriak-quickdocs-3.4
quickdocs_sources:
- https://openriak.github.io/riak/ObjectAPI.html#commit-hooks
tags:
- diataxis
- kv
- how-to
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- how-to/develop/write-commit-hook.md
related:
- reference/extensions-and-specialist-interfaces/custom-code-and-hook-interfaces
- reference/configuration/bucket-properties-and-defaults
- how-to/application-data/create-and-activate-bucket-types
- how-to/application-data/make-conditional-reads-and-writes
- foundations/data-and-consistency/objects-keys-and-buckets
- foundations/data-and-consistency/bucket-types-and-data-policies
- foundations/data-and-consistency/causality-version-vectors-and-siblings
---

Deploy an Erlang commit hook and associate it with the intended bucket policy. Test the hook's return contract and failure behaviour before allowing application writes through it.

## Implement and distribute the module

Use the pre-commit or post-commit callback contract in [Custom code and hook interfaces]({{< product-version-root >}}reference/extensions-and-specialist-interfaces/custom-code-and-hook-interfaces/). Keep execution bounded; synchronous external dependencies can delay or fail database writes. A post-commit callback must not recursively write the same key without a guard against re-entry.

Compile against the deployment's OTP and Riak interfaces, then install the module in the configured code path on every node that can coordinate a write. Confirm the expected module version is loaded everywhere before enabling the policy.

## Associate the hook

Set the bucket type's `precommit` or `postcommit` property to the module/function entries documented in [Bucket properties and defaults]({{< product-version-root >}}reference/configuration/bucket-properties-and-defaults/). Use [Create and activate bucket types]({{< product-version-root >}}how-to/application-data/create-and-activate-bucket-types/) for a new type or the metadata command below for an existing one:

{{< cli-example key="shell:riak admin bucket-type update" >}}

## Test success and failure

Write a valid object and confirm the intended transformation or notification. Write an invalid object and verify the expected rejection. Test a hook exception and timeout in an isolated environment, and confirm application retry behaviour does not duplicate external effects.

To roll back, remove the hook from the policy before removing its module from nodes. Verify writes succeed without the hook, then remove the code during controlled maintenance.
