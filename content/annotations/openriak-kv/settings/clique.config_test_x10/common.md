# Description

Test fixture populated by a Clique configuration callback with ten times the input value. The tests read it to confirm that the callback ran; it is not an operator setting.

# Datatype

Integer

# Constraints

- Integer produced by the test callback. Test fixture only.

# Inferred default

No production default; the test callback computes ten times its input (for example, `470`).

# Tags

feature: cluster-management
repository: clique
module: clique_config
concept: testing

# Notes

This is the Erlang application environment key `config_test_x10` in `clique`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [clique/src/clique_config.erl](https://github.com/OpenRiak/clique/blob/90d72664ea7e7550403d44f3f03204839194eb93/src/clique_config.erl#L509)

# Reviewed against

3.4.0: 3e49bf65401f17b5ec3b2558c30dc483f2c5e2a62b5d437514520d5badd2754c
3.4.1: 3e49bf65401f17b5ec3b2558c30dc483f2c5e2a62b5d437514520d5badd2754c
