# Metadata

command: shell:riak unpack
versions: 3.4.0, 3.4.1

# Summary

Unpack an Erlang release archive.

# Description

This operates on Erlang release-handler packages and release identifiers. It is separate from installing or upgrading an OS package. The target archive and upgrade instructions must be compatible with the running release.

# Arguments

## version

datatype: release identifier
required: true
repeatable: false

### Description

Release-handler identifier as reported by versions, or the identifier of the prepared release archive. It is not necessarily the OS package version.

# Examples

## reference-example-1

title: A prepared release

### Invocation

```sh
riak unpack TARGET_VERSION
```

### Description

Replace TARGET_VERSION with a compatible, prepared release-handler identifier. Follow the upgrade procedure before invoking it.

### Expected output

Release-handler progress or a diagnostic explaining why the release cannot be installed or removed.

# Results

## reference-result-1

### Description

Success changes release-handler state. Confirm the resulting state with riak versions and verify node health.

# Reviewed against

3.4.0: 098de3abd3adffbb79af564b7d9bb46bb665055b8b68c5b31e93a93ff8f85612
3.4.1: 1f2967149e1b5834ee0e23aca10827133a6eea67156e34af24a90b945c6f5ac2

# Tags

feature: node-operations
repository: riak
module: riak
concept: node-lifecycle
