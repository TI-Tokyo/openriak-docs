---
title: 'Log files and message formats'
description: 'Define the names, fields, states, limits, and version applicability for log files and message formats.'
weight: 5
diataxis: 'reference'
product: 'OpenRiak KV'
product_version: '3.4.0'
status: 'editorially-rewritten'
draft: true
audience:
  - 'operators'
migration_source_root: '\\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv'
migration_sources:
  - '\\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv\admin\logging.md'
migration_review:
  - 'Commands or links derived from the 3.2.5 documentation were version-normalized for 3.4.0 and require technical verification.'
legacy_3_2_5_sources:
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\using\reference\logging.md'
source_material:
  - 'legacy-3.2.5'
  - 'live-3.2.5'
  - 'proposed-kv'
  - 'openriak-quickdocs-3.4'
quickdocs_sources:
  - 'https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#logging'
  - 'https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#logging-and-statistics'
tags: ['diataxis', 'kv', 'reference']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Define the names, fields, states, limits, and version applicability for log files and message formats.

## Details

### Logging Reference

[cluster ops log]: {{< product-version-root >}}how-to/operate/change-log-level/

Logging in OpenRiak KV is handled by a Basho-produced logging framework for
[Erlang](http://www.erlang.org) called
[lager](https://github.com/basho/lager).

lager provides a number of configuration options that you can use to fine-tune your OpenRiak cluster's logging output. A compact listing of parameters can be found in our [configuration files]({{< product-version-root >}}reference/configuration/#logging) documentation. A more thorough explanation of these options can be found in this document.

#### Log Directory

OpenRiak's log files are stored in a `/log` directory on each node. The
location of that directory differs from platform to platform. The table
below shows you where log files are stored on all supported operating
systems.

OS | Directory
:--|:---------
Ubuntu, Debian, CentOS, RHEL | `/var/log/riak`
Solaris, OpenSolaris | `/opt/riak/log`
Source install and Mac OS X | `./log` (where the `.` represents the root installation directory)

#### Log Files

Below is a list of files that can be found in each node's `/log`
directory:

File | Significance
:----|:------------
`console.log` | Console log output
`crash.log` | Crash logs
`erlang.log` | Logs emitted by the [Erlang VM]({{< product-version-root >}}reference/) on which Riak runs.
`error.log` | [Common errors]({{< product-version-root >}}reference/) emitted by Riak.
`run_erl.log` | The log file for an Erlang process called `run_erl`. This file can typically be ignored.

#### Log Syntax

Riak logs tend to be structured like this:

```log
<date> <time> [<level>] <PID> <prefix>: <message>
```

The `date` segment is structured `YYYY-MM-DD`, `time` is structured
`hh:mm:ss.sss`, `level` depends on which log levels are available in the
file you are looking at (consult the sections below), the `PID` is the
Erlang process identifier for the process in which the event occurred,
and the message `prefix` will often identify the Riak subsystem
involved, e.g. `riak_ensemble_peer` or `alarm_handler` (amongst many
other possibilities).

**Warning: Log messages may contain newline characters**
As of OpenRiak KV 3.2.5 a few of the log messages may contain newline
characters, preventing reliable identification of the end of each log
when attempting log files ingestion by external tools.

A known workaround is ingesting not the logs enabled by the
`log.console` configurable parameter but rather the logs as enabled by
the `log.syslog` configurable parameter and processed by syslog,
e.g. exploiting the
[`no-multi-line`](https://www.balabit.com/documents/syslog-ng-ose-3.5-guides/en/syslog-ng-ose-guide-admin/html-single/index.html)
option (e.g. see [this StackExchange topic
answer](https://unix.stackexchange.com/questions/317422/is-there-a-way-to-rewrite-parts-of-a-message-globally-instead-of-inserting-rewri/317474#317474))
- or equivalent - of syslog implementations.

The exception to this syntax is in crash logs (stored in `crash.log`
files). For crash logs, the syntax tends to be along the following
lines:

```log
<date> <time> =<report title>====
<message>
```

Here is an example crash report:

```log
2014-10-17 15:56:38 =ERROR REPORT====
Error in process <0.4330.323> on node 'dev1@127.0.0.1' with exit value: ...
```

#### Log Files

In each node's `/log` directory, you will see at least one of each of
the following:

File | Contents
:----|:--------
`console.log` | General messages from all Riak subsystems
`crash.log` | Catastrophic events, such as node failures, running out of disk space, etc.
`erlang.log` | Events from the Erlang VM on which Riak runs
`run_erl.log` | The command-line arguments used when starting Riak

##### Log File Rotation

Riak maintains multiple separate files for `console.log`, `crash.log`,
`erlang.log`, and `error.log`, which are rotated as each file reaches
its maximum capacity of 100 KB. In each node's `/log` directory, you may
see, for example, files name `console.log`, `console.log.0`,
`console.log.1`, and so on. OpenRiak's log rotation is somewhat non
traditional, as it does not always log to `*.1` (e.g. `erlang.log.1`)
but rather to the oldest log file.

After, say, `erlang.log.1` is filled up, the logging system will begin
writing to `erlang.log.2`, then `erlang.log.3`, and so on. When
`erlang.log.5` is filled up, it will loop back to `erlang.log.1`.

#### SASL

[SASL](http://www.erlang.org/doc/man/sasl_app.html) (System Architecture
Support Libraries) is Erlang's built-in error logger. You can enable it
and disable it using the `sasl` parameter (which can be set to `on` or
`off`). It is disabled by default. The following would enable it:

```riakconf
sasl = on
```

#### Error Messages

By default, Riak stores error messages in `./log/error.log` by default.
You can change this using the `log.error.file` parameter. Here is an
example, which uses the default:

```riakconf
log.error.file = ./log/error.log
```

By default, error messages are redirected into lager, i.e. the
`log.error.redirect` parameter is set to `on`. The following would
disable the redirect:

```riakconf
log.error.redirect = off
```

You can also throttle the number of error messages that are handled per
second. The default is 100.

```riakconf
log.error.messages_per_second = 100
```

#### Crash Logs

Riak crash logs are stored in `./log/crash.log` by default. You can
change this using the `log.crash.file` parameter. This example uses the
default:

```riakconf
log.crash.file = ./log/crash.log
```

While crash logs are kept by default, i.e. the `log.crash` parameter is
set to `on`, you can disable crash logs like this:

```riakconf
log.crash = off
```

##### Crash Log Rotation

Like other Riak logs, crash logs are rotated. You can set the crash logs
to be rotated either when a certain size threshold is reached and/or at
designated times.

You can set the rotation time using the `log.crash.rotation` parameter.
The default is `$D0`, which rotates the logs every day at midnight. You
can also set the rotation to occur weekly, on specific days of the
month, etc. Complete documentation of the syntax can be found
[here](https://github.com/basho/lager/blob/master/README.md#internal-log-rotation).
Below are some examples:

* `$D0` - Every night at midnight
* `$D23` - Every day at 23:00 (11 pm)
* `$W0D20` - Every week on Sunday at 20:00 (8 pm)
* `$M1D0` - On the first day of every month at midnight
* `$M5D6` - On the fifth day of the month at 6:00 (6 am)

To set the maximum size of the crash log before it is rotated, use the
`log.crash.size` parameter. You can specify the size in KB, MB, etc. The
default is `10MB`.

##### Other Crash Log Settings

The maximum size of individual crash log messages can be set using the
`log.crash.maximum_message_size`, using any size denomination you wish,
e.g. `KB` or `MB`  The default is 64 KB. The following would set that
maximum message size to 1 MB:

```riakconf
log.crash.maximum_message_size = 1MB
```

#### Syslog

Riak log output does not go to syslog by default, i.e. the `log.syslog`
setting is set to `off` by default. To enable syslog output:

```riakconf
log.syslog = on
```

If syslog output is enabled, you can choose a prefix to be appended to
each syslog message. The prefix is `riak` by default.

```riakconf
log.syslog.ident = riak
```

##### Syslog Level and Facility Level

If syslog is enabled, i.e. if `log.syslog` is set to `on`, you can
select the log level of syslog output from amongst the available levels,
which are listed in the table below. The default is `info`.

* `alert`
* `critical`
* `debug`
* `emergency`
* `error`
* `info`
* `none`
* `notice`
* `warning`

In addition to a log level, you must also select a [facility
level](https://en.wikipedia.org/wiki/Syslog#Facility) for syslog
messages amongst the available levels, which are listed in the table
below. The default is `daemon`.

* `auth`
* `authpriv`
* `clock`
* `cron`
* `daemon`
* `ftp`
* `kern`
* `lpr`
* `mail`
* `news`
* `syslog`
* `user`
* `uucp`

In addition to these options, you may also choose one of `local0`
through `local7`.

#### Console Logs

Riak console logs can be emitted to one of three places: to a log file
(you can choose the name and location of that file), to standard output,
or to neither. This is determined by the value that you give to the
`log.console` parameter, which gives you one of four options:

* `file` - Console logs will be emitted to a file. This is OpenRiak's
    default behavior. The location of that file is determined by the
    `log.console.file` parameter. The default location is
    `./log/console.log` on an installation from [source]({{< product-version-root >}}how-to/install/source/), but will differ on platform-specific installation,
    e.g.  `/var/log/riak` on Ubuntu, Debian, CentOS, and RHEL or
    `/opt/riak/log` on Solaris-based platforms.
* `console` - Console logs will be emitted to standard output, which
    can be viewed by running the [`riak attach-direct`]({{< product-version-root >}}reference/commands/riak/#attach-direct) command
* `both` - Console logs will be emitted both to a file and to standard
    output
* `off` - Console log messages will be disabled

In addition to the the placement of console logs, you can also choose
the severity of those messages using the `log.console.level` parameter.
The following four options are available:

* `info` (the default)
* `debug`
* `warning`
* `error`

#### Enabling and Disabling Debug Logging

Checkout [Cluster Operations: Enabling and Disabling Debug Logging][cluster ops log]

#### Logging

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

It is possible to change logging at run time via [`remote_console`]({{< product-version-root >}}how-to/operate/use-remote-console/) by following the [standard Erlang logger guide](https://www.erlang.org/doc/apps/kernel/logger_chapter#example-add-a-handler-to-log-info-events-to-file).

The `background` filter and handler is targeted at `tictacaae` logs, and recurring metric logs which are triggered by frequent ticks.  The `backend` filter and handler will presently only handle leveled logs.  The leveled log level can be set independently to the general log level in `riak.conf` using `leveled.log_level`: though it will not be possible to alter this log level at run-time as with the general log (e.g. the module log level cannot be reduced to a lower log level than the `leveled.log_loglevel` for leveled logs, the leveled filter is applied before the kernel logger filter).

> [!WARNING]
> Migration review required: Commands or links derived from the 3.2.5 documentation were version-normalized for 3.4.0 and require technical verification.
