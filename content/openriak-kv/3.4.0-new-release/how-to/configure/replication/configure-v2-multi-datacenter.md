---
title: 'Configure legacy multi-datacenter replication'
description: 'Show operators how to configure legacy multi-datacenter replication and validate data movement.'
weight: 9
diataxis: 'how-to'
product: 'OpenRiak KV'
product_version: '3.4.0'
status: 'editorially-rewritten'
draft: true
audience:
  - 'operators'
legacy_3_2_5_sources:
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\configuring\v2-multi-datacenter.md'
  - 'Legacy multi-datacenter replication terminology and commands require compatibility review.'
source_material:
  - 'legacy-3.2.5'
  - 'live-3.2.5'
  - 'proposed-kv'
  - 'openriak-quickdocs-3.4'
quickdocs_sources:
  - 'https://openriak.github.io/riak/ReplicationGuide.html#legacy-replication---riak_repl'
tags: ['diataxis', 'kv', 'how-to']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Show operators how to configure legacy multi-datacenter replication and validate data movement.

## Before you begin

Administrative access to the nodes you will change; a copy of the current configuration; and a maintenance window if the setting requires a restart.

## Overview

### V2 Multi-Datacenter Replication

[config v2 ssl]: {{< product-version-root >}}how-to/configure/replication/secure-replication/

**Deprecation Warning**
v2 Multi-Datacenter Replication is deprecated and will be removed in a future version. Please use [v3]({{< product-version-root >}}how-to/configure/replication/configure-v3-multi-datacenter/) instead.

OpenRiak's Multi-Datacenter Replication capabilities offer a
variety of configurable parameters.

#### File

The configuration for replication is kept in the `riak_repl` section of
each node's `advanced.config`. That section looks like this:

```advancedconfig
{riak_repl, [
             {fullsync_on_connect, true},
             {fullsync_interval, 360},
             % Debian/Centos/RHEL:
             {data_root, "/var/lib/riak/data/riak_repl"},
             % Solaris:
             % {data_root, "/opt/riak/data/riak_repl"},
             % FreeBSD/SmartOS:
             % {data_root, "/var/db/riak/riak_repl"},
             {queue_size, 104857600},
             {server_max_pending, 5},
             {client_ack_frequency, 5}
            ]}
```

#### Usage

These settings are configured using the standard Erlang config file
syntax, i.e. `{Setting, Value}`. For example, if you wished to set
`ssl_enabled` to `true`, you would insert the following line into the
`riak_repl` section (appending a comma if you have more settings to
follow):

```advancedconfig
{riak_repl, [
             % Other configs
             {ssl_enabled, true},
             % Other configs
            ]}
```

#### Settings

Once your configuration is set, you can verify its correctness by
running the following command:

```bash
riak chkconfig
```

The output from this command will point you to syntactical and other
errors in your configuration files. This files will be created with the current system time and date in the name.

The output should appear similar to the example below:

```
config is OK
-config /var/lib/riak/generated.conf/app.2023.01.01.12.00.00.config -args_file /var/lib/riak/generated.conf/vm.2023.01.01.12.00.00.args -vm_args /var/lib/riak/generated.conf/vm.2023.01.01.12.00.00.args
```
A full list of configurable parameters can be found in the sections
below.

**Note:**
In OpenRiak KV 3.0.1+ the `riak-repl` command has been changed to `riak repl` (with no hyphen). For execution purposes, please use `riak repl`. Please be aware that the output from `riak repl` may quote `riak-repl` in command execution examples as it has inherited OpenRiak KV 2.x functionality.

#### Fullsync Settings

Setting | Options | Default | Description
:-------|:--------|:--------|:-----------
`fullsync_on_connect` | `true`, `false` | `true` | Whether or not to initiate a fullsync on initial connection from the secondary cluster
`fullsync_strategies` | `keylist` | `[keylist]` | A *list* of fullsync strategies to be used by replication.<br />**Note**: Please contact Basho support for more information.
`fullsync_interval`   | `mins` (integer), `disabled` | `360` | How often to initiate a fullsync of data, in minutes. This is measured from the completion of one fullsync operation to the initiation of the next. This setting only applies to the primary cluster (listener). To disable fullsync, set `fullsync_interval` to `disabled` and `fullsync_on_connect` to `false`.**

#### SSL Settings

