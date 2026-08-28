---
title: 'Upgrade an OpenRiak cluster'
description: 'Show operators how to upgrade an openriak cluster with prechecks, verification, and recovery guidance.'
weight: 17
diataxis: 'how-to'
product: 'OpenRiak KV'
product_version: '3.4.0'
status: 'editorially-rewritten'
draft: true
audience:
  - 'operators'
migration_source_root: '\\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv'
migration_sources:
  - '\\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv\admin\upgrade\upgrade-checklist.md'
  - '\\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv\admin\upgrade\upgrading.md'
migration_review:
  - 'Release-specific installation, upgrade, downgrade, or quick-start instructions require verification against OpenRiak KV 3.4.0 packages.'
  - 'Commands or links derived from the 3.2.5 documentation were version-normalized for 3.4.0 and require technical verification.'
  - 'Legacy version text or MDX syntax remains and requires editorial review.'
legacy_3_2_5_sources:
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\setup\upgrading.md'
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\setup\upgrading\checklist.md'
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\setup\upgrading\cluster.md'
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\setup\upgrading\multi-datacenter.md'
  - 'Package, platform, installation, upgrade, or downgrade details require release-specific verification for OpenRiak KV 3.4.0.'
source_material:
  - 'legacy-3.2.5'
  - 'live-3.2.5'
  - 'proposed-kv'
  - 'openriak-quickdocs-3.4'
quickdocs_sources:
  - 'https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#upgrading-a-node'
tags: ['diataxis', 'kv', 'how-to']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Show operators how to upgrade an openriak cluster with prechecks, verification, and recovery guidance.

## Before you begin

A healthy cluster, current backups, and access to cluster status and logs. Record the starting state before making an operational change.

## Overview

### Upgrading OpenRiak KV

[upgrade checklist]: ./checklist
[upgrade version]: ./version
[upgrade cluster]: ./cluster
[upgrade mdc]: ./multi-datacenter

#### In This Section

##### [Production Checklist][upgrade checklist]

An overview of what to consider before upgrading OpenRiak KV in a production environment.

[Learn More >>][upgrade checklist]

##### [Upgrading to OpenRiak KV 3.2.5][upgrade version]

A tutorial on updating to OpenRiak KV 3.2.5

[Learn More >>][upgrade version]

### Production Checklist

[perf open files]: /kv/3.4.0/how-to/tune/set-open-files-limit/
[perf index]: /kv/3.4.0/how-to/tune/
[ntp]: http://www.ntp.org/
[security basics]: /kv/3.4.0/how-to/secure/enable-security/
[cluster ops load balance]: /kv/3.4.0/how-to/configure/load-balancing-proxy/
[config reference]: /kv/3.4.0/reference/configuration/
[config backend]: /kv/3.4.0/how-to/configure/backends/
[usage conflict resolution]: /kv/3.4.0/how-to/develop/resolve-conflicts/
[concept eventual consistency]: /kv/3.4.0/explanation/consistency/eventual-consistency/
[apps replication properties]: /kv/3.4.0/explanation/replication/references-and-triggers/
[concept strong consistency]: /kv/3.4.0/reference/specialized-apis/strong-consistency-api/
[cluster ops bucket types]: /kv/3.4.0/how-to/operate/manage-bucket-types/
[use admin commands]: /kv/3.4.0/reference/commands/
[use admin riak control]: /kv/3.4.0/reference/commands/riak-control/
[cluster ops inspect node]: /kv/3.4.0/how-to/operate/inspect-node-and-cluster/
[troubleshoot http]: /kv/3.4.0/how-to/troubleshoot/http-204/
[use admin riak admin]: /kv/3.4.0/reference/commands/riak/ admin
[SANs]: http://en.wikipedia.org/wiki/Storage_area_network

Deploying OpenRiak KV to a realtime production environment from a development or testing environment can be a complex process. While the specifics of that process will always depend on your environment and practices, there are some basics for you to consider and a few questions that you will want to ask while making this transition.

We've compiled these considerations and questions into separate categories for you to look over.

#### System

* Are all systems in your cluster as close to identical as possible in
  terms of both hardware and software?
* Have you set appropriate [open files limits][perf open files] on all
  of your systems?
* Have you applied the [OpenRiak KV performance improvement recommendations][perf index]?

#### Network

