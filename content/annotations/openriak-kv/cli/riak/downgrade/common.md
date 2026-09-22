# Metadata

command: shell:riak downgrade
versions: 3.4.0, 3.4.1

# Summary

Downgrade to a prepared Erlang release.

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
riak downgrade TARGET_VERSION
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

3.4.0: c8b88bbf98926adf8cf097c12519809e2d6db5e4023cd446c0cdc29bd36b6f83
3.4.1: c8b88bbf98926adf8cf097c12519809e2d6db5e4023cd446c0cdc29bd36b6f83
