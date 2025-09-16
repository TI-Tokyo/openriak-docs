---
sidebar_position: 7
title: Installing On Ubuntu or Debian
sidebar_label: "Use Ubuntu"
date: 2025-09-16
---

[setup-using-docker]: ../../setup/install/docker
[docker]: https://www.docker.com/
[leveled]: ../../configure/guides/backends/configure-leveled

# Installing OpenRiak KV on Ubuntu

This guide provides the steps for installing OpenRiak KV on the most recent version of Ubuntu/Debian.

## Installing OpenRiak

1. From a terminal window download the OpenRiak package with the following:


```
wget https://files.tiot.jp/riak/kv/3.2/3.2.5/ubuntu/noble64/riak_3.2.5-OTP25_amd64.deb
```


2. In the same terminal window, to install the Riak package run this and answer any prompts in the process:

```
dpkg -i riak_3.2.5-OTP25_amd64.deb
```


## Next steps - Verifying OpenRiak install

Once the node has been installed, we recommend verifying the node is able to start and respond to requests by following the steps [here](: ../../setup/install/verify).