* Are all systems using the same [NTP servers][ntp] to
  synchronize clocks?
* Are you sure that your NTP clients' configuration is monotonic (i.e.
  that your clocks will not roll back)?
* Is DNS correctly configured for all systems' production deployments?
* Are connections correctly routed between all Riak nodes?
* Are connections correctly set up in your load balancer?
* Are your [firewalls][security basics] correctly configured?
* Check that network latency and throughput are as expected for all of the
  following (we suggest using [iperf][ntp] to verify):
  - between nodes in the cluster
  - between the load balancer and all nodes in the cluster
  - between application servers and the load balancer
* Do all Riak nodes appear in the load balancer's rotation?
* Is the load balancer configured to balance connections with roundrobin
  or a similarly random [distribution scheme][cluster ops load balance]?

#### OpenRiak KV

* Check [configuration files][config reference]:
  - Does each machine have the correct name and IP settings in
    `riak.conf` (or in `app.config` if you're using the older
    configuration files)?
  - Are all [configurable settings][config reference] identical
    across the cluster?
  - Have all of the settings in your configuration file(s) that were
    changed for debugging purposes been reverted back to production
    settings?
  - If you're using [multiple data backends][config backend], are all of your
    bucket types configured to use the correct backend?
  - If you are using Riak Security, have you checked off all items in
    the [security checklist][security basics] and turned on security?
  - If you're using [multiple data backends][config backend], do all machines'
    config files agree on their configuration?
  - Do all nodes agree on the value of the [`allow_mult`][config basic] setting?
  - Do you have a [sibling resolution][usage conflict resolution] strategy in
    place if `allow_mult` is set to `true`?
  - Have you carefully weighed the [consistency trade-offs][concept eventual consistency] that must be made if `allow_mult` is set to `false`?
  - Are all of your [apps replication properties][apps replication properties] configured correctly and uniformly across the cluster?
  - If you are using [strong consistency][concept strong consistency] for some or all of your
    data:
      * Does your cluster consist of at least three nodes? If it does
        not, you will not be able to use this feature, and you are
        advised against enabling it.
      * If your cluster does consist of at least three nodes, has the
        strong consistency subsystem been [enabled][config strong consistency] on all nodes?
      * Is the [`target_n_val`][config reference] that is set on each node higher than any `n_val` that you intend to use for strongly consistent bucket types (or any bucket types for that matter)? The default is 4, which will likely need to be raised if you are using strong consistency.
  - Have all [bucket types][cluster ops bucket types] that you intend to use
    been created and successfully activated?
  - If you are using [`riak_control`][use admin riak control], is it enabled on the node(s) from which you intend to use it?
* Check data mount points:
  - Is `/var/lib/riak` mounted?
  - Can you grow that disk later when it starts filling up?
  - Do all nodes have their own storage systems (i.e. no
    [SANs]), or do you have a plan in place for switching to that configuration later?
* Are all OpenRiak KV nodes up?
  - Run `riak ping` on all nodes. You should get `pong` as a response.
  - Run `riak admin wait-for-service riak_kv <node_name>@<IP>` on each
    node. You should get `riak_kv is up` as a response.

The `<node_name>@<IP>` string should come from your [configuration
    file(s)][configure reference].
* Do all nodes agree on the ring state?
  - Run `riak admin ringready`. You should get `TRUE ALL nodes agree on
    the ring [list_of_nodes]`.
  - Run `riak admin member-status`. All nodes should be valid (i.e.
    listed as `Valid: 1`), and all nodes should appear in the list
  - Run `riak admin ring-status`. The ring should be ready (`Ring Ready:
    true`), there should be no unreachable nodes (`All nodes are up and
    reachable`), and there should be no pending changes to the ring
    (`No pending changes`).
  - Run `riak admin transfers`. There should be no active transfers (`No
    transfers active`).

#### Operations

* Does your monitoring system ensure that [NTP][ntp] is
  running?
