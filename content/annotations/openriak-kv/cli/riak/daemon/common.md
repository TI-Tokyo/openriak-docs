# Metadata

command: shell:riak daemon
versions: 3.4.0, 3.4.1

# Summary

Start the node as a background daemon.

# Description

Creates the release pipe and log directories, launches run_erl and waits for the node before running post-start hooks. Use the OS service manager when it owns the node.

# Arguments

# Examples

## reference-example-1

title: Service-account invocation

### Invocation

```sh
riak daemon
```

### Description

Run as the account that owns the node. For startup commands, first ensure the node is stopped; replace VERSION with the installed release directory where shown.

### Expected output

The command returns after startup and hooks; use ping to confirm reachability.

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

The command returns after startup and hooks; use ping to confirm reachability.

# Reviewed against

3.4.0: e450156f935950ed29e45d67b3dd58f37e46d5fdd9d2ceb1d758b7ca6613977d
3.4.1: e450156f935950ed29e45d67b3dd58f37e46d5fdd9d2ceb1d758b7ca6613977d
