# Metadata

command: shell:riak admin security alter-group
versions: 3.4.0, 3.4.1

# Summary

Change a security group.

# Description

Updates the specified role options. Existing grants and source rules are managed with their own subcommands.

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

3.4.0: bf0a2d0582e1d5bf1e4ceab67d6afc7f95ec266ec84cff1eb0c37e8ec20472de
3.4.1: bf0a2d0582e1d5bf1e4ceab67d6afc7f95ec266ec84cff1eb0c37e8ec20472de

# Tags

feature: security
repository: riak_core
module: riak_core_console
concept: authentication
