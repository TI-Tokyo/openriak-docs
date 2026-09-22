# Metadata

command: shell:riak eval
versions: 3.4.0, 3.4.1

# Summary

Evaluate an Erlang expression on the running node.

# Description

Quote the entire expression for the shell and terminate it with a period. Results are printed as Erlang terms. Expressions execute on the target node and can mutate or stop it.

# Arguments

## Exprs

datatype: Erlang expression
required: true
repeatable: false

### Description

Erlang expression, for example `node().` or `1 + 2.`. Quote it as one shell argument.

# Reviewed against

3.4.0: 05fd2955e5e3032e33e437d2975257e866bda6e29eefd22e40dbd57e140b1163
3.4.1: 05fd2955e5e3032e33e437d2975257e866bda6e29eefd22e40dbd57e140b1163
