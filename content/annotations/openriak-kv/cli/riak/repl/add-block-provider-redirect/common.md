# Metadata

command: shell:riak repl add-block-provider-redirect
versions: 3.4.0, 3.4.1

# Summary

Redirect block-provider requests to another cluster ID.

# Description

These mappings support Riak CS block-provider recovery after a cluster replacement. They operate on generated cluster identifiers, not clustername labels.

# Arguments

## from-cluster

datatype: cluster identifier
required: true
repeatable: false

### Description

Generated cluster ID, as printed by show-local-cluster-id. Quote it as one shell argument. This is not the symbolic cluster name.

## to-cluster

datatype: cluster identifier
required: true
repeatable: false

### Description

Replacement cluster’s generated ID. Quote it as one shell argument.

# Examples

## shell-riak-repl-add-block-provider-redirect:an-example-identifier

### Description

Use a block-provider mapping during recovery when the provider identifier must change. Replace the example identifiers with those reported by the affected cluster.

# Reviewed against

3.4.0: 85de8e8a40188974cc05f6a044a33321b9667ee1b8a9c222077fa22a2c1c862d
3.4.1: 85de8e8a40188974cc05f6a044a33321b9667ee1b8a9c222077fa22a2c1c862d

# Tags

feature: legacy-replication
repository: riak_repl
module: riak_repl_console
concept: cross-cluster-replication
