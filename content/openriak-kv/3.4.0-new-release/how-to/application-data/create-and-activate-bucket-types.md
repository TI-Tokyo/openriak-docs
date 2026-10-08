---
title: Create and activate bucket types
description: Create a bucket type to apply a shared object policy or select a distributed data type. Type creation
  and activation are separate operations; activation makes the type available to applications.
weight: 370
diataxis: how-to
product: OpenRiak KV
product_version: 3.4.0
status: reviewed
draft: true
audience:
- operators
legacy_3_2_5_sources:
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\using\cluster-operations\bucket-types.md
source_material:
- legacy-3.2.5
- live-3.2.5
- proposed-kv
- openriak-quickdocs-3.4
quickdocs_sources:
- https://openriak.github.io/riak/InstallAndStartGuide.html#configuration-of-riak---bucket-properties
- https://openriak.github.io/riak/InstallAndStartGuide.html#property---allow_mult
- https://openriak.github.io/riak/InstallAndStartGuide.html#property---dvv_enabled
- https://openriak.github.io/riak/InstallAndStartGuide.html#property---general-readwrite-parameters
- https://openriak.github.io/riak/InstallAndStartGuide.html#property---last_write_wins
- https://openriak.github.io/riak/InstallAndStartGuide.html#property---n_val
- https://openriak.github.io/riak/InstallAndStartGuide.html#property---node_confirms
- https://openriak.github.io/riak/InstallAndStartGuide.html#property---notfound_ok
- https://openriak.github.io/riak/InstallAndStartGuide.html#property---pr-and-pw
- https://openriak.github.io/riak/InstallAndStartGuide.html#property---small_vclock
- https://openriak.github.io/riak/InstallAndStartGuide.html#property---sync_on_write
tags:
- diataxis
- kv
- how-to
editorial_review: complete
technical_review: complete
last_reviewed: '2026-09-27'
review_scope: content review
review-by: TI Tokyo/JOM
restructured_from:
- how-to/operate/manage-bucket-types.md
related:
- how-to/application-data/use-bucket-types-in-an-application
- how-to/application-data/resolve-concurrent-object-updates
- reference/configuration/bucket-properties-and-defaults
- reference/commands/riak/admin/bucket-type
- foundations/data-and-consistency/objects-keys-and-buckets
- foundations/data-and-consistency/bucket-types-and-data-policies
- foundations/data-and-consistency/causality-version-vectors-and-siblings
features: ["bucket-properties","client-operations"]
concepts: ["data-access","data-policy"]
---

Create a bucket type to apply a shared object policy or select a distributed data type. Type creation and activation are separate operations; activation makes the type available to applications.

## Define the policy

Choose a stable type name and inspect the properties in [Bucket properties and defaults]({{< product-version-root >}}reference/configuration/bucket-properties-and-defaults/). For ordinary objects with application-managed conflicts, this example enables siblings:

{{< cli-example key="shell:riak admin bucket-type create" args=`documents '{"props":{"allow_mult":true}}'` >}}

## Inspect and activate

{{< cli-example key="shell:riak admin bucket-type status" args="documents" >}}

Confirm the proposed properties, then activate:

{{< cli-example key="shell:riak admin bucket-type activate" args="documents" >}}

Repeat the above status command until the type is active. If the type already exists, inspect it before changing anything; do not assume it has the example's policy.

## Verify the bucket type

1. Address an object with `/types/documents/buckets/BUCKET/keys/KEY`. 
2. Write and read a sample, and exercise concurrent updates to verify the policy. 

You need to create the matching type separately in every replication destination before sending typed objects there.
