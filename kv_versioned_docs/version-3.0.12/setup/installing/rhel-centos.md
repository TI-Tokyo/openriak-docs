---
title: "RHEL and CentOS"
sidebar_position: 307
sidebar_label: RHEL & CentOS
pagination_label: "RHEL and CentOS"
hide_table_of_contents: true
last_update:
  author: RiakDocs
  date: 2022-12-20
---
import RiakDocsNote from '@site/src/components/RiakDocs/RiakDocsNote';


[install source index]: ./../source
[install source erlang]: ./../source/erlang
[install verify]: ./../verify

Riak KV can be installed on CentOS- or Red-Hat-based systems using a binary
package or by [compiling Riak from source code][install source index]. The following steps have been tested to work with Riak on
CentOS/RHEL 6.9, 7.5.1804 and 8.1.1911 .

> **Note on SELinux**
>
> CentOS enables SELinux by default, so you may need to disable SELinux if
you encounter errors.

## Installing From Package

If you wish to install the RHEL/CentOS packages by hand, follow these
instructions.

### For Centos 8 / RHEL 8

Before installing Riak on CentOS 8/RHEL 8, we need to satisfy some Erlang dependencies
from EPEL first by installing the EPEL repository:

```bash
sudo yum install -y epel-release
```

Once the EPEL has been installed, you can install CentOS 8/RHEL 8 using yum, which we recommend:

```bash
wget https://files.tiot.jp/riak/kv/3.0/3.0.12/rhel/8/riak-3.0.12-1.el8.x86_64.rpm
sudo yum localinstall -y riak-3.0.12-1.el8.x86_64.rpm
```

Or you can install the `.rpm` package manually:

```bash
wget https://files.tiot.jp/riak/kv/3.0/3.0.12/rhel/8/riak-3.0.12-1.el8.x86_64.rpm
sudo rpm -Uvh riak-3.0.12-1.el8.x86_64.rpm
```

### For Centos 7 / RHEL 7

You can install CentOS 7/RHEL 7 using yum, which we recommend:

```bash
wget https://files.tiot.jp/riak/kv/3.0/3.0.12/rhel/7/riak-3.0.12-1.el7.x86_64.rpm
sudo yum localinstall -y riak-3.0.12-1.el7.x86_64.rpm
```

Or you can install the `.rpm` package manually:

```bash
wget https://files.tiot.jp/riak/kv/3.0/3.0.12/rhel/7/riak-3.0.12-1.el7.x86_64.rpm
sudo rpm -Uvh riak-3.0.12-1.el7.x86_64.rpm
```

### For Centos 6 / RHEL 6

You can install using yum, which we recommend:

```bash
wget https://files.tiot.jp/riak/kv/3.0/3.0.12/rhel/6/riak-3.0.12-1.el6.x86_64.rpm
sudo yum localinstall -y riak-3.0.12-1.el6.x86_64.rpm

```

Or you can install the `.rpm` package manually:

```bash
wget https://files.tiot.jp/riak/kv/3.0/3.0.12/rhel/6/riak-3.0.12-1.el6.x86_64.rpm
sudo rpm -Uvh riak-3.0.12-1.el6.x86_64.rpm
```

## Installing From Source

Riak requires an [Erlang](http://www.erlang.org/) installation.
Instructions can be found in [Installing Erlang][install source erlang].

Building from source will require the following packages:

* `gcc`
* `gcc-c++`
* `glibc-devel`
* `make`
* `pam-devel`

You can install these with yum:

```bash
sudo yum install gcc gcc-c++ glibc-devel make git pam-devel
```

Now we can download and install Riak:

```bash
wget https://files.tiot.jp/riak/kv/3.0/3.0.12/riak-3.0.12.tar.gz
tar zxvf riak-3.0.12.tar.gz
cd riak-3.0.12
make rel
```

You will now have a fresh build of Riak in the `rel/riak` directory.

## Next Steps

Now that Riak is installed, check out [Verifying a Riak Installation][install verify].

