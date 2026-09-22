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

3.4.0: 748829ba17be18f43b4e6023bbf8fdec13facd112a16b85c5856afb7efc1e060
3.4.1: 748829ba17be18f43b4e6023bbf8fdec13facd112a16b85c5856afb7efc1e060
