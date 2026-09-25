# Description

Internal flag recording whether the setup utility is running as an escript. Setup computes and stores it so its error handling can choose between printing help and halting the script or raising an Erlang error.

# Datatype

Boolean

# Allowed values

- `true`
- `false`

# Constraints

- Use the Erlang atoms `true` or `false`.

# Inferred default

`false` before setup determines whether it is running as an escript; setup then stores the computed boolean.

# Tags

feature: installation
repository: setup
module: setup_lib
concept: runtime

# Notes

This is the Erlang application environment key `$setup_is_escript` in `kernel`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [setup/src/setup_lib.erl](https://github.com/OpenRiak/setup/blob/76133196bfe9903f8b7914ce3a85d9cffff5dfc1/src/setup_lib.erl#L71)

# Reviewed against

3.4.0: ae7342b4ca63847ca446278e1a86c152d78223b62152b625eaac2b8b6bfe78b7
3.4.1: ae7342b4ca63847ca446278e1a86c152d78223b62152b625eaac2b8b6bfe78b7
