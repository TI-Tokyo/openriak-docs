# Metadata

command: shell:riak
versions: 3.4.0, 3.4.1

# Summary

Manage an OpenRiak node and access its administration tools.

# Description

Use a subcommand to start or stop a node, open an Erlang shell, run administrative operations, or manage replication. OS service-manager commands are listed separately where they apply.

# Arguments

# Options

## --no-permanent

omit: true
datatype: flag (no value)
required: false
repeatable: false

### Description

For release installation or upgrade, leave the installed release non-permanent. This flag does not apply to arbitrary subcommands.

## --relx-disable-hooks

omit: true
datatype: flag (no value)
required: false
repeatable: false

### Description

Disable the release launcher’s configured lifecycle hooks for the supported launcher operation.

# Notes

The tested Alpine 3.24 packages include a `/usr/sbin/riak` wrapper that corrupts some numeric and quoted arguments. Administrative and replication examples therefore invoke the bundled release launcher explicitly, with its generated VM arguments file:

```sh
VMARGS_PATH=/var/lib/riak/vm.args /usr/lib/riak/bin/riak admin member-status
```

Use the paths from your installation if they differ. The long executable path still runs the documented `riak` command; it bypasses the package wrapper without changing the installed files.


`--no-permanent` belongs to release installation and upgrade commands; it is not a general option for every `riak` subcommand.

The release launcher also recognizes the internal flag `--relx-disable-hooks`. For that invocation, it clears the pre-start, post-start, pre-stop, post-stop, pre-install/upgrade, post-install/upgrade and status hook lists. It does not change the configuration permanently or disable hooks inside the running Riak application.

The launcher adds this flag itself when `riak daemon` starts its inner `console` process. The outer launcher handles the startup hooks, so the inner process must skip them to avoid running them twice.

In the Alpine runtime, startup hooks normally generate configuration, check whether Riak is already running, check the file-descriptor limit, set launcher log-size and code-loading defaults, wait for startup, and write the PID file. Manually disabling these hooks can skip those steps. The stop, install/upgrade and status hook lists are empty in the inspected images.

This is an internal launcher flag, not a general administrative option. Although the launcher scans all arguments for it, it does not remove it from the arguments passed to the selected command. Putting it before the subcommand prevents normal command dispatch; appending it to an administrative command can cause an extra-argument error. Let the daemon launcher supply it when needed.

# Examples

## reference-example-1

title: Choose a subcommand

### Invocation

```sh
riak help
```

### Description

Display the launcher or command-group usage. Some groups return a nonzero status when invoked without a subcommand.

### Expected output

Usage text listing available subcommands.

# Errors

## reference-error-1

### Condition

No recognised subcommand was supplied.

### Description

Usage is printed; legacy groups can also return an error term or a nonzero process status.

### Remedy

Select a subcommand from the syntax links and provide its required arguments.

## reference-error-2

### Condition

The configured Erlang node cannot be reached.

### Description

Commands that contact the running VM report a ping, RPC or distribution-connection failure.

### Remedy

Check that Riak is running and that the configured node name, cookie and distribution connectivity match. Use the operating-system service manager when appropriate.

# Results

## reference-result-1

### Description

The selected subcommand determines the result. Invoking the group without a valid subcommand displays usage rather than performing a data operation.

# Reviewed against

3.4.0: 0d5be13d88cb2fe49ae6fb17535935462d36c76ec087f4f58de618b5584a0959
3.4.1: 0d5be13d88cb2fe49ae6fb17535935462d36c76ec087f4f58de618b5584a0959
