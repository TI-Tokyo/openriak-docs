# Metadata

command: shell:riak admin bucket-type status
versions: 3.4.0, 3.4.1

# Summary

Inspect a bucket type and its properties.

# Description

Read the activation state and properties. Use this after create, activate or update to check the result.

# Arguments

## type

datatype: bucket type name
required: true
repeatable: false

### Description

Bucket type name, for example `cli_reference_type`. Creation and activation are separate steps.

# Reviewed against

3.4.0: a9a341d9f256c440a9553dad6278bf4d61899e7d05a9a7bf6d25a8188b83feae
3.4.1: a9a341d9f256c440a9553dad6278bf4d61899e7d05a9a7bf6d25a8188b83feae

# Tags

feature: bucket-properties
repository: riak_kv
module: riak_kv_console
concept: data-policy
