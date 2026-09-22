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

3.4.0: 9fa4347127b2650c7a7126a079627db24fdb75abf2c024eb50bf39d24d68f6e3
3.4.1: 9fa4347127b2650c7a7126a079627db24fdb75abf2c024eb50bf39d24d68f6e3
