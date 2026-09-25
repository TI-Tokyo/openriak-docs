# Description

Registry of permission names supported by each application. The security subsystem checks requested grants and revocations against this registry and rejects unknown permissions; the registry itself does not grant access to users.

# Datatype

List

# Constraints

- List of `{Application, PermissionAtoms}` pairs; each permission list contains atoms. External permission names use `application.permission`.

# Inferred default

`[]` before applications register their permission namespaces.

# Tags

feature: security
repository: riak_core
module: riak_core_security
concept: authentication

# Notes

This is the Erlang application environment key `permissions` in `riak_core`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_core/src/riak_core_security.erl](https://github.com/OpenRiak/riak_core/blob/2903cdc194fa4d538dd6f6da359e8465c11bb3c2/src/riak_core_security.erl#L1050)

# Reviewed against

3.4.0: 072576c536397d8731a04147b6c9424448a9983bcd01e880a95f8b576c44cbca
3.4.1: 072576c536397d8731a04147b6c9424448a9983bcd01e880a95f8b576c44cbca
