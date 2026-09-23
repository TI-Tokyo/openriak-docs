# Metadata

command: shell:riak admin security add-group
versions: 3.4.0, 3.4.1

# Summary

Create a security group.

# Description

The new role can be used in grant and group-membership rules. Configure authentication sources separately.

# Arguments

## group

datatype: group name
required: true
repeatable: false

### Description

Security group name, for example `cli_readers`.

## option=value

datatype: key=value assignment
required: false
repeatable: true

### Description

One or more assignments. Use `groups=cli_readers` for membership and `password=...` for a user password. Quote values containing shell metacharacters.

# Reviewed against

3.4.0: cb281472d0be87c83655599f81ca98102d5a27a5c5ef164552e9936310075544
3.4.1: cb281472d0be87c83655599f81ca98102d5a27a5c5ef164552e9936310075544

# Tags

feature: security
repository: riak_core
module: riak_core_console
concept: authentication
