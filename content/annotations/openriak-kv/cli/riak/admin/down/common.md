# Metadata

command: shell:riak admin down
versions: 3.4.0, 3.4.1

# Summary

Mark a member as down for cluster coordination.

# Description

Marks a node down in the ring; it does not stop its operating-system process. This can change the claimant and clear staged changes.

# Arguments

## node

datatype: Erlang node name
required: true
repeatable: false

### Description

Full Erlang node name, for example `openriak-kv@node1.test`.

# Results

## reference-result-1

### Description

On a valid request, the ring metadata is updated or the membership operation starts. Monitor ring-status and transfers; the acknowledgment is not completion of handoff.

# Reviewed against

3.4.0: 4f2d677c37bd280b85fb6fcc62d31cfb605543ca4d2bfff0d2777def8cd47b21
3.4.1: 7b783e25bcffd8c71968f667df214b353954b0e4409f3cac6cb93705feaad57d

# Tags

feature: node-operations
repository: riak_kv
module: riak_kv_console
concept: node-lifecycle
