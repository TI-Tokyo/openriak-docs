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

3.4.0: 5eae513295b330e54b400a983711c1ddfec6d59523c674b96256f1ec311e676a
3.4.1: 5eae513295b330e54b400a983711c1ddfec6d59523c674b96256f1ec311e676a
