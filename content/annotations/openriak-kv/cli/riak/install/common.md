# Metadata

command: shell:riak install
versions: 3.4.0, 3.4.1

# Summary

Install a release through the Erlang release handler.

# Description

This operates on Erlang release-handler packages and release identifiers. It is separate from installing or upgrading an OS package. The target archive and upgrade instructions must be compatible with the running release.

# Arguments

## version

datatype: release identifier
required: true
repeatable: false

### Description

Release-handler identifier as reported by versions, or the identifier of the prepared release archive. It is not necessarily the OS package version.

# Options

## --no-permanent

datatype: flag (no value)
required: false
repeatable: false

### Description

Do not mark the installed release permanent. A later restart can return to the previous permanent release.

# Examples

## reference-example-1

title: A prepared release

### Invocation

```sh
riak install TARGET_VERSION
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

3.4.0: 9b4797e1be538975f4c5589eedbb98522bf08424dbe862a551e21c20c7dc09f5
3.4.1: be0d82b36ecdf7c6c9240aa149a2f3d1711166e25af608f2a8dfdc4288dfe108

# Tags

feature: node-operations
repository: riak
module: riak
concept: node-lifecycle
