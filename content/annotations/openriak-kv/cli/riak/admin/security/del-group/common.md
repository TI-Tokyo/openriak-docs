# Metadata

command: shell:riak admin security del-group
versions: 3.4.0, 3.4.1

# Summary

Delete a security group.

# Description

Removes the named role from security configuration. Review grants and dependent role memberships before removing it.

# Arguments

## group

datatype: group name
required: true
repeatable: false

### Description

Security group name, for example `cli_readers`.

# Reviewed against

3.4.0: e2717af1bb213ca98947aac434edff2011a5e0223aaae1937568699d47ea270c
3.4.1: e2717af1bb213ca98947aac434edff2011a5e0223aaae1937568699d47ea270c

# Tags

feature: security
repository: riak_core
module: riak_core_console
concept: authentication
