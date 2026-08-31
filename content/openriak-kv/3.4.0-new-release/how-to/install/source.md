---
title: 'Build and install OpenRiak from source'
description: 'Show operators how to build and install openriak from source and confirm that the installation is ready.'
weight: 8
diataxis: 'how-to'
product: 'OpenRiak KV'
product_version: '3.4.0'
status: 'editorially-rewritten'
draft: true
audience:
  - 'operators'
legacy_3_2_5_sources:
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\setup\installing\source.md'
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\setup\installing\source\erlang.md'
  - 'Package, platform, installation, upgrade, or downgrade details require release-specific verification for OpenRiak KV 3.4.0.'
source_material:
  - 'legacy-3.2.5'
  - 'live-3.2.5'
  - 'proposed-kv'
  - 'openriak-quickdocs-3.4'
quickdocs_sources:
  - 'https://openriak.github.io/riak/InstallAndStartGuide.html#generating-a-package'
  - 'https://openriak.github.io/riak/InstallAndStartGuide.html#install-erlangotp'
  - 'https://openriak.github.io/riak/InstallAndStartGuide.html#local-cluster'
  - 'https://openriak.github.io/riak/InstallAndStartGuide.html#local-release'
  - 'https://openriak.github.io/riak/InstallAndStartGuide.html#make-riak'
  - 'https://openriak.github.io/riak/InstallAndStartGuide.html#starting-riak-by-make-method'
tags: ['diataxis', 'kv', 'how-to']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Show operators how to build and install openriak from source and confirm that the installation is ready.

## Overview

### OpenRiak KV From Source

