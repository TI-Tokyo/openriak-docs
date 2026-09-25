# Description

Internal copy of registered capability definitions, saved in the application environment so the capability server can reload them after a restart. Applications normally populate it through capability registration.

# Datatype

List

# Constraints

- Ordered dictionary of capability identifiers and internal capability records, maintained by `riak_core_capability`; populate through capability registration rather than constructing records manually.

# Inferred default

`[]` before capabilities are registered.

# Tags

feature: cluster-management
repository: riak_core
module: riak_core_capability
concept: compatibility, runtime

# Notes

This is the Erlang application environment key `registered_capabilities` in `riak_core`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_core/src/riak_core_capability.erl](https://github.com/OpenRiak/riak_core/blob/2903cdc194fa4d538dd6f6da359e8465c11bb3c2/src/riak_core_capability.erl#L629)

# Reviewed against

3.4.0: 5c55f914263bd893284f3a91c32aba9e61ec4adb4fdd1016cdd21d345c22ff52
3.4.1: 5c55f914263bd893284f3a91c32aba9e61ec4adb4fdd1016cdd21d345c22ff52
