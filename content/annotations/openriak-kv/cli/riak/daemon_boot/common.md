# Metadata

command: shell:riak daemon_boot
versions: 3.4.0, 3.4.1

# Summary

Start a background daemon using a selected boot script.

# Description

The selected boot script determines which applications start. Pipe and log directories must be writable by the service account.

# Arguments

## bootfile

datatype: filesystem path
required: true
repeatable: false

### Description

Boot-file path without the .boot suffix. Use a boot script installed with the selected release.

# Examples

## reference-example-1

title: Service-account invocation

### Invocation

```sh
riak daemon_boot /usr/lib/riak/releases/VERSION/start
```

### Description

Run as the account that owns the node. For startup commands, first ensure the node is stopped; replace VERSION with the installed release directory where shown.

### Expected output

A background VM using the selected boot file.

# Errors

## reference-error-1

### Condition

Another VM uses the configured node name, or required runtime paths are not writable.

### Description

Startup fails with a distribution, boot-file, configuration or filesystem error.

### Remedy

Check the existing process and run as the service account; correct the boot/configuration paths and inspect the node logs.

# Results

## reference-result-1

### Description

A background VM using the selected boot file.

# Reviewed against

3.4.0: 72e850e4ddba1e9218539feb1a41a41596d8e081f4468f5dee7f5ef006c48c90
3.4.1: 72e850e4ddba1e9218539feb1a41a41596d8e081f4468f5dee7f5ef006c48c90
