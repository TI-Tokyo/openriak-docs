# Metadata

command: shell:riak admin security del-user
versions: 3.4.0, 3.4.1

# Summary

Delete a security user.

# Description

Removes the named role from security configuration. Review grants and dependent role memberships before removing it.

# Arguments

## user

datatype: user name
required: true
repeatable: false

### Description

Security user name, for example `cli_reader`. Names are distinct from Erlang node names.

# Reviewed against

3.4.0: 6f964145cad8719b50ba2feb6d7e548905dd366ad273e06859caf2fa1a77cc0d
3.4.1: 6f964145cad8719b50ba2feb6d7e548905dd366ad273e06859caf2fa1a77cc0d

# Tags

feature: security
repository: riak_core
module: riak_core_console
concept: authentication
