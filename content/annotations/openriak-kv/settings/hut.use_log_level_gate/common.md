# Description

Enables Hut's severity filter, which compares each log message with `hut.level`. When false, Hut passes messages to its logging backend without applying this gate.

# Datatype

Boolean

# Allowed values

- `true`
- `false`

# Constraints

- Use the Erlang atoms `true` or `false`.

# Inferred default

`true`.

# Tags

feature: observability
repository: hut
module: hut.hrl
concept: diagnostics

# Notes

This is the Erlang application environment key `use_log_level_gate` in `hut`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [hut/include/hut.hrl](https://github.com/OpenRiak/hut/blob/d1e1b4851f4efd1e7b45fdfe4b9a7d089c032442/include/hut.hrl#L16)

# Reviewed against

3.4.0: 12fbc609528b26983f22a9cf9aaba3dffc314238194fa35053a7114a880c8c0a
3.4.1: 12fbc609528b26983f22a9cf9aaba3dffc314238194fa35053a7114a880c8c0a
