# Description

LevelDB options for the temporary database built by the legacy secondary-index anti-entropy repair tool. The tool always forces `create_if_missing` and `error_if_exists` to true.

# Datatype

List

# Constraints

- LevelDB option property list. The consumer forces `create_if_missing` and `error_if_exists` to `true`, overriding those entries.

# Inferred default

`[{write_buffer_size, 20971520}, {max_open_files, 20}]`.

# Tags

feature: legacy-aae
repository: riak_kv
module: riak_kv_2i_aae
concept: replica-repair, storage

# Notes

This is the Erlang application environment key `anti_entropy_leveldb_opts` in `riak_kv`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_kv/src/riak_kv_2i_aae.erl](https://github.com/OpenRiak/riak_kv/blob/48285d5d7aa72c4167e338b3d28ae9ba434cfcb7/src/riak_kv_2i_aae.erl#L395)

# Reviewed against

3.4.0: 0b80860d551af5059c03094ffb2e5350a2c8cdec0b55ceb07e391aaaec346f68
3.4.1: 8f8f344bec262c2fdaae1ca6a00a03aa13054fb823a3f881573f06a136c02ecd
