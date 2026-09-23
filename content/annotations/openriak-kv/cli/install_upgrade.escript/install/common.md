# Metadata

command: shell:install_upgrade.escript install
versions: 3.4.0, 3.4.1

# Summary

Install through the Erlang release handler.

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
riak install TARGET_VERSION
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

3.4.0: 19b4a78915853e0c8a466c2605d39232950682caccfcfce554d67f501a900c21
3.4.1: 19b4a78915853e0c8a466c2605d39232950682caccfcfce554d67f501a900c21

# Tags

feature: node-operations
repository: riak
module: install_upgrade.escript
concept: node-lifecycle
