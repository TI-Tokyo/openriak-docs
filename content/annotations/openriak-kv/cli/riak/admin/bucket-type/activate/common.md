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

3.4.0: ef9e8363dead9a86fef71a979ae6ef84bb7a8f284bae43bae0ca4afe8d54a59a
3.4.1: ef9e8363dead9a86fef71a979ae6ef84bb7a8f284bae43bae0ca4afe8d54a59a
