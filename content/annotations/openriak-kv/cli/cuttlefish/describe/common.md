# Metadata

command: shell:cuttlefish describe
versions: 3.4.0, 3.4.1

# Summary

Describe a setting from the installed schemas.

# Description

This bundled helper is normally called by the Riak launcher. Its executable is /usr/lib/riak/bin/cuttlefish in the Alpine package. Supply the installed schema location and input configuration when invoking it directly.

# Arguments

## variable

datatype: configuration setting name
required: true
repeatable: false

### Description

Setting name to describe, for example `ring_size`.

# Options

## --help

datatype: flag (no value)
required: false
repeatable: false

### Description

Print helper usage.

## --etc_dir

datatype: directory path
required: false
repeatable: false
default: /etc

### Description

Base configuration directory. Used to derive default input and generated-file locations.

## --dest_dir

datatype: directory path
required: false
repeatable: false

### Description

Directory for generated runtime files. It must be writable.

## --dest_file

datatype: filename
required: false
repeatable: false

### Description

Base name of the generated configuration file.

## --schema_dir

datatype: directory path
required: false
repeatable: false

### Description

Directory containing .schema files.

## --schema_file

datatype: file path
required: false
repeatable: true

### Description

Individual schema file. Repeated files are processed in command-line order after schema_dir files.

## --conf_file

datatype: file path
required: false
repeatable: true

### Description

Input cuttlefish configuration file. Repeat to load multiple files.

## --advanced_conf_file

datatype: file path
required: false
repeatable: false

### Description

Additional Erlang advanced configuration file merged with the schema-generated result.

## --log_level

datatype: logging level
required: false
repeatable: false
default: notice

### Description

Logging level for this helper’s own diagnostics.

## --print

datatype: flag (no value)
required: false
repeatable: false

### Description

Print schema mappings to standard error.

## --max_history

datatype: non-negative integer
required: false
repeatable: false
default: 3

### Description

Maximum number of generated configuration-file histories to retain.

## --silent

datatype: flag (no value)
required: false
repeatable: false
default: false

### Description

Suppress normal helper output.

## --allow_extra

datatype: flag (no value)
required: false
repeatable: false
default: false

### Description

Accept configuration keys not found in a schema instead of failing validation. Use only when extra keys are intentional.

# Examples

## reference-example-1

title: Describe a setting

### Invocation

```sh
riak escript bin/cuttlefish describe ring_size --schema_dir /path/to/schema
```

### Description

Replace the schema path with the installed schema directory.

### Expected output

The setting’s schema documentation, or a diagnostic if no matching schema mapping exists.

# Errors

## reference-error-1

### Condition

An input or schema path is missing, or a setting fails schema validation.

### Description

The helper prints a configuration error and cannot produce valid runtime configuration.

### Remedy

Correct the path, setting name or value and rerun chkconfig before starting Riak.

# Results

## reference-result-1

### Description

Successful schema translation produces effective settings or runtime files, depending on the operation. Generation does not start the node.

# Reviewed against

3.4.0: 7aa057c43d0ef2ef657af61a9f5ae7ef5b5840402d21514194cf4fb0dd334093
3.4.1: 7aa057c43d0ef2ef657af61a9f5ae7ef5b5840402d21514194cf4fb0dd334093

# Tags

feature: node-operations
repository: cuttlefish
module: cuttlefish_escript
concept: node-lifecycle, retention
