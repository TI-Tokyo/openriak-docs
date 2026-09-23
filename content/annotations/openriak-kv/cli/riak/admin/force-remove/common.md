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

3.4.0: e72a4a3c5580470f03b3b76d1164a841d8f0b903193dbb24a81db184f17986e4
3.4.1: e72a4a3c5580470f03b3b76d1164a841d8f0b903193dbb24a81db184f17986e4

# Tags

feature: node-operations
repository: riak_kv
module: riak_kv_console
concept: node-lifecycle
