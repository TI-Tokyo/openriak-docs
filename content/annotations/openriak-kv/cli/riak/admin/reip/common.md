# Metadata

command: shell:riak admin reip
versions: 3.4.0, 3.4.1

# Summary

Report that automatic reip is unsupported.

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

# Results

## reference-result-1

### Description

The manual path rewrites stored ring information; the automatic reip path does not perform a supported rewrite.

# Reviewed against

3.4.0: 1677fb46fbf80b5be605a103eddf9bb57643fb2948288ccca1345f3c9a190f2e
3.4.1: 1365b244ff321e43ca3a846f6c6f75769263d0e39fc321dfc24128c481dde586

# Tags

feature: node-operations
repository: riak
module: riak-admin
concept: node-lifecycle
