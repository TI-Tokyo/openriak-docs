# Metadata

command: shell:riak admin bucket-type activate
versions: 3.4.0, 3.4.1

# Summary

Activate an existing bucket type.

# Description

Activation makes a previously created type available for bucket operations. Check its properties before activating; some type properties cannot be changed afterward.

# Arguments

## type

datatype: bucket type name
required: true
repeatable: false

### Description

Bucket type name, for example `cli_reference_type`. Creation and activation are separate steps.

# Reviewed against

3.4.0: 6b28abd866da336c8d0529a6c7c63cc54be3a9f0c10a806c353aaba697a39d2e
3.4.1: 6b28abd866da336c8d0529a6c7c63cc54be3a9f0c10a806c353aaba697a39d2e

# Tags

feature: bucket-properties
repository: riak_kv
module: riak_kv_console
concept: data-policy
