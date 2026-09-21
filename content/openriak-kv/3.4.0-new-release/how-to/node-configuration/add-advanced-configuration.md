---
title: Add advanced configuration
description: Use `advanced.config` only for settings that require Erlang application terms or are not exposed through
  `riak.conf`. Prefer a named `riak.conf` setting when the schema provides it.
weight: 220
diataxis: how-to
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- operators
source_material:
- openriak-quickdocs-3.4
quickdocs_sources:
- https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#extending-configuration
- https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#using-advancedconfig
tags:
- diataxis
- kv
- how-to
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- how-to/configure/advanced-configuration.md
related:
- how-to/node-configuration/inspect-and-manage-effective-configuration
- how-to/node-configuration/validate-configuration-before-startup
- how-to/node-configuration/set-runtime-environment-variables
- reference/configuration/configuration-files-syntax-and-precedence
- reference/configuration/runtime-environment-variables
- foundations/cluster-architecture/rings-partitions-and-virtual-nodes
- foundations/cluster-architecture/the-lifecycle-of-a-read-and-a-write
---

Use `advanced.config` only for settings that require Erlang application terms or are not exposed through `riak.conf`. Prefer a named `riak.conf` setting when the schema provides it.

## Check the mapping

Find the setting's application and internal name in [All configuration settings and defaults]({{< product-version-root >}}reference/configuration/all-configuration-settings-and-defaults/). Confirm its type and whether changing it requires a restart. Do not copy an internal key from another release without checking the matching source or metadata.

## Edit and validate

Back up the existing files. Place the required application/key/value tuple in the installed release's advanced configuration file, preserving valid Erlang term syntax and its terminating period. See [Configuration files, syntax, and precedence]({{< product-version-root >}}reference/configuration/configuration-files-syntax-and-precedence/) for file precedence and syntax.

{{< cli-example key="shell:riak chkconfig" >}}

Resolve parser and translation errors before restarting. Keep related changes together in configuration management so a later package upgrade does not silently remove the override.

## Confirm the effective value

After a controlled restart, inspect the generated configuration and the relevant runtime application environment. Exercise the affected operation and compare its metrics with the pre-change baseline. Revert the file and restart if the intended effect is not observed.
