---
sidebar_position: 2
title: Quick Start using Vagrant
sidebar_label: "Use Vagrant"
date: 2025-11-07
---

[root site]: [!site]
[root project]: [!project]
[root version]: [!version]
[options]: #dev-cluster-options
[vagrantubuntu]: #a-vagrant-ubuntu-based-dev-cluster
[vagrantrocky]: #a-vagrant-rocky-linux-based-dev-cluster

# Dev cluster options

In this guide we will be providing two guides for building quick 5 node dev clusters. One cluster is Ubuntu based, the other is Rocky Linux.

# A vagrant-ubuntu based dev cluster

This quickp-start guide is aimed at getting a local five-node cluster of OpenRiak KV for local testing and development.


## Assumptions in a Ubuntu-based cluster

  1. You want a single five node cluster for testing and development purposes only.
  2. You want dont care about specific configurations or advanced features

## Settings

  1. We will use Ubuntu 24.04 as our operating system.
  2. We will use OpenRiak KV version 3.2.5.
  3. We will use [Leveled][leveled] as our backend.
  4. We will turn on the TicTac Active Anti-Entropy (TicTac AAE) feature.
  5. We will turn on the Store Heads feature.

## Creating the Vagrant file and the first node

>[!NOTE] Note on values used in this documentation
>In this documentation we will be using the following Node names and placeholder IP addresses:
>Riak1 - 127.0.0.1
>Riak2 - 127.0.0.2
>Riak3 - 127.0.0.3
>Riak4 - 127.0.0.4
>Riak5 - 127.0.0.5
>
>You should ensure that you correct replace all the IP addresses with the appropriate range for your test system and replace the Node Names if you wish for system-relevant names.

1. First, we need to create the basic outline for our first node, which requires the following:

  ```ruby
    # -*- mode: ruby -*-
    # vi: set ft=ruby :

    Vagrant.configure("2") do |config|

      ##########
      # Riak 1 #
      ##########
      config.vm.define "riak1" do |riak|
        riak.vm.box = "ubuntu/jammy64"
        riak.vm.hostname = "riak1"
        riak.vm.network :private_network, ip: "127.0.0.1"

        riak.vm.provider :virtualbox do |v|
        v.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
        v.customize ["modifyvm", :id, "--memory", 1024]
        v.customize ["modifyvm", :id, "--name", "riak1"]
        end

        riak.vm.provision "shell", inline: <<-SHELL
  ```

In this setion we have defined the Vagrant box name "riak1", the Operating system and version (Ubuntu/jammy64), enabled networking, defined the IP address for the box and assined a maximum memory value.

2. Next we need to fetch the required OpenRiak package and set a shared directory so we can easily move files from the host system to the Vagrant machine and vice-versa:

  ```ruby
    set -e
    wget -q https://files.tiot.jp/riak/kv/3.4/3.4.0/ubuntu/jammy64/riak_3.4.0-OTP26_amd64.deb
    cp riak* /vagrant/data
  ```

3. Then install OpenRiak and set Nodename, listener IPs and the various OpenRiak config options we listed above, plus setting the nofile limits required for smooth OpenRiak operation:

  ```ruby
    # Install Riak
    sudo dpkg -i riak_3.4.0-OTP26_amd64.deb || sudo apt-get -f install -y

    # Adjust riak.config values for Nodename, listener IPs.
    sudo sed -i "s/nodename = riak@127.0.0.1/nodename = riak@192.168.56.20/" /etc/riak/riak.conf
    sudo sed -i "s/listener.http.internal = 127.0.0.1:8098/listener.http.internal = 192.168.56.20:8098/" /etc/riak/riak.conf

    # Disable Active Entropy, and enable Tictac AAE and change backend to leveled
    sudo sed -i "s/anti_entropy = active/anti_entropy = passive/" /etc/riak/riak.conf
    sudo sed -i "s/storage_backend = bitcask/storage_backend = leveled/" /etc/riak/riak.conf
    sudo sed -i "s/tictacaae_active = passive/tictacaae_active = active/" /etc/riak/riak.conf
    sudo rm -rf /tmp/erl_pipes

    # OS tweak for better Riak performance
    echo "* soft nofile 65536" | sudo tee -a /etc/security/limits.conf
    echo "* hard nofile 65536" | sudo tee -a /etc/security/limits.conf
  ```

