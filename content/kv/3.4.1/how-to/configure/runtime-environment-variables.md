---
title: 'Set runtime environment variables'
description: 'Show operators how to set supported runtime environment variables and verify their effective values.'
weight: 12
diataxis: 'how-to'
product: 'OpenRiak KV'
product_version: '3.4.1'
status: 'editorially-rewritten'
draft: true
audience:
  - 'operators'
source_material:
  - 'openriak-quickdocs-3.4'
quickdocs_sources:
  - 'https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#setting-environment-variables-at-runtime'
tags: ['diataxis', 'kv', 'how-to']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Show operators how to set supported runtime environment variables and verify their effective values.

## Before you begin

Administrative access to the nodes you will change; a copy of the current configuration; and a maintenance window if the setting requires a restart.

## Overview

### Setting environment variables at runtime

All configuration in `riak.conf` is converted into erlang environment variables, and it is those variables that are used by the code.  The `riak.conf` is referred to only as the node is started - `riak.conf` changes will have no impact until the next restart.

To change the configuration of Riak at run-time, the variables can be changed via `remote_console` using the [application:set_env/3 function](https://www.erlang.org/doc/apps/kernel/application.html#set_env/3).

Note though, that:

- Some environment variables will be read by long-lived processes at startup, and so making runtime changes will have no effect.
- Configuration parameters will be translated into environment variables values by the cuttlefish schema - the configured value may not be a valid value for the environment variable e.g. `enabled`/`disabled` flags will commonly be translated into `true`/`false` boolean environment variables.  Changing an environment variable to the untranslated value may lead to node crashes.

In general, never change an environment variable at run-time via `remote_console` without first reading and understanding the code that uses it.

## Verify the result

Confirm that the intended setting is active on every affected node, then check cluster health and the relevant logs for warnings.
