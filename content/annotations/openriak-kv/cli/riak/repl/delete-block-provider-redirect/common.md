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

3.4.0: ca7a71223ad632298c0d5532546b49aba8ed269fc1a76f2156a5407c4250dcc4
3.4.1: ca7a71223ad632298c0d5532546b49aba8ed269fc1a76f2156a5407c4250dcc4

# Tags

feature: legacy-replication
repository: riak_repl
module: riak_repl_console
concept: cross-cluster-replication
