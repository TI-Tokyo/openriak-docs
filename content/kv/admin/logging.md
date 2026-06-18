---
title: Logging
sidebar_label: "Logging"
date: 2026-06-17
---
import { ConfigReferenceProvider } from '@site/src/components/ConfigReference/ConfigReferenceContext';
import { ConfigListing }             from '@site/src/components/ConfigReference/ConfigListing';
import { ConfigDefaultValue }      from '@site/src/components/ConfigReference/ConfigDefaultValue';
import InlineCodeWithCopy          from '@site/src/components/InlineCodeWithCopy/InlineCodeWithCopy';

[root site]: [!site]
[root project]: [!project]
[root version]: [!version]
[directory]: #log-directory
[logfiles]: #log-files
[syntax]: #log-syntax
[rotation]: #log-file-rotation
[console]: #console-logs
[error]: #error-messages
[crash]: #crash-logs
[debug]: #enabling-and-disabling-debug-logging


>[!MEMO]Loggingg in OpenRiak
>Logging in Riak KV is handled by a Basho-made but OpenSource logging framework for Erlang called [lager](https://github.com/OpenRiak/lager) .
>lager provides a number of configuration options that you can use to fine-tune your OpenRiak cluster’s logging output. 

# Log Directory

OpenRiak stores it's log files in a `/log` directory on each node. This directory location varies depending on the platform. 
The table below shows you where log files are stored on all supported platforms:

    |------------------------------------------------------|-----------------------------------------------------|
    | OS                                                   | Directory                                           |
    |------------------------------------------------------|-----------------------------------------------------|
    | Ubuntu, Debian, Rocky, Alpine, RHEL/CentOS, Raspbian | /var/log/riak                                       |
    | Source install and macOS                             | ./log (where `.` is the root installation directory)|
    |------------------------------------------------------|-----------------------------------------------------|

# Log Files

OpenRiak stores a number of different log files in each nodes `/log` directory:

    |-----------------|------------------------------------------------------------------------|
    | File            | Significance                                                           |
    | ----------------|------------------------------------------------------------------------|
    | **console.log** | Console log output                                                     |
    | **crash.log**   | Crash logs capturing fatal errors and stack traces                     |
    | **erlang.log**  | Logs emitted directly by the Erlang VM on which OpenRiak runs          |
    | **error.log**   | Common errors emitted by OpenRiak                                      |
    | **run_erl.log** | Log file for the ``run_erl`` wrapper process; typically safe to ignore |
    |-----------------|------------------------------------------------------------------------|

# Log Syntax

The majority off OpenRiak logs are structured as follows:

```bash
<date> <time> [<level>] <PID> <prefix>: <message>
```

The `date` portion follows the `YYYY‑MM‑DD` format, and the `time` portion uses `hh:mm:ss.sss`. The `level` varies depending on which log level has been set in the `riak.conf` file (see below). The `PID` is the Erlang process that generated the event. The message `prefix` typically indicates the OpenRiak subsystem involved such as: `riak_ensemble_peer` or `alarm_handler`, among many others.

>[!NOTE]Log Messages may contain newline characters
>As of OpenRiak KV 3.2.5 a few of the log messages may contain newline characters, preventing reliable identification of the end of each log when attempting log files ingestion by external tools.
>A known workaround is ingesting not the logs enabled by the `log.console` configurable parameter but rather the logs as enabled by the `log.syslog` configurable parameter and processed by syslog,

Crash logs are an exception to the syntax rules above - They follow a similar format to below:

    ```bash
        <date> <time> =<report title>====
        <message>
    ```

This is an example of a crash report:

    ```bash
        2026-06-18 12:56:38 =ERROR REPORT====
        Error in process <0.4330.323> on node 'dev1@127.0.0.1' with exit value: ...
    ```

# Log File Rotation

OpenRiak maintains multiple separate files for `console.log`, `crash.log`, `erlang.log`, and `error.log`, which are rotated as each file reaches its maximum capacity of 100 KB. In each node’s /log directory, you may see, for example, files name `console.log`, `console.log.0`, `console.log.1`, and so on. OpenRiak’s log rotation is somewhat non traditional, as, by default, it logs to the oldest log file, rather than `*.1`.

For example:
If `erlang.log.1` is filled up, the logging system will begin writing to `erlang.log.2` continuing onto 3,4 and 5. When `erlang.log.5` is filled up, it loops back to writing to `erlang.log.1`.

# SASL 

[SASL](https://www.erlang.org/doc/apps/sasl/) (System Architecture Support Libraries) is Erlang’s built-in error logger. You can enable it and disable it using the sasl parameter (which can be set to `on` or `off`). It is disabled by default. The following would enable it:

    ```bash
        sasl = on
    ```

# Console Logs

OpenRiak console logs can be emitted to one of three places: to a log file (you can choose the name and location of that file), to standard output, or to neither. This is determined by the value that you give to the log.console parameter, which gives you one of four options:

    * `file` - Console logs will be emitted to a file. This is OpenRiak’s default behavior. The location of that file is determined by the `log.console.file` parameter. The default location is `./log/console.log` on an installation from source, but will differ on platform-specific installation, e.g. `/var/log/riak` on Ubuntu, Debian, CentOS, and RHEL.
    * `console` - Console logs will be emitted to standard output, which can be viewed by running the `riak attach-direct` command
    * `both` - Console logs will be emitted both to a file and to standard output
    * `off` - Console log messages will be disabled - This may be used when you have your own method for logging from OpenRiak

In addition to the the placement of console logs, you can also choose the severity of those messages using the log.console.level parameter. The following four options are available:

    * info (the default)
    * debug
    * warning
    * error

# Error Messages

OpenRiak will store error messages in `./log/error.log` by default. You can change this using the `log.error.file` parameter.

Here is an example, which uses the default:

    ```bash
        log.error.file = ./log/error.log
    ```

Error messages are redirected into lager By default, i.e. the `log.error.redirect` parameter is set to on. The following would disable the redirect:

    ```bash
        log.error.redirect = off
    ```

To throttle the nubmer of error messages that are handled per second (in cases where this is overloading) you can change the following (default setting is 100):

    ```bash
        log.error.messages_per_second = 100
    ```

# Crash Logs

OpenRiak stores crash logs in `./log/crash.log` by default. You can change this using the `log.crash.file` parameter. This example uses the default:

    ```bash
        log.crash.file = ./log/crash.log
    ```

While crash logs are kept by default, i.e. the `log.crash` parameter is set to on, you can disable crash logs like this:

    ```bash
        log.crash = off
    ```

## Crash Log Rotation

Crash logs get rotated just like the other OpenRiak logs. You can have them rotate when they hit a certain size, at specific times, or both.

The rotation schedule is controlled with `log.crash.rotation`. By default it’s set to `$D0`, which means the crash log rolls over every night at midnight. You can change this to rotate weekly, at a particular hour, or on certain days of the month. A few examples:

    * `$D0` — every night at midnight  
    * `$D23` — every day at 23:00 (11 pm)  
    * `$W0D20` — Sundays at 20:00 (8 pm)  
    * `$M1D0` — the first day of each month at midnight  
    * `$M5D6` — the fifth day of each month at 06:00  

If you want the log to rotate based on size, you can use `log.crash.size`. You can specify the size in `KB`, `MB`, etc. and the default is `10MB`.

Complete documentation of the syntax can be found on the github [here](https://github.com/openriak/lager/blob/master/README.md#internal-log-rotation)

# Syslogg Level and Facility Level

If syslog is enabled, i.e. if `log.syslog` is set to `on`, you can select the log level of syslog output from amongst the available levels, which are listed in the table below. The default is `info`.

    * alert
    * critical
    * debug
    * emergency
    * error
    * info
    * none
    * notice
    * warning

>[!NOTE]Note on using debug level logging
>Debug level logging is *not* recommended for long term running of a node as it adds significant load to the system and can result in performance issues over an extended period.

In addition to a log level, you must also select a facility level for syslog messages amongst the available levels, which are listed in the table below. The default is daemon.

    * auth
    * authpriv
    * clock
    * cron
    * daemon
    * ftp
    * kern
    * lpr
    * mail
    * news
    * syslog
    * user
    * uucp

In addition to these options, you may also choose one of `local0` through `local7`.

# Enabling and Disabling Debug Logging

If you’d like to enable debug logging on the current node, i.e. set the console log level to `debug`, you can do so without restarting the node by accessing the Erlang console directly using the `riak attach` command. Once you run this command and drop into the console, enter the following:

    ```bash
        lager:set_loglevel(lager_file_backend, "/var/log/riak/console.log", debug).
    ```

You should replace the file location above (/var/log/riak/console.log) with your platform-specific location, e.g. ./log/console.log for a source installation. This location is specified by the log.console.file parameter explained above.

If you’d like to enable debug logging on all nodes instead of just one node, you can enter the Erlang console of any running by running `riak attach` and enter the following:

    ```bash
        rp(rpc:multicall(lager, set_loglevel, [lager_file_backend, "/var/log/riak/console.log", debug])).
    ```
As before, use the appropriate log file location for your cluster.

At any time, you can set the log level back to info:

    ```bash
        rp(rpc:multicall(lager, set_loglevel, [lager_file_backend, "/var/log/riak/console.log", info])).
    ```



