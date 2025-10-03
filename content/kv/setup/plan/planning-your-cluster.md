---
sidebar_position: 1
title: Planning a cluster
sidebar_label: Planning-a-cluster
pagination_label: Planning
sidebar_class_name: kv-setup-plan
date: 2025-09-25
---

[operating-system]: : ../../setup/install/index
[choosing-a-backend]: : ../../setup/install/plan/planning-your-cluster

## Contents

1. Introduction
2. Operating System
3. Backend
4. Capacity
5. Networking


## Introduction

There are a number of factors that should be considered when planning a new OpenRiak cluster. These factors will all play a part in defining how your cluster performs on a long term basis and the level of maintenance required.

## Operating System

The [operating-system] you choose will largely not influence Openriak's performance, however there are some important things that should be considered when choosing.

1. Support community - Distributions with smaller communities will have less support easily accessible for problems.
2. Long Term Support (LTS) - Long term support for updates is essential to minimise disruption to your system and to help keep it secure. Choosing a distribution with a short LTS date will leave your system vulnerable to any future security holes found after support has ended without upgrading.
3. End of Life (EOL) - As with the Long Term Support date, knowing when your distribution has been set for EOL will allow you to plan your cluster's long-term life in a better way.

The following Operating systems have packages available:

* RHEL
* Rocky Linux
* Ubuntu/Debian
* Raspbian OS
* Oracle Linux
* Amazon Linux

## Backend

Choosing a backend can be the biggest decision you make in cluster planning. The wrong backend for your use-case could lead to poor performance for your users.
[PLACEHOLDER]
Different backends allow you to select a storage engine that suits for your operations needs. For example, if your use case requires maximum throughput, data persistence, and a bounded keyspace, then Bitcask is a good choice. On the other hand, if you need to store a large number of keys or to use secondary indexes, LevelDB is likely a better choice.

## Capacity

There are a number of variables that can play a part in the capacity of your cluster:

* RAM - One of the most essential resources for deciding on the size of your cluster. Ample memory is essential for running queries and caching data for rapid responses.
* Disk
* Ring Size/Partition count
* Bandwidth
* I/O

## Networking

When it comes to networking, there are two generally accepted methods for load-balancing across your cluster.

1. Virtual IPs - Any of the normal options should be appropriate, but we do not recommend VRRP behaviour for a Virtual IP as you'll lose the benefit of spreading query load to all nodes in the ring.

2. Reverse-proxy - Any of the solutions in the following list should be appropriate: 
* haproxy
* squid
* varnish
* nginx
* lighttpd
* Apache

