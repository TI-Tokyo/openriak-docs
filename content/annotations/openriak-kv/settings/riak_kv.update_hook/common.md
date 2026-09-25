# Description

Optional module implementing the vnode update-hook behaviour. The vnode calls it when objects change, passing the object information, update reason and partition so integrations such as search indexing can follow writes and deletes.

# Datatype

Module atom

# Constraints

- Module atom implementing `update/3`, or `undefined` to disable the callback.

# Inferred default

Unset (`undefined`); no update hook is called.

# Tags

feature: object-storage
repository: riak_kv
module: riak_kv_vnode
concept: data-model

# Notes

This is the Erlang application environment key `update_hook` in `riak_kv`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_kv/src/riak_kv_vnode.erl](https://github.com/OpenRiak/riak_kv/blob/48285d5d7aa72c4167e338b3d28ae9ba434cfcb7/src/riak_kv_vnode.erl#L4982)

# Reviewed against

3.4.0: c5b9d4e411f24d32ec3cb35da17458377c3d81c01b596005aff1b952a6582c90
3.4.1: 0c3667fe2d05832493db94bf9e251a988be2dad7cfb16bdc8f54f796f594af84
