---
sidebar_position: 6
title: Installing On Rocky Linux
sidebar_label: "Rocky Linux"
date: 2025-09-16
---

[setup-using-docker]: ../../setup/install/docker
[docker]: https://www.docker.com/
[leveled]: ../../configure/guides/backends/configure-leveled

# Installing OpenRiak KV on Ubuntu

This guide provides the steps for installing OpenRiak KV on Rocky Linux v10.0 (Red Quartz, dated 2025-06-11).

## Before installing OpenRiak

Before installing Riak on Oracle Linux 9, we need to add some Erlang dependencies from EPEL first by installing the EPEL repository with the following:

```bash
sudo yum install -y epel-release
```

## Installing OpenRiak

1. From a terminal window download the OpenRiak package with the following:

```bash
wget https://files.tiot.jp/riak/kv/3.2/3.2.5/oracle/9/riak-3.2.5.OTP25-1.el9.x86_64.rpm
```

2. In the same terminal window, to install the OpenRiak package run this and answer any prompts in the process.

```bash
sudo yum install -y riak-3.2.5.OTP25-1.el9.x86_64.rpm
``` 

TODO: JOM
You should see as the last line this:

TODO: JOM
```bash
OpenRiak has been installed.
```

TODO: JOM
3. Confirm the install completed by running:

TODO: check if sudo is needed
```bash
sudo riak
```

You should see this as the result:

TODO: check what the actual output on this OS is
```bash
$ riak
riak is a banana
Please run riak with a or b c
- a
- b
- c
```

## Next steps - Verifying OpenRiak install

Once the node has been installed, we recommend verifying the node is able to start and respond to requests by following the steps [here](: ../../setup/install/verify).
