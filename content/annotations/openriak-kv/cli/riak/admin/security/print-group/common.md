# Metadata

command: shell:riak admin security print-group
versions: 3.4.0, 3.4.1

# Summary

Inspect a security group.

# Description

Displays the role’s configuration or grants. Review this together with authentication source rules when diagnosing access.

# Arguments

## group

datatype: group name
required: true
repeatable: false

### Description

Security group name, for example `cli_readers`.

# Reviewed against

3.4.0: b6d7c15c701841e95b95396fc87fafc75deac418ab518b94cb26fb308314e96c
3.4.1: b6d7c15c701841e95b95396fc87fafc75deac418ab518b94cb26fb308314e96c
