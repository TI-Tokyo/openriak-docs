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

3.4.0: 2b76c97236c7d368555aecf1d6d0a46b1274477827802f408c22201413cf61a4
3.4.1: 2b76c97236c7d368555aecf1d6d0a46b1274477827802f408c22201413cf61a4

# Tags

feature: security
repository: riak_core
module: riak_core_console
concept: authentication
