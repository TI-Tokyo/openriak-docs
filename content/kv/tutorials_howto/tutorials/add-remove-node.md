---
sidebar_position: 1
title: Adding or Removing a node
sidebar_label: "add or remove node"
date: 2026-06-02
---
[root site]: [!site]
[root project]: [!project]
[root version]: [!version]
[assumptions]: #assumptions
[joinanode]: #joining-a-node-to-an-existing-cluster
[joinmultiple]: #joining-multiple-nodes-together-into-a-cluster
[removeanode]: #removing-a-node-from-a-cluster


>[!MEMO] Introduction
>This tutorial is intended to teach you how to add or remove a node from a cluster, or to join a group of nodes together at once.

## Assumptions

This guide assumes the following:

1. That your nodes are running on one of the supported operating systems
2. That your nodes are running a version of OpenRiak that is at least V3.0 or higher.
3. That the node(s) you want to join together are not currently in a cluster.
4. That all nodes are in good health

## Cluster Architecture

This section is for reference only, as this should make no difference to the overall steps for enabled TicTac Active Anti-Entropy.

The following section will show the intended structure of each cluster and the names/addresses that each node will use for this tutorial. You should change these nodenames to ones that are suitable for your environment.

### Nodes intended to be joined

|-------------------|--------------|
| Node designation  | IP Address   |
| ------------------|--------------|
|       riak1a      | 192.168.0.20 |
|       riak2a      | 192.168.0.21 |
|       riak3a      | 192.168.0.22 |
|       riak4a      | 192.168.0.23 |
|       riak5a      | 192.168.0.24 |
| ------------------|--------------|

>[!NOTE] Note on joining nodes together
>For clarity, we will be showing two examples for joining nodes to a cluster.
>The first example will show joining one node to an existing cluster. The second example will show joining five nodes together into one cluster.

## Joining a node to an existing cluster

This section will show you how to connect an existing or new node, to a cluster.

1. Prepare the new node, ensuring that the contents of `riak.conf` file are configured correctly and, where needed, identical to the other nodes in the cluster you are intending to join the node to.

2. On the node you are joining to the cluster, run the following command, replacing the node names with the ones for your nodes:

    ```bash
        riak admin cluster join riak@192.168.0.21
    ```

This will produce the following output:

    ```bash
        Success: staged join request for 'riak@192.168.0.20' to 'riak@192.168.0.21'
        ok
    ```

3. Assuming the previous steps have worked correctly, you need to check the cluster plan:

    ```bash
        riak admin cluster plan
    ```

You will see a similar output to below:

    ```bash
        =============================== Staged Changes ================================
        Action         Details(s)
        -------------------------------------------------------------------------------
        join           'riak@192.168.56.20'
        -------------------------------------------------------------------------------


        NOTE: Applying these changes will result in 1 cluster transition

        ###############################################################################
                                 After cluster transition 1/1
        ###############################################################################

        ================================= Membership ==================================
        Status     Ring    Pending    Node
        -------------------------------------------------------------------------------
        valid       0.0%     18.8%    riak@192.168.56.20
        valid      25.0%     20.3%    riak@192.168.56.21
        valid      25.0%     20.3%    riak@192.168.56.22
        valid      25.0%     20.3%    riak@192.168.56.23
        valid      25.0%     20.3%    riak@192.168.56.24
        -------------------------------------------------------------------------------
        Valid:5 / Leaving:0 / Exiting:0 / Joining:0 / Down:0

        Transfers resulting from cluster changes: 12
        3 transfers from 'riak@192.168.56.21' to 'riak@192.168.56.20'
        3 transfers from 'riak@192.168.56.22' to 'riak@192.168.56.20'
        3 transfers from 'riak@192.168.56.23' to 'riak@192.168.56.20'
        3 transfers from 'riak@192.168.56.24' to 'riak@192.168.56.20'

        ok
    ```

Check the information output from the above command, ensuring that you are joining the correct node to the correct cluster.

>[!NOTE]Note on Cluster Plan
>You *must* run `riak admin cluster plan` before performing any join request, as OpenRiak will refuse to proceed to committing the plan if you do not.

4. If you have check the output of `riak admin cluster plan` and you are confident that you are joining the correct node to the correct cluster, you now need to commit the plan:

    ```
        riak admin cluster commit
    ```

You will see the following output:

    ```bash
        Cluster changes committed
        ok
    ```

5. You will now need to monitor transfers, using the following:

    ```bash
        riak admin transfers
    ```

Once transfers have completed, you'll see the following:

    ```bash
        No transfers active

        Active Transfers:


        ok
    ```

This indicates the join process has been completed!

## Joining multiple nodes together into a cluster:

Before you join any nodes, for the sake of simplicity, you should select one node to act as the leader for the join activities. This is the node that the rest of the nodes in this cluster will be joining. We will call this node the "leader" which is represented by the nodename `riak@192.168.0.20`.

1. Prepare the first node to join your leader., ensuring that the contents of `riak.conf` file are configured correctly and, where needed, identical to the other nodes in the cluster you are intending to form.

2. On the first node you are joining to the cluster, run the following command, replacing the nodenames with the ones for your nodes:

    ```bash
        riak admin cluster join riak@192.168.0.20
    ```

This will produce the following output:

    ```bash
        Success: staged join request for 'riak@192.168.0.21' to 'riak@192.168.0.20'
        ok
    ```

3. Assuming the previous steps have worked correctly, you need to check the cluster plan:

    ```bash
        riak admin cluster plan
    ```

