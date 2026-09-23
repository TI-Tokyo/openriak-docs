# Metadata

command: shell:riak admin top
versions: 3.4.0, 3.4.1

# Summary

Continuously display Erlang process activity.

# Description

Runs the Erlang etop monitor with text output and tracing disabled. The command remains active until interrupted; compare repeated samples when investigating load.

# Arguments

# Options

## -interval

datatype: positive integer seconds
required: false
repeatable: false

### Description

Seconds between display updates, for example `5`.

## -sort

datatype: sort key
required: false
repeatable: false

### Valid values

- reductions
- memory
- msg_q

### Description

Process measurement used to order rows.

## -lines

datatype: positive integer
required: false
repeatable: false

### Description

Maximum number of process rows displayed, for example `10`.

# Examples

## reference-example-1

title: Largest process mailboxes

### Invocation

```sh
riak admin top -interval 5 -sort msg_q -lines 10
```

### Description

Display ten processes ordered by mailbox size, refreshing every five seconds. Interrupt the monitor when finished.

### Expected output

Repeated process tables with the selected ordering.

# Errors

## reference-error-1

### Condition

The monitor cannot connect, or an etop option is invalid.

### Description

Etop prints a connection or option error.

### Remedy

Check the node identity and cookie; use a positive interval/row count and a documented sort key.

# Results

## reference-result-1

### Description

Displays live process statistics. It is a continuous monitor rather than a one-shot health check.

# Reviewed against

3.4.0: eef9c37d50a92db3fb193a9ed0573901fe8ea20967edc209cb8ce35881a02673
3.4.1: eef9c37d50a92db3fb193a9ed0573901fe8ea20967edc209cb8ce35881a02673

# Tags

feature: node-operations
repository: riak
module: riak-admin
concept: node-lifecycle
