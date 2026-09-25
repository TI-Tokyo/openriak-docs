# Description

Release-metadata directory override read by the setup utility. When absent, setup checks `RELDIR` and then derives a `releases` directory from the Erlang root or client-node directory.

# Datatype

Directory path

# Constraints

- Directory path string. A configured application value takes precedence over the environment/root calculation.

# Inferred default

The `RELDIR` environment variable if nonempty, otherwise `releases` under the Erlang root (or client root in a client installation).

# Tags

feature: installation
repository: setup
module: setup_lib
concept: filesystem-layout

# Notes

This is the Erlang application environment key `releases_dir` in `sasl`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [setup/src/setup_lib.erl](https://github.com/OpenRiak/setup/blob/76133196bfe9903f8b7914ce3a85d9cffff5dfc1/src/setup_lib.erl#L122)

# Reviewed against

3.4.0: 77f33c4755cdd650e380c47dca2f21a6497838dcbf02d0d54cf0018aba50f37f
3.4.1: 77f33c4755cdd650e380c47dca2f21a6497838dcbf02d0d54cf0018aba50f37f
