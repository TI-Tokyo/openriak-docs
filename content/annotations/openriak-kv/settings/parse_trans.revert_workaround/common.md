# Description

Cached decision controlling a parse_trans workaround for reverting syntax trees containing implicit function references. If no boolean is configured, parse_trans probes the Erlang syntax tools and stores whether the workaround is needed.

# Datatype

Boolean

# Allowed values

- `true`
- `false`

# Constraints

- An explicit boolean overrides the probe; other values trigger automatic detection.

# Inferred default

Computed by probing the runtime syntax tools, then cached in the application environment.

# Tags

feature: erlang-runtime
repository: parse_trans
module: parse_trans
concept: compatibility

# Notes

This is the Erlang application environment key `revert_workaround` in `parse_trans`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [parse_trans/src/parse_trans.erl](https://github.com/OpenRiak/parse_trans/blob/160498e19878fd383fac25e72b8565dee3aeffa7/src/parse_trans.erl#L651)

# Reviewed against

3.4.0: e60dca12c8d51df81d70beb94a6f4fa6a60978271e7e3f751999d59268872243
3.4.1: e60dca12c8d51df81d70beb94a6f4fa6a60978271e7e3f751999d59268872243
