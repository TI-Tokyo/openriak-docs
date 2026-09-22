# Metadata

command: shell:riak admin tictacaae maxresults
versions: 3.4.0, 3.4.1

# Summary

Read or change the maximum AAE exchange results.

# Description

Omit the value to read the runtime setting; supply a value to change it on the selected node. Persist the corresponding configuration separately if the change must survive restart.

# Arguments

## VALUE

datatype: integer from 1 to 1000000
required: false
repeatable: false

### Description

New value for maximum AAE exchange results. Omit to read the current setting.

# Options

## --format

datatype: output writer
required: false
repeatable: false
default: human

### Valid values

- csv
- human
- json

### Description

Select the Clique output writer. `human` is readable terminal output; `csv` renders tables only; `json` renders structured status records. The launcher can append an `ok` line, so complete stdout is not necessarily a standalone JSON document. An unknown writer warns and falls back to `human`.

## --help

datatype: flag (no value)
required: false
repeatable: false

### Description

Print usage without executing the command. The short spelling is `-h`.

## --node

datatype: Erlang node name or all
required: false
repeatable: false
default: local node

### Description

Full Erlang node name, or `all` to select all available nodes. Omit to select the local node.

# Results

## outcome

### Description

With no value, this returns the current AAE result limit. With a value, it changes the limit; read it back to verify the change.

# Reviewed against

3.4.0: 0f28419d1289f2e1565e23f375677716c822f5f29b2407b33a10158be3f78552
3.4.1: 0f28419d1289f2e1565e23f375677716c822f5f29b2407b33a10158be3f78552
