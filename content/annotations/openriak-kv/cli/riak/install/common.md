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

3.4.0: ba644010ee82c7d72be53488a9feb6a4c8f50db250622dc7e03660cc241d0f3a
3.4.1: ba644010ee82c7d72be53488a9feb6a4c8f50db250622dc7e03660cc241d0f3a
