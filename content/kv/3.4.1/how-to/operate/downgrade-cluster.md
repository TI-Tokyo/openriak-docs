---
title: 'Downgrade an OpenRiak cluster'
description: 'Show operators how to downgrade an openriak cluster with prechecks, verification, and recovery guidance.'
weight: 7
diataxis: 'how-to'
product: 'OpenRiak KV'
product_version: '3.4.1'
status: 'editorially-rewritten'
draft: true
audience:
  - 'operators'
source_material:
  - 'legacy-3.2.5'
  - 'live-3.2.5'
  - 'proposed-kv'
migration_source_root: '\\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv'
migration_sources:
  - '\\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv\admin\downgrade\downgrading.md'
migration_review:
  - 'Release-specific installation, upgrade, downgrade, or quick-start instructions require verification against OpenRiak KV 3.4.1 packages.'
legacy_3_2_5_sources:
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\setup\downgrade.md'
  - 'Package, platform, installation, upgrade, or downgrade details require release-specific verification for OpenRiak KV 3.4.1.'
tags: ['diataxis', 'kv', 'how-to']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Show operators how to downgrade an openriak cluster with prechecks, verification, and recovery guidance.

## Before you begin

A healthy cluster, current backups, and access to cluster status and logs. Record the starting state before making an operational change.

## Overview

### Downgrading

[rolling upgrade]: /kv/3.4.1/how-to/operate/upgrade-cluster/
[config ref]: /kv/3.4.1/reference/configuration/
[concept aae]: /kv/3.4.1/explanation/replication/active-anti-entropy/
[aae status]: /kv/3.4.1/reference/commands/riak-admin/#aae-status

Downgrades of OpenRiak KV are tested and supported for two feature release versions, with the general procedure being similar to that of a [rolling upgrade][rolling upgrade].

Depending on the versions involved in the downgrade, there are additional steps to be performed before, during, and after the upgrade on on each node. These steps are related to changes or new features that are not present in the downgraded version.

#### Overview

For every node in the cluster:

1. Stop OpenRiak KV.
2. Back up OpenRiak's `etc` and `data` directories.
3. Downgrade the OpenRiak KV.
6. Start OpenRiak KV.
7. Monitor the reindex of the data.
8. Finalize process and restart OpenRiak KV.

##### Guidelines

* Riak control should be disabled throughout the rolling downgrade process.
* [Configuration Files][config ref] must be replaced with those of the version being downgraded to.

##### Components That Complicate Downgrades

| Feature | automatic | required | Notes |
|:---|:---:|:---:|:---|
| Active Anti-Entropy file format changes | ✔ |  | Can be opted out using a [capability](/kv/3.4.1/how-to/operate/downgrade-cluster/)

##### When Downgrading is No Longer an Option

If you enabled LZ4 compression in LevelDB and/or enabled global expiration in LevelDB when you installed KV 3.2.5, you cannot downgrade.

#### General Process

**Note:**
While the cluster contains mixed version members, if you have not set the cluster to use the legacy AAE tree format, you will see the `bad_version` error emitted to the log any time nodes with differing versions attempt to exchange AAE data (including AAE fullsync).

This is benign and similar to the `not_built` and `already_locked` errors which can be seen during normal AAE operation. These events will stop once the downgrade is complete.

##### Stop OpenRiak KV

1\. Stop OpenRiak KV:

```bash
riak stop
```
2\. Back up your OpenRiak KV /etc and /data directories:

```bash
sudo tar -czf riak_backup.tar.gz /var/lib/riak /etc/riak
```

3\. Downgrade OpenRiak KV:

```RHEL/CentOS
sudo rpm -Uvh »riak_package_name«.rpm
```

```Ubuntu
sudo dpkg -i »riak_package_name«.deb
```

##### Start the node

4\. Start OpenRiak KV:

```bash
riak start
```

##### Monitor the reindex of the data

5\. Monitor the build and exchange progress using the `riak admin aae-status` command.

The **All** column shows how long it has been since a partition exchanged with all of its sibling replicas.  Consult the [`riak admin aae-status` documentation][aae status] for more information about the AAE status output.

Once the `riak admin aae-status` shows values in the **All** column, the node will have successfully rebuilt all of the indexed data.

##### Finalize process

6\. If you raised the concurrency AAE currency settings in riak.conf during **Step 5**, stop the node and remove the increased AAE thresholds.

7\. Verify that transfers have completed:

```bash
riak admin transfers
```

> [!WARNING]
> Migration review required: Release-specific installation, upgrade, downgrade, or quick-start instructions require verification against OpenRiak KV 3.4.1 packages.

## Verify the result

Compare cluster health and workload behaviour with the recorded starting state, and confirm that all affected nodes have converged.
