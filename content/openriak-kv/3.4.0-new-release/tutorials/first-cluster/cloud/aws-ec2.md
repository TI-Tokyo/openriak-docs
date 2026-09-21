---
title: Build a learning cluster on AWS EC2
description: Run the five-node Docker learning cluster on an AWS EC2 instance and access it through an SSH tunnel.
  You will create and remove the AWS resources yourself. All five database nodes share one VM in this lesson; they
  do no
weight: 30
diataxis: tutorial
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- new-operators
source_material:
- proposed-kv
tags:
- diataxis
- kv
- tutorial
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- tutorials/first-cluster/cloud.md
related:
- tutorials/first-cluster/build-and-explore-a-docker-cluster
- how-to/performance/tune-a-deployment-on-aws
- how-to/security/restrict-client-node-and-administrative-network-access
- how-to/planning-a-deployment/size-a-cluster-and-reserve-recovery-headroom
- foundations/overview/what-openriak-kv-is
- foundations/cluster-architecture/rings-partitions-and-virtual-nodes
---

Run the five-node Docker learning cluster on an AWS EC2 instance and access it through an SSH tunnel. You will create and remove the AWS resources yourself. All five database nodes share one VM in this lesson; they do not provide availability across EC2 instances or Availability Zones.

## Prepare your AWS workspace

You need an AWS account with permission to create an EC2 instance, its security group, and an EBS root volume, plus an SSH client and Docker familiarity. Select one Region and record it. These resources incur charges while they exist, including retained disks after the instance stops.

In the EC2 console, launch an Ubuntu Server 24.04 LTS instance from Canonical's verified publisher. Select x86_64 for this lesson, at least 4 vCPUs and 16 GiB RAM, and a 40 GiB encrypted gp3 root disk. These are lab allocations, not production sizing guidance. Record the AMI ID, instance type, subnet, instance ID, and volume ID so the setup can be reproduced.

Choose a subnet with the outbound internet access needed for package and image downloads. Create a dedicated security group with inbound SSH from your current public IP only. Do not expose the database ports publicly. Choose or create an SSH key pair whose private key you control. Review the root volume's **Delete on termination** setting before launching. See [AWS instance launch parameters](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-instance-launch-parameters.html) for the console fields.

## Connect and prepare Docker

Replace `INSTANCE_ADDRESS` and the key filename with your values:

```sh
chmod 600 learning-ec2.pem
ssh -i learning-ec2.pem ubuntu@INSTANCE_ADDRESS
```

On the instance, install Docker Engine and the Compose plugin using [Docker's Ubuntu installation instructions](https://docs.docker.com/engine/install/ubuntu/). Verify that `docker compose version` succeeds under the user that will run the lab. If your installation requires `sudo`, use it consistently for the Compose commands.

## Build the learning cluster

Complete [Build and explore a Docker cluster]({{< product-version-root >}}tutorials/first-cluster/build-and-explore-a-docker-cluster/) on the EC2 instance. Download the version-matched Compose and environment files there, keep their HTTP and PB ports bound to `127.0.0.1`, and store the bind-mounted data on the instance's EBS filesystem.

Wait for five valid members, select the lesson's Leveled backend before writing data, and run its greeting write/read. Run these checks on the instance first; a failed database request there cannot be fixed by an SSH tunnel.

## Read from your laptop

Open a second local terminal and leave this tunnel running:

```sh
ssh -N -i learning-ec2.pem -L 18098:127.0.0.1:18098 ubuntu@INSTANCE_ADDRESS
```

In another local terminal:

```sh
curl --fail http://127.0.0.1:18098/ping
curl --fail http://127.0.0.1:18098/buckets/learning/keys/greeting
```

Expect `OK` and `Hello OpenRiak`. If local port 18098 is already occupied, use a different local tunnel port and change the curl URL to match. Keep the EC2 database ports private.

## Remove the resources

On the instance, run `docker compose down` in the lab directory. Close the SSH tunnel. Terminate the exact instance recorded earlier, then check that its root volume was deleted. Delete any retained lab volumes or snapshots you deliberately created, release any lab Elastic IP, and remove the unused lab security group and key pair. Do not delete shared account resources. [AWS termination behaviour](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/how-ec2-instance-termination-works.html) describes what termination removes and what can remain.
