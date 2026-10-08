# Metadata

command: shell:riak admin force-remove
versions: 3.4.0, 3.4.1

# Summary

Remove a member using the legacy immediate command.

# Description

Prefer the staged cluster subcommands for planned topology changes.

# Arguments

## node

datatype: Erlang node name
required: true
repeatable: false

### Description

Full Erlang node name, for example `openriak-kv@node1.test`.

# Options

## -f

datatype: flag (no value)
required: false
repeatable: false

### Description

Acknowledge use of the legacy immediate membership operation. Review staged cluster commands before choosing this path.

# Results

## reference-result-1

### Description

On a valid request, the ring metadata is updated or the membership operation starts. Monitor ring-status and transfers; the acknowledgment is not completion of handoff.

# Reviewed against

3.4.0: dd73f2cc244820bdb233bf9d5c44ea162cb245dc83f1fe38c6a62a48706ddb20
3.4.1: 02b2de3c0bce4534bfa9abed0c1a63832a4f809c4b9b108e9df33afdbbfd08c3

# Tags

feature: node-operations
repository: riak_kv
module: riak_kv_console
concept: node-lifecycle
