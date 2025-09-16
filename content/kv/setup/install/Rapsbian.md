---
sidebar_position: 2
title:Installing On Raspbian
sidebar_label: "Use Raspbian"
---

[setup-using-docker]: ../../setup/install/docker
[docker]: https://www.docker.com/
[leveled]: ../../configure/guides/backends/configure-leveled

# Installing OpenRiak KV on Raspbian

This guide provides the steps for installing OpenRiak KV on the most recent version of Raspbian.

## Installing on Raspbian

1. From a terminal window download the OpenRiak package with the following:


```
wget https://files.tiot.jp/riak/kv/3.2/3.2.5/raspbian/bullseye/riak-dbgsym_3.2.5-OTP25_arm64.deb
```


2. Next, you can use the following command to install the package:

```
sudo dpkg -i riak-dbgsym_3.2.5-OTP25_arm64.deb
```

## Next steps - Verifying OpenRiak install

Once the node has been installed, we recommend verifying the node is able to start and respond to requests by following the steps [here](: ../../setup/install/verify).
