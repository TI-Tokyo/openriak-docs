---
title: "Riak 1.4: Riak Control"
date: "2013-07-16T09:00:52+00:00"
author: "Hector Castro"
original_url: "http://basho.com/posts/technical/riak-1-4-riak-control/"
archive_url: "https://web.archive.org/web/20170801115550http://basho.com/posts/technical/riak-1-4-riak-control/"
categories:
  - "Operations"
  - "Releases"
---
*July 16, 2013*

Riak Control is a web-based administrative console for inspecting and manipulating Riak clusters.

Although Riak Control is maintained as a separate application, the necessary code for Control ships with Riak 1.1 and above and requires no additional installation steps. For details on setting up Riak Control, check out [our docs](http://docs.basho.com/riak/1.4.0/references/appendices/Riak-Control/#Setting up-Riak-Control).

Those are things you may already know about Control. Now let’s look at the changes in 1.4.

## Cluster Management with Staging

The `riak-admin` command-line tool has offered staged clustering since Riak 1.2. Riak 1.4 brings that functionality to Control.

The new Cluster Management interface allows you to stage cluster node additions and removals. Once the changes have been reviewed, they can be committed to the cluster. After being committed, Control displays partition transfers and memory utilization changes as they occur.

Staged changes to the cluster:

![Staged Changes](../images/riak-1-4-riak-control/StagedChanges.png)

Changes committed; transfers active:

![Changes Committed](../images/riak-1-4-riak-control/ChangesCommitted.png)

Cluster stabilizes after changes:

![Cluster Stabilized](../images/riak-1-4-riak-control/ClusterStabilized.png)

## Standalone Node Management Interface

Because the Cluster Management interface now operates on staged changes, actions that cannot be staged have been moved to the Node Management interface. Here, changes to individual nodes, such as stopping or marking them as down, can be applied.

![Node Management](../images/riak-1-4-riak-control/NodeManagement.png)

## Contributing to Riak Control

Riak Control’s user interface is built using [Ember.js](https://github.com/emberjs/ember.js), and for persistence, [Ember Data](https://github.com/emberjs/data). The backend is written in Erlang using [Webmachine](https://github.com/basho/webmachine).

Riak Control’s modular design prevents users from having to understand every detail of its existing functionality to contribute. If you’re interested in contributing, we have outlined the process of [setting up a development environment](https://github.com/basho/riak_control/wiki/Getting-Started-With-Development), as well as some basic [rules for contribution](https://github.com/basho/riak_control/wiki/Contributing-to-Riak-Control).

Check out our [Riak 1.4 announcement](http://basho.com/basho-announces-availability-of-riak-1-4) to learn what else is included in this release.

[Hector Castro](https://twitter.com/hectcastro)
