---
title: 'Extend configuration with advanced.config'
description: 'Show operators how to add advanced configuration without obscuring settings managed in riak.conf.'
weight: 11
diataxis: 'how-to'
product: 'OpenRiak KV'
product_version: '3.4.0'
status: 'editorially-rewritten'
draft: true
audience:
  - 'operators'
source_material:
  - 'openriak-quickdocs-3.4'
quickdocs_sources:
  - 'https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#extending-configuration'
  - 'https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#using-advancedconfig'
tags: ['diataxis', 'kv', 'how-to']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Show operators how to add advanced configuration without obscuring settings managed in riak.conf.

## Before you begin

Administrative access to the nodes you will change; a copy of the current configuration; and a maintenance window if the setting requires a restart.

## Overview

### Using advanced.config

The advanced.config file is found within the `platform_etc_dir` (a location configured within `riak.conf`), which is normally the system `/etc/riak` folder, after a package-based build of Riak.  The file bypasses the Riak-specific configuration mechanism, and uses the native Erlang method for passing configuration into an Erlang application.  The file may be used for advanced configuration purposes, to supply environment variables to Riak which are not currently covered by the riak.conf schema files.

The variables need to represented as an Erlang object, which is a list of mappings between an application and a list of key/value pairs, as [described in the Erlang documentation](https://www.erlang.org/doc/apps/kernel/config.html).

e.g.

```erlang
[
    {
        riak_kv,
        [
            {delete_mode, keep},
            {add_paths, "other/"}
        ]
    }
].
```

Any configuration added in advanced.config will override any configuration set in the riak.conf file.

## Verify the result

Confirm that the intended setting is active on every affected node, then check cluster health and the relevant logs for warnings.
