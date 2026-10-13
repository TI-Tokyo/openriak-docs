# Metadata

command: shell:riak admin security print-grants
versions: 3.4.0, 3.4.1

# Summary

Inspect a user’s effective grants.

# Description

Displays the role’s configuration or grants. Review this together with authentication source rules when diagnosing access.

# Arguments

## user

datatype: user name
required: true
repeatable: false

### Description

Security user name, for example `cli_reader`. Names are distinct from Erlang node names.

# Reviewed against

3.4.0: 835e9929484f3959d10be094d6ccac47352791e82cc93f3c8f59ac36a0f4566b
3.4.1: 835e9929484f3959d10be094d6ccac47352791e82cc93f3c8f59ac36a0f4566b

# Tags

feature: security
repository: riak_core
module: riak_core_console
concept: authentication