* Are you collecting [time series data][cluster ops inspect node] on
  the whole cluster?
  - System metrics
    + CPU load
    + Memory used
    + Network throughput
    + Disk space used/available
    + Disk input/output operations per second (IOPS)
  - Riak metrics (from the [`/stats`][troubleshoot http] HTTP endpoint or
    using [`riak admin`][use admin riak admin])
    + Latencies: `GET` and `PUT` (mean/median/95th/99th/100th)
    + Vnode stats: `GET`s, `PUT`s, `GET` totals, `PUT` totals
    + Node stats: `GET`s, `PUT`s, `GET` totals, `PUT` totals
    + Finite state machine (FSM) stats:
      * `GET`/`PUT` FSM `objsize` (99th and 100th percentile)
      * `GET`/`PUT` FSM `times` (mean/median/95th/99th/100th)
    + Protocol buffer connection stats
      * `pbc_connects`
      * `pbc_active`
      * `pbc_connects_total`
* Are the following being graphed (at least the key metrics)?
  - Basic system status
  - Median and 95th and 99th percentile latencies (as these tend to be
    leading indicators of trouble)

#### Application and Load

* Have you benchmarked your cluster with simulated load to confirm that
  your configuration will meet your performance needs?
* Are the [develop client libraries] in use in your application up to date?
* Do the client libraries that you're using support the version of OpenRiak KV
  that you're deploying?

#### Confirming Configuration with Riaknostic

Recent versions of OpenRiak KV ship with Riaknostic, a diagnostic utility that
can be invoked by running `riak admin diag <check>`, where `check` is
one of the following:

* `disk`
* `dumps`
* `memory_use`
* `nodes_connected`
* `ring_membership`
* `ring_preflists`
* `ring_size`
* `sysctl`

Running `riak admin diag` with no additional arguments will run all
checks and report the findings. This is a good way of verifying that
you've gotten at least some of the configurations mentioned above
correct, that all nodes in your cluster are up, and that nothing is
grossly misconfigured. Any warnings produced by `riak admin diag` should
be addressed before going to production.

#### Troubleshooting and Support

* For free support, go to the /community page to find helpful links
* To open a support ticket (which requires a support contact with TI Tokyo), go to https://support.tiot.jp/
  - Normal and Low are for issues not immediately impacting production
    systems
  - High is for problems that impact production or soon-to-be-production
    systems, but where stability is not currently compromised
  - Urgent is for problems causing production outages or for those
    issues that are likely to turn into production outages very soon.
    On-call engineers respond to urgent requests within 30 minutes,
    24 / 7.
* Does your team know how to gather `riak-debug` results from the whole
  cluster when opening tickets? If not, that process goes something like
  this:
  - SSH into each machine, run `riak-debug`, and grab the resultant
    `.tar.gz` file
  - Attach all debug tarballs from the whole cluster each time you open
    a new High- or Urgent-priority ticket

#### The Final Step: Taking it to Production

Once you've been running in production for a month or so, look back at
the metrics gathered above. Based on the numbers you're seeing so far,
configure alerting thresholds on your latencies, disk consumption, and
memory. These are the places most likely to give you advance warning of
trouble.

When you go to increase capacity down the line, having historic metrics
will give you very clear indicators of having resolved scaling problems,
as well as metrics for understanding what to upgrade and when.

### Upgrading a Cluster

[production checklist]: /kv/3.4.0/how-to/operate/upgrade-cluster/
[use admin riak control]: /kv/3.4.0/reference/commands/riak-control/
[use admin commands]: /kv/3.4.0/reference/commands/
[use admin riak admin]: /kv/3.4.0/reference/commands/riak/ admin
[usage secondary-indexes]: /kv/3.4.0/how-to/develop/query-secondary-indexes/
[release notes]: https://github.com/basho/riak/blob/master/RELEASE-NOTES.md
[riak enterprise]: http://basho.com/products/riak-kv/
[cluster ops mdc]: /kv/3.4.0/reference/replication-api/runtime-controls/
[config v3 mdc]: /kv/3.4.0/how-to/configure/replication/configure-v3-multi-datacenter/
[jmx monitor]: /kv/3.4.0/reference/operations/jmx/
[snmp]: /kv/3.4.0/reference/operations/snmp/

**Note on upgrading OpenRiak KV from older versions**
OpenRiak KV upgrades are tested and supported for two feature release versions.
For example, upgrades from 1.1.x to 1.3.x are tested and supported,
while upgrades from 1.1.x to 1.4.x are not. When upgrading to a new
version of OpenRiak KV that is more than two feature releases ahead, we
recommend first upgrading to an intermediate version. For example, in an
upgrade from 1.1.x to 1.4.x, we recommend upgrading from 1.1.x to 1.3.x
before upgrading to 1.4.x.

