---
sidebar_position: 5
title: Installing On RHEL
sidebar_label: "Use RHEL"
date: 2025-09-16
---

[setup-using-docker]: ../../setup/install/docker
[docker]: https://www.docker.com/
[leveled]: ../../configure/guides/backends/configure-leveled

# Installing OpenRiak KV on RHEL

This guide provides the steps for installing OpenRiak KV on the most recent version of Raspbian.

## Installing on RHEL 8

1. From a terminal window download the OpenRiak package with the following:


`wget https://files.tiot.jp/riak/kv/3.2/3.2.5/rhel/8/riak-3.2.5.OTP25-1.el8.x86_64.rpm`


2. From here, there are two methods for installing RHEL:
 
Using Yum which we recommend:

```
sudo yum localinstall -y riak-3.2.5.OTP25-1.el8.x86_64.rpm
```

Or install the package manually with:

```
sudo rpm -Uvh riak-3.2.5.OTP25-1.el8.x86_64.rpm
```

# Installing on RHEL 9

1. From a terminal window download the OpenRiak package with the following:


`wget https://files.tiot.jp/riak/kv/3.2/3.2.5/rhel/9/riak-3.2.5.OTP25-1.el9.x86_64.rpm`


2. From here, there are two methods for installing RHEL:
 
Using Yum which we recommend:

```
sudo yum localinstall -y riak-3.2.5.OTP25-1.el9.x86_64.rpm
```

Or install the package manually with:

```
sudo rpm -Uvh riak-3.2.5.OTP25-1.el9.x86_64.rpm
```

## Next steps - Verifying OpenRiak install

Once the node has been installed, we recommend verifying the node is able to start and respond to requests by following the steps [here](: ../../setup/install/verify).
