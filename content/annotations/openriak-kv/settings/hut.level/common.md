# Description

Minimum severity accepted by Hut's logging macros when `hut.use_log_level_gate` is enabled. Messages below this level are discarded before reaching the selected logging backend.

# Datatype

Enum

# Allowed values

- `debug`
- `info`
- `notice`
- `warning`
- `error`
- `critical`
- `alert`
- `emergency`

# Constraints

- Logging severity atom.

# Inferred default

`info`.

# Tags

feature: observability
repository: hut
module: hut.hrl
concept: diagnostics

# Notes

This is the Erlang application environment key `level` in `hut`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [hut/include/hut.hrl](https://github.com/OpenRiak/hut/blob/d1e1b4851f4efd1e7b45fdfe4b9a7d089c032442/include/hut.hrl#L19)

# Reviewed against

3.4.0: 96ab3e95cafc8aa282462e85832612144aee056051e7790957bafc47048b91f0
3.4.1: 96ab3e95cafc8aa282462e85832612144aee056051e7790957bafc47048b91f0
