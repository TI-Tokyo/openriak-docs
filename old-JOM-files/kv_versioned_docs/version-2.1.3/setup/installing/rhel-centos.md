---
title: "RHEL and CentOS"
sidebar_position: 304
sidebar_label: RHEL & CentOS
pagination_label: "RHEL and CentOS"
hide_table_of_contents: true
last_update:
  author: RiakDocs
  date: 2015-12-10
---
import RiakDocsNote from '@site/src/components/RiakDocs/RiakDocsNote';


[install source index]: ./../source
[install source erlang]: ./../source/erlang
[install verify]: ./../verify

Riak KV can be installed on CentOS- or Red-Hat-based systems using a binary
package or by [compiling Riak from source code][install source index]. The following steps have been tested to work with Riak on
CentOS/RHEL 5.10, 6.5, and 7.0.1406.

> **Note on SELinux**
>
> CentOS enables SELinux by default, so you may need to disable SELinux if
you encounter errors.

For versions of Riak prior to 2.0, Basho used a self-hosted
[rpm](http://www.rpm.org/) repository for CentOS and RHEL packages. For versions 2.0 and later, TI Tokyo hosts these at https://files.tiot.jp.

Platform-specific pages are linked below:

* [el5](https://files.tiot.jp/riak/kv/2.1/2.1.1/rhel/5/riak-2.1.1-1.el5.x86_64.rpm)
* [el6](https://files.tiot.jp/riak/kv/2.1/2.1.1/rhel/6/riak-2.1.1-1.el6.x86_64.rpm)
* [el7](https://files.tiot.jp/riak/kv/2.1/2.1.1/rhel/7/riak-2.1.1-1.el7.centos.x86_64.rpm)
* [Fedora 19](https://files.tiot.jp/riak/kv/2.1/2.1.1/fedora/19/riak-2.1.1-1.fc19.x86_64.rpm)

## Installing with Yum and Packages

If you wish to install the RHEL/CentOS packages by hand, follow these
instructions.

#### For Centos 5 / RHEL 5

Download the package and install:

```bash
wget https://files.tiot.jp/riak/kv/2.1/2.1.1/rhel/5/riak-2.1.1-1.el5.x86_64.rpm
sudo yum install riak-2.1.3-1.el5.x86_64
```

#### For Centos 6 / RHEL 6

Download the package and install:

```bash
wget https://files.tiot.jp/riak/kv/2.1/2.1.1/rhel/6/riak-2.1.1-1.el6.x86_64.rpm
sudo yum install riak-2.1.3-1.el6.x86_64
```

## Installing with rpm

#### For Centos 5 / RHEL 5

```bash
wget https://files.tiot.jp/riak/kv/2.1/2.1.1/rhel/5/riak-2.1.1-1.el5.x86_64.rpm
sudo rpm -Uvh riak-2.1.3-1.el5.x86_64.rpm
```

#### For Centos 6 / RHEL 6

```bash
wget https://files.tiot.jp/riak/kv/2.1/2.1.1/rhel/6/riak-2.1.1-1.el6.x86_64.rpm
sudo rpm -Uvh riak-2.1.3-1.el6.x86_64.rpm
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
wget http://s3.amazonaws.com/downloads.basho.com/riak/2.1/2.1.3/riak-2.1.3.tar.gz
tar zxvf riak-2.1.3.tar.gz
cd riak-2.1.3
make rel
```

You will now have a fresh build of Riak in the `rel/riak` directory.

## Next Steps

Now that Riak is installed, check out [Verifying a Riak Installation][install verify].