This section will out put the following to the console:

  ```bash
    # Set nofile limits
    riak1: * soft nofile 65536
    riak1: * hard nofile 65536
  ```
4. Now we can set OpenRiak to start, and check that it is running before moving onto our second node.

  ```ruby
    echo "Starting OpenRiak"
    sudo riak chkconfig
    echo "Config checked"
    sudo -n riak start
    echo "OpenRiak has been started"
    sudo riak ping
    SHELL
    end
  ```

If you want to run a single node, this example will work, as once you see following output from the console, the machine has been built & can be interacted with:

  ```bash
    riak1: pong
  ```

We do not recommend a single node development cluster as this will not compare to real world performance and may lead to some odd behaviour. The minimum we would recommend is three nodes, with 5 being optimal for testing.

# Creating additional nodes
Now that we've completed these steps, we can repeat them for the next node three, with the addition of a function to join the node to the first node:

  ```ruby 
    ##########
    # Riak 2 #
    ##########
    config.vm.define "riak2" do |riak|
    riak.vm.box = "ubuntu/jammy64"
    riak.vm.hostname = "riak2"
    riak.vm.network :private_network, ip: "127.0.0.2"

    riak.vm.provider :virtualbox do |v|
      v.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
      v.customize ["modifyvm", :id, "--memory", 1024]
      v.customize ["modifyvm", :id, "--name", "riak2"]
    end

    riak.vm.provision "shell", inline: <<-SHELL
    set -e
    wget -q https://files.tiot.jp/riak/kv/3.4/3.4.0/ubuntu/jammy64/riak_3.4.0-OTP26_amd64.deb
    cp riak* /vagrant/data

    # Install Riak
    sudo dpkg -i riak_3.4.0-OTP26_amd64.deb || sudo apt-get -f install -y

    # Adjust the node name, Listener IPs, enabled
    sudo sed -i "s/nodename = riak@127.0.0.1/nodename = riak@127.0.0.2/" /etc/riak/riak.conf
    sudo sed -i "s/listener.http.internal = 127.0.0.1:8098/listener.http.internal = 127.0.0.2:8098/" /etc/riak/riak.conf
    sudo sed -i "s/anti_entropy = active/anti_entropy = passive/" /etc/riak/riak.conf
    sudo sed -i "s/TicTacanti_entropy = active/anti_entropy = passive/" /etc/riak/riak.conf
    sudo sed -i "s/storage_backend = bitcask/storage_backend = leveled/" /etc/riak/riak.conf
    sudo rm -rf /tmp/erl_pipes

    # OS tweak for better Riak performance
    echo "* soft nofile 65536" | sudo tee -a /etc/security/limits.conf
    echo "* hard nofile 65536" | sudo tee -a /etc/security/limits.conf

    echo "Starting OpenRiak"
    sudo riak chkconfig
    echo "Config checked"
    sudo -n riak start
    echo "OpenRiak has been started"
    sudo riak ping
    echo "Joining cluster plan"
    sleep 20
    sudo riak admin cluster join riak@127.0.0.1
  SHELL
    end
  ```

This section can be repeated for nodes 2, 3 and 4.

We've added a function for the command line to wait 20 seconds before running `riak admin cluster join` as this allows for OpenRiak to fully start on the backend, otherwise this function will fail.


## Adding the final node and joining all the nodes together

The final node creation process also includes the following commands:

```bash
sudo riak admin cluster plan
sudo riak admin cluster commit
```

