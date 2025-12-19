---
title: Ring Changes
sidebar_label: "Ring Changes"
---

[root site]: [!site]
[root project]: [!project]
[root version]: [!version]

[example values]: #values-used-in-these-examples
[node add]: #adding-a-node
[node remove]: #removing-a-node
[node replace]: #replacing-a-node
[node naming]: [!version]configure/basics#nodename
[node restore]: [!version]admin/recovery/replace-a-node
[config reference]: [!version]configure/reference
[partition transfers]: #monitor-transfers

# Ring Changes 

## Overview

This page covers the variety of methods for performing ring changes within an OpenRiak cluster, whether that be [adding a node][node add], [removing a node][node remove] or [replacing nodes][node replace].

> [!INFO]
> Applications can continue using the cluster as normal while these operations are occuring.

> [!Tip] Values used in these examples
> Read about the [values used in these examples][example values].

## Adding a new node

> [!CODE] `riak admin cluster` commands
>
> ```bash
> riak admin cluster join <nodename>
> riak admin cluster plan
> riak admin cluster commit
> ```

Adding new nodes to your cluster is a relatively simple process. 

> [!WARNING]- What if this is not a new node?
>
> If your node has existing data, then that data will not be accessible after it has joined the cluster and the data may be lost.
>
> Do not join a node with pre-existing data to a cluster unless you are performing a [restore from backup][node restore].

1. Copy over the [config files][config reference] from an existing node in the cluster.

   The exact mechanism for doing this will depend on your environment. We assume from this point on that your config files are identical to an existing node's config files.

2. On the new node, update the config files

   It is essential to change:
     - `nodename` to reflect the IPv4, IPv6 or FQDN of the new node
     - the `listener` group of settings
   
   Optional changes include:
    - data storage paths if these are different to your existing nodes
   
   Never change `ring_size` as that has to be consistant on all nodes in your cluster.
   
3. On the new node, tell it to ask to join a cluster using an existing node (in this case `riak@10.0.20.1`):

  ```bash
  riak admin cluster join riak@10.0.20.1
  ```

  The correct response will be similar to this:

  ```bash
  Success: staged join request for 'riak@10.0.20.4' to 'riak@10.0.20.1'
  ```

  The node has not yet joined the existing cluster, but it has requested to join the cluster. The node is said to be "staged" to join the cluster.

4. Repeat steps 1-3 on all the new nodes you wish to ask to join to the cluster.

5. On any node, existing or staged, tell the cluster to create a plan to actually add the new nodes:
   
    ```bash
    riak admin cluster plan
    ```
    
    You can run this after joining each new node, or once after you have joined them all.
   
    You will see an output similar to below:

    ```bash
    =============================== Staged Changes ================================
    Action         Details(s)
    -------------------------------------------------------------------------------
    join           'riak@10.0.20.4'
    join           'riak@10.0.20.5'
    join           'riak@10.0.20.6'
    -------------------------------------------------------------------------------


    NOTE: Applying these changes will result in 1 cluster transition

    ###############################################################################
                            After cluster transition 1/1
    ###############################################################################

    ================================= Membership ==================================
    Status     Ring    Pending    Node
    -------------------------------------------------------------------------------
    valid      33.4%     16.7%    'riak@10.0.20.1'
    valid      33.3%     16.7%    'riak@10.0.20.2'
    valid      33.3%     16.6%    'riak@10.0.20.3'
    valid       0.0%     16.7%    'riak@10.0.20.4'
    valid       0.0%     16.7%    'riak@10.0.20.5'
    valid       0.0%     16.6%    'riak@10.0.20.6'
    -------------------------------------------------------------------------------
    Valid:6 / Leaving:0 / Exiting:0 / Joining:0 / Down:0
    ```

    The above output shows that after the staged changes are committed the ring will rebalance around the new nodes (aka the new cluster members) and each node will now be responsible for an equal share of data.

    If there are any expected new nodes that are not listed, go back and check steps 1-3 on that node and re-run this step.

6. On any node, existing or staged, tell the cluster to actually add the new nodes:

    ```bash
    riak admin cluster commit
    ```

    Which produces the following output:

    ```bash
    Cluster changes committed
    ```

    The nodes will be now be considered part of the cluster, however the cluster's data will not yet be spread over the new nodes. This will happen automatically, but you should wait until it is finished before performing any further significant admin actions.

7. Monitor the process of rebalancing the cluster's data `riak admin transfers` as detailed [here][partition transfers].

## Removing a node

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

## Replacing a node

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

>[!NOTE]
>You will notice that compared to a normal node join operation, there is an extra step where all 3 nodes are present. This is a temporary step while the data of the exiting node is transfered to the replacement one.
>

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

>[!NOTE] Note on ring settings
>You’ll need to make sure that no other ring changes occur between the time when you start the new node and the ring settles with the new IP info.
>
>The ring is considered settled when the new node reports `true` when you run the `riak admin ringready` command.

## Values used in these examples

> [!NOTE]
> The examples use IPv4 node names. You can also use IPv6 and Fully Qualified Domain Name (FQDN) node names.
>
> For more information about node naming conventions, please check out the [node name][node naming] section.

### Existing nodes

  This is a node which is already part of the OpenRiak cluster. A new node can use any of these existing nodes to join a cluster.

  | Node ID | Type of name   | Example          |
  |:--------|:---------------|:-----------------|
  | 1       | IPv4 address   | `riak@10.0.20.1` | 
  | 2       | IPv4 address   | `riak@10.0.20.2` | 
  | 3       | IPv4 address   | `riak@10.0.20.3` | 

### New nodes

  These are nodes which have not joined an OpenRiak cluster yet.

  | Node ID | Type of name   | Example          |
  |:--------|:---------------|:-----------------|
  | 4       | IPv4 address   | `riak@10.0.20.4` | 
  | 5       | IPv4 address   | `riak@10.0.20.5` | 
  | 6       | IPv4 address   | `riak@10.0.20.6` | 

