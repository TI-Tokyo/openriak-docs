---
sidebar_position: 3
title: Upgrading OpenRiak
sidebar_label: "Upgrading"
---

# Contents
1. [Before upgrading](#before-upgrading)
2. [Example upgrade steps for Debian/Ubuntu](#example-upgrade-steps-for-debian/ubuntu)
3. [Example upgrade steps for Oracle Linux](#example-upgrade-steps-for-oracle-linux)

# Before upgrading

Before upgrading you should review the following important notes:

* If you are using OpenRiak Control, you should ensure this is disabled during the rolling upgrade process
* Do not skip the process of backing up your /etc and /data directories, as losing these could be fatal to your node/cluster should something go wrong during the upgrade process.

# Example upgrade steps for Debian/Ubuntu

The following is an example of how to ugprade an OpenRiak KV cluster running on Debian/ubuntu.

1. Stop Riak KV:

```bash
riak stop
```

2. Back up the Riak KV node’s /etc and /data directories:

```bash
sudo tar -czf riak_backup.tar.gz /var/lib/riak /etc/riak
```

3. Upgrade Riak KV:

```bash
sudo dpkg -i <riak_package_name>.deb
```

4. Restart Riak KV:

```bash
riak start
```

5. Verify Riak KV is running the new version:

```bash
riak versions
```

You should see an output that reports your installed version, check that this matches your intended final version such as below:

```bash
# riak versions
Installed versions:
* 3.2.5 permanent
```

6. Wait for the riak_kv service to start:

```bash
riak admin wait-for-service riak_kv »target_node«»target_node« is the node which you have just upgraded (e.g. riak@192.168.1.11)
```

When it is complete, you will see the following output:

```bash
riak_kv is up
```

7. Wait for any hinted handoff transfers to complete:

While the node was offline, other nodes may have accepted writes on its behalf. This data is transferred to the node when it becomes available. We do this with the follow:

```bash
riak admin transfers
```

When transfers have complete, you will see the following output:

```bash
# riak admin transfers

No transfers active

Active Transfers:


ok
```

8. Repeat the process for the remaining nodes in the cluster.

9. If in use, re-enable OpenRiak Control for the cluster once everything is complete.

# Example upgrade steps for Oracle Linux

The following is an example of how to ugprade an OpenRiak KV cluster running on Debian/ubuntu.

1. Stop Riak KV:

```bash
riak stop
```

2. Back up the Riak KV node’s /etc and /data directories:

```bash
sudo tar -czf riak_backup.tar.gz /var/lib/riak /etc/riak
```

3. Upgrade Riak KV:

```bash
sudo dpkg -i <riak_package_name>.deb
```

4. Restart Riak KV:

```bash
riak start
```

5. Verify Riak KV is running the new version:

```bash
riak versions
```

You should see an output that reports your installed version, check that this matches your intended final version such as below:

```bash
# riak versions
Installed versions:
* 3.2.5 permanent
```

6. Wait for the riak_kv service to start:

```bash
riak admin wait-for-service riak_kv »target_node«»target_node« is the node which you have just upgraded (e.g. riak@192.168.1.11)
```

When it is complete, you will see the following output:

```bash
riak_kv is up
```

7. Wait for any hinted handoff transfers to complete:

While the node was offline, other nodes may have accepted writes on its behalf. This data is transferred to the node when it becomes available. We do this with the follow:

```bash
riak admin transfers
```

When transfers have complete, you will see the following output:

```bash
# riak admin transfers

No transfers active

Active Transfers:


ok
```

8. Repeat the process for the remaining nodes in the cluster.

9. If in use, re-enable OpenRiak Control for the cluster once everything is complete.