[install source erlang]: {{< product-version-root >}}how-to/install/source/
[downloads]: {{< product-version-root >}}downloads/
[install debian & ubuntu#source]: {{< product-version-root >}}how-to/install/debian-ubuntu/
[install freebsd#source]: {{< product-version-root >}}reference/releases/supported-platforms/
[install mac osx#source]: {{< product-version-root >}}reference/releases/supported-platforms/
[install rhel & centos#source]: {{< product-version-root >}}how-to/install/rhel-rocky/#installing-from-source
[install verify]: {{< product-version-root >}}how-to/install/verify-installation/

Riak should be installed from source if you are building on a platform
for which a package does not exist or if you are interested in
contributing to Riak.

#### Dependencies

##### Erlang

To install Riak, you will need to have [Erlang](http://www.erlang.org/) installed. We strongly recommend using Basho's patched version of Erlang to install Riak 2.0+. All of the patches in this version have been incorporated into later versions of the official Erlang/OTP release.

See [Installing Erlang][install source erlang] for instructions.

##### Git

Riak depends on source code located in multiple Git repositories. Install [Git](https://git-scm.com/) on the target system before attempting the build.

##### GCC

Riak will not compile with Clang. Please make sure your default C/C++
compiler is [GCC](https://gcc.gnu.org/).

#### Installation

The following instructions generate a complete, self-contained build of
Riak in `$RIAK/rel/riak` where `$RIAK` is the location of the cloned source.

##### Installing from GitHub

The [Riak Github respository](http://github.com/basho/riak) has much
more information on building and installing Riak from source. To clone
and build Riak from source, follow the steps below.

Clone the repository using [Git](http://git-scm.com) and build:

```bash
git clone git://github.com/basho/riak.git
cd riak
make locked-deps
make rel
```

#### Platform-Specific Instructions

For instructions about specific platforms, see:

* [Debian & Ubuntu][install debian & ubuntu#source]
  * [FreeBSD][install freebsd#source]
  * [Mac OS X][install mac osx#source]
  * [RHEL & CentOS][install rhel & centos#source]

If you are running Riak on a platform not in the list above and need
some help getting it up and running, join The Riak Mailing List and
inquire about it there. We are happy to help you get up and running with
Riak.

##### Windows

Riak is not currently supported on Microsoft Windows.

#### Next Steps

Now that Riak is installed, check out [Verifying a Riak Installation][install verify].

### Installing Erlang

[install index]: {{< product-version-root >}}how-to/install/
[security basics]: {{< product-version-root >}}how-to/secure/enable-security/

Pre-packaged versions of Riak include an Erlang installation. If you are building Riak from source, you will need to install [Basho's patched version of Erlang](https://files.tiot.jp/riak/erlang/otp_src_R16B02-basho10.tar.gz). **If you do not use this version of Erlang, you will not be able to use OpenRiak's [security features][security basics].**

> **Note on Official Support**
>
> Please note that only packaged OpenRiak KV installs are officially supported. Visit [Installing OpenRiak KV][install index] for installing a supported Riak package.

#### Prerequisites

##### Contents

* [kerl](#kerl-prerequisites)
* [Debian/Ubuntu]({{< product-version-root >}}how-to/install/source/)
* [FreeBSD/Solaris]({{< product-version-root >}}how-to/install/source/)
* [Mac OS X](#mac-os-x-prerequisites)
* [RHEL/CentOS]({{< product-version-root >}}how-to/install/source/)

To build and install Erlang you must have a GNU-compatible build system and these tools:

**Unpacking**

* [GNU unzip](http://www.gzip.org/) or a modern uncompressing utility.
* [GNU Tar](http://www.gnu.org/software/tar/) for working with GNU TAR archives.

**Building**

* [autoconf](http://www.gnu.org/software/autoconf/autoconf.html): generates configure scripts.
* [make](http://www.gnu.org/software/make/): generates executables and other non-source files of a program.
* [gcc](https://gcc.gnu.org/): for compiling C.
* [ncurses](http://www.gnu.org/software/ncurses/): for terminal-based interfaces.
* [OpenSSL](https://www.openssl.org/): toolkit that implements SSL and TSL protocols.
* [Java SE JDK](http://www.oracle.com/technetwork/java/javase/downloads/index.html): platform for deploying Java.

#### kerl Prerequisites

[kerl](https://github.com/yrashk/kerl) is the quickest way to install different versions of Erlang on most systems.

Install kerl by running the following command:

```bash
curl -O https://raw.githubusercontent.com/spawngrid/kerl/master/kerl
chmod a+x kerl
```

If you are using Mac OS X, FreeBSD, or Solaris, see the following sections for additional requirements before building with kerl.

Otherwise, continue with [Installing with kerl](#installing-with-kerl).

##### Configuring kerl on FreeBSD/Solaris

Start by by creating a `~/.kerlrc` file:

```bash
touch ~/.kerlrc
```

Next add the following contents to your `~/.kerlrc` file:

```shell
KERL_CONFIGURE_OPTIONS="--disable-hipe --enable-smp-support --enable-threads
                        --enable-kernel-poll --without-odbc"
```

Then check for the presence of autoconf by running:

```shell
which autoconf
```
If this returns `autoconf not found`, install autoconf by running:

```shell
sudo pkg update
sudo pkg install autoconf
```

Once you've configured kerl and installed autoconf continue with [Installing with kerl](#installing-with-kerl).

##### Configuring kerl on Mac OS X

To compile Erlang as 64-bit on Mac OS X you need to instruct kerl to pass the correct flags to the `configure` command.

```shell
KERL_CONFIGURE_OPTIONS="--disable-hipe --enable-smp-support --enable-threads
                        --enable-kernel-poll --without-odbc --enable-darwin-64bit"
```

On OS X 10.9 (Mavericks) or later, you may need to install [autoconf](https://www.gnu.org/software/autoconf/).

Check for the presence of autoconf by running:

```shell
which autoconf
```

If this returns `autoconf not found`, install autoconf with:

With Homebrew:

```shell
brew install autoconf
```

Or with curl:

```shell
curl -O http://ftp.gnu.org/gnu/autoconf/autoconf-2.69.tar.gz
tar zxvf autoconf-2.69.tar.gz
cd autoconf-2.69
./configure && make && sudo make install
```

#### Debian/Ubuntu Prerequisites

##### Dependencies

To install the required dependencies run the following `apt-get` commands:

```bash
sudo apt-get update
sudo apt-get install build-essential autoconf libncurses5-dev openssl libssl-dev fop xsltproc unixodbc-dev git
```

##### GUI Dependencies

If you're using a graphical environment and want to use Erlang's GUI utilities, you will need to install additional dependencies.

> **Note on build output**
>
>These packages are not required for operation of an OpenRiak node.
Notes in the build output about missing support for wxWidgets can be
safely ignored when installing Riak in a typical non-graphical server
environment.

To install packages for graphics support use the following `apt-get` command:

```bash
sudo apt-get install libwxbase2.8 libwxgtk2.8-dev libqt4-opengl-dev
```

##### Next Steps

Once you've installed the prerequisites, continue with [Installing on Debian/Ubuntu]({{< product-version-root >}}how-to/install/source/).

#### FreeBSD/Solaris Prerequisites

##### Dependencies

To install the required dependencies run the following `pkg` command:

```bash
sudo pkg update
sudo pkg install gcc autoconf gmake flex
```

To install packages for graphics support use the following `pkg` command:

```bash
sudo pkg install wx28-gtk2-2.8.12_4
```

##### Next Steps

Once you've installed the prerequisites, continue with [Installing on FreeBSD/Solaris]({{< product-version-root >}}how-to/install/source/).

#### Mac OS X Prerequisites

* [XCode Developer Tools](http://developer.apple.com/) - Apple Software Development Tools.
* [Homebrew](http://brew.sh/) (*optional*) - Package Manager.

First install [XCode Developer Tools](http://developer.apple.com/). XCode is a set software development tools for developing on OS X.

We also recommend installing [Homebrew](http://brew.sh/), a package manager for OS X. Homebrew is not required to install Erlang and is optional.

Next, if you are running OS X 10.9 (Mavericks) or later, you may need to
install [autoconf](https://www.gnu.org/software/autoconf/). To check for
the presence of autoconf run:

```bash
which autoconf
```

With Homebrew:

```bash
brew install autoconf
```

Or with curl:

```bash
curl -O http://ftp.gnu.org/gnu/autoconf/autoconf-2.69.tar.gz
tar zxvf autoconf-2.69.tar.gz
cd autoconf-2.69
./configure && make && sudo make install
```

Once you've installed the prerequisites continue with [Installing on Mac OS X](#installing-on-mac-os-x).

#### RHEL/CentOS Prerequisites

##### Dependencies

To install the required dependencies run the following `yum` command:

```bash
sudo yum install gcc gcc-c++ glibc-devel make ncurses-devel openssl-devel autoconf java-1.8.0-openjdk-devel git
```

To install packages for graphics support use the following `blank` command:

```bash
sudo yum install wxBase.x86_64
```

##### Next Steps

Once you've installed the prerequisites, continue with [Installing on RHEL/CentOS]({{< product-version-root >}}how-to/install/source/).

#### Installation

* [Installing with kerl](#installing-with-kerl)
* [Installing on Debian/Ubuntu]({{< product-version-root >}}how-to/install/source/)
* [Installing on FreeBSD/Solaris]({{< product-version-root >}}how-to/install/source/)
* [Installing on Mac OS X](#installing-on-mac-os-x)
* [Installing on RHEL/CentOS]({{< product-version-root >}}how-to/install/source/)

#### Installing with kerl

First make sure you have installed the necessary dependencies and prerequisites found in [kerl Prerequisites](#kerl-prerequisites).

With [kerl](https://github.com/yrashk/kerl)  installed, you can install Basho's recommended version of
Erlang [from Github](https://github.com/basho/otp) using the following
command:

```bash
./kerl build git git://github.com/basho/otp.git OTP_R16B02_basho10 R16B02-basho10
```

This builds the Erlang distribution and performs all of the steps
required to manually install Erlang for you.

After Erlang is successfully built, you can install the build as follows:

```bash
./kerl install R16B02-basho10 ~/erlang/R16B02-basho10
. ~/erlang/R16B02-basho10/activate
```

The last line activates the Erlang build that was just installed into
`~/erlang/R16B02-basho10`.

> See the kerl [README](https://github.com/yrashk/kerl) for more details on the available commands.

Confirm Erlang installed to the correct location:

```bash
which erl
```

And start Erlang from your terminal with:

```bash
erl
```

#### Installing on Debian/Ubuntu

First make sure you have installed the necessary dependencies found in [Debian/Ubuntu Prerequisites]({{< product-version-root >}}how-to/install/source/).

Next download [Basho's patched version of Erlang](https://files.tiot.jp/riak/erlang/otp_src_R16B02-basho10.tar.gz).

Using `wget`:

```bash
wget https://files.tiot.jp/riak/erlang/otp_src_R16B02-basho10.tar.gz
```

Then unpack the download with:

```bash
tar zxvf otp_src_R16B02-basho10.tar.gz
```

Next `cd` into the unpacked directory, build and install Erlang with:

```bash
cd OTP_R16B02_basho10
./otp_build autoconf
./configure && make && sudo make install
```

```bash
erl
```

#### Installing on FreeBSD/Solaris

First make sure you installed the necessary dependencies in [FreeBSD/Solaris Prerequisites]({{< product-version-root >}}how-to/install/source/).

Next download [Basho's patched version of Erlang](https://files.tiot.jp/riak/erlang/otp_src_R16B02-basho10.tar.gz):

```bash
ftp https://files.tiot.jp/riak/erlang/otp_src_R16B02-basho10.tar.gz
```

```bash
cd OTP_R16B02_basho10
./otp_build autoconf
./configure && gmake && sudo gmake install
```

Confirm Erlang installed to the correct location by running:

```bash
erl
```

#### Installing on Mac OS X

First make sure you have installed the necessary dependencies found in [Mac OS X Prerequisites](#mac-os-x-prerequisites).

You can install Erlang in several ways on OS X:

* [From Source](#installing-on-mac-os-x-from-source)
* [Homebrew](#installing-on-mac-os-x-with-homebrew)
* [MacPorts](#installing-on-mac-os-x-with-macports)

#### Installing on Mac OS X from Source

```bash
curl -O https://files.tiot.jp/riak/erlang/otp_src_R16B02-basho10.tar.gz
```

Follow the steps below to configure Erlang for your operating system.

##### Configuring Erlang on Mavericks (OS X 10.9), Mountain Lion (OS X 10.8), and Lion (OS X 10.7)

If you're on Mavericks (OS X 10.9), Mountain Lion (OS X 10.8), or Lion
(OS X 10.7) you can use LLVM (the default) or GCC to compile Erlang.

Using LLVM:

```bash
CFLAGS=-O0 ./configure --disable-hipe --enable-smp-support --enable-threads \
--enable-kernel-poll --enable-darwin-64bit
```

Or if you prefer GCC:

```bash
CC=gcc-4.2 CPPFLAGS='-DNDEBUG' MAKEFLAGS='-j 3' \
./configure --disable-hipe --enable-smp-support --enable-threads \
--enable-kernel-poll --enable-darwin-64bit
```

###### Configuring Erlang on Snow Leopard (OS X 10.6)

If you're on Snow Leopard (OS X 10.6) or Leopard (OS X 10.5) with an
Intel processor:

```bash
./configure --disable-hipe --enable-smp-support --enable-threads \
--enable-kernel-poll  --enable-darwin-64bit
```

###### Configuring Erlang on older versions of OS X

If you're on a non-Intel processor or older version of OS X:

```bash
./configure --disable-hipe --enable-smp-support --enable-threads \
--enable-kernel-poll
```

After you've configured your system `cd` into the unpacked directory, build and install Erlang with:

```bash
erl
```

#### Installing on Mac OS X with Homebrew

To install Erlang with Homebrew, use this command:

```bash
brew install erlang
```

```bash
erl
```

#### Installing on Mac OS X with MacPorts

Installing with MacPorts:

```bash
port install erlang +ssl
```

```bash
erl
```

#### Installing on RHEL/CentOS

First make sure you have installed the necessary dependencies and prerequisites found in [RHEL/CentOS Prerequisites]({{< product-version-root >}}how-to/install/source/).

Using `wget`:

> **Note for RHEL6/CentOS6**
>
> In certain versions of RHEL6 and CentO6 the `openSSL-devel` package
ships with Elliptical Curve Cryptography partially disabled. To
communicate this to Erlang and prevent compile- and run-time errors, the
environment variable `CFLAGS="-DOPENSSL_NO_EC=1"` needs to be added to
Erlang's `./configure` call.
>
> The full `make` invocation then becomes
>
> ```bash
CFLAGS="-DOPENSSL_NO_EC=1" ./configure && make && sudo make install
```

```bash
erl
```

#### Install Erlang/OTP

Installation guides for different OTP versions are available via erlang.org:

- [OTP 24 Installation Guide](https://www.erlang.org/docs/24/installation_guide/install);
- [OTP 26 Installation Guide](https://www.erlang.org/docs/26/installation_guide/install).

For convenience [`kerl` may be used to simplify the installation of Erlang/OTP](https://github.com/kerl/kerl).

Some points to note when installing Erlang:

- If using OTP 24 take note of [CVE-2022-37026](https://nvd.nist.gov/vuln/detail/CVE-2022-37026).
- Of the optional dependencies for OTP, only OpenSSL is required for Riak.
- The OpenSSL 3.0 integration in OTP 24 is not currently considered to be production-ready and stable.
- If using OpenRiak KV 3.0.16 and OTP 22.3, Riak does not support Erlang/OTP running in [HIPE mode](https://www.erlang.org/docs/22/man/hipe_app).  HIPE is retired as of OTP 24.
- There are significant performance advantages in running Riak on OTP 26, when compared with OTP 24.3.
- The Erlang/OTP team are only committed to fixing issues in the three most recent major versions of Erlang.  Although Erlang 24.3 is mature and very stable, migrating forward to a Riak release running on a presently supported Erlang version is recommended.
- It is not possible to [migrate directly using a rolling restart]({{< product-version-root >}}how-to/operate/upgrade-cluster/) from OpenRiak KV 3.0 to OpenRiak KV 3.4 due to breaking changes in the Erlang distribution protocol.  Migrating directly between these versions with zero down-time can only be managed using [the cluster migration strategy]({{< product-version-root >}}how-to/configure/replication/migrate-cluster/).

#### Make Riak

There are three basic approaches to building Riak once the repository has been cloned, a tag or branch has been selected, and the dependencies have been installed: a local release, a local cluster or generating a package.

#### Local release

To create a local release, run `make rel`.  This will build a release of Riak in the `rel/riak` folder within the repository clone.  This can be configured, started and joined into a cluster as with any Riak node.

#### Local cluster

To create a local development cluster, which is ideal for experimenting with Riak, run `make devclean; make devrel`.  This will clean and rebuild a group of 8 Riak instances in the `dev/dev<n>` folder within the repository clone.

#### Generating a package

To generate a package, running `make package` will build a package for the current local platform.  This can then be deployed to another server of that type using the standard package management tool (e.g. `dpkg` on debian systems).

- Running `make package` will require the local machine to have appropriate build tools installed;
- The `make package` process will output WARNING level errors during the `make package` process;
- The underlying information used as part of `make package` can be in the [`pkg` section](https://github.com/OpenRiak/riak/tree/openriak-3.4/rel/pkg) of the Riak repository.

#### Starting Riak by Make Method

Starting Riak changes depending on how Riak was made - a [local release]({{< product-version-root >}}how-to/install/source/) or [local development cluster]({{< product-version-root >}}tutorials/first-cluster/), or through [package deployment]({{< product-version-root >}}how-to/operate/start-stop-restart-node/).  In all cases Riak is released using [the relx release generator](https://rebar3.org/docs/deployment/releases/), and inherits the control commands from the `relx` extended start script; but the location and method for accessing that script will vary.

## Verify the result

Confirm the installed version on every node, wait for services and transfers to settle, and run application smoke tests before proceeding.
