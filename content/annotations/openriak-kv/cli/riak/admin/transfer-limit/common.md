# Metadata

command: shell:riak admin transfer-limit
versions: 3.4.0, 3.4.1

# Summary

Read or change the concurrent handoff limit.

# Description

Without arguments, list current limits. A limit alone updates the local node; a node and limit update that node. A higher limit can increase disk and network load.

# Arguments

## node

datatype: Erlang node name
required: false
repeatable: false

### Description

Node whose limit is to be changed. Omit to use the local node. Only supply a node when also supplying a limit.

## limit

datatype: non-negative integer
required: false
repeatable: false

### Description

Maximum simultaneous transfers. Omit all arguments to read limits. For example, `2` allows two concurrent transfers.

# Reviewed against

3.4.0: a1b68b73f0199986f3db92d88984550538d15eb6e0bc0336956c98a20d6288fc
3.4.1: a1b68b73f0199986f3db92d88984550538d15eb6e0bc0336956c98a20d6288fc
