# Metadata

command: shell:install_upgrade.escript downgrade
versions: 3.4.0, 3.4.1

# Summary

Downgrade through the Erlang release handler.

# Description

This is an internal launcher helper. Use the corresponding riak command so the distribution identity, cookie and release environment are supplied consistently.

# Arguments

## DistInfoStr

datatype: Erlang tuple string
required: true
repeatable: false

### Description

Serialized Erlang tuple `{ReleaseName, NameType, NodeName, Cookie}`. The launcher builds this from its configured distribution identity.

## Version

datatype: release identifier
required: true
repeatable: false

### Description

Prepared release-handler identifier. Omitted for versions.

# Options

## --no-permanent

datatype: flag (no value)
required: false
repeatable: false

### Description

For install or upgrade, leave the installed release non-permanent.

# Examples

## reference-example-1

title: Use the supported launcher

### Invocation

```sh
riak downgrade TARGET_VERSION
```

### Description

Use the launcher to supply the helper’s distribution tuple. Replace TARGET_VERSION with a prepared compatible release where shown.

### Expected output

Release-handler status or maintenance progress.

# Errors

## reference-error-1

### Condition

The distribution tuple cannot be parsed, the node is unreachable, or the requested release cannot be installed.

### Description

The helper reports a parsing, RPC or release-handler error and exits nonzero.

### Remedy

Use the riak launcher, verify the node identity and prepare a compatible release package.

# Results

## reference-result-1

### Description

The helper calls the running node’s release handler. Acknowledgment is not a substitute for checking riak versions and application health afterward.

# Reviewed against

3.4.0: 18556db11f7e1a8449400f8f6c742d84e91d3fca4f4d223b596ddc9d7f28bca3
3.4.1: 18556db11f7e1a8449400f8f6c742d84e91d3fca4f4d223b596ddc9d7f28bca3
