---
title: Inspect and manage effective configuration
description: Inspect the configuration a node actually uses before diagnosing behaviour or changing a deployment.
weight: 240
diataxis: how-to
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- operators
migration_source_root: \\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv
migration_sources:
- \\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv\configure\guides\managing-configuration.md
legacy_3_2_5_sources:
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\configuring\managing.md
source_material:
- legacy-3.2.5
- live-3.2.5
- proposed-kv
- openriak-quickdocs-3.4
quickdocs_sources:
- https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#accessing-configuration
- https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#extending-configuration
tags:
- diataxis
- kv
- how-to
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- how-to/configure/manage-configuration.md
related:
- how-to/node-configuration/add-advanced-configuration
- how-to/node-configuration/set-runtime-environment-variables
- how-to/node-configuration/validate-configuration-before-startup
- how-to/monitoring-and-diagnostics/collect-diagnostic-evidence
- reference/configuration/all-configuration-settings-and-defaults
- reference/configuration/configuration-files-syntax-and-precedence
- foundations/cluster-architecture/rings-partitions-and-virtual-nodes
- foundations/cluster-architecture/the-lifecycle-of-a-read-and-a-write
---

Inspect the configuration a node actually uses before diagnosing behaviour or changing a deployment.

## Validate the input files

{{< cli-example key="shell:riak chkconfig" >}}

Confirm that the command addresses the intended installation and configuration directory. Fix schema or syntax errors before comparing values.

## Compare configured and effective values

Inspect the generated application configuration and VM arguments for the running process, using the platform directories in [Node identity, directories, and ring settings]({{< product-version-root >}}reference/configuration/node-identity-directories-and-ring-settings/). Compare them with `riak.conf`, `advanced.config`, service environment files, and launch arguments. Resolve precedence using [Configuration files, syntax, and precedence]({{< product-version-root >}}reference/configuration/configuration-files-syntax-and-precedence/). Do not edit generated files as the persistent source of configuration.

For values that may have changed since startup, use the remote console to read the owning Erlang application's environment. A process may cache configuration; use its dedicated status interface where available.

## Record differences

Compare every affected node, not only the node receiving a client request. Record explicit overrides separately from metadata defaults. Redact cookies, passwords, and private keys before sharing diagnostics.

After a change, repeat the inspection and the affected application operation. A matching file on disk is insufficient if the node has not loaded it.
