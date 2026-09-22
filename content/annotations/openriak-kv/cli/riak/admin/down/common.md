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

3.4.0: 9cfe52e1e8ebbabebb97b269733a02c0560a161912480a6b745098908a01ba17
3.4.1: 9cfe52e1e8ebbabebb97b269733a02c0560a161912480a6b745098908a01ba17
