---
title: 'Install OpenRiak on Amazon Linux'
description: 'Show operators how to install openriak on amazon linux and confirm that the installation is ready.'
weight: 3
diataxis: 'how-to'
product: 'OpenRiak KV'
product_version: '3.4.1'
status: 'editorially-rewritten'
draft: true
audience:
  - 'operators'
source_material:
  - 'legacy-3.2.5'
  - 'live-3.2.5'
  - 'proposed-kv'
migration_source_root: '\\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv'
migration_sources:
  - '\\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv\setup\install\linux\amazon-linux.md'
migration_review:
  - 'Internal links still refer to the earlier documentation hierarchy and must be retargeted to the Diátaxis paths.'
  - 'Release-specific installation, upgrade, downgrade, or quick-start instructions require verification against OpenRiak KV 3.4.1 packages.'
legacy_3_2_5_sources:
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\setup\installing\amazon-web-services.md'
  - 'Package, platform, installation, upgrade, or downgrade details require release-specific verification for OpenRiak KV 3.4.1.'
tags: ['diataxis', 'kv', 'how-to']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Show operators how to install openriak on amazon linux and confirm that the installation is ready.

## Before you begin

A supported operating system and package source, verified backups, release notes for the exact target version, and a rolling-change plan for production clusters.

## Overview

### Amazon Web Services

#### Launching Riak VMs via the AWS Marketplace

**Note**
The AWS Marketplace does not always have the most recent versions of Riak available. To use the latest version of Riak, please refer to the [Installing from Package](#installing-from-package) section underneath.

In order to launch a Riak virtual machine via the AWS Marketplace, you will first need to sign up for an [Amazon Web Services](http://aws.amazon.com) account.

1. Navigate to [https://aws.amazon.com/marketplace/](https://aws.amazon.com/marketplace/) and sign in with your Amazon Web Services account.

2. Locate Riak in the **Databases & Caching** category or search for Riak from any page.

3. Set your desired AWS region, EC2 instance type, firewall settings, and key pair

![AWS Marketplace Instance Settings]({{< baseurl >}}images/aws-marketplace-settings.png)

4. Click the **Accept Terms and Launch with 1-Click** button.

##### Security Group Settings

Once the virtual machine is created, you should verify that your selected EC2 security group is properly configured for Riak.

1. In the AWS EC2 Management Console, click **Security Groups**, then click the name of the security group for your Riak VM.

2. Click on the **Inbound** tab in the lower pane.  Your security group should include the following open ports:

* 22 (SSH)
  * 8087 (Riak Protocol Buffers Interface)
  * 8098 (Riak HTTP Interface)

3. You will need to add additional rules within this security group to allow your Riak instances to communicate.  For each port range below, create a new **Custom TCP rule** with the source set to the current security group ID (found on the **Details** tab).

* Port range: 4369
  * Port range: 6000-7999
  * Port range: 8099

4. When complete, your security group should contain all of the rules listed below. If you are missing any rules, add them in the lower panel and then click the **Apply Rule Changes** button.

![EC2 Security Group Settings]({{< baseurl >}}images/aws-marketplace-security-group.png)

We also recommend that you read more about OpenRiak's [Security and Firewalls]({{< baseurl >}}kv/3.4.1/how-to/secure/).

#### Clustering Riak on AWS

You will need need to launch at least 3 instances to form an OpenRiak cluster.  When the instances have been provisioned and the security group is configured, you can connect to them using SSH or PuTTY as the ec2-user.

You can find more information on connecting to an instance on the official [Amazon EC2 instance guide](http://docs.amazonwebservices.com/AWSEC2/latest/UserGuide/AccessingInstances.html).

**Note**
The following clustering setup will _not_ be resilient to instance restarts
unless deployed in Amazon VPC.

**Note on Package Based Installation**
 If installing to AWS by package, further configuration to _riak.conf_ to set the node name and listening IP addresses is necessary for the below steps to function.

1. On the first node, obtain the internal IP address:

```bash
    curl http://169.254.169.254/latest/meta-data/local-ipv4
    ```

2. For all other nodes, use the internal IP address of the first node:

```bash
    sudo riak admin cluster join riak@<ip.of.first.node>
    ```

3. After all of the nodes are joined, execute the following:

```bash
    sudo riak admin cluster plan
    ```

If this looks good:

```bash
    sudo riak admin cluster commit
    ```

To check the status of clustering use:

```bash
    sudo riak admin member_status
    ```

You now have an OpenRiak cluster running on AWS.

#### Installing From Package

##### Amazon Linux 2023 (x86_64)

All published OpenRiak KV 3.4.1 Amazon Linux packages use OTP 26. Install the
x86_64 package using `yum`:

```bash
wget https://files.tiot.jp/riak/kv/3.4/3.4.1/amazon/2023%20%28x86_64%29/riak-3.4.1.OTP26-1.amzn2023.x86_64.rpm
sudo yum localinstall -y riak-3.4.1.OTP26-1.amzn2023.x86_64.rpm
```

Or you can install the `.rpm` package manually:

```bash
wget https://files.tiot.jp/riak/kv/3.4/3.4.1/amazon/2023%20%28x86_64%29/riak-3.4.1.OTP26-1.amzn2023.x86_64.rpm
sudo rpm -i riak-3.4.1.OTP26-1.amzn2023.x86_64.rpm
```

##### Amazon Linux 2023 (ARM64)

Use the package matching the Graviton generation of the EC2 instance:

```bash
# Graviton2
wget https://files.tiot.jp/riak/kv/3.4/3.4.1/amazon/2023%20%28graviton2%29/riak-3.4.1.OTP26-1.amzn2023.aarch64.rpm

# Graviton3
wget https://files.tiot.jp/riak/kv/3.4/3.4.1/amazon/2023%20%28graviton3%29/riak-3.4.1.OTP26-1.amzn2023.aarch64.rpm

sudo yum localinstall -y riak-3.4.1.OTP26-1.amzn2023.aarch64.rpm
```

#### Next Steps

Now that Riak is installed and you have set the [Security Group Settings](#security-group-settings), check out [Verifying a Riak Installation][install verify].

> [!WARNING]
> Migration review required: Internal links still refer to the earlier documentation hierarchy and must be retargeted to the Diátaxis paths.

## Verify the result

Confirm the installed version on every node, wait for services and transfers to settle, and run application smoke tests before proceeding.
