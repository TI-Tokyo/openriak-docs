---
title: "Cluster Management Improvements in Riak 1.2"
date: "2012-09-13T00:00:00+00:00"
author: "Basho"
original_url: "http://basho.com/posts/technical/cluster-management-improvements-in-riak-1-2/"
archive_url: "https://web.archive.org/web/20170801115433http://basho.com/posts/technical/cluster-management-improvements-in-riak-1-2/"
categories:
  - "Operations"
  - "Releases"
---
*September 13, 2012*

Last month we released [Riak 1.2](http://basho.com/blog/technical/2012/08/07/Riak-1-2-released/) , with a number of improvements in Riak stats, the protobufs API, LevelDB backend and repair/recovery capabilities. Riak 1.2 also features a new strategy for making cluster changes like adding and removing nodes. With the new approach, Riak allows you to stage changes, view the impact on the cluster, and then commit or abort changes. The increased visibility lets Riak operators make more informed decisions about when and how to scale up, scale down and upgrade or replace nodes. Additionally, you can now make multiple changes, like adding a number of nodes, at the same time – critical for large-scale clusters.

## Pre 1.2 Cluster Management

In prior versions of Riak, users made changes to the cluster using commands under the “riak-admin” syntax. To add or remove a node to the cluster, you would simply call “riak-admin join” or “riak-admin leave,” and the Riak cluster would immediately begin to handoff data and ownership as appropriate. While this approach was simple, it did raise two issues we’ve tried to address with the new cluster management capabilities:

- **Coordinating cluster changes:** Prior to Riak 1.2, there was no way to group changes together. Changes were entered sequentially, and if there was more than one change (e.g. joining multiple nodes to a cluster), the first change would happen in a single transition and the remaining changes (e.g. the rest of the joins) would occur together in a second transition. In the case of multiple joins, in the first transition, data is transferred from the cluster to the new node. Then, in the second transition, some of the data transferred to the first new node is then transferred to the other new nodes, wasting network bandwidth and disk space. This proved particularly problematic for production deployments in which nodes were frequently added or removed.
- **Planning:** The pre-1.2 approach to cluster management didn’t give you visibility into how your changes would affect the cluster before you made them. For instance, the only way to know how many transfers a join would take would be to start the join and then run “riak-admin ring-status”. Likewise, you couldn’t know what ownership would look like until after the join.

## Staged Clustering

We addressed both of the above issues with a new approach we’re calling ‘Staged Clustering’.

In Riak 1.2, instead of joins, leaves, etc. taking place immediately, they’re first staged. After staging cluster changes, you can view how the changes will affect the cluster, seeing how ring ownership will change and how many transfers between nodes will need to occur to complete the transition. After looking at the plan, you can then add or remove changes staged to be committed, scrap the plan, or execute it as is.

![Staged Clustering Riak](../images/cluster-management-improvements-in-riak-1-2/cluster-management-staged_clustering.png)

**Staged Clustering High Level Process**

The ‘Staged Clustering’ interface is implemented in Riak’s command line tool, riak-admin, under the ‘cluster’ command. Underneath the ‘cluster’ command are subcommands used to stage, view, and commit cluster changes (e.g. to join the current cluster to node dev1, you’d use: ‘riak-admin cluster join dev1’ ). You can read more about the new syntax in the [Riak Wiki](http://wiki.basho.com/Command-Line-Tools---riak-admin.html). Currently, the new approach to cluster management is not implemented in [Riak Control](http://basho.com/products/riak-control/), our open-source management and monitoring GUI, but is planned for a later release.

## Example

Let’s take a look at how the new cluster management strategy would work in a scenario where we wanted to add three nodes to an existing node (dev1) to form a four-node cluster.

1. **View the Current Member Status**

First, we call ‘riak-admin member\_status’ to get a view of the current cluster, the nodes in it and their current ring ownership:

![Member Status Riak](../images/cluster-management-improvements-in-riak-1-2/cluster-management-riak-admin_member_status.png)

2. **Stage Joining New Nodes**

Next, we’ll join three nodes (dev2, dev3, dev4) to the cluster using the cluster command.

`bash  
dev2: riak-admin cluster join dev1  
dev3: riak-admin cluster join dev1  
dev4: riak-admin cluster join dev1`

The joins are now staged for commit.

3. **View How Staged Changes Will Affect the Cluster**

Now we can use the new ‘riak-admin cluster plan’ command to see the impact of the joins on the cluster, viewing changes to ring ownership and transfers that need to occur.

`bash  
riak-admin cluster plan`

![Cluster Management Plan Riak](../images/cluster-management-improvements-in-riak-1-2/cluster-management-plan.png)

In the output, we see: the changes staged for commit, the number of resulting cluster transitions (1), how the data will be distributed around the ring after transition (25% on each node), and the number of transfers the transition will take (48 total).

4. **Commit Changes**

If we want to commit these changes, we use the commit command:

`bash  
riak-admin cluster commit`

These changes start taking place immediately. If we run ‘riak-admin member\_status’, we can see the status of the transition. Additionally, we’ve fleshed out the ‘riak-admin transfers’ command to give you [much more visibility into active transfers](http://basho.com/blog/technical/2012/06/25/Riak-Admin-Transfers-in-1-2-Release/) in Riak 1.2.

## Other Resources

For more in-depth information on the new cluster management stuff in Riak 1.2, check out [this recorded webinar](http://info.basho.com/1.2webinar.html) with Basho engineer Joseph Blomstedt and the [updated docs](http://wiki.basho.com/Command-Line-Tools---riak-admin.html).
