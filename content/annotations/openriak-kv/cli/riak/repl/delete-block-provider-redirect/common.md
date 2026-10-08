# Metadata

command: shell:riak repl delete-block-provider-redirect
versions: 3.4.0, 3.4.1

# Summary

Remove a block-provider cluster redirect.

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

## shell-riak-repl-delete-block-provider-redirect:an-example-identifier

### Description

Use a block-provider mapping during recovery when the provider identifier must change. Replace the example identifiers with those reported by the affected cluster.

# Reviewed against

3.4.0: 591e808b086cdf49b21fdd2eabd4b9e6d2df29ec6a85ebd6451f36f0bdfee231
3.4.1: 591e808b086cdf49b21fdd2eabd4b9e6d2df29ec6a85ebd6451f36f0bdfee231

# Tags

feature: legacy-replication
repository: riak_repl
module: riak_repl_console
concept: cross-cluster-replication
