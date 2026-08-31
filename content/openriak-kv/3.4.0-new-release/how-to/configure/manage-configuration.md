---
title: 'Inspect and manage configuration'
description: 'Show operators how to inspect and manage configuration and verify the result.'
weight: 7
diataxis: 'how-to'
product: 'OpenRiak KV'
product_version: '3.4.0'
status: 'editorially-rewritten'
draft: true
audience:
  - 'operators'
migration_source_root: '\\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv'
migration_sources:
  - '\\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv\configure\guides\managing-configuration.md'
legacy_3_2_5_sources:
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\configuring\managing.md'
source_material:
  - 'legacy-3.2.5'
  - 'live-3.2.5'
  - 'proposed-kv'
  - 'openriak-quickdocs-3.4'
quickdocs_sources:
  - 'https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#accessing-configuration'
  - 'https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#extending-configuration'
tags: ['diataxis', 'kv', 'how-to']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Show operators how to inspect and manage configuration and verify the result.

## Before you begin

Administrative access to the nodes you will change; a copy of the current configuration; and a maintenance window if the setting requires a restart.

## Overview

### Managing Your Configuration

[use admin riak cli]: {{< product-version-root >}}reference/commands/riak/
[use admin riak cli#chkconfig]: {{< product-version-root >}}reference/commands/riak/#chkconfig

#### Retrieving a Configuration Listing

**Note:** This command has been deprecated in OpenRiak KV 3.2.5 onwards and will no longer function.

At any time, you can get a snapshot of currently applied configurations
through the command line. For a listing of *all* of the configs
currently applied in the node:

```bash
riak config effective
```

This will output a long list of the following form:

```
anti_entropy = active
anti_entropy.bloomfilter = on
anti_entropy.concurrency_limit = 2
#### and so on
```

For detailed information about a particular configuration variable, use
the `config describe <variable>` command. This command will output a
description of what the parameter configures, which datatype you should
use to set the parameter (integer, string, enum, etc.), the default
value of the parameter, the currently set value in the node, and the
name of the parameter in `app.config` in older versions of Riak (if
applicable).

For in-depth information about the `ring_size` variable, for example:

```bash
riak config describe ring_size
```

This will output the following:

```
Documentation for ring_size
Number of partitions in the cluster (only valid when first
creating the cluster). Must be a power of 2, minimum 8 and maximum
1024.

Datatype     : [integer]
   Default Value: 64
   Set Value    : undefined
   app.config   : riak_core.ring_creation_size
```

##### Checking Your Configuration

The [`riak`][use admin riak cli] command line tool has a
[`chkconfig`][use admin riak cli#chkconfig] command that enables you to
determine whether the syntax in your configuration files is correct.

```bash
riak chkconfig
```

If your configuration files are syntactically sound, you should see the
output `config is OK` followed by a listing of files that were checked.
You can safely ignore this listing. If, however, something is
syntactically awry, you'll see an error output that provides details
about what is wrong.

The error message will specify which configurable parameters are
syntactically unsound and attempt to provide an explanation why.

Please note that the `chkconfig` command only checks for syntax. It will
_not_ be able to discern if your configuration is otherwise unsound,
e.g. if your configuration will cause problems on your operating system
or doesn't activate subsystems that you would like to use.

##### Debugging Your Configuration

If there is a problem with your configuration but you're having trouble
identifying the problem, there is a command that you can use to debug
your configuration:

```bash
riak config generate -l debug
```

If there are issues with your configuration, you will see detailed
output that might provide a better sense of what has gone wrong in the
config generation process.

#### Accessing configuration

From the command line it is possible to view the current description of a configuration option using `riak admin describe <option_name>` e.g. `riak admin describe conditional_put_mode `.

Note that the result of `describe` request is the current schema documentation of an option; whereas if a `riak.conf` file has been kept in place between upgrades, that `riak.conf` file may not have the up to date description.  The command-line `describe` is a more reliable way of understanding the present advice for a configuration option.

[retrieve conf val]: {{< product-version-root >}}how-to/configure/manage-configuration/
[check config]: {{< product-version-root >}}how-to/configure/manage-configuration/

## Verify the result

Confirm that the intended setting is active on every affected node, then check cluster health and the relevant logs for warnings.
