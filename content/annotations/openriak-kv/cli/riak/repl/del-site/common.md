# Metadata

command: shell:riak repl del-site
versions: 3.4.0, 3.4.1

# Summary

Remove a legacy replication site.

# Description

This configures the deprecated replication protocol. Use named-cluster connections for current replication deployments.

# Arguments

## sitename

datatype: site name
required: true
repeatable: false

### Description

Legacy site label, for example `cli_site`.

# Reviewed against

3.4.0: 7e364add9f2c737b95af895a2a26ac9f89418785ed1d731afa96008d0fe78fab
3.4.1: 7e364add9f2c737b95af895a2a26ac9f89418785ed1d731afa96008d0fe78fab
