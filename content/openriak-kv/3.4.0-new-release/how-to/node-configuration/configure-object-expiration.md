---
title: Configure object expiration
description: Configure expiration only for a backend that supports the required retention behaviour. Test it in
  an isolated deployment before applying it to existing data.
weight: 290
diataxis: how-to
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- operators
legacy_3_2_5_sources:
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\configuring\global-object-expiration.md
source_material:
- legacy-3.2.5
- live-3.2.5
- proposed-kv
- openriak-quickdocs-3.4
quickdocs_sources:
- https://openriak.github.io/riak/InitialDesignDecisions.html#deleting-data---changing-the-choice
tags:
- diataxis
- kv
- how-to
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- how-to/configure/global-object-expiration.md
related:
- how-to/planning-a-deployment/choose-a-deletion-and-retention-policy
- how-to/data-inspection-and-repair/erase-a-selected-set-of-keys
- how-to/data-inspection-and-repair/reap-eligible-tombstones
- reference/configuration/object-expiration-and-reclamation-settings
- foundations/data-and-consistency/deletion-tombstones-and-expiration
- foundations/storage-and-performance/persistence-filesystems-and-space-reclamation
---

Configure expiration only for a backend that supports the required retention behaviour. Test it in an isolated deployment before applying it to existing data.

## Check the backend and policy

The current expiration-related schema is below. A setting for LevelDB does not apply to Leveled or Bitcask. LevelDB is deprecated; use explicit erase and reap workflows when they better match the retention requirement.

{{< configuration-reference-table >}}
^bitcask\.expiry
^leveldb\.expiration
{{< /configuration-reference-table >}}

Record whether expiration is based on storage metadata or application timestamps, what happens to updates, and whether expired objects produce the deletion evidence required by your replication topology.

## Apply a small test

Set the backend-specific expiry enablement and retention interval on every affected node. Validate, restart as required, and write uniquely named sample objects before and after the change. Do not assume previously stored objects acquire an expiry schedule retroactively.

## Verify retention and reclamation

Read samples before and after the interval, update one sample partway through, and repeat the test after a node outage and replication catch-up. Check both read behaviour and eventual disk reclamation; a logically expired value and a removed file are different states.

If the behaviour does not meet the policy, disable new expiry according to the schema and investigate before applying it more broadly. Disabling expiry cannot recover already removed data.
