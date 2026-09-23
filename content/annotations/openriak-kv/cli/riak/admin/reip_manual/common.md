# Metadata

command: shell:riak admin reip_manual
versions: 3.4.0, 3.4.1

# Summary

Rewrite a node name in persisted ring state.

# Description

The node must be stopped. Back up the ring files before using the manual rewrite and follow the node-renaming procedure. The automatic reip path explicitly reports that it is unsupported.

# Arguments

## old_nodename

datatype: Erlang node name
required: true
repeatable: false

### Description

Original full node name stored in the ring.

## new_nodename

datatype: Erlang node name
required: true
repeatable: false

### Description

Replacement full node name.

## ring_dir

datatype: absolute directory path
required: true
repeatable: false

### Description

Absolute path to the stopped node’s ring directory.

## cluster_name

datatype: cluster name
required: true
repeatable: false

### Description

Cluster-name component of the ring filename, for example default in riak_core_ring.default.TIMESTAMP.

# Results

## reference-result-1

### Description

The manual path rewrites stored ring information; the automatic reip path does not perform a supported rewrite.

# Reviewed against

3.4.0: 2420cbf516fb8f5f863ee8e08001225e2caa0e5243e11a9b6595de8a669fb0e2
3.4.1: 2420cbf516fb8f5f863ee8e08001225e2caa0e5243e11a9b6595de8a669fb0e2

# Tags

feature: node-operations
repository: riak
module: riak-admin
concept: node-lifecycle
