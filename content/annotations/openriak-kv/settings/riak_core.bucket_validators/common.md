# Description

Registry of application modules that validate bucket properties. The bucket-property validation path uses these callbacks to check proposed settings before accepting them.

# Datatype

List

# Constraints

- List of `{Application, Module}` atom pairs identifying bucket validation implementations. Managed through `riak_core:register/2`.

# Inferred default

`[]` when unregistered; applications populate this registry at startup.

# Tags

feature: bucket-properties
repository: riak_core
module: riak_core
concept: data-policy

# Notes

This is the Erlang application environment key `bucket_validators` in `riak_core`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_core/src/riak_core.erl](https://github.com/OpenRiak/riak_core/blob/2903cdc194fa4d538dd6f6da359e8465c11bb3c2/src/riak_core.erl#L282)

# Reviewed against

3.4.0: eeb74b2424681377b80cbc69054bfa6fa440fdd163218cec8abae1ed5001f619
3.4.1: eeb74b2424681377b80cbc69054bfa6fa440fdd163218cec8abae1ed5001f619
