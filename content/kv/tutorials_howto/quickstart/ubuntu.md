---
sidebar_position: 2
title: Quick Start using Ubuntu
sidebar_label: "Use Ubuntu"
date: 2025-09-16
---
import { ConfigReferenceProvider } from '@site/src/components/ConfigReference/ConfigReferenceContext';
import { ConfigListing }             from '@site/src/components/ConfigReference/ConfigListing';
import { ConfigDefaultValue }      from '@site/src/components/ConfigReference/ConfigDefaultValue';
import InlineCodeWithCopy          from '@site/src/components/InlineCodeWithCopy/InlineCodeWithCopy';
[root site]: [!site]
[root project]: [!project]
[root version]: [!version]
[ubuntu]: #a-ubuntu-based-dev-cluster
[assumptions]: #assumptions
[settings]: #settings
[install]: #installing-openriak
[firstsetup]: #setting-openriak-up-for-the-first-time
[joining]: #joining-the-nodes-together
[nextsteps]: #next-steps
[leveled]: ../../configure/guides/backends/configure-leveled

## A ubuntu based dev cluster

This quickp-start guide is aimed at getting a local five-node cluster of OpenRiak KV for local testing and development.


## Assumptions

  1. You have a blank [Ubuntu][ubuntu] installation.
  2. You want a single five node cluster for testing and development purposes only.
  3. You want dont care about specific configurations or advanced features

## Settings

  1. We will use Ubuntu 24.04 as our operating system.
  2. We will use OpenRiak KV version 3.2.5.
  3. We will use [Leveled][leveled] as our backend.
  4. We will turn on the TicTac Active Anti-Entropy (TicTac AAE) feature.
  5. We will turn on the Store Heads feature.
  6. We will make both Web (HTTP) and Protocol Buffer API interfaces available.
  7. We will listen on `127.0.0.1` on the default ports (`8098` for web and `8087` for Protocol Buffers).

## Installing OpenRiak

  1. From a terminal window download the Riak pack with the following:

  ```bash
    wget https://files.tiot.jp/riak/kv/3.2/3.2.5/ubuntu/noble64/riak_3.2.5-OTP25_amd64.deb
  ```

  2. In the same terminal window, run `dpkg -i riak_3.2.5-OTP25_amd64.deb` to install the Riak package, answering any prompts in the process.

## Setting OpenRiak up for the first time

  1. Next we need to make some changes to the `riak.conf` file, so we will change to that directory with `cd /etc/riak/`

  2. Open the `riak.conf` file using your preferred editor. In this case, we are using Nano, but you can use any.

Once we have the file open, we need to adjust the following configuration values:

>[!NOTE]Note on configuration values
>The Node name should include the address that this node is reachable at. For this example we'll use variations of 127.0.0.x, but you should confirm your nodes external IP address.

  3. For the `nodename` section, we will change the name to our nodes IP. For this example, we are `nodename = riak@172.0.0.10`.

>[!NOTE]Note on renaming nodes
>It is important that you *only* change the section of the node name after the `riak@` part of the nodename. If you remove `riak@` from the name, then the node will be unreachable.

  * Change the value of `anti_entropy` from `active` to `passive`

  * Change the value of `storage_backend` to `leveled`

  * Change the value of `tictacaae_active` to `active`

  * Change the value of `tictacaae_storeheads` to `enabled`

Then save and exit.

  4. Once you have made the above changes, you should be able to start your first node with `riak start`

>[!NOTE] Note on Verifying install
>Once the node has been installed, we recommend verifying the node is able to start and respond to requests by following the steps [here](: ../../setup/install/verify).

  1. Repeat thse steps for each of the nodes in your cluster.

## Joining the nodes together

  1. You will need to make the same changes on each of the next 4 nodes to prepare them to join together.

  2. On each nodes *except* the first node, run `riak admin cluster join <riak@172.0.0.10> (replacing the IP address with the one for your first node).

You should see an output like below:

  ```bash
    Success: staged join request for 'riak@127.0.0.2' to 'riak@127.0.0.1
  ```

  3. After performing this on all the nodes, from any node run `riak admin cluster plan`. You should see a similar output to below:

  ```bash
    =============================== Staged Changes ================================
    Action         Details(s)
    -------------------------------------------------------------------------------
    join           'riak@127.0.0.2'
    join           'riak@127.0.0.3'
    join           'riak@127.0.0.4'
    join           'riak@127.0.0.5'
    -------------------------------------------------------------------------------


    NOTE: Applying these changes will result in 1 cluster transition

    ###############################################################################
                             After cluster transition 1/1
    ###############################################################################

    ================================= Membership ==================================
    Status     Ring    Pending    Node
    -------------------------------------------------------------------------------
    valid     100.0%     20.3%    'riak@127.0.0.1'
    valid       0.0%     20.3%    'riak@127.0.0.2'
    valid       0.0%     20.3%    'riak@127.0.0.3'
    valid       0.0%     20.3%    'riak@127.0.0.4'
    valid       0.0%     18.8%    'riak@127.0.0.5'
    -------------------------------------------------------------------------------
    Valid:5 / Leaving:0 / Exiting:0 / Joining:0 / Down:0

    Transfers resulting from cluster changes: 51
      13 transfers from 'riak@172.17.0.2' to 'riak@172.17.0.4'
      13 transfers from 'riak@172.17.0.2' to 'riak@172.17.0.3'
      12 transfers from 'riak@172.17.0.2' to 'riak@172.17.0.6'
      13 transfers from 'riak@172.17.0.2' to 'riak@172.17.0.5'
  ```

  4. You will need to wait for transfers to complete before the joining is finished. This can be done with the `riak admin transfers` command, which outputs the following when no transfers are active:

  ```bash
    No transfers active

    Active Transfers:
  ```

### Next Steps

That's it! you've now got a fully functional 5 node OpenRiak KV cluster operational. You can now add data and perform other functions as you wish.