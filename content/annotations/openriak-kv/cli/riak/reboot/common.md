# Metadata

command: shell:riak reboot
versions: 3.4.0, 3.4.1

# Summary

Reboot the Erlang VM through the release launcher.

# Description

Invokes init:reboot/0. Return to service depends on the configured heart or external supervision behaviour.

# Arguments

# Examples

## reference-example-1

title: Service-account invocation

### Invocation

```sh
riak reboot
```

### Description

Run as the account that owns the node. For startup commands, first ensure the node is stopped; replace VERSION with the installed release directory where shown.

### Expected output

The old VM exits and the configured restart mechanism is expected to launch its replacement.

# Results

## reference-result-1

### Description

The old VM exits and the configured restart mechanism is expected to launch its replacement.

# Reviewed against

3.4.0: 6c8c816b65a32e2aaa7abff96a34a94fa7f96a69aead0b2c474520aa6c6a760e
3.4.1: 6c8c816b65a32e2aaa7abff96a34a94fa7f96a69aead0b2c474520aa6c6a760e

# Tags

feature: node-operations
repository: riak
module: riak
concept: node-lifecycle
