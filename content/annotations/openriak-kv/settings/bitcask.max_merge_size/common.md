# Description

Maximum amount of Bitcask data selected for one merge. Limiting a merge bounds its work; smaller merges may need more passes to reclaim accumulated dead data.

# Tags

feature: bitcask
repository: riak_kv
module: riak_kv_bitcask_backend
concept: compaction, storage

# Reviewed against

3.4.0: 37bff3630fafaa193bda7daa17460a27579f09a0a8711f72983967ef8ab2f757
3.4.1: 05cad1089f00c177ce462568ce75f621634b14343d87f32198267c929c42ab75
