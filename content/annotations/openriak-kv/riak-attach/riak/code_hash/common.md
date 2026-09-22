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

3.4.0: 4588bcd857ae34541a2824650dea3f8d3bbaae0dcc549baefd3fa2ab2566f503
3.4.1: 4588bcd857ae34541a2824650dea3f8d3bbaae0dcc549baefd3fa2ab2566f503
