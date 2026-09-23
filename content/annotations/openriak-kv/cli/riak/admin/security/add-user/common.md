# Metadata

command: shell:riak admin security add-user
versions: 3.4.0, 3.4.1

# Summary

Create a security user.

# Description

The new role can be used in grant and group-membership rules. Configure authentication sources separately.

# Arguments

## user

datatype: user name
required: true
repeatable: false

### Description

Security user name, for example `cli_reader`. Names are distinct from Erlang node names.

## option=value

datatype: key=value assignment
required: false
repeatable: true

### Description

One or more assignments. Use `groups=cli_readers` for membership and `password=...` for a user password. Quote values containing shell metacharacters.

# Reviewed against

3.4.0: bbb7dc9f79e28f223b677758acb96d4b891c67414e8119f6d883f170ae628dbf
3.4.1: bbb7dc9f79e28f223b677758acb96d4b891c67414e8119f6d883f170ae628dbf

# Tags

feature: security
repository: riak_core
module: riak_core_console
concept: authentication
