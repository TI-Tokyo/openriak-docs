---
sidebar_position: 3
title: Managing Configuration
sidebar_label: "Managing Configuration"
---
import { ConfigReferenceProvider } from '@site/src/components/ConfigReference/ConfigReferenceContext';
import { ConfigListing }             from '@site/src/components/ConfigReference/ConfigListing';
import { ConfigDefaultValue }      from '@site/src/components/ConfigReference/ConfigDefaultValue';
import InlineCodeWithCopy          from '@site/src/components/InlineCodeWithCopy/InlineCodeWithCopy';

## Contents

- [Retrieving a configuration value](#retrieving-configuration-value)
- [Checking your Conf](#checking-your-config)


## Retrieving Configuration value

You can retrieve the value of any configuration option with the following command:

```bash
$ sudo riak admin show <value>
```

If you replace <value> with the configuration option you want to check such as below:

```bash
$ sudo riak admin show storage_backend
```

Then you will receive back a response such as below, which shows the node the command was run on, and the value of the listed option:

```bash
sudo riak admin show storage_backend

+--------------+-----------------------+
|     node     |    storage_backend    |
+--------------+-----------------------+
|riak@127.0.0.1|riak_kv_leveled_backend|
+--------------+-----------------------+

ok
```

This process also works if you want to check all nodes at once:

```bash
sudo riak admin show storage_backend

+--------------+-----------------------+
|     node     |    storage_backend    |
+--------------+-----------------------+
|riak@127.0.0.1|riak_kv_leveled_backend|
|riak@127.0.0.2|riak_kv_leveled_backend|
|riak@127.0.0.3|riak_kv_leveled_backend|
|riak@127.0.0.4|riak_kv_leveled_backend|
|riak@127.0.0.5|riak_kv_leveled_backend|
+--------------+-----------------------+

ok
```

You can also use this to check multiple options at once by listing them simultaneously such as this:

```bash
## riak admin show anti_entropy storage_backend -all
+-----------------+------------+-----------------------+
|      node       |anti_entropy|    storage_backend    |
+-----------------+------------+-----------------------+
|riak@127.0.0.1   |  {off,[]}  |riak_kv_leveled_backend|
|riak@127.0.0.2   |  {off,[]}  |riak_kv_leveled_backend|
|riak@127.0.0.3   |  {off,[]}  |riak_kv_leveled_backend|
|riak@127.0.0.4   |  {off,[]}  |riak_kv_leveled_backend|
|riak@127.0.0.5   |  {off,[]}  |riak_kv_leveled_backend|
+-----------------+------------+-----------------------+

ok
```

This combination of commands allows you to quickly check that the values are consistent across one or all your nodes at the same time.

## Checking your config

There is a command that can be performed via the command line that allows you to run a check whether the syntax in your configuration file is correct. 

```bash
riak chkconfig
```

If your config file is syntactically correct, then you should see the follow:

```bash
$ riak chkconfig

config is OK
-config <path to output of generated configs>
```
The command also outputs a set of generated config files that show the values that OpenRiak is using when the command was run and the path to where they are stored.

