# Metadata

command: shell:riak help
versions: 3.4.0, 3.4.1

# Summary

Display release-launcher usage.

# Description

With no topic, prints the top-level command list. The launcher exits nonzero for this no-topic usage path; that is not a node-health failure.

# Arguments

## topic

datatype: topic name
required: false
repeatable: false

### Description

Optional launcher help topic.

# Options

## --no-permanent

omit: true

# Reviewed against

3.4.0: 7972ab9bab8914d4f59a08c6926f02f101302f32f8b95c7be66fd71eaead2034
3.4.1: 7972ab9bab8914d4f59a08c6926f02f101302f32f8b95c7be66fd71eaead2034

# Tags

feature: node-operations
repository: riak
module: riak
concept: node-lifecycle