These commands output a check of the cluster plan (nodes 2,3,4 and 5 all joining node 1), then commits the plan so that the process can begin.

  ```ruby
    ##########
    # Riak 5 #
    ##########
    config.vm.define "riak5" do |riak|
      riak.vm.box = "ubuntu/jammy64"
      riak.vm.hostname = "riak5"
      riak.vm.network :private_network, ip: "127.0.0.5"

      riak.vm.provider :virtualbox do |v|
        v.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
        v.customize ["modifyvm", :id, "--memory", 1024]
        v.customize ["modifyvm", :id, "--name", "riak5"]
      end

      riak.vm.provision "shell", inline: <<-SHELL
    set -e
    wget -q https://files.tiot.jp/riak/kv/3.4/3.4.0/ubuntu/jammy64/riak_3.4.0-OTP26_amd64.deb
    cp riak* /vagrant/data

    # Install Riak
    sudo dpkg -i riak_3.4.0-OTP26_amd64.deb || sudo apt-get -f install -y
    sudo sed -i "s/nodename = riak@127.0.0.1/nodename = riak@127.0.0.5/" /etc/riak/riak.conf
    sudo sed -i "s/listener.http.internal = 127.0.0.1:8098/listener.http.internal = 127.0.0.5:8098/" /etc/riak/riak.conf
    sudo sed -i "s/anti_entropy = active/anti_entropy = passive/" /etc/riak/riak.conf
    sudo sed -i "s/storage_backend = bitcask/storage_backend = leveled/" /etc/riak/riak.conf
    sudo rm -rf /tmp/erl_pipes

    # OS tweak for better Riak performance
    echo "* soft nofile 65536" | sudo tee -a /etc/security/limits.conf
    echo "* hard nofile 65536" | sudo tee -a /etc/security/limits.conf

    echo "Starting OpenRiak"
    sudo riak chkconfig
    echo "Config checked"
    sudo -n riak start
    echo "OpenRiak has been started"
    sudo riak ping
    echo "Joining cluster plan"
    sleep 20
    sudo riak admin cluster join riak@127.0.0.1
    sudo riak admin cluster plan
    sudo riak admin cluster commit
    echo "Cluster built and joined!"
    SHELL
    end
  end
  ```

When the final node has been built, the console will output "riak5: Cluster built and joined!" to indicate all tasks are complete.

# Next Steps

That's it! you've now got a fully functional 5 node OpenRiak KV Ubuntu-based cluster operational. You can now add data and perform other functions as you wish.

# A vagrant-rocky linux based dev cluster

This quickp-start guide is aimed at getting a local five-node cluster of OpenRiak KV for local testing and development.


## Assumptions in a rocky-based cluster

  1. You want a single five node cluster for testing and development purposes only.
  2. You want dont care about specific configurations or advanced features

## Settings

  1. We will use Rocky Linux 10 as our operating system.
  2. We will use OpenRiak KV version 3.2.5.
  3. We will use [Leveled][leveled] as our backend.
  4. We will turn on the TicTac Active Anti-Entropy (TicTac AAE) feature.
  5. We will turn on the Store Heads feature.

## Creating the Vagrant file and the first node

>[!NOTE] Note on values used in this documentation
>In this documentation we will be using the following Node names and placeholder IP addresses:
>Riak1 - 127.0.0.1
>Riak2 - 127.0.0.2
>Riak3 - 127.0.0.3
>Riak4 - 127.0.0.4
>Riak5 - 127.0.0.5
>
>You should ensure that you correct replace all the IP addresses with the appropriate range for your test system and replace the Node Names if you wish for system-relevant names.

1. First, we need to create the basic outline for our first node, which requires the following:

```ruby
# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|

  ##########
  # Riak 1 #
  ##########
  config.vm.define "riak1" do |riak|
    riak1.vm.box = "generic/rocky9"
    config.vm.box_version = "4.3.12"
    riak.vm.hostname = "riak1"
    riak.vm.network :private_network, ip: "127.0.0.1"

    riak.vm.provider :virtualbox do |v|
      v.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
      v.customize ["modifyvm", :id, "--memory", 1024]
      v.customize ["modifyvm", :id, "--name", "riak1"]
    end

    riak.vm.provision "shell", inline: <<-SHELL
```

