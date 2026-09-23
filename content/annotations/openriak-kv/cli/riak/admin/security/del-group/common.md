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

3.4.0: 7765e1b18ddbabab6173726a7ffe6b580e60934f6249028b579492918ff445f8
3.4.1: 7765e1b18ddbabab6173726a7ffe6b580e60934f6249028b579492918ff445f8

# Tags

feature: security
repository: riak_core
module: riak_core_console
concept: authentication
