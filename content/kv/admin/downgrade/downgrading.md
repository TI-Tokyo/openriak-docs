---
sidebar_position: 3
title: Downgrading OpenRiak
sidebar_label: "Downgrading"
---

## Contents

1.[Introduction](#introduction)
2.[The downgrade process](#2-the-downgrade-process)

## Introduction

Downgrades of OpenRiak KV are generally tested and supported for the most recent LTS version of the operating system supporter and the previous version to that.

Depending on the versions involved in the downgrade, there are additional steps to be performed before, during, and after the upgrade on on each node. These steps are related to changes or new features that are not present in the downgraded version.

## The downgrade process

The following is an example process for downgrading with Ubuntu/Debian based systems. You should adjust and test the commands for your specific OS>

### To-Note - change this to link to FAQ page/reference
While the cluster contains mixed version members, if you have not set the cluster to use the legacy AAE tree format, you will see the `bad_version` error emitted to the log any time nodes with differing versions attempt to exchange AAE data (including AAE fullsync).

This is benign and similar to the `not_built` and `already_locked` errors which can be seen during normal AAE operation. These events will stop once the downgrade is complete.

## Stop OpenRiak KV and make a back up.

1. Stop OpenRiak KV:

```bash
riak stop
```

2. Make a back-up of your OpenRiak KV /etc and /data directories.

```bash
sudo tar -czf riak_backup.tar.gz /var/lib/riak /etc/riak
```

3. Downgrade OpenRiak KV

```bash
sudo dpkg -i »riak_package_name«.deb
```

## Start the node

4. Start OpenRiak KV

```bash
riak start
```

5. Monitor transfers to ensure they complete with:

```bash
riak admin transfers
```
