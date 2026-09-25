# Description

Registry of application bucket-fixup modules. Riak runs these callbacks when preparing bucket properties and installing a ring, allowing applications to fill in or normalize their bucket settings.

# Datatype

List

# Constraints

- List of `{Application, Module}` atom pairs identifying bucket fixup implementations. Managed through `riak_core:register/2`.

# Inferred default

`[]` when unregistered; applications populate this registry at startup.

# Tags

feature: bucket-properties
repository: riak_core
module: riak_core
concept: data-policy

# Notes

This is the Erlang application environment key `bucket_fixups` in `riak_core`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_core/src/riak_core.erl](https://github.com/OpenRiak/riak_core/blob/2903cdc194fa4d538dd6f6da359e8465c11bb3c2/src/riak_core.erl#L276)

# Reviewed against

3.4.0: b70332dd4813e092b9c7ecc573fa10cba079847f549c387443b33f856d24b31f
3.4.1: b70332dd4813e092b9c7ecc573fa10cba079847f549c387443b33f856d24b31f
