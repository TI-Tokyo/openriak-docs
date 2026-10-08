# Metadata

command: erlang:riak:code_hash/0
versions: 3.4.0, 3.4.1

# Summary

Calculate the loaded Riak code fingerprint.

# Description

The result is a base-62 representation of an MD5 digest over the Riak application’s module binaries. It is useful for comparing deployments, not as a security signature.

# Arguments

# Results

## outcome

### Description

A working application layout would return a hash of loaded Riak code. These runtimes do not expose the expected riak application module list, so the call raises badmatch instead of returning a hash.

# Reviewed against

3.4.0: c83239b4579866c29ab30de897e019e2ed52329236ef84c3053ba5eac98744d8
3.4.1: c83239b4579866c29ab30de897e019e2ed52329236ef84c3053ba5eac98744d8

# Tags

feature: node-operations
repository: riak_kv
module: riak
concept: node-lifecycle
