# Description

Binary representation used to store Riak objects: `0` is the original Erlang term format and `1` is the more compact representation. Leveled persists format `1` even when `0` is configured here.

# Tags

feature: object-storage
repository: riak_kv
module: riak_kv_app
concept: data-model

# Reviewed against

3.4.0: c7c44968655f85161294946725ae65ab505131a32291114a60a28213f31533e3
3.4.1: d0fddc673b0ce9372d88e2f91f804e9e4e592b068f0f8dc4b3328f067b4b3365
