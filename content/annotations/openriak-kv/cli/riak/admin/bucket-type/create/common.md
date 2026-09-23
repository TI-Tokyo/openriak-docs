# Metadata

command: shell:riak admin bucket-type create
versions: 3.4.0, 3.4.1

# Summary

Create an inactive bucket type.

# Description

Creation registers the type and its initial properties. Wait for the type to become available across the cluster, then activate it before using typed buckets.

# Arguments

## type

datatype: bucket type name
required: true
repeatable: false

### Description

Bucket type name, for example `cli_reference_type`. Creation and activation are separate steps.

## properties

datatype: JSON object
required: false
repeatable: false

### Description

JSON object containing a `props` object. Quote the whole JSON value in the shell, for example `'{"props":{"allow_mult":true}}'`.

# Reviewed against

3.4.0: e65ba9757d85819731aa433b2c3058733761f67bc2a8944bc74065106d649f0b
3.4.1: e65ba9757d85819731aa433b2c3058733761f67bc2a8944bc74065106d649f0b

# Tags

feature: bucket-properties
repository: riak_kv
module: riak_kv_console
concept: data-policy
