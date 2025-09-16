
sidebar_position: 1
title:Installing On Alpine Linux
sidebar_label: "Use Alpine Linux"
date: 2025-09-16
---

# Installing OpenRiak KV on Alpine Linux

This guide provides the steps for installing OpenRiak KV on the most recent version of Alpine Linux.

## Installing on Alpine Linux

1. First, we need to add the OpenRiak repository:

```
Run echo https://files.tiot.jp/alpine/v3.21/main >> /etc/apk/repositories
```

2. Next you need to download and install the OpenRiak repository public key:

```
wget http://files.tiot.jp/alpine/alpine@tiot.jp.rsa.pub -O /etc/apk/keys/alpine@tiot.jp.rsa.pub
```

3. Then update your list of packages:

```
apk update
```

4. Install OpenRiak:

For the latest version, run:
```
apk add riak
```

## Next steps - Verifying OpenRiak install

Once the node has been installed, we recommend verifying the node is able to start and respond to requests by following the steps [here](: ../../setup/install/verify).