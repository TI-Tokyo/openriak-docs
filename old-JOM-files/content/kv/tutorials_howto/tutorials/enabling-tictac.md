---
sidebar_position: 1
title: Enabling TicTac Active Anti-Entropy
sidebar_label: "Enable TicTac AAE"
date: 2026-05-17
---
[root site]: [!site]
[root project]: [!project]
[root version]: [!version]
[assumptions]: #assumptions
[architecture]: #cluster-architecture
[check]: #what-to-check-before-enabling-tictac-active-anti-entropy-aae
[applychanges]: #applying-the-changes


>[!MEMO] Introduction
>This tutorial explains how to enable Tic-Tac Active Anti-Entropy in your OpenRiak Cluster.


## Assumptions

This guide assumes the following:

1. That your cluster is running on one of the supported operating systems
2. That your cluster is running a version of OpenRiak that is at least V3.0 or higher.
3. That your cluster does not already have TicTac AAE running, or has not run TicTac AAE previously 

## Cluster Architecture

This section is for reference only, as this should make no difference to the overall steps for enabled TicTac Active Anti-Entropy.

The following section will show the intended structure of each cluster and the names/addresses that each node will use for this tutorial. You should change these nodenames to ones that are suitable for your environment.

### Primary Cluster

|-------------------|--------------|
| Node designation  | IP Address   |
| ------------------|--------------|
|       riak1a      | 192.168.0.20 |
|       riak2a      | 192.168.0.21 |
|       riak3a      | 192.168.0.22 |
|       riak4a      | 192.168.0.23 |
|       riak5a      | 192.168.0.24 |
| ------------------|--------------|

## What to know and check before enabling TicTac Active Anti-Entropy (AAE)

Before enabling TicTac Active Anti_Entropy, there are a few things you should check before hand.

1. Version -If you are on an older version of OpenRiak/Riak, ensure you are on at least version 3.0.1+, as previous to this version TicTac AAE was either non-existent or in very early development and not ready for full production deployment.
2. Legacy AAE - If you do not wish to run legacy AAE alongside TicTac, you should ensure that has been disabled by setting the value of `anti_emtropy` in your `riak.conf` file to `passive`.
3. System Resources - Enabling TicTac AAE will result in a slight increase in memory, CPU and disk utilisation, so you should ensure that all of these resources have sufficient bandwidth for the increase. It is generally recommended that less than 70% utilisation of any one resource is best practice to allow for sudden spikes.
4. Testing - Ensure proper testing in a non-production environment with comparable load to production before deployment.
5. Key store - When running in parallel mode, which will be the default if the backend does not support native tictac aae (i.e. is not leveled), what type of parallel key store should be kept - leveled_ko (leveled and key-ordered), or leveled_so (leveled and segment ordered).

## Enabling Tictac Active Anti-Entropy

To enable TicTac AAE in your cluster follow the following steps:

>[!NOTE] Note on rolling restarts
>This guide assumes you will be performing a rolling restart to all nodes in this cluster after making the change. If you are not and wish to apply it to all nodes in the cluster at once, you just need to stop all nodes in the cluster at once rather than one by one.

1. In each node in your cluster, open the `riak.conf` file.

2. Change the following value:

    ```bash
        tictactaae_active = passive
    ```

To active as below:

    ```bash
        tictacaae_active = active
    ```

3. If needed, change the value of the `tictacaae_rebuildwait` and `tictacaae_rebuilddelay` to suit your organisations requirements. These two functions control the build time and the rebuild delay of TicTac AAE.

>[!NOTE] Note on changing `tictacaae_rebuildwait` and `tictacaee_rebuilddelay`.
>These two values, if changed without testing, can cause a significant increase in resource usage in systems and should not be adjusted in production without thorough testing first.

4. Once you have made the changes and saved them, you will need to restart each node in the cluster. See the next section on performing a rolling restart.

## Applying the changes

Once you have completed the changes to `riak.conf` you will need to restart all the nodes in the cluster to apply the change. The steps below follow a rolling restart method for applying this change. 

On the first node in your cluster: 

1. Run `riak stop`

2. After waiting a suitable amount of time (generally a minute or two should be fine), start the node up with `riak daemon`. If Riak starts without issue, you will see no output.
You can check if Riak is up with:

    ```bash
        ping
    ```
This should produce the response:

    ```bash
        pong
    ```

3. Once the node is up, you need to wait for transfers between nodes, before you move onto the next node. You can check transfer status with:

    ```bash
        riak admin transfers
    ```

If transfers have completed, you'll see a similar output to below:

    ```bash
        No transfers active

        Active Transfers:


        ok
    ```

If transfers are not complete you will see something similar to:

    ```bash
       192.168.0.22 waiting to handoff 46 partitions
    ```

This means you will need to wait for those partitions to finish before continuing.

>[!NOTE]Note on stuck transfers
>Sometimes transfers can get stuck and need to be restarted, you can do this by setting `riak admin transfer-limit 0`, waiting a few seconds, then setting it back to the previous limit (default is 2)

4. Once you have completed the above on your first node, you can move onto the next node in the sequence.

That's it! Once you've completed this, assuming no issues, you'll be good to go!


