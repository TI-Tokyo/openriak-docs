---
sidebar_position: 1
title: Upgrade Checklist
sidebar_label: "Upgrade Checklist"
---

## Contents
1. [System](#system)
2. [Network](#network)
3. [Operations](#operations)
4. [Testing and load with your application](#testing-and-load-with-your-application)
5. [OpenRiak KV](#OpenRiak-KV)

Deploying OpenRiak to a production environment can be a complex process so it is important that you ensure you have the proper checks in place for both OpenRiak and it's respective host systems. Though there are a considerable number of variables depending on your systems design, we have compiled a list of items to consider and check.

## System

Improperly configured systems are one of the biggest reasons for failures in new deployments, so it is essential they are thoroughly checked.

* Are all systems in your cluster as close to identical as possible in terms of both hardware and software?
* Have you set appropriate open files limits on all systems?

## Network

Correct network configuration is essential to allowing all your OpenRiak nodes to properly communicate with eachother and with outside systems. Incorrect configurations could lead to individual nodes dropping out, cascades or other network-related failures.

* Are all systems using the same NTP servers to synchronize clocks?
* Are you sure that your NTP clients’ configuration is monotonic (i.e. that your clocks will not roll back)?
* Is DNS correctly configured for all systems’ deployments?
* Are connections correctly routed between all OpenRiak nodes?
* Are connections correctly set up in your load balancer?
* Are your firewalls correctly configured?
* Check that network latency and throughput are as expected for all of the following (we suggest using iperf to verify):
    - between nodes in the cluster
    - between the load balancer and all nodes in the cluster
    - between application servers and the load balancer
* Do all OpenRiak nodes appear in the load balancer’s rotation?
* Is the load balancer configured to balance connections with roundrobin or a similarly random distribution scheme?


## Operations

* Does your monitoring system ensure that NTP is running?
* Are you collecting time series data on the whole cluster?
    ** System metrics
    ** CPU load
    ** Memory used
    ** Network throughput
    ** Disk space used/available
    ** Disk input/output operations per second (IOPS)
    ** Riak metrics (from the /stats HTTP endpoint or using [riak admin][use admin riak admin])
    ** Latencies: GET and PUT (mean/median/95th/99th/100th)
    ** Vnode stats: GETs, PUTs, GET totals, PUT totals
    ** Node stats: GETs, PUTs, GET totals, PUT totals
        ** Finite state machine (FSM) stats:
            *** GET/PUT FSM objsize (99th and 100th percentile)
            *** GET/PUT FSM times (mean/median/95th/99th/100th)
        ** Protocol buffer connection stats
            *** pbc_connects
            *** pbc_active
            *** pbc_connects_total
* Are the following being graphed (at least the key metrics)?
    * Basic system status
    * Median and 95th and 99th percentile latencies (as these tend to be leading indicators of trouble)

## Testing and load with your application

Inadaquate load testing of clusters and applications can lead to a significant amount of problems with a new/upgraded OpenRiak cluster. You should review the following (but not exhaustive) list of items to check.

* Have you run benchmark tests with simulated loads against your cluster and checked the results against expectations?
* Are the client libraries used by your application on the correct version/in need of an update?
* Do the client libraries you are using support the deployed version of OpenRiak KV

## OpenRiak KV

