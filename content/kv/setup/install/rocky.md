---
sidebar_position: 2
title:Installing On Rocky Linux
sidebar_label: "Rocky Linux"
---

[setup-using-docker]: ../../setup/install/docker
[docker]: https://www.docker.com/
[leveled]: ../../configure/guides/backends/configure-leveled

# Installing OpenRiak KV on Ubuntu

This guide provides the steps for installing OpenRiak KV on the most recent version of Rock Linux.


## Before installing OpenRiak
Before installing Riak on Oracle Linux 9, we need to add some Erlang dependencies from EPEL first by installing the EPEL repository with the following:

`sudo yum install -y epel-release`

## Installing OpenRiak

1. From a terminal window download the OpenRiak package with the following:


`wget https://files.tiot.jp/riak/kv/3.2/3.2.5/oracle/9/riak-3.2.5.OTP25-1.el9.x86_64.rpm`


2. In the same terminal window, run `sudo yum install -y riak-3.2.5.OTP25-1.el9.x86_64.rpm` to install the OpenRiak package, answering any prompts in the process.

## Next steps - Verifying OpenRiak install

Once the node has been installed, we recommend verifying the node is able to start and respond to requests by following the steps [here](: ../../setup/install/verify).
