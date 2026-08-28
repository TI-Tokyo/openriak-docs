---
title: 'Configure logging'
description: 'Show operators how to configure logging and verify the result.'
weight: 6
diataxis: 'how-to'
product: 'OpenRiak KV'
product_version: '3.4.0'
status: 'editorially-rewritten'
draft: true
audience:
  - 'operators'
migration_source_root: '\\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv'
migration_sources:
  - '\\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv\configure\logging.md'
migration_review:
  - 'Legacy version text or MDX syntax remains and requires editorial review.'
source_material:
  - 'source-code-release-notes-3.4'
  - 'live-3.2.5'
  - 'proposed-kv'
  - 'openriak-quickdocs-3.4'
quickdocs_sources:
  - 'https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#logging'
tags: ['diataxis', 'kv', 'how-to']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Show operators how to configure logging and verify the result.

## Before you begin

Administrative access to the nodes you will change; a copy of the current configuration; and a maintenance window if the setting requires a restart.

## Overview

### Logging

All components of Riak use the kernel logger for logging.  The logger can be configured via `riak.conf`, and there are five parts of the configuration:

- Set the log level (`logger.level`);
- Set the file path and file name for each of the log files that are to be used (`logger.file`, `logger.error_file` etc).  The paths required are dependent on the configuration of `additional_handlers`.
- Set the log format (`logger.format`).
  - See the [erlang logger guide](https://www.erlang.org/doc/apps/kernel/logger.html) for metadata available to add to logs e.g. `mfa`, `pid`, `file`, `line`, `domain`, `msg`.
- **Available from OpenRiak KV 3.4.0.**Set the logs to be filtered from the default (console) log file (`logger.default_filters`).
  - This can be used to divert recurring or verbose logs to specific log files (if additional handlers are defined for these logs), or simply have them be ignored.
- **Available from OpenRiak KV 3.4.0.**Set the additional handlers to defined for logs (`logger.additional_handlers`);
  - Where logs are filtered from defaults, they can be diverted to alternative files using `additional_handlers`;
  - Adding json to `additional_handlers` will write all logs to separate json file in a json format.

For example, an alternative configuration in `riak.conf` could be used such as:

```console
logger.format = [time," [",level,"] pid=",pid," mfa=",mfa," ",msg,"\n"].
logger.background_file = $(platform_log_dir)/async.log
logger.default_filters = crash, error, progress, report, sasl, background, backend
logger.additional_handlers = crash, error, background, backend
```

It is possible to change logging at run time via [`remote_console`](/kv/3.4.0/how-to/operate/use-remote-console/) by following the [standard Erlang logger guide](https://www.erlang.org/doc/apps/kernel/logger_chapter#example-add-a-handler-to-log-info-events-to-file).

The `background` filter and handler is targeted at `tictacaae` logs, and recurring metric logs which are triggered by frequent ticks.  The `backend` filter and handler will presently only handle leveled logs.  The leveled log level can be set independently to the general log level in `riak.conf` using `leveled.log_level`: though it will not be possible to alter this log level at run-time as with the general log (e.g. the module log level cannot be reduced to a lower log level than the `leveled.log_loglevel` for leveled logs, the leveled filter is applied before the kernel logger filter).

> [!WARNING]
> Migration review required: Legacy version text or MDX syntax remains and requires editorial review.

## Verify the result

Confirm that the intended setting is active on every affected node, then check cluster health and the relevant logs for warnings.
