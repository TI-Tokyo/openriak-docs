# Metadata

command: shell:riak console_boot
versions: 3.4.0, 3.4.1

# Summary

Start a foreground shell using a selected boot script.

# Description

Supply the boot script explicitly. Its application list determines which services start.

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
riak console_boot /usr/lib/riak/releases/VERSION/start
```

### Description

Run as the account that owns the node. For startup commands, first ensure the node is stopped; replace VERSION with the installed release directory where shown.

### Expected output

Startup logs and an Erlang prompt when the boot script succeeds.

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

Startup logs and an Erlang prompt when the boot script succeeds.

# Reviewed against

3.4.0: b67732ffb293431256a2cd850d6bdd5bc648e548c0dddd1b6fbbedadd260ef46
3.4.1: b67732ffb293431256a2cd850d6bdd5bc648e548c0dddd1b6fbbedadd260ef46
