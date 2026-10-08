# Metadata

command: shell:riak admin security alter-user
versions: 3.4.0, 3.4.1

# Summary

Change a security user.

# Description

Updates the specified role options. Existing grants and source rules are managed with their own subcommands.

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

3.4.0: dbd2a01ca2fbfba061a0255af2e20b3673f26b9b93f20c65702d76fbdf1e1013
3.4.1: dbd2a01ca2fbfba061a0255af2e20b3673f26b9b93f20c65702d76fbdf1e1013

# Tags

feature: security
repository: riak_core
module: riak_core_console
concept: authentication
