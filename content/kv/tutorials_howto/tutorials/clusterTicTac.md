---
sidebar_position: 1
title: Working with TicTac AAE & NextGen Repication 
sidebar_label: "Working with TTAAE and NextGen Repl"
date: 2026-05-16
---
[root site]: [!site]
[root project]: [!project]
[root version]: [!version]
[assumptions]: #assumptions
[design]: #cluster-design
[installingg]: #getting-started---installing-openriak

>[!MEMO] Introduction
>This page is intended to provide a detailed guide on setting up 2 full OpenRiak clusters of 5 nodes each, running TicTAc AAE on the leveled backend, with Nextgen Replication running
>This will include:
>1. Installing OpenRiak on Ubuntu
>2. Best practice changes to the Operating system.
>3. Defining nodenames, configuring the backend, then enabling TicTac AAE.
>4. Launching the nodes and connecting them together into a cluster
>5. Adjusting the `riak.conf` files to allow connection between the two.

## Assumptions

To start, we have made the following assumptions:

1. You want two clusters running the most recent version of OpenRiak, with TicTac Active-Anti Entropy and NextGen Replication.
2. You will be running a clean install of Ubuntu
3. You want to use the leveled backend for OpenRiak
4. You want to use the HTTP interface for your nodes to communicate with eachother.

## Cluster design

The following section will show the intended structure of each cluster and the names/addresses that each node will use for this tutorial. You should change these nodenames to ones that are suitable for your environment.

### Cluster A - Primary Cluster

|-------------------|---------------|
| Node designation  | IP Address    |
| ------------------|---------------|
|       riak1a      | 192.168.56.20 |
|       riak2a      | 192.168.56.21 |
|       riak3a      | 192.168.56.22 |
|       riak4a      | 192.168.56.23 |
|       riak5a      | 192.168.56.24 |
| ------------------|---------------|

### Cluster B - Secondary Cluster

|-------------------|---------------|
| Node designation  | IP Address    |
| ------------------|---------------|
|       riak1b      | 192.168.56.20 |
|       riak2b      | 192.168.56.21 |
|       riak3b      | 192.168.56.22 |
|       riak4b      | 192.168.56.23 |
|       riak5b      | 192.168.56.24 |
| ------------------|---------------|

## Getting started - Installing OpenRiak

This guide assumes you are using a clean Ubuntu image intended for an enterprise environment.

1. Fetch the OpenRiak package from the files.tiot.jp website:

    ```bash
        wget -q https://files.tiot.jp/riak/kv/3.4/3.4.0/ubuntu/jammy64/riak_3.4.0-OTP26_amd64.deb
    ```
    
    You should see a response similar to below when it is completed:

    ```bash
        (11.3 MB/s) - ‘riak_3.4.0-OTP26_amd64.deb.2’ saved [29514288/29514288]
    ```

2. Install the OpenRiak package:

    ```bash
        sudo dpkg -i riak_3.4.0-OTP26_amd64.deb
    ```

    You will seen output similar to the following:
    
    ```bash
        Selecting previously unselected package riak.
        (Reading database ... 64296 files and directories currently installed.)
        Preparing to unpack riak_3.4.0-OTP26_amd64.deb ...
        Unpacking riak (3.4.0-OTP26) ...
        Setting up riak (3.4.0-OTP26) ...
    ```

3.