If you run [Riak Control](/kv/3.4.0/reference/commands/riak-control/), you should disable it during the rolling upgrade process.

OpenRiak KV nodes negotiate with each other to determine supported
operating modes. This allows clusters containing mixed-versions of OpenRiak KV
to properly interoperate without special configuration, and simplifies
rolling upgrades.

Before starting the rolling upgrade process on your cluster, check out the [Upgrading OpenRiak KV: Production Checklist][production checklist] page, which covers details and questions to consider while upgrading.

#### Debian/Ubuntu

The following example demonstrates upgrading an OpenRiak KV node that has been
installed with the Debian/Ubuntu packages provided by Basho.

1\. Stop OpenRiak KV:

```bash
riak stop
```

2\. Back up the OpenRiak KV node's `/etc` and `/data` directories:

```bash
sudo tar -czf riak_backup.tar.gz /var/lib/riak /etc/riak
```

3\. Upgrade OpenRiak KV:

```bash
sudo dpkg -i <riak_package_name>.deb
```

4\. Restart OpenRiak KV:

```bash
riak start
```

5\. Verify OpenRiak KV is running the new version:

```bash
riak version
```

6\. Wait for the `riak_kv` service to start:

```bash
riak admin wait-for-service riak_kv »target_node«
```

* `»target_node«` is the node which you have just upgraded (e.g.
`riak@192.168.1.11`)

7\. Wait for any hinted handoff transfers to complete:

```bash
riak admin transfers
```

* While the node was offline, other nodes may have accepted writes on its
behalf. This data is transferred to the node when it becomes available.

8\. Repeat the process for the remaining nodes in the cluster.

#### RHEL/CentOS

The following example demonstrates upgrading an OpenRiak KV node that has been
installed with the RHEL/CentOS packages provided by Basho.

2\. Back up OpenRiak KV's `/etc` and `/data` directories:

```bash
sudo rpm -Uvh <riak_package_name>.rpm
```

5\. Verify that OpenRiak KV is running the new version:

* `»target_node«` is the node which you have just upgraded (e.g.
riak@192.168.1.11)

#### Solaris/OpenSolaris

The following example demonstrates upgrading an OpenRiak KV node that has been
installed with the Solaris/OpenSolaris packages provided by Basho.

**Note:**
If you are using the service management facility (SMF) to manage OpenRiak KV,
you will have to stop OpenRiak KV via `svcadm` instead of using `riak stop`:

```bash
sudo svcadm disable riak
```

```bash
sudo gtar -czf riak_backup.tar.gz /opt/riak/data /opt/riak/etc
```

3\. Uninstall OpenRiak KV:

```bash
sudo pkgrm BASHOriak
```

4\. Install the new version of OpenRiak KV:

```bash
sudo pkgadd -d <riak_package_name>.pkg
```

**Note:**
If you are using the service management facility (SMF) to manage OpenRiak KV,
you will have to start OpenRiak KV via `svcadm` instead of using `riak start`:

```bash
sudo svcadm enable riak
```

`»target_node«` is the node which you have just upgraded (e.g.
`riak@192.168.1.11`)

While the node was offline, other nodes may have accepted writes on its
behalf. This data is transferred to the node when it becomes available.

#### Rolling Upgrade to Enterprise

If you would like to upgrade an existing OpenRiak KV cluster to a commercially
supported [OpenRiak KV Enterprise][riak enterprise] cluster with [multi-datacenter replication][cluster ops mdc], undertake the following steps:

1. Shut down the node you are going to upgrade.
2. Back up your `etc` (app.config and vm.args) and `data`
directories.
3. Uninstall your OpenRiak KV package.
4. Install the `riak_ee` package.
5. A standard package uninstall should not have removed your data
   directories. If it did, move your backup to where the data directory
   should be.
6. Copy any customizations from your backed-up vm.args to the
   `riak_ee` installed vm.args file, these files may be identical.
7. The app.config file from `riak_ee` will be significantly different from your backed-up file. While it will contain all of the same sections as your original, it will have many new ones. Copy the customizations from your original app.config file into the appropriate sections in the new one. Ensure that the following sections are present in app.config:
  * `riak_core` - the `cluster_mgr` setting must be present. See [MDC v3 Configuration][config v3 mdc] for more information.
  * `riak_repl` - See [MDC v3 Configuration][config v3 mdc] for more information.
  * `riak_jmx` - See [JMX Monitoring][jmx monitor] for more information.
  * `snmp` - See [SNMP][snmp] for more information.