Setting | Options | Default | Description
:-------|:--------|:--------|:-----------
`ssl_enabled` | `true`, `false` | `false` | Enable SSL communications
`keyfile` | `path` (string) | `undefined` | Fully qualified path to an SSL `.pem` key file
`cacertdir` | `path` (string) | `undefined` | The `cacertdir` is a fully-qualified directory containing all the CA certificates needed to verify the CA chain back to the root
`certfile` | `path` (string) | `undefined` | Fully qualified path to a `.pem` cert file
`ssl_depth` | `depth` (integer) | `1` | Set the depth to check for SSL CA certs. See [1](#f1).
`peer_common_name_acl` | `cert` (string) | `"*"` | Verify an SSL peer’s certificate common name. You can provide an ACL as a list of common name *patterns*, and you can wildcard the leftmost part of any of the patterns, so `*.basho.com` would match `site3.basho.com` but not `foo.bar.basho.com` or `basho.com`. See [4](#f4).

#### Queue, Object, and Batch Settings

Setting | Options | Default | Description
:-------|:--------|:--------|:-----------
`data_root` | `path` (string) | `data/riak_repl` | Path (relative or absolute) to the working directory for the replication process
`queue_size` | `bytes` (integer) | `104857600` (100 MiB) | The size of the replication queue in bytes before the replication leader will drop requests. If requests are dropped, a fullsync will be required. Information about dropped requests is available using the `riak repl status` command
`server_max_pending` | `max` (integer) | `5` | The maximum number of objects the leader will wait to get an acknowledgment from, from the remote location, before queuing the request
`vnode_gets` | `true`, `false` | `true` | If `true`, repl will do a direct get against the vnode, rather than use a `GET` finite state machine
`shuffle_ring` | `true`, `false` | `true `| If `true`, the ring is shuffled randomly. If `false`, the ring is traversed in order. Useful when a sync is restarted to reduce the chance of syncing the same partitions.
`diff_batch_size` | `objects` (integer) | `100` | Defines how many fullsync objects to send before waiting for an acknowledgment from the client site

#### Client Settings

Setting | Options | Default | Description
:-------|:--------|:--------|:-----------
`client_ack_frequency` | `freq` (integer) | `5` | The number of requests a leader will handle before sending an acknowledgment to the remote cluster
`client_connect_timeout` | `ms` (integer) | `15000` | The number of milliseconds to wait before a client connection timeout occurs
`client_retry_timeout` | `ms` (integer) | `30000` | The number of milliseconds to wait before trying to connect after a retry has occurred

#### Buffer Settings

Setting | Options | Default | Description
:-------|:--------|:--------|:-----------
`sndbuf` | `bytes` (integer) | OS dependent | The buffer size for the listener (server) socket measured in bytes
`recbuf` | `bytes` (integer) | OS dependent | The buffer size for the site (client) socket measured in bytes

#### Worker Settings

Setting | Options | Default | Description
:-------|:--------|:--------|:-----------
`max_get_workers` | `max` (integer) | `100` | The maximum number of get workers spawned for fullsync. Every time a replication difference is found, a `GET` will be performed to get the actual object to send. See [2](#f2).
`max_put_workers` | `max` (integer) | `100` | The maximum number of put workers spawned for fullsync. Every time a replication difference is found, a `GET` will be performed to get the actual object to send. See [3](#f3).
`min_get_workers` | `min` (integer) | `5` | The minimum number of get workers spawned for fullsync. Every time a replication difference is found, a `GET` will be performed to get the actual object to send. See [2](#f2).
`min_put_workers` | `min` (integer) | `5` | The minimum number of put workers spawned for fullsync. Every time a replication difference is found, a `GET` will be performed to get the actual object to send. See [3](#f3).

1. <a name="f1"></a>SSL depth is the maximum number of non-self-issued
 intermediate certificates that may follow the peer certificate in a valid
 certificate chain. If depth is `0`, the PEER must be signed by the trusted
 ROOT-CA directly; if `1` the path can be PEER, CA, ROOT-CA; if depth is `2`
 then PEER, CA, CA, ROOT-CA and so on.

2. <a name="f2"></a>Each get worker spawns 2 processes, one for the work and
 one for the get FSM (an Erlang finite state machine implementation for `GET`
 requests). Be sure that you don't run over the maximum number of allowed
 processes in an Erlang VM (check `vm.args` for a `+P` property).

3. <a name="f3"></a>Each put worker spawns 2 processes, one for the work, and
  one for the put FSM (an Erlang finite state machine implementation for `PUT`
  requests). Be sure that you don't run over the maximum number of allowed
  processes in an Erlang VM (check `vm.args` for a `+P` property).

4. <a name="f4"></a>If the ACL is specified and not the special value `*`,
 peers presenting certificates not matching any of the patterns will not be
 allowed to connect.
 If no ACLs are configured, no checks on the common name are done, except
 as described for [Identical Local and Peer Common Names][config v2 ssl].

#### Legacy Replication - riak_repl

The previous replication solution in Riak, `riak_repl`, is still available to configure.  The `riak_repl` solution is stable, and has not been modified since Riak 2.2.3 (other than the conversion to be fully open-source in Riak 2.2.5).

The [legacy documentation]({{<baseurl>}}openriak-kv/2.2.3/configuring/v3-multi-datacenter/index.html) can be used to set up `riak_repl`.  The v3 of riak_repl should always be used in preference to previous versions.

Some notes on `riak_repl` and the comparison to NextGen replication in Riak:

- `riak_repl` is not under active development, but remains functional.
- `riak-repl` has no support for replication and reconciliation between clusters with different ring sizes, so cannot be used to reliably transition between clusters of different ring sizes.
- `riak_repl` uses a PUSH model to replicate real-time changes.
- `riak_repl` will attempt to migrate queues between nodes when nodes go down.
  - Despite the additional resilience, anecdotal evidence indicates that real-time replication is generally less reliable than NextGen replication (i.e. it is more likely to drop replication events).
- `riak_repl` has an anti-entropy based method of full-sync reconciliation, using the legacy active anti-entropy service.
  - The AAE-based full-sync in `riak_repl` is faster at resolving deltas, but will fail to complete during tree rebuilds;
  - Users of full-sync have needed to use manually prompted rebuild windows to address this problem (i.e. a period where full-sync is suspended, and rebuilds are completed in parallel).
  - As clusters scale, the AAE rebuild windows will be an ongoing management overhead, and clusters may scale to the point that rebuilds cannot complete in the available window.
- `riak_repl` has a keylisting form of full-sync which will do a full key and clock comparison on a vnode-by-vnode basis.
  - A keylisting full-sync can be resource intensive and will take a significant amount of time to complete on clusters of non-trivial scale.

The use of `riak_repl` is deprecated, and when a retirement schedule is agreed it will be advertised via [OpenRiak discussions](https://github.com/orgs/OpenRiak/discussions).

## Verify the result

Confirm that the intended setting is active on every affected node, then check cluster health and the relevant logs for warnings.
