---
title: "Reviving the Zombie App for OSCON"
date: "2015-07-20T14:42:26+00:00"
author: "Stephen Condon"
original_url: "http://basho.com/posts/technical/reviving-the-zombie-app-for-oscon/"
archive_url: "https://web.archive.org/web/20170801115139http://basho.com/posts/technical/reviving-the-zombie-app-for-oscon/"
categories:
  - "Community & Events"
---
# Returning to the Fight

Zombies have been all around us for 2 years now and we’re starting to lose the battle.

![banner-zombies](../images/reviving-the-zombie-app-for-oscon/banner-zombies.jpg)

Riak KV is the natural choice to fight off the zombie hordes. It scales as the war rages on and stays online even as our administrators are consumed (by other work).

My dear colleagues, the Brothers Kerrigan, taught us how to hunt them [using inverted indexes in Riak](./index-for-fun-and-for-profit.md). They took the next step to empower us all to win the war by creating [an application to visualize their location](./indexing-the-zombie-apocalypse-with-riak.md).

It hasn’t been enough.

With the inevitable degradation of the Internet, we’ve needed a way to fight the oncoming horde as individuals. **[Download the Vagrantfile](https://github.com/basho-labs/vagrant-zombie-riak)** and join the fight.

*:: Breaking character ::*

The inverted-indexes implementation, appreciatively nicknamed The Zombie Riak demo, has been a great way to highlight using Riak in a production application architecture. There are great ways to extend upon this project that I’ll list below.

[Vagrant](https://www.vagrantup.com/), started by [Mitchell Hashimoto](https://twitter.com/mitchellh) and part of the amazing suite of work from [Hashicorp](https://hashicorp.com/), is a standard for spinning up a local environment. Thanks to its simplicity and a little scripting, you can run The Zombie Riak demo right on your own laptop: <https://github.com/basho-labs/vagrant-zombie-riak>

# 

# How’s it Work?

The Vagrantfile is familiar in syntax:

The magic happens in two calls: `provision.sh` and `zombie.sh` run through the shell provisioner (more on the shell provisioner in Vagrant [here](http://docs.vagrantup.com/v2/provisioning/shell.html)). The first installs Riak KV and configures everything from Riak Search to leveldb as the storage backend. This file is an extension of how Engineers at Basho, like Bryce Kerley, [test the client libraries using vagrant](https://github.com/basho-labs/riak-ruby-vagrant). The second file gets an environment ready to install the inverted-indexes repository:

Walking through the file, you find a great deal of environmental configuration, validation and lastly the running of our web server using Ruby’s `unicorn` gem. This all takes place with a simple `vagrant up` now.

# 

# Join the War Against Zombies

[Get started with this example application](https://github.com/basho-labs/vagrant-zombie-riak#getting-started) and learn how to hunt zombies in Riak KV from the comfort of your laptop. Take the time to explore some of the nuances:

- How data is loaded into Riak KV in `load_data.rb`
- Explore how the app discovers Riak KV instances in `riak_hosts.rb`
- Understand how inverted indexes are generated in `index/inverted_index.rb`

There is a range of tools we could add to our toolset to fight off our brain-hungry foes. Here are a few that [are now in issues on the repo](https://github.com/basho-labs/vagrant-zombie-riak/issues):

- Improve any of the visualizations, features or documentation are more than welcome: they’re appreciated
- Design a manual upload server that can push new zombies into the database using a client or just using cURL
- Create a Zombie Sighting Report System so the concentration of live zombies in an area can quickly be determined based on the count and last report date
- Add a correlation feature, utilizing Graph CRDTs, so we can find our way back to Patient Zero
- Prepare for demand of our system by configuring Nginx as a caching and load-balancing system
- Add a crowdsourced Inanimate Zombie Reporting System so that members of the non-zombie population can report inanimate zombies. Incorporate Baysian filtering to prevent false reporting by zombies. They kind of just mash on the keyboard so this shouldn’t be too difficult

[![sudo gimme your BRAINZ](../images/reviving-the-zombie-app-for-oscon/BashoZombie.png)](../images/reviving-the-zombie-app-for-oscon/BashoZombie.png)
