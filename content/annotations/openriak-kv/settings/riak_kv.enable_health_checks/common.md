# Description

Registers KV's vnode-mailbox health check with Riak Core at startup. When enabled and Core health checks are active, excessive vnode backlogs can cause the KV service to be marked unavailable.

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

feature: object-storage
repository: riak_kv
module: riak_kv_app
concept: diagnostics, overload-protection

# Notes

This is the Erlang application environment key `enable_health_checks` in `riak_kv`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_kv/src/riak_kv_app.erl](https://github.com/OpenRiak/riak_kv/blob/48285d5d7aa72c4167e338b3d28ae9ba434cfcb7/src/riak_kv_app.erl#L243)

# Reviewed against

3.4.0: 2466506917b1d9043191d931370ae963bc2fe259ae669ba637ccacc229f23454
3.4.1: 28cb1099a98f2a19ff3f68331a57b9cc2f81626d9cdafee71be6870511fcca06
