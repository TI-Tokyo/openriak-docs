# Description

Registry mapping authentication source names to custom authentication modules. Riak security looks up the configured source here and invokes the module's `auth/4` callback for sources outside the built-in methods.

# Datatype

List

# Constraints

- List of `{SourceName, Module}` pairs, with atom names. Each module supplies the custom authentication `auth/4` callback.

# Inferred default

`[]` before authentication modules register themselves.

# Tags

feature: security
repository: riak_core
module: riak_core_security
concept: authentication

# Notes

This is the Erlang application environment key `auth_mods` in `riak_core`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_core/src/riak_core_security.erl](https://github.com/OpenRiak/riak_core/blob/2903cdc194fa4d538dd6f6da359e8465c11bb3c2/src/riak_core_security.erl#L456)

# Reviewed against

3.4.0: 0a4212313167f176572e2cef27f8d28c33bf5220dc837f4aa5e5c84316604833
3.4.1: 0a4212313167f176572e2cef27f8d28c33bf5220dc837f4aa5e5c84316604833
