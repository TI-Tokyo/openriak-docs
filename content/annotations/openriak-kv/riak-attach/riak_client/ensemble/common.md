# Metadata

command: erlang:riak_client:ensemble/1
versions: 3.4.0, 3.4.1

# Summary

Find the strong-consistency ensemble responsible for a key.

# Description

Returns `{kv, Partition, NVal}` from the current ring and bucket properties.

# Arguments

## BKey

datatype: bucket/key tuple
required: true
repeatable: false

### Description

Pair `{Bucket, Key}`, for example `{<<"cli_reference">>, <<"present">>}`.

# Reviewed against

3.4.0: 3c68e624df9c37479cb6082772f23086a2b8cedbfa7b4416484eb45014117bdd
3.4.1: 3c68e624df9c37479cb6082772f23086a2b8cedbfa7b4416484eb45014117bdd
