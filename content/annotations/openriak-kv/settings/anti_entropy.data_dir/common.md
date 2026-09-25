# Description

Directory containing legacy AAE hash-tree data. Defaults to `$(platform_data_dir)/anti_entropy`, beneath the platform's configured data root; changing `platform_data_dir` changes this default unless `anti_entropy.data_dir` is explicitly set. These trees support replica comparison and are distinct from the stored objects themselves.

# Notes

The default shown in the reference is the resolved package default for the selected OS. The current metadata for both documented releases resolves `platform_data_dir` to `/var/lib/riak` on every listed OS, giving `/var/lib/riak/anti_entropy`; this is not a fixed path in the schema. The [Cuttlefish mapping](https://github.com/OpenRiak/riak_kv/blob/48285d5d7aa72c4167e338b3d28ae9ba434cfcb7/priv/riak_kv.schema#L483) derives the directory from `platform_data_dir`.

# Tags

feature: legacy-aae
repository: riak_kv
module: riak_kv_index_hashtree
concept: filesystem-layout, replica-repair

# Reviewed against

3.4.0: 729a4789141319228ecb131747caa52146851b306bd609a743e61282997aad27
3.4.1: c7b49f93679d52e3aa5caa0eead6585c932f5a0dda9e5879b221a22b7363114c