In this setion we have defined the Vagrant box name "riak1", the Operating system and version (Ubuntu/jammy64), enabled networking, defined the IP address for the box and assined a maximum memory value.

2. Next we need to fetch the required OpenRiak package and set a shared directory so we can easily move files from the host system to the Vagrant machine and vice-versa:

  ```ruby
    set -e
    wget https://files.tiot.jp/riak/kv/3.2/3.2.5/oracle/9/riak-3.2.5.OTP25-1.el9.x86_64.rpm
    cp riak* /vagrant/data
  ```

3. Then install OpenRiak and set Nodename, listener IPs and the various OpenRiak config options we listed above, plus setting the nofile limits required for smooth OpenRiak operation:

  ```ruby
    # Install Riak
    sudo yum install -y riak-3.2.5.OTP25-1.el9.x86_64.rpm

    # Adjust riak.config values for Nodename, listener IPs.
    sudo sed -i "s/nodename = riak@127.0.0.1/nodename = riak@192.168.56.20/" /etc/riak/riak.conf
    sudo sed -i "s/listener.http.internal = 127.0.0.1:8098/listener.http.internal = 192.168.56.20:8098/" /etc/riak/riak.conf

    # Disable Active Entropy, and enable Tictac AAE and change backend to leveled
    sudo sed -i "s/anti_entropy = active/anti_entropy = passive/" /etc/riak/riak.conf
    sudo sed -i "s/storage_backend = bitcask/storage_backend = leveled/" /etc/riak/riak.conf
    sudo sed -i "s/tictacaae_active = passive/tictacaae_active = active/" /etc/riak/riak.conf
    sudo rm -rf /tmp/erl_pipes

    # OS tweak for better Riak performance
    echo "* soft nofile 65536" | sudo tee -a /etc/security/limits.conf
    echo "* hard nofile 65536" | sudo tee -a /etc/security/limits.conf
  ```

This section will out put the following to the console:

  ```bash
    # Set nofile limits
    riak1: * soft nofile 65536
    riak1: * hard nofile 65536
  ```

4. Now we can set OpenRiak to start, and check that it is running before moving onto our second node.

  ```ruby
    echo "Starting OpenRiak"
    sudo riak chkconfig
    echo "Config checked"
    sudo -n riak start
    echo "OpenRiak has been started"
    sudo riak ping
    SHELL
    end
  ```

If you want to run a single node, this example will work, as once you see following output from the console, the machine has been built & can be interacted with:

  ```bash
    riak1: pong
  ```

We do not recommend a single node development cluster as this will not compare to real world performance and may lead to some odd behaviour. The minimum we would recommend is three nodes, with 5 being optimal for testing.

# Creating additional nodes

Now that we've completed these steps, we can repeat them for the next node three, with the addition of a function to join the node to the first node:

  ```ruby 
    ##########
    # Riak 2 #
    ##########
    config.vm.define "riak2" do |riak|
      riak.vm.box = "ubuntu/jammy64"
      riak.vm.hostname = "riak2"
      riak.vm.network :private_network, ip: "127.0.0.2"

      riak.vm.provider :virtualbox do |v|
      v.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
      v.customize ["modifyvm", :id, "--memory", 1024]
      v.customize ["modifyvm", :id, "--name", "riak2"]
      end

    riak.vm.provision "shell", inline: <<-SHELL
    set -e
    wget -q https://files.tiot.jp/riak/kv/3.4/3.4.0/ubuntu/jammy64/riak_3.4.0-OTP26_amd64.deb
    cp riak* /vagrant/data

    # Install Riak
    sudo yum install -y riak-3.2.5.OTP25-1.el9.x86_64.rpm

    # Adjust the node name, Listener IPs, enabled
    sudo sed -i "s/nodename = riak@127.0.0.1/nodename = riak@127.0.0.2/" /etc/riak/riak.conf
    sudo sed -i "s/listener.http.internal = 127.0.0.1:8098/listener.http.internal = 127.0.0.2:8098/" /etc/riak/riak.conf
    sudo sed -i "s/anti_entropy = active/anti_entropy = passive/" /etc/riak/riak.conf
    sudo sed -i "s/TicTacanti_entropy = active/anti_entropy = passive/" /etc/riak/riak.conf
    sudo sed -i "s/storage_backend = bitcask/storage_backend = leveled/" /etc/riak/riak.conf
    sudo rm -rf /tmp/erl_pipes

    # OS tweak for better Riak performance
    echo "* soft nofile 65536" | sudo tee -a /etc/security/limits.conf
    echo "* hard nofile 65536" | sudo tee -a /etc/security/limits.conf

    echo "Starting OpenRiak"
    sudo riak chkconfig
    echo "Config checked"
    sudo -n riak start
    echo "OpenRiak has been started"
    sudo riak ping
    echo "Joining cluster plan"
    sleep 20
      sudo riak admin cluster join riak@127.0.0.1
    SHELL
    end
  ```

