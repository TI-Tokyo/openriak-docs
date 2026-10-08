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

3.4.0: d7ad7cf75f55fbc4cde1a979e165acbf9c78d24220196624cd2c6907ba85584e
3.4.1: a3ecbdcfe86b8d8f23f53b7d35d7295b74100ce78c85836179421ba1752ecc89

# Tags

feature: node-operations
repository: riak
module: riak-admin
concept: node-lifecycle
