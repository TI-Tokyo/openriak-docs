---
title: 'Back up an OpenRiak node'
description: 'Show operators how to back up an openriak node with prechecks, verification, and recovery guidance.'
weight: 3
diataxis: 'how-to'
product: 'OpenRiak KV'
product_version: '3.4.0'
status: 'editorially-rewritten'
draft: true
audience:
  - 'operators'
legacy_3_2_5_sources:
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\using\cluster-operations\backing-up.md'
source_material:
  - 'legacy-3.2.5'
  - 'live-3.2.5'
  - 'proposed-kv'
  - 'openriak-quickdocs-3.4'
quickdocs_sources:
  - 'https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#backup---ring-folder-and-cluster-metadata'
  - 'https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#backup---the-preferred-building-block'
  - 'https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#backup-options'
  - 'https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#bitcask---backups'
  - 'https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#leveled---hot-backups'
tags: ['diataxis', 'kv', 'how-to']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Show operators how to back up an openriak node with prechecks, verification, and recovery guidance.

## Before you begin

A healthy cluster, current backups, and access to cluster status and logs. Record the starting state before making an operational change.

## Overview

### Backing Up

[concept clusters]: {{< baseurl >}}kv/3.4.0/explanation/foundations/clusters-rings-and-partitions/
[config reference]: {{< baseurl >}}kv/3.4.0/reference/configuration/
[plan backend leveldb]: {{< baseurl >}}kv/3.4.0/explanation/storage/leveldb/
[plan backend bitcask]: {{< baseurl >}}kv/3.4.0/explanation/storage/bitcask/
[use ref strong consistency]: {{< baseurl >}}kv/3.4.0/reference/specialized-apis/strong-consistency-api/
[concept aae]: {{< baseurl >}}kv/3.4.0/explanation/replication/active-anti-entropy/
[aae read repair]: {{< baseurl >}}kv/3.4.0/explanation/replication/active-anti-entropy/#read-repair-vs-active-anti-entropy

OpenRiak KV is a [clustered][concept clusters] system built to survive a wide range of failure scenarios, including the loss of nodes due to network or hardware failure. Although this is one of OpenRiak KV's core strengths, it cannot withstand all failure scenarios.

Backing up data (duplicating the database on a different long-term storage system) is a common approach to mitigating potential failure scenarios.

This page covers how to perform backups of OpenRiak KV data.

#### Overview

OpenRiak KV backups can be performed using operating system features or filesystems that support snapshots, such as LVM or ZFS, or by using tools like rsync or tar.

Choosing your OpenRiak KV backup strategy will depend on your already-established backup methodologies and the backend configuration of your nodes.

The basic process for getting a backup of OpenRiak KV from a node is as follows:

1. Stop OpenRiak KV with `riak stop`.
2. Backup the appropriate data, ring, and configuration directories.
3. Start OpenRiak KV.

Downtime of a node can be significantly reduced by using an OS feature or filesystem that supports snapshotting.

**Backups and eventual consistency**
Due to OpenRiak KV's eventually consistent nature, backups can become slightly inconsistent from node to node.

Data could exist on some nodes and not others at the exact time a backup is made. Any inconsistency will be corrected once a backup is restored, either by OpenRiak's [active anti-entropy]({{< baseurl >}}kv/3.4.0/explanation/replication/active-anti-entropy/) processes or when the object is read, via [read repair]({{< baseurl >}}kv/3.4.0/explanation/replication/active-anti-entropy/#read-repair-vs-active-anti-entropy).

#### OS-Specific Directory Locations

The default OpenRiak KV data, ring, and configuration directories for each of the supported operating systems is as follows:

##### Debian and Ubuntu

Data | Directory
:----|:---------
Bitcask | `/var/lib/riak/bitcask`
LevelDB | `/var/lib/riak/leveldb`
Ring | `/var/lib/riak/ring`
Configuration | `/etc/riak`
Cluster Metadata | `/var/lib/riak/cluster_meta`
Strong consistency | `/var/lib/riak/ensembles`

###### Fedora and RHEL

###### FreeBSD

Data | Directory
:----|:---------
Bitcask | `/var/db/riak/bitcask`
LevelDB | `/var/db/riak/leveldb`
Ring | `/var/db/riak/ring`
Configuration | `/usr/local/etc/riak`
Cluster Metadata | `/var/db/riak/cluster_meta`
Strong consistency | `/var/db/riak/ensembles`

