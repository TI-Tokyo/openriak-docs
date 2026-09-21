---
title: Release notes
linkTitle: Release Notes
description: Changes and compatibility notes for OpenRiak KV 3.4.0.
weight: -20
diataxis: reference
product: OpenRiak KV
product_version: 3.4.0
audience:
- all-readers
tags:
- diataxis
- kv
- reference
- release-notes
draft: true
status: needs-review
review_scope:
- link-checking
- content
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-17'
review-by: TI Tokyo/JOM
related:
- how-to/cluster-lifecycle/upgrade-a-cluster
- reference/orientation-and-compatibility/feature-status-and-deprecations
---

OpenRiak KV 3.4.0 introduces the current Query API and token-assisted conditional PUTs, with operational improvements for logging, anti-entropy, and repair.

## Additions and changes

- [Endpoints and request schema]({{< product-version-root >}}reference/query-api/endpoints-and-request-schema/) provides projection, filtering, set combination, and several result accumulation modes.
- [Conditional requests and latch objects]({{< product-version-root >}}reference/http-api/conditional-requests-and-latch-objects/) describes token-assisted conditional writes and their limits.
- [Configure split and JSON log handlers]({{< product-version-root >}}how-to/node-configuration/configure-split-and-json-log-handlers/) configures split handlers and JSON logging.
- [AAE commands]({{< product-version-root >}}reference/commands/aae/) provides CLI inspection, rebuild controls, and file-output folds for TicTac AAE.
- [Control repair impact during application traffic]({{< product-version-root >}}how-to/data-inspection-and-repair/control-repair-impact-during-application-traffic/) covers repair under application load, including the improved repair options.
- [Exclude temporary data from cached AAE trees]({{< product-version-root >}}how-to/replication-and-reconciliation/exclude-temporary-data-from-cached-aae-trees/) controls whether selected data participates in cached AAE trees.

The release supports OTP 24 and OTP 26. [Feature status and deprecations]({{< product-version-root >}}reference/orientation-and-compatibility/feature-status-and-deprecations/) records the deprecated backend, query, consistency, and legacy interfaces; review them before upgrading an existing deployment.

Source: [OpenRiak release notes](https://github.com/OpenRiak/riak/blob/77bbdbe5cd86428d98f9953c1fecb579a4d96b14/RELEASE-NOTES.md).
