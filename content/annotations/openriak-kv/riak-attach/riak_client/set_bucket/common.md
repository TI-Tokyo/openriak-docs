# Metadata

command: erlang:riak_client:set_bucket/3
versions: 3.4.0, 3.4.1

# Summary

Set bucket-specific property overrides.

# Description

Pass a property list. Changes apply to the bucket’s behaviour; they do not rewrite existing objects immediately.

# Arguments

## Bucket

datatype: binary or pair of binaries
required: true
repeatable: false

### Description

See the shared `Bucket` argument on the parent module page.

## BucketProps

datatype: property list
required: true
repeatable: false

### Description

List of `{Property, Value}` pairs, for example `[{allow_mult, true}]`. Property validity depends on the backend and bucket type.

## Client

datatype: riak_client handle
required: true
repeatable: false

### Description

See the shared `Client` argument on the parent module page.

# Reviewed against

3.4.0: bcf72c8a3a373c3c199abec1535034744b55fc87fcc7082a559643f84d5891ba
3.4.1: bcf72c8a3a373c3c199abec1535034744b55fc87fcc7082a559643f84d5891ba

# Tags

feature: client-operations
repository: riak_kv
module: riak_client
concept: data-access
