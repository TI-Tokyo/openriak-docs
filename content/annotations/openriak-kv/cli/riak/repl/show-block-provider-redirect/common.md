# Metadata

command: shell:riak repl show-block-provider-redirect
versions: 3.4.0, 3.4.1

# Summary

Inspect a block-provider cluster redirect.

# Description

These mappings support Riak CS block-provider recovery after a cluster replacement. They operate on generated cluster identifiers, not clustername labels.

# Arguments

## from-cluster

datatype: cluster identifier
required: true
repeatable: false

### Description

Generated cluster ID, as printed by show-local-cluster-id. Quote it as one shell argument. This is not the symbolic cluster name.

# Examples

## shell-riak-repl-show-block-provider-redirect:an-example-identifier

### Description

Use a block-provider mapping during recovery when the provider identifier must change. Replace the example identifiers with those reported by the affected cluster.

# Reviewed against

3.4.0: 6a2c7a7e0e9dc7221fdb924ecf9e76fd959292dd796c64143c18438c0edae1c0
3.4.1: 6a2c7a7e0e9dc7221fdb924ecf9e76fd959292dd796c64143c18438c0edae1c0
