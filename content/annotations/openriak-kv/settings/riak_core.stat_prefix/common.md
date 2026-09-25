# Description

Leading component of Riak's Exometer metric names. Statistics registration, updates and lookups use this namespace prefix, which defaults in the source to `riak`.

# Datatype

Atom

# Constraints

- An Erlang atom used as the prefix of metric names.

# Inferred default

`riak`.

# Tags

feature: observability
repository: riak_core
module: riak_core_stat
concept: diagnostics

# Notes

This is the Erlang application environment key `stat_prefix` in `riak_core`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_core/src/riak_core_stat.erl](https://github.com/OpenRiak/riak_core/blob/2903cdc194fa4d538dd6f6da359e8465c11bb3c2/src/riak_core_stat.erl#L140)

# Reviewed against

3.4.0: e7b30c3a6525a359699744dda714f344e355fadc2ac35409162ec909f5b276c5
3.4.1: 062e5a7b46d354948e85ccd5b5760eb63dc27c26c29d774a3937a981d5c108b7
