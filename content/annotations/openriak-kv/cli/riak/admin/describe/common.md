# Metadata

command: shell:riak admin describe

# Summary

Read the schema documentation for one or more configuration settings.

# Description

Read documentation for configuration settings in the node’s installed schema. Supply setting **names**, such as `ring_size` or `storage_backend`; use `riak admin show` to read their current values.

# Options

## --format

required: false
repeatable: false

### Description

Choose the output representation. `human` prints readable documentation;
`json` prints an array of text records.

`csv` only renders tables, so it omits this command’s setting descriptions.
The launcher appends `ok` after successful output. An unknown format prints
a warning and falls back to `human`.

## --help

required: false
repeatable: false
datatype: flag (no value)

### Description

Show usage without requesting a setting description. The short spelling is `-h`.

# Notes

Inspect the response as well as the process exit status. In the tested releases, missing or unknown setting names print an error term even though the launcher exits with status 0.

# Examples

## describe:one-setting

### Description

Describe `ring_size`. The response explains the setting’s purpose and constraints; it does not report the cluster’s current ring size.

## describe:two-settings

### Description

Describe two settings in one request. Separate their names with spaces.

# Related documentation

- [Read current setting values](../show/).
- [Configuration settings](../../../../configuration/).

# Reviewed against

3.4.0: 2f7e6c65659f42a6ab01bc2271c0341c7abfddad8596d95112d25b3b15a83f1f
3.4.1: 2f7e6c65659f42a6ab01bc2271c0341c7abfddad8596d95112d25b3b15a83f1f