8. Start OpenRiak KV on the upgraded node.

#### Basho Patches

After upgrading, you should ensure that any custom patches contained in
the `basho-patches` directory are examined to determine their
application to the upgraded version. If you find that patches no longer
apply to the upgraded version, you should remove them from the
`basho-patches` directory prior to operating the node in production.

The following lists locations of the `basho-patches` directory for
each supported operating system:

- CentOS & RHEL Linux: `/usr/lib64/riak/lib/basho-patches`
- Debian & Ubuntu Linux: `/usr/lib/riak/lib/basho-patches`
- FreeBSD: `/usr/local/lib/riak/lib/basho-patches`
- SmartOS: `/opt/local/lib/riak/lib/basho-patches`
- Solaris 10: `/opt/riak/lib/basho-patches`

#### Riaknostic

It is a good idea to also verify some basic configuration and general
health of the OpenRiak KV node after upgrading by using OpenRiak KV's built-in
diagnostic utility Riaknostic.

Ensure that OpenRiak KV is running on the node, and issue the following
command:

```bash
riak admin diag
```

Make the recommended changes from the command output to ensure optimal
node operation.

### Upgrading Multi-Datacenter

#### TODO

How to update to a new version with multi-datacenter.

#### Upgrading a node

Riak upgrades are all designed to support in-place rolling upgrades across the cluster - a [rolling restart](/kv/3.4.0/how-to/operate/rolling-restart/) with a package deployment between the stop and start.

The following upgrade path has been specifically tested:

`2.2.3` -> `2.2.5` -> `2.9.n` -> `3.0.n` -> `3.2.n` -> `3.4.n`

More direct upgrade paths skipping steps may be possible.  New features are added using either a negotiation of capability within the cluster, or with the feature disabled by default in configuration.  Once a capability is mature, after at least two steps in the path, the negotiation may be retired and replaced with a static assumption of capability.

> When using the eleveldb backend with `snappy` compression (which is the default compression method when eleveldb is used in multi-backend setups), there are potentially multiple broken upgrade paths, even with minor release changes.  The release notes should be checked for issues before progressing with an update, and specific pre-live testing of any upgrade path is essential when using `snappy` compression.

It is not possible via rolling restart to upgrade from an OTP version 22 or prior, to an upgrade with an OTP version of 25 or higher.  For example, direct upgrades from `3.0.n` to `3.4.n` are not supported unless `3.0.n` is built with OTP 22, and `3.4.n` is built with OTP 24.

It is recommended to test all upgrades in pre-production environments.  If no pre-production environment is available, then a pilot node should be upgraded first in the cluster for an agreed time period (e.g. 24 hours).  If there are issues with the upgrade, then the pilot node can be stopped, cleared and [repaired](/kv/3.4.0/how-to/operate/replace-node/).  Most large-scale production users of Riak rely on pre-production testing or pilot nodes to assure changes, and do not depend on a [backup/restore safety net](/kv/3.4.0/explanation/operations/backups-and-restores/) during a rolling upgrade.

If local changes have been made to `riak.conf`, the package manager should leave the `riak.conf` file unchanged during an upgrade.  A release change may alter a default value in configuration, and if that default value was originally added to the `riak.conf` uncommented - the new default will not take effect following the upgrade, as the `riak.conf` is not altered.

> In configuration management of `riak.conf` files, the potential issue of changing defaults needs to be accounted for i.e. ensure the managed version of `riak.conf` is seeded with a new default `riak.conf` file produced for each release, before context-specific changes are applied.

As with other rolling operations, the operations can be accelerated through the use of locations, by changing a location per-cycle not just a node per-cycle.  Awaiting both the triggering and completion of handoffs between cycles is required for a smooth transition.

> [!WARNING]
> Migration review required: Release-specific installation, upgrade, downgrade, or quick-start instructions require verification against OpenRiak KV 3.4.0 packages; Commands or links derived from the 3.2.5 documentation were version-normalized for 3.4.0 and require technical verification; Legacy version text or MDX syntax remains and requires editorial review.

## Verify the result

Compare cluster health and workload behaviour with the recorded starting state, and confirm that all affected nodes have converged.
