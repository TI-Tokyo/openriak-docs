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

3.4.0: 90101a5d345274bacd39633bfd49bb407e87d2ac4a68af57661c64c3eb8ab409
3.4.1: 90101a5d345274bacd39633bfd49bb407e87d2ac4a68af57661c64c3eb8ab409
