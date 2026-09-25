# Description

Registry associating applications with health-check `{Module, Function, Arguments}` callbacks. Applications normally populate it through Riak Core registration, and the node watcher uses the registered callback when monitoring a service.

# Datatype

List

# Constraints

- List of `{Application, {Module, Function, Arguments}}` entries. Application, module and function are atoms; arguments is a list.

# Inferred default

Unset; lookup returns `undefined` until an application registers a health check.

# Tags

feature: cluster-management
repository: riak_core
module: riak_core
concept: diagnostics

# Notes

This is the Erlang application environment key `health_checks` in `riak_core`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_core/src/riak_core.erl](https://github.com/OpenRiak/riak_core/blob/2903cdc194fa4d538dd6f6da359e8465c11bb3c2/src/riak_core.erl#L294)

# Reviewed against

3.4.0: ee832b604e60e00ac5a5c675a7a8c170866e22ca3a4954eabec5b8c7b8798736
3.4.1: ee832b604e60e00ac5a5c675a7a8c170866e22ca3a4954eabec5b8c7b8798736