This section can be repeated for nodes 2, 3 and 4.

We've added a function for the command line to wait 20 seconds before running `riak admin cluster join` as this allows for OpenRiak to fully start on the backend, otherwise this function will fail.


## Adding the final node and joining all the nodes together

The final node creation process also includes the following commands:

  ```bash
    sudo riak admin cluster plan
    sudo riak admin cluster commit
  ```

These commands output a check of the cluster plan (nodes 2,3,4 and 5 all joining node 1), then commits the plan so that the process can begin.

  ```ruby
    ##########
    # Riak 5 #
    ##########
    config.vm.define "riak5" do |riak|
      riak.vm.box = "ubuntu/jammy64"
      riak.vm.hostname = "riak5"
      riak.vm.network :private_network, ip: "127.0.0.5"

      riak.vm.provider :virtualbox do |v|
    v.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
    v.customize ["modifyvm", :id, "--memory", 1024]
    v.customize ["modifyvm", :id, "--name", "riak5"]
    end

      riak.vm.provision "shell", inline: <<-SHELL
    set -e
    wget -q https://files.tiot.jp/riak/kv/3.4/3.4.0/ubuntu/jammy64/riak_3.4.0-OTP26_amd64.deb
    cp riak* /vagrant/data

    # Install Riak
    sudo yum install -y riak-3.2.5.OTP25-1.el9.x86_64.rpm
  cp riak* /vagrant/data

    # install riak
    sudo sed -i "s/nodename = riak@127.0.0.1/nodename = riak@127.0.0.5/" /etc/riak/riak.conf
    sudo sed -i "s/listener.http.internal = 127.0.0.1:8098/listener.http.internal = 127.0.0.5:8098/" /etc/riak/riak.conf
    sudo sed -i "s/anti_entropy = active/anti_entropy = passive/" /etc/riak/riak.conf
    sudo sed -i "s/TicTacanti_entropy = active/anti_entropy = passive/" /etc/riak/riak.conf
    sudo sed -i "s/storage_backend = bitcask/storage_backend = leveled/" /etc/riak/riak.conf
    sudo rm -rf /tmp/erl_pipes

    # OS tweak for better Riak performance
    echo "* soft nofile 65536" | sudo tee -a /etc/security/limits.conf
    echo "* hard nofile 65536" | sudo tee -a /etc/security/limits.conf

    echo "Starting OpenRiak"
    sudo riak chkconfig
    echo "Config checked"
    sudo -n riak start
    echo "OpenRiak has been started"
    sudo riak ping
    echo "Joining cluster plan"
    sleep 20
    sudo riak admin cluster join riak@127.0.0.1
    sudo riak admin cluster plan
    sudo riak admin cluster commit
    echo "Cluster built and joined!"
    SHELL
      end
  end
  ```

When the final node has been built, the console will output "riak5: Cluster built and joined!" to indicate all tasks are complete.

# Next Steps

That's it! you've now got a fully functional 5 node OpenRiak KV Rocky-linux cluster operational. You can now add data and perform other functions as you wish.