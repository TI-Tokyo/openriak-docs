---
title: Runtime environment variables
weight: 120
product: OpenRiak KV
product_version: 3.4.0
diataxis: reference
draft: true
status: editorially-rewritten
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
description: Runtime environment variables are read by the launcher, packaging, or service manager. They are distinct
  from the schema-backed settings in `riak.conf`.
related:
- how-to/node-configuration/set-runtime-environment-variables
- reference/configuration/configuration-files-syntax-and-precedence
- reference/configuration/erlang-vm-and-runtime-settings
- reference/commands/riak
- foundations/data-and-consistency/bucket-types-and-data-policies
---

Runtime environment variables are read by the launcher, packaging, or service manager. They are distinct from the schema-backed settings in `riak.conf`.

## Scope and precedence

A variable exported in an interactive terminal is not automatically present in a service started by systemd, OpenRC, or a container entrypoint. The effective environment is the one passed to the running process by that deployment mechanism.

The release's launcher help is available through {{< cli key="shell:riak help" >}}. Use its advertised options and the installed service definition when selecting an alternate configuration path or execution mode. Do not assume a variable documented for another package controls this launcher.

## Configuration values

Use the settings catalogue for supported Erlang VM and application values. Environment substitution, service overrides, and direct VM arguments can bypass parts of that configuration path, so record them alongside the managed configuration.

## Verification

Inspect the service definition and the effective configuration on the intended host. Verify the node identity, listeners, and directories after startup; a variable being present in a shell is not evidence that OpenRiak used it.
