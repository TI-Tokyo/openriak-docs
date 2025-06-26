---
title: "Oracle Linux"
sidebar_position: 306
sidebar_label: Oracle Linux
pagination_label: "Oracle Linux"
hide_table_of_contents: true
last_update:
  author: RiakDocs
  date: 2023-12-08
---
import RiakDocsNote from '@site/src/components/RiakDocs/RiakDocsNote';


[install source index]: ./../source
[install source erlang]: ./../source/erlang
[install verify]: ./../verify

## Installing From Package

If you wish to install the Oracle Linux package by hand, follow these
instructions.

### For Oracle Linux 8

**Note** There are various Riak packages available for different OTP versions, please ensure that you are using the correct package for your OTP version.

Before installing Riak on Oracle Linux 8, we need to satisfy some Erlang dependencies
from EPEL first by installing the EPEL repository:

```bash
sudo yum install -y epel-release
```

Once the EPEL has been installed, you can install Riak on Oracle Linux 8 using yum, which we recommend:

```bash
wget https://files.tiot.jp/riak/kv/3.0/3.0.16/oracle/8/riak-3.0.16.OTP22.3-1.el8.src.rpm
sudo yum install -y riak-3.0.16.OTP22.3-1.el8.src.rpm
```

## Next Steps

Now that Riak is installed, check out [Verifying a Riak Installation][install verify].

