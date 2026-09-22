# Metadata

command: shell:riak admin cluster join
versions: 3.4.0, 3.4.1

# Summary

Stage this node to join an existing cluster.

# Description

This stages a topology change. Review `riak admin cluster plan`, then run `riak admin cluster commit` to apply the reviewed plan. Use member-status and transfers to monitor convergence.

# Arguments

## node

datatype: Erlang node name
required: true
repeatable: false

### Description

Full Erlang node name, for example `openriak-kv@node2.test`.

# Results

## outcome

### Description

A successful call stages a join; `cluster plan` shows the proposed membership change before commit. The example invokes the bundled release launcher and verifies the resulting membership.

# Reviewed against

3.4.0: 401ee3db5a9346f34aadc8145dda76b6e0a619695bb17e0aa467554c6f75e1a0
3.4.1: 401ee3db5a9346f34aadc8145dda76b6e0a619695bb17e0aa467554c6f75e1a0
