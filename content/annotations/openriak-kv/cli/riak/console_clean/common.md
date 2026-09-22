# Metadata

command: shell:riak console_clean
versions: 3.4.0, 3.4.1

# Summary

Start a clean foreground Erlang shell with release paths.

# Description

Uses start_clean and interactive code loading for diagnostics. This is not the normal application boot.

# Arguments

# Examples

## reference-example-1

title: Service-account invocation

### Invocation

```sh
riak console_clean
```

### Description

Run as the account that owns the node. For startup commands, first ensure the node is stopped; replace VERSION with the installed release directory where shown.

### Expected output

A clean Erlang prompt; application startup differs from the normal release boot.

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

A clean Erlang prompt; application startup differs from the normal release boot.

# Reviewed against

3.4.0: a3a712ea28ddfe638d395600de579160c097d3e3c6c0f723522a9f37e5f13bd2
3.4.1: a3a712ea28ddfe638d395600de579160c097d3e3c6c0f723522a9f37e5f13bd2
