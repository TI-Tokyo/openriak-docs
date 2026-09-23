# Metadata

command: shell:riak admin reformat-indexes
versions: 3.4.0, 3.4.1

# Summary

Reformat secondary-index metadata for compatibility.

# Description

This maintenance operation is backend-dependent. Choose concurrency and batch size appropriate to the data set; use downgrade only for the reverse-format operation.

# Arguments

## concurrency

datatype: positive integer
required: false
repeatable: false

### Description

Concurrent reformatting workers. Omit to use the implementation default.

## batch size

datatype: positive integer
required: false
repeatable: false

### Description

Entries processed per batch. Supply only after concurrency.

# Options

## --downgrade

datatype: flag (no value)
required: false
repeatable: false

### Description

Convert indexes toward the older representation. Put this after numeric arguments.

# Examples

## reference-example-1

title: One worker and a bounded batch

### Invocation

```sh
riak admin reformat-indexes 1 100
```

### Description

Use during a planned backend/index-format maintenance operation.

### Expected output

Job-start confirmation and progress or a backend error.

# Errors

## reference-error-1

### Condition

Numeric arguments or downgrade-switch placement are invalid.

### Description

The parser prints expected options or invalid trailing arguments.

### Remedy

Put concurrency and batch size before the optional --downgrade flag.

# Results

## reference-result-1

### Description

Starts index reformatting with the selected worker and batch limits.

# Reviewed against

3.4.0: bd7e6e3d2bf562925cd6bd0fc8a3755e6c9db7702b67521785a180a741c9e20d
3.4.1: bd7e6e3d2bf562925cd6bd0fc8a3755e6c9db7702b67521785a180a741c9e20d

# Tags

feature: secondary-indexes
repository: riak_kv
module: riak_kv_console
concept: querying