You will see a similar output to below:

    ```bash
        =============================== Staged Changes ================================
        Action         Details(s)
        -------------------------------------------------------------------------------
        join           'riak@192.168.56.21'
        join           'riak@192.168.56.22'
        join           'riak@192.168.56.23'
        join           'riak@192.168.56.24'
        -------------------------------------------------------------------------------


        NOTE: Applying these changes will result in 1 cluster transition

        ###############################################################################
                                 After cluster transition 1/1
        ###############################################################################

        ================================= Membership ==================================
        Status     Ring    Pending    Node
        -------------------------------------------------------------------------------
        valid     100.0%     20.3%    riak@192.168.56.20
        valid       0.0%     20.3%    riak@192.168.56.21
        valid       0.0%     20.3%    riak@192.168.56.22
        valid       0.0%     20.3%    riak@192.168.56.23
        valid       0.0%     18.8%    riak@192.168.56.24
        -------------------------------------------------------------------------------
        Valid:5 / Leaving:0 / Exiting:0 / Joining:0 / Down:0

        Transfers resulting from cluster changes: 51
        13 transfers from 'riak@192.168.56.20' to 'riak@192.168.56.23'
        13 transfers from 'riak@192.168.56.20' to 'riak@192.168.56.22'
        13 transfers from 'riak@192.168.56.20' to 'riak@192.168.56.21'
        12 transfers from 'riak@192.168.56.20' to 'riak@192.168.56.24'

        ok
    ```

This plan shows you what notes are joining your leader, and the layout of the ring after the plan is commited.
You should check this plan thoroughly to ensure it is correct configured.

4. Once you've checked the plan, you can commit the changes:

    ```bash
        riak admin cluster commit
    ```

You will see the following output:

    ```bash
        Cluster changes committed
        ok
    ```

5. You will now need to monitor transfers, using the following:

    ```bash
        riak admin transfers
    ```

Once transfers have completed, you'll see the following:

    ```bash
        No transfers active

        Active Transfers:


        ok
    ```

This indicates the join process has been completed and you can now continue with your cluster!


## Removing a node from a cluster

This section will show you how to remove an existing, healthy node from a cluster.

1. On the node in question run the following:

    ```bash
        riak admin cluster leave
    ```

This will produce an output similar to the following:

    ```bash
        Success: staged leave request for 'riak@192.168.0.20'
        ok
    ```

>[!NOTE]Note on Cluster Plan
>You *must* run `riak admin cluster plan` before performing any join request, as OpenRiak will refuse to proceed to committing the plan if you do not.

2. Next, on the same node, run `riak admin cluster plan`, which will produce a similar output to below:

    ```
        =============================== Staged Changes ================================
        Action         Details(s)
        -------------------------------------------------------------------------------
        leave          'riak@192.168.56.20'
        -------------------------------------------------------------------------------


        NOTE: Applying these changes will result in 1 cluster transition

        ###############################################################################
                                 After cluster transition 1/1
        ###############################################################################

        ================================= Membership ==================================
        Status     Ring    Pending    Node
        -------------------------------------------------------------------------------
        leaving    20.3%      0.0%    riak@192.168.56.20
        valid      20.3%     25.0%    riak@192.168.56.21
        valid      20.3%     25.0%    riak@192.168.56.22
        valid      20.3%     25.0%    riak@192.168.56.23
        valid      18.8%     25.0%    riak@192.168.56.24
        -------------------------------------------------------------------------------
        Valid:4 / Leaving:1 / Exiting:0 / Joining:0 / Down:0

        Transfers resulting from cluster changes: 52
          3 transfers from 'riak@192.168.56.23' to 'riak@192.168.56.21'
          3 transfers from 'riak@192.168.56.22' to 'riak@192.168.56.24'
          3 transfers from 'riak@192.168.56.24' to 'riak@192.168.56.21'
          4 transfers from 'riak@192.168.56.23' to 'riak@192.168.56.24'
          3 transfers from 'riak@192.168.56.20' to 'riak@192.168.56.23'
          3 transfers from 'riak@192.168.56.21' to 'riak@192.168.56.23'
          4 transfers from 'riak@192.168.56.22' to 'riak@192.168.56.23'
          3 transfers from 'riak@192.168.56.24' to 'riak@192.168.56.23'
          3 transfers from 'riak@192.168.56.20' to 'riak@192.168.56.22'
          4 transfers from 'riak@192.168.56.21' to 'riak@192.168.56.22'
          3 transfers from 'riak@192.168.56.23' to 'riak@192.168.56.22'
          3 transfers from 'riak@192.168.56.24' to 'riak@192.168.56.22'
          4 transfers from 'riak@192.168.56.20' to 'riak@192.168.56.21'
          3 transfers from 'riak@192.168.56.20' to 'riak@192.168.56.24'
          3 transfers from 'riak@192.168.56.22' to 'riak@192.168.56.21'
          3 transfers from 'riak@192.168.56.21' to 'riak@192.168.56.24'

        ok
    ```

3.  Then you need to commit the changes, with the following:

    ```bash
        riak admin cluster commit
    ```

This will produce the following output:

    ```bash
        Cluster changes committed
        ok
    ```

4. You will now need to monitor transfers, using the following:

    ```bash
        riak admin transfers
    ```

Once transfers have completed, you'll see the following:

    ```bash
        No transfers active

        Active Transfers:


        ok
    ```

This indicates the leave process has been completed!
