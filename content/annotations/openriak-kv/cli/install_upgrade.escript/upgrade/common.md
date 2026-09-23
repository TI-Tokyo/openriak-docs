# Metadata

command: shell:install_upgrade.escript upgrade
versions: 3.4.0, 3.4.1

# Summary

Upgrade through the Erlang release handler.

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
riak upgrade TARGET_VERSION
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

3.4.0: f847f55e41016342e9d533aad3d98478a6ebe72e2df67f5a1d3209b65c5e239f
3.4.1: f847f55e41016342e9d533aad3d98478a6ebe72e2df67f5a1d3209b65c5e239f

# Tags

feature: node-operations
repository: riak
module: install_upgrade.escript
concept: node-lifecycle
