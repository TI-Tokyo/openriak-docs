---
sidebar_position: 2
title:Installing On Ubuntu or Debian
sidebar_label: "Use Ubuntu"
---

[setup-using-docker]: ../../setup/install/docker
[docker]: https://www.docker.com/
[leveled]: ../../configure/guides/backends/configure-leveled

# Installing OpenRiak KV on Ubuntu

This guide provides the steps for installing OpenRiak KV on the most recent version of Ubuntu/Debian.

## Installing OpenRiak

1. From a terminal window download the OpenRiak package with the following:


`wget https://files.tiot.jp/riak/kv/3.2/3.2.5/ubuntu/noble64/riak_3.2.5-OTP25_amd64.deb`


2. In the same terminal window, run `dpkg -i riak_3.2.5-OTP25_amd64.deb` to install the Riak package, answering any prompts in the process.

## Next steps - Verifying OpenRiak install

Once the node has been installed, we recommend verifying the node is able to start and respond to requests by following the steps [here](: ../../setup/install/verify).
