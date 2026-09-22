# Metadata

command: shell:riak console
versions: 3.4.0, 3.4.1

# Summary

Start the node in the foreground with an Erlang shell.

# Description

Uses the release boot script and embedded code loading. Start it only when another instance of the same node is not running.

# Arguments

# Examples

## reference-example-1

title: Service-account invocation

### Invocation

```sh
riak console
```

### Description

Run as the account that owns the node. For startup commands, first ensure the node is stopped; replace VERSION with the installed release directory where shown.

### Expected output

An Erlang prompt and application startup logs.

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

An Erlang prompt and application startup logs.

# Reviewed against

3.4.0: b36fac0f272a51536a984f1b16b29981c438f95b5bf64bcbf38a78737ceedd6d
3.4.1: b36fac0f272a51536a984f1b16b29981c438f95b5bf64bcbf38a78737ceedd6d
