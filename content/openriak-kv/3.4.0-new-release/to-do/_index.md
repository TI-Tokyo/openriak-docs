---
title: To Do
description: Editorial inventory, release validation, and rendering checks.
weight: 1000
product: OpenRiak KV
product_version: 3.4.0
draft: true
hide_provenance: true
cascade:
  draft: true
  hide_provenance: true
---

The four documentation areas have been reorganised and their reader-facing content reviewed. These pages track the implemented locations and the validation still needed before publication.

## Implemented inventories

- [Foundations](foundations/): 40 explanation topics in eight subsections.
- [How-to](how-to/): 148 task guides in 15 subsections.
- [Reference](reference/): 136 planned lookup topics in 13 subsections, plus the expanded generated command catalogue.
- [Tutorials](tutorials/): 39 learning topics in seven subsections. Cloud exercises are grouped by provider, starting with AWS EC2.

The menus follow a learning progression. Related documentation appears at the end of pages, and linked workflows include previous/next navigation. Redirects are intentionally omitted for these unpublished paths.

## Validation still required

- Rehearse native platform installation, AWS EC2 and Vagrant provisioning, complete recovery/replication/security exercises, and the remaining language examples on their stated environments.
- Review operational procedures against the deployment's actual failure, retention, and security requirements before publication. Editorial review and successful rendering are separate from runtime validation.
- Complete partial settings metadata extraction. The deployed metadata records unresolved dependency warnings; do not invent missing defaults in prose.
- Establish tested compatibility for specialist integrations such as the Redis add-on, JMX bridge, SNMP, and Riak Control. Their pages now state the verification boundary instead of repeating obsolete installation instructions.
- Resolve the Alpine system wrapper's handling of quoted JSON arguments in the packaging repository. The learning shell uses the release launcher and active VM arguments as a documented workaround.

## Runtime issues found during this review

- The 3.4.0 Alpine 3.24 / OTP 26 image reproduced a Query API continuation failure: `riak_kv_query_server` called `hd([])` when a vnode supplied an empty batch and the HTTP request timed out. Resolve and retest this before recommending Query API pagination. The larger-result tutorial now uses tested secondary-index pagination.
- A projected-attribute grouped-count probe returned no rows on that image even though the matching index entries were present. The published exercise now groups the direct `city_bin` index and produces the expected counts. Investigate projected-term accumulation separately; do not mark it verified from this exercise.

## Verified examples and contracts

The local five-node 3.4.0 Alpine/OTP 26 cluster has exercised bucket-type creation, counters, sets, grow-only sets, maps, HyperLogLog, and exact/projected Query API fixtures, combination queries (intersection, union and subtraction), direct-index grouped counts, and secondary-index continuations. The Python, Node.js, and Java HTTP examples passed their read, update, index, and delete checks. Protocol Buffers definitions are tied to the pinned release source, and CLI pages are generated from deployed metadata for both versions.

Hugo builds, metadata/generator regression tests, and browser checks cover both documentation versions. Browser checks cover reference filtering and sorting, command help and OS variants, workflow links, heading hierarchy, and mobile layouts.

Use [For Review](for-review/) for page-level review records and [Tests](tests/) for rendering components. Keep additional runtime results with the page or verification report rather than marking every inherited page tested at once.

## Authoring rules

Keep concepts in Foundations, procedures in How-to, learning exercises in Tutorials, and exact contracts in Reference. Use settings, CLI, and package metadata for their respective values and interfaces. Deliberate example values must be labelled as examples. Use the shared searchable reference-table component for product reference tables, and keep related links and workflow navigation current when moving a page.
