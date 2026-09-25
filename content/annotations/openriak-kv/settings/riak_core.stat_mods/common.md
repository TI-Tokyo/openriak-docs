# Description

Registry of application statistics modules maintained by Riak Core's registration API. It records the modules responsible for providing and registering each application's statistics.

# Datatype

List

# Constraints

- List of `{Application, Module}` atom pairs identifying statistics implementations. Managed through `riak_core:register/2`.

# Inferred default

`[]` when unregistered; applications populate this registry at startup.

# Tags

feature: observability
repository: riak_core
module: riak_core
concept: diagnostics

# Notes

This is the Erlang application environment key `stat_mods` in `riak_core`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_core/src/riak_core.erl](https://github.com/OpenRiak/riak_core/blob/2903cdc194fa4d538dd6f6da359e8465c11bb3c2/src/riak_core.erl#L288)

# Reviewed against

3.4.0: 79e9a73cf53eb880ed8877088ae8091a295d470d2462b6a74d2f6947eadc4c81
3.4.1: 79e9a73cf53eb880ed8877088ae8091a295d470d2462b6a74d2f6947eadc4c81
