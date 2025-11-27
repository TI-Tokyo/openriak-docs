---
title: Ring Changes
sidebar_label: "Ring Changes"
---

# Overview

This page covers the variety of methods for performing ring changes within an OpenRiak cluster, whether that be adding a node, removing a node or replacing nodes.

# Adding a node

Adding a node to your cluster is a relatively simple process, assuming this is a brand new node you are adding. Once you've set your nodename and made any other changes to your `riak.conf` that you need to make, follow these steps:

1. On the node you wish to add to the cluster run:

```bash
riak admin cluster join riak@192.168.1.11 riak@192.168.1.10
```

2. Check that the node has been staged to join the cluster with:

```bash
riak admin cluster plan
```
You can use this method to stage multiple nodes to join a single cluster at once.
You will see an output similar to below:

```bash
=============================== Staged Changes ================================
Action         Details(s)
-------------------------------------------------------------------------------
join           'riak@192.168.1.11'
join           'riak@192.168.1.12'
join           'riak@192.168.1.13'
join           'riak@192.168.1.14'
-------------------------------------------------------------------------------


NOTE: Applying these changes will result in 1 cluster transition

###############################################################################
                         After cluster transition 1/1
###############################################################################

================================= Membership ==================================
Status     Ring    Pending    Node
-------------------------------------------------------------------------------
valid     100.0%     20.3%    'riak@192.168.1.10'
valid       0.0%     20.3%    'riak@192.168.1.11'
valid       0.0%     20.3%    'riak@192.168.1.12'
valid       0.0%     20.3%    'riak@192.168.1.13'
valid       0.0%     18.8%    'riak@192.168.1.14'
-------------------------------------------------------------------------------
Valid:5 / Leaving:0 / Exiting:0 / Joining:0 / Down:0
```

You can see from the above output that after the staged changes are committed the ring will rebalance around the new member.

3. If the changes look correct to you (i.e. the node is joining the correct cluster) then you will need to commit the changes:

```bash
riak admin cluster commit
```

Which produces the following output:

```bash
Cluster changes committed
```

4. You can then monitor the process of the node(s) joining with `riak admin transfers`.

# Removing a node

Removing a node from a cluster is a relatively simple process if your cluster is in a healthy state. If your cluster is not in a healthy state, further investigation should be done before removing a node to ensure you do not overload the remaining nodes.

To remove a node from a cluster:

1. Assuming your cluster is healthy and able to sustain a node leave request, run the following command:

```bash
riak admin cluster leave
```

You will see an output similar to below:

```bash
Success: staged leave request for 'riak@192.168.1.11'
ok
```

2. Check the resulting output of cluster plan: 

```bash
riak admin cluster plan
```

Expected output of a 2 node cluster:

```bash
=============================== Staged Changes ================================
Action         Details(s)
-------------------------------------------------------------------------------
leave          'riak@192.168.1.11'
-------------------------------------------------------------------------------


NOTE: Applying these changes will result in 2 cluster transitions

###############################################################################
                         After cluster transition 1/2
###############################################################################

================================= Membership ==================================
Status     Ring    Pending    Node
-------------------------------------------------------------------------------
leaving    50.0%      0.0%    riak@192.168.1.10
valid      50.0%    100.0%    riak@192.168.1.11
-------------------------------------------------------------------------------
Valid:1 / Leaving:1 / Exiting:0 / Joining:0 / Down:0

WARNING: Not all replicas will be on distinct nodes

Transfers resulting from cluster changes: 32
  32 transfers from 'riak@172.17.0.3' to 'riak@172.17.0.2'

###############################################################################
                         After cluster transition 2/2
###############################################################################

================================= Membership ==================================
Status     Ring    Pending    Node
-------------------------------------------------------------------------------
valid     100.0%      --      riak@192.168.1.11
-------------------------------------------------------------------------------
Valid:1 / Leaving:0 / Exiting:0 / Joining:0 / Down:0

WARNING: Not all replicas will be on distinct nodes

ok
```

3. If the plan looks correct, commit the plan:

```bash
riak admin cluster commit
```

With an expected output of:

```bash
Cluster changes committed
ok
```

4. Monitor transfers until complete with:

```bash
riak admin transfers
```

This should complete the node leave process.

# Replacing a node

Replacing a node is a similar process to adding a node to your cluster, except that it has an extra step.

1. First we need to backup the data directory on the node being replaced:

```bash
sudo tar -czf riak_backup.tar.gz /var/lib/riak /etc/riak
```

If you run into problems while replacing the node, you can restore the data for the node from this.

2. Follow the steps above for creating and setting up a new node.

3. Start the new node

```bash
riak start
```

4. Plan the join of the new node to the existing cluster. 

```bash
riak admin cluster join riak@192.168.1.10
```

5. Plan the replacement of the existing node with the new node:

```bash
riak admin cluster replace riak@192.168.1.11 riak@192.168.1.12
```

6. Check the changes with `riak admin cluster plan`:

```bash
=============================== Staged Changes ================================
Action         Details(s)
-------------------------------------------------------------------------------
replace        'riak@192.168.1.11' with 'riak@192.168.1.12'
join           'riak@192.168.1.10'
-------------------------------------------------------------------------------


NOTE: Applying these changes will result in 2 cluster transitions

###############################################################################
                         After cluster transition 1/2
###############################################################################

================================= Membership ==================================
Status     Ring    Pending    Node
-------------------------------------------------------------------------------
leaving    50.0%      0.0%    riak@192.168.1.10
valid      50.0%     50.0%    riak@192.168.1.11
valid       0.0%     50.0%    riak@192.168.1.12
-------------------------------------------------------------------------------
Valid:2 / Leaving:1 / Exiting:0 / Joining:0 / Down:0

WARNING: Not all replicas will be on distinct nodes

Transfers resulting from cluster changes: 32
  32 transfers from 'riak@192.168.1.11' to 'riak@192.168.1.12'

###############################################################################
                         After cluster transition 2/2
###############################################################################

================================= Membership ==================================
Status     Ring    Pending    Node
-------------------------------------------------------------------------------
valid      50.0%      --      riak@192.168.1.10
valid      50.0%      --      riak@192.168.1.12
-------------------------------------------------------------------------------
Valid:2 / Leaving:0 / Exiting:0 / Joining:0 / Down:0

WARNING: Not all replicas will be on distinct nodes

ok
```

---
**Note**
You will notice that compared to a normal node join operation, there is an extra step where all 3 nodes are present. This is a temporary step while the data of the exiting node is transfered to the replacement one.
---

7. Assuming everything looks correct, commit the plan:

```bash
riak admin cluster commit
```

You should see the following:

```bash 
Cluster changes committed
ok
```

8. If the plan does not look correct, you can clear it with the following command and start again:

```bash
riak admin cluster clear
```

---
**Note on Ring Settling**

You’ll need to make sure that no other ring changes occur between the time when you start the new node and the ring settles with the new IP info.

The ring is considered settled when the new node reports `true` when you run the `riak admin ringready` command.
---