###### OS X

Data | Directory
:----|:---------
Bitcask | `./data/bitcask`
LevelDB | `./data/leveldb`
Ring | `./data/riak/ring`
Configuration | `./etc`
Cluster Metadata | `./data/riak/cluster_meta`
Strong consistency | `./data/ensembles`

**Note**: OS X paths are relative to the directory in which the package
was extracted.

###### SmartOS

Data | Directory
:----|:---------
Bitcask | `/var/db/riak/bitcask`
LevelDB | `/var/db/riak/leveldb`
Ring | `/var/db/riak/ring`
Configuration | `/opt/local/etc/riak`
Cluster Metadata | `/var/db/riak/cluster_meta`
Strong consistency | `/var/db/riak/ensembles`

###### Solaris

Data | Directory
:----|:---------
Bitcask | `/opt/riak/data/bitcask`
LevelDB | `/opt/riak/data/leveldb`
Ring | `/opt/riak/ring`
Configuration | `/opt/riak/etc`
Cluster Metadata | `/opt/riak/cluster_meta`
Strong consistency | `/opt/riak/data/ensembles`

#### Performing Backups

**Deprecation notice**
In previous versions of OpenRiak KV, there was a [`riak admin backup`]({{< baseurl >}}kv/3.4.0/reference/commands/riak-admin/#backup) command commonly used for
backups. This functionality is now deprecated. We strongly recommend using the backup procedure documented below instead.

Backups can be accomplished through a variety of common methods. Standard utilities such `cp`, `rsync`, and `tar` can be used, as well as any backup system already in place in your environment.

A simple shell command, like those in the following examples, are sufficient for creating a backup of your Bitcask or LevelDB data, ring, and OpenRiak KV configuration directories for a binary package-based OpenRiak KV Linux
installation.

The following examples use `tar`:

**Note:**
Backups must be performed on while OpenRiak KV is stopped to prevent data loss.

##### Bitcask

```bash
tar -czf /mnt/riak_backups/riak_data_`date +%Y%m%d_%H%M`.tar.gz \
  /var/lib/riak/bitcask /var/lib/riak/ring /etc/riak
```

##### LevelDB

```bash
tar -czf /mnt/riak_backups/riak_data_`date +%Y%m%d_%H%M`.tar.gz \
  /var/lib/riak/leveldb /var/lib/riak/ring /etc/riak
```

##### Cluster Metadata

```bash
tar -czf /mnt/riak_backups/riak_data_`date +%Y%m%d_%H%M`.tar.gz \
  /var/lib/riak/cluster_meta
```

##### Strong Consistency Data

Persistently stored data used by OpenRiak's [strong consistency][use ref strong consistency] feature
can be stored in an analogous fashion:

```bash
tar -czf /mnt/riak_backups/riak_data_`date +%Y%m%d_%H%M`.tar.gz \
  /var/lib/riak/ensembles
```

#### Restoring a Node

The method you use to restore a node will differ depending on a combination of factors, including node name changes and your network environment.

If you are replacing a node with a new node that has the same node name (typically a fully qualified domain name or IP address), then restoring the node is a simple process:

1. Install Riak on the new node.
2. Restore your old node's configuration files, data directory, and ring
   directory.
3. Start the node and verify proper operation with `riak ping`,
   `riak admin status`, and other methods you use to check node health.

If the node name of a restored node (`-name` argument in `vm.args` or
`nodename` parameter in `riak.conf`) is different than the name of the
node that the restored backup was taken from, you will need to
additionally:

1. Mark the original instance down in the cluster using
   [`riak admin down <node>`]({{< baseurl >}}kv/3.4.0/reference/commands/riak-admin/#down)
2. Join the restored node to the cluster using
   [`riak admin cluster join <node>`]({{< baseurl >}}kv/3.4.0/reference/commands/riak-admin/)
3. Replace the original instance with the renamed instance with
   [`riak admin cluster force-replace <node1> <node2>`]({{< baseurl >}}kv/3.4.0/reference/commands/riak-admin/)
4. Plan the changes to the cluster with `riak admin cluster plan`
5. Finally, commit the cluster changes with `riak admin cluster commit`

**Note:**
For more information on the `riak admin cluster` commands, refer to our documentation on [cluster administration]({{< baseurl >}}kv/3.4.0/reference/commands/).

For example, if there are five nodes in the cluster with the original node names `riak1.example.com` through `riak5.example.com` and you wish to restore `riak1.example.com` as `riak6.example.com`, you would execute the following commands on `riak6.example.com`.

1. Join to any existing cluster node.

```bash
    riak admin cluster join riak@riak2.example.com
    ```

2. Mark the old instance down.

```bash
    riak admin down riak@riak1.example.com
    ```

3. Force-replace the original instance with the new one.

```bash
    riak admin cluster force-replace \
        riak@riak1.example.com riak@riak6.example.com
    ```

4. Display and review the cluster change plan.

```bash
    riak admin cluster plan
    ```

5. Commit the changes to the cluster.

```bash
    riak admin cluster commit
    ```

Your [configuration files][config reference] should also be changed to match the new name in addition to running the commands (the `-name` setting in `vm.args` in the older config system, and the `nodename` setting in `riak.conf` in the newer system).

If the IP address of any node has changed, verify that the changes are reflected in your configuration files to ensure that the HTTP and Protocol Buffers interfaces are binding to the correct addresses.

A robust DNS configuration can simplify the restore process if the IP addresses of the nodes change, but the hostnames are used for the node names and the hostnames stay the same. Additionally, if the HTTP and Protocol Buffers interface settings are configured to bind to all IP interfaces (0.0.0.0), then no changes will need to be made to your configuration files.

When performing restore operations involving `riak admin cluster force-replace`, we recommend that you start only one node at a time and verify that each node that is started has the correct name for itself
and for any other nodes whose names have changed:

1. Verify that the correct name is present your configuration file.
2. Once the node is started, run `riak attach` to connect to the node. The prompt obtained should contain the correct node name.
    - (It may be necessary to enter an Erlang atom by       typing `x.` and pressing Enter)
3. Disconnect from the attached session with **Ctrl-G + q**.
4. Finally, run `riak admin member_status` to list all of the nodes and verify that all nodes listed have the correct names.

#### Restoring a Cluster

Restoring a cluster from backups is documented [on its own page]({{< baseurl >}}kv/3.4.0/how-to/troubleshoot/recover-cluster-failure/#cluster-recovery-from-backups).

#### Backup options

Before considering backups, it is worth noting that as a distributed database there is no single commit position that represents a point of truth.  Therefore there is no way to effectively backup at a point, and restore to a point.  The overall state is eventually consistent.

- Riak is designed to operate as a resilient cluster, and also as a broader system of resilience from having multiple clusters that both replicate between each other and have continuous reconciliation to ensure they are in-sync.
- Major changes to the database will often occur in the application, not the database.  The application is in control of the data schema, and hence the migration of objects between schema versions.
- Self-healing is used to handle repair scenarios - i.e. recovering data from peers within the cluster, and the system is designed to perform predictably during the healing process.

Production users of Riak commonly have relatively lightweight backup and recovery strategies when compared to traditional database management systems; eventual consistency allows the global recovery of state without the need to focus on recovering state first back to a point in time.  In general, greater effort is placed into building the resilience of the system, and also the management of change within the application i.e. ensuring the application adopts lazy migration strategies for schema changes that don't require large point-in-time migration events.

If an individual node fails, do not restore an individual node from backup.  It is generally much more efficient and reliable to use [the `repair` process]({{< baseurl >}}kv/3.4.0/how-to/operate/replace-node/) to recover data on a node.  It is not normal practice to keep backups simply for the purpose of restoring individual nodes, even where those nodes may rely on ephemeral disks.

Note that in cloud environments, if an inefficient backup method is chosen (e.g. snapshots of block-service file-system volumes), then backup costs may consume a dominant proportion of overall Riak infrastructure costs.

#### Backup - the preferred building block

As part of the replication approach of Riak it is possible to replicate, and reconcile between clusters with different `n_val`s, different node counts, different vnode counts (i.e. ring sizes) and different storage backends.  It is common in Riak production systems to maintain a single-node, `n_val=1` cluster, with a potentially lower ring size, that represents a backup; where that cluster may be in a diverse geographical location to the primary production clusters.

Having a backup cluster may be considered as a backup in itself, or as a staging post from which to take further backups.

The real-time replication process that keeps the backup in-sync uses a queue on the source cluster, and that queue will grow (as small on-disk references to changes) should the sink (i.e. the backup cluster) pause consumption.  After resuming replication, the sink cluster will catch-up on the missing changes from the queue, and when reconciliation is re-enabled that catch-up can be confirmed.  There is flexibility to disconnect a backup cluster, hold it at a point in time, and then in the future reconnect and fast-forward to the current state, then prove that the fast-forward was successful - with automatic resolution of any unexpected deltas.

Backup clusters are not a prerequisite for taking backups, but they can be a flexible and efficient starting point; and in some cases act as an alternative.

#### Leveled - hot backups

If a cluster uses only the leveled backend, a hot backup may be taken across the cluster using the `riak_client:hotbackup/4` function from [the `remote_console`]({{< baseurl >}}kv/3.4.0/how-to/operate/use-remote-console/) on any node within the cluster.

There are four inputs to the function required:

- A backup path; all nodes will be required to support the same path, the path cannot be to the current folder in which leveled is running, but the path must be on the same volume as the current data path (e.g. you could use `<PLATFORM_DATA_DIR>/backup` as a backup to `<PLATFORM_DATA_DIR>/leveled`).
- The `n_val` of the cluster.
- The coverage plan `n_val` of the cluster; to prompt a backup on all vnodes concurrently these two results should match.  It is possible to backup only one copy of the data i.e. by setting the `n_val` to 3 and the coverage `n_val` to 1. It is, though, easier to understand and reason about the result of the backup if the cluster uses the same `n_val` for all buckets, and the coverage plan `n_val` is set to that `n_val`.
- A client; e.g. a `C` where `{ok, C} = riak:local_client()`.

The backup at each vnode backend will first:

- roll the active journal file, and start a new empty active journal file, so that the Journal of the leveled store is now an entirely immutable set of files;
- take a snapshot of the store, and return it to the controlling process (so that the vnode is free to continue its work).  This snapshot process is an extremely fast in-memory process that spawns a new snapshot "Inker" (the managing process for the Journal), which has the same knowledge of the current Inker of the file structure of the Journal.

The actual backup is then called on the snapshot:

- It will write the Journal manifest (the data structure that defines the list of file references that represents the Journal) to the backup path;
- It will then for each file within that Journal manifest write a hard-link to a new file in the backup path;
- The snapshot will then close, and any pending changes held in the active Journal because of the snapshot will be released.

It is important to note that there will be minimal impact on the disk footprint within the volume from taking the backup.  The hard-link only requires the backup partition to grow when the files are mutated - but the journal files are not mutated, they are immutable.

Because the active journal file was "rolled" at the start of the process, new writes to the database will go into a new active journal that is not linked to the backup directory.  It is only when journal compaction is run, that there may be a disk-space impact from the existence of the backup.  If journal compaction compacts a set of files it will re-write a new set of files (that are not linked to the backup), and then delete the old files.  If a backup link still exists for those deleted files, the space will now not be reclaimed due to those hard links.

The best practice for copying the hot backup to an alternative location, should that be required, is not defined.  There are example solutions, such as [the S3 sync](https://github.com/OpenRiak/leveled-hotbackup-s3-sync) project which may provide a potential approach.  The S3 sync project is particularly interesting, as before copying the Journal files to S3 it creates "hints" files so that it is possible to read individual objects in the back using S3 commands - without requiring the backup to be restored.  Other standard solutions may be used (e.g. `rsync` to offline the backup).

#### Bitcask - backups

There is no Riak-managed solution for backing up bitcask backends.  Note though, that other than for bitcask merge each backend consists of immutable files and a single active, append-only file.

The tested mechanism for backing up a bitcask store, requires the node to be stopped for the backup to be taken.

#### Backup - ring folder, and cluster metadata

As well as the storage backend data folder, a Riak node also stores data in a ring folder, and in a cluster metadata folder - with both found in the `platform_data_dir` with a standard configuration.  Backing up these folders is critical to the recovery should all nodes in the cluster be lost.  They are required for the cluster to understand the distribution of data.  The restored data alone, without this metadata, will be inaccessible.

## Verify the result

Compare cluster health and workload behaviour with the recorded starting state, and confirm that all affected nodes have converged.
