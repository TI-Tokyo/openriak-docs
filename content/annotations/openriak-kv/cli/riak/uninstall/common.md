# Metadata

command: shell:riak uninstall
versions: 3.4.0, 3.4.1

# Summary

Remove an unused Erlang release.

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
riak uninstall TARGET_VERSION
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

3.4.0: 54fec6af2090544eef945ae32c9a0ff58c15b4bf492a69d462e4b0ff17003729
3.4.1: 5b15074e423092ddff85085715f3bf9f4eab074eceadfa76734f488ae0833ad5

# Tags

feature: node-operations
repository: riak
module: riak
concept: node-lifecycle
