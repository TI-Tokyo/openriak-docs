# Description

Test fixture used by Clique's configuration tests to verify that setting a value updates the application environment. It has no production configuration role.

# Datatype

Integer

# Constraints

- Integer parsed from the test configuration string. Test fixture only.

# Inferred default

No production default; the test sets the value explicitly (for example, `42`).

# Tags

feature: cluster-management
repository: clique
module: clique_config
concept: testing

# Notes

This is the Erlang application environment key `config_test` in `clique`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [clique/src/clique_config.erl](https://github.com/OpenRiak/clique/blob/90d72664ea7e7550403d44f3f03204839194eb93/src/clique_config.erl#L481)

# Reviewed against

3.4.0: a58702b127da7fad384effe9f9f257e6668d53d65fcaef651ede1f5e1a9c3404
3.4.1: a58702b127da7fad384effe9f9f257e6668d53d65fcaef651ede1f5e1a9c3404
