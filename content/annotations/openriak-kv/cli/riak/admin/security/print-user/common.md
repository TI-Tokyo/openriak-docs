# Metadata

command: shell:riak admin security print-user
versions: 3.4.0, 3.4.1

# Summary

Inspect a security user.

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

3.4.0: 0cc9e467b594fe276de8bc1368fa0dd90dff8e8701d8bde6786281bf07377367
3.4.1: f2c5b47a42bc125792778ab3dbb91577536a2845c561ecc72b7541ac3de12668

# Tags

feature: security
repository: riak_core
module: riak_core_console
concept: authentication
