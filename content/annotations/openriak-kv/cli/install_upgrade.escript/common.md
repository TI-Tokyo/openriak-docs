# Metadata

command: shell:install_upgrade.escript
versions: 3.4.0, 3.4.1

# Summary

Run release-handler maintenance.

# Description

This is an internal launcher helper. Use the corresponding riak command so the distribution identity, cookie and release environment are supplied consistently.

# Arguments

## Command

datatype: operation
required: true
repeatable: false

### Valid values

- install
- upgrade
- downgrade
- unpack
- uninstall
- versions

### Description

Release operation selected by the launcher.

## DistInfoStr

datatype: Erlang tuple string
required: true
repeatable: false

### Description

Serialized Erlang tuple `{ReleaseName, NameType, NodeName, Cookie}`. The launcher builds this from its configured distribution identity.

## Version

datatype: release identifier
required: false
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
riak versions
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

3.4.0: 733e9b475fba367fed5eecd17796b7f172955481a6d8f454da2a2c76e0e73bf0
3.4.1: 733e9b475fba367fed5eecd17796b7f172955481a6d8f454da2a2c76e0e73bf0
