# Metadata

command: shell:riak admin join
versions: 3.4.0, 3.4.1

# Summary

Join another node using the legacy immediate command.

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

3.4.0: eba992eaf55b16ca1a3ed8a58ea6819884005dc8091b2598e4ec2cf92a820cc1
3.4.1: eba992eaf55b16ca1a3ed8a58ea6819884005dc8091b2598e4ec2cf92a820cc1
