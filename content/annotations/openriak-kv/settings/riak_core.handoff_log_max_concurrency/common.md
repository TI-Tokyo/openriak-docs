# Description

Enables informational logging when a handoff terminates because the maximum handoff concurrency was reached. These expected capacity rejections are otherwise omitted from the log.

# Datatype

Boolean

# Allowed values

- `true`
- `false`

# Constraints

- Use the Erlang atoms `true` or `false`.

# Inferred default

`false`.

# Tags

feature: handoff
repository: riak_core
module: riak_core_handoff_manager
concept: diagnostics, partition-transfer

# Notes

This is the Erlang application environment key `handoff_log_max_concurrency` in `riak_core`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_core/src/riak_core_handoff_manager.erl](https://github.com/OpenRiak/riak_core/blob/2903cdc194fa4d538dd6f6da359e8465c11bb3c2/src/riak_core_handoff_manager.erl#L306)

# Reviewed against

3.4.0: d9361db7eaf613301e820501695190419f440cd5250e16dbe8c673640832c3b5
3.4.1: 5b76dc8d7e2e6bd92b3467e81016f84494a50d2bbcbdd573773bf4cba2f282a7
