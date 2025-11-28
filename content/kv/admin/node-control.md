---
title: Node Control
sidebar_label: "Node Control"
---

# Contents

# Overview

This section covers the various commands used in general control of your node, including starting and stopping a node, inspecting the node and other operations.

# Starting and stopping a node

## Starting a node

To start an OpenRiak node, you will use the following command:

```bash
riak start
```

If the node has started successfully, you will not see any response from OpenRiak.

## Stopping a node

To stop an OpenRiak node, you will use the following command:

```bash
riak stop
```

If the node has stopped successfully, you will not see any response from OpenRiak.

## Checking if a node is running

If you are uncertain whether an OpenRiak node is running currently, you can check with the following:

```bash
riak ping
```

If the node is running, you should see the following response:

```bash
pong
```

If a node is not running or has crashed, you will see:

```bash
Node riak@127.0.0.1 is not responding to pings
```

# Inspecting your node

There are a variety of ways to inspect your node for a variety of reasons, from checking it can read and write, to reviewing the performance statistics.

## Testing read and write

If you want to test if your node is able to read and write, you can use the following command:

```bash
riak admin test
```

You should see the following output, or something similar:

```bash
Successfully completed 1 read/write cycle to 'riak@127.0.0.1'
```

If you see a different output to this, your node may be in trouble and this will require further investigation.

## Checking node status

`riak admin status` is a subcommand of the `riak admin` command that is included with every installation of OpenRiak. The status subcommand provides data related to the current operating status for a node. The output of `riak admin status` is extensive and outlined below:



## Checking cluster status

You can check the status of your cluster with:

```bash
riak admin cluster status
```

You will see an output that contains your clusters node names, ring status, availability, ring share and any pending transfers:


## Checking with riak-debug

The `riak-debug` command can be used to identify and diagnose common problems with your OpenRiak KV nodes. The command runs a series of operations to collect data, logs and information, condensing it all into a compressed folder for you to extract and review.

---
**Note**

Extensive use of `riak-debug` as part of regular monitoring is strongly not recommended as it can lead to overloads if a node is already in an unhealthy state. Operators should utilise alternative methods listed in this document to inspect their node regularly.
---

You can see an example of the use of `riak-debug` and the output from the command below:

```bash
$ riak-debug
..........EEEEE.......EE................ /usr/lib64/riak/riak@127.0.0.1-riak-debug.tar.gz
```

