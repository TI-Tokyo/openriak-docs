# Metadata

command: shell:riak admin leave
versions: 3.4.0, 3.4.1

# Summary

Leave the cluster using the legacy immediate command.

# Description

Prefer the staged cluster subcommands for planned topology changes.

# Arguments

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

3.4.0: 9d427546b78439714c6c172e02da939caca7a1975a51827f241050251eb04d36
3.4.1: f95f76c1b66f77940dc77f776ae7cbbde0332fba2b95c1122d5f62f9458de29c

# Tags

feature: node-operations
repository: riak_kv
module: riak_kv_console
concept: node-lifecycle
