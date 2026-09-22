# Metadata

command: shell:riak debug
versions: 3.4.0, 3.4.1

# Summary

Collect a diagnostic archive for a node.

# Description

Gather selected configuration, logs, patches and command output into a tar.gz file. The default selection includes configuration, logs, patches, Riak commands and system commands.

# Notes

Configuration archives may include credentials or other private configuration. Review the archive before sharing it. RIAK_EXCLUDE can exclude additional filename patterns; SSL key/certificate files are skipped by default unless --ssl-certs is requested.

# Arguments

## FILENAME

datatype: file path or -
required: false
repeatable: false

### Description

Output archive path. Use `-` for standard output. Omit to use NODE_NAME-riak-debug.tar.gz or HOSTNAME-riak-debug.tar.gz in the current directory.

# Options

## -name

omit: true


## --help

datatype: flag (no value)
required: false
repeatable: false

### Description

Print diagnostic-tool usage.

## --cfgs

datatype: flag (no value)
required: false
repeatable: false

### Description

Include files from the configured Riak configuration directory, subject to exclusions.

## --extracmds

datatype: flag (no value)
required: false
repeatable: false

### Description

Include additional, potentially expensive diagnostic commands. Run this selection on one node at a time.

## --logs

datatype: flag (no value)
required: false
repeatable: false

### Description

Include Riak logs.

## --patches

datatype: flag (no value)
required: false
repeatable: false

### Description

Include the patch directory.

## --riakcmds

datatype: flag (no value)
required: false
repeatable: false

### Description

Include Riak administrative command output.

## --ssl-certs

datatype: flag (no value)
required: false
repeatable: false

### Description

Include SSL certificate and key files that are normally excluded. Review the archive’s contents before sharing.

## --syscmds

datatype: flag (no value)
required: false
repeatable: false

### Description

Include operating-system diagnostic command output.

## --verbose

datatype: flag (no value)
required: false
repeatable: false

### Description

Print detailed failure diagnostics.

## --yzcmds

datatype: flag (no value)
required: false
repeatable: false

### Description

Request the unadvertised legacy search diagnostic selection. It may be unavailable when search is not installed.

## -c

datatype: flag (no value)
required: false
repeatable: false

### Description

Include files from the configured Riak configuration directory, subject to exclusions.

## -e

datatype: flag (no value)
required: false
repeatable: false

### Description

Include additional, potentially expensive diagnostic commands. Run this selection on one node at a time.

## -h

datatype: flag (no value)
required: false
repeatable: false

### Description

Print diagnostic-tool usage.

## -l

datatype: flag (no value)
required: false
repeatable: false

### Description

Include Riak logs.

## -p

datatype: flag (no value)
required: false
repeatable: false

### Description

Include the patch directory.

## -r

datatype: flag (no value)
required: false
repeatable: false

### Description

Include Riak administrative command output.

## -s

datatype: flag (no value)
required: false
repeatable: false

### Description

Include operating-system diagnostic command output.

## -v

datatype: flag (no value)
required: false
repeatable: false

### Description

Print detailed failure diagnostics.

## -y

datatype: flag (no value)
required: false
repeatable: false

### Description

Request the unadvertised legacy search diagnostic selection. It may be unavailable when search is not installed.

# Examples

## reference-example-1

title: Logs only

### Invocation

```sh
riak debug --logs /tmp/riak-logs.tar.gz
```

### Description

Collect logs into a named archive. Confirm there is enough disk space and review its contents before sharing.

### Expected output

A compressed diagnostic archive at the selected path, plus collection diagnostics.

# Errors

## reference-error-1

### Condition

An output path is not writable or a selected command/file is unavailable.

### Description

The collector reports a failure and the archive may omit affected items.

### Remedy

Choose a writable destination, use the node’s service account where appropriate, and inspect verbose diagnostics.

# Results

## reference-result-1

### Description

Produces the requested archive. Individual commands or files can fail collection; inspect diagnostics and archive contents rather than assuming every item was captured.

# Reviewed against

3.4.0: 2ad7ef17f3399662cfc73c94393a943e8ce5113eaa620707ba2b81fce8530570
3.4.1: 2ad7ef17f3399662cfc73c94393a943e8ce5113eaa620707ba2b81fce8530570
