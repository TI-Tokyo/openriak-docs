---
sidebar_position: 1
title: Verifying your Cluster
sidebar_label: "Verifying your Cluster"
---

After you’ve installed OpenRiak KV, we recommend checking the status of each node to ensure that requests are being properly served.

This section covers way to test that your OpenRiak nodes are operating correctly, including: Starting the node, running a test, and checking the config files.

# riak chkconfig

It is generally recommended to run `riak chkconfig` before starting your node for the first time and after any significant changes/replaced nodes.
This command will output an syntax issues with your config files.

If your configuration file is syntaxically correct, you will see the following output with a list of files that were checked:

```bash
config is OK 
```

### Note: The `chkconfig` command will *not* check that the nodename is correct or that there are no performance or other behavioural issues with the configuration file.


# Starting an OpenRiak node

The quickest and easiest way to check that OpenRiak has install properly is to start the node and ping it, though this will not allow you to check for config problems before hand.

To start an OpenRiak node, use the following command:

```bash
riak start
```

A successful start will return no output. If there is a problem starting the node, an error message is printed to standard error.

Once the node has started, you can check that it is running with:

```bash
riak ping
```

If the node is running you will see:

```bash
pong
```

If the node is not running you will see:

```bash
Node <nodename> not responding to pings
```

If you see the second response, then your first step will be to check your configuration file and ensure everything is properly configured.

# Testing the nodes ability to read and write.

## Testing with admin test

OpenRiak has a built in function to test a nodes ability to read and write data, which is as follows:

```bash
riak admin test
```

A successful run of this command will output something similar to the following:

```bash
Successfully completed 1 read/write cycle to <node name>
```

If you attempt to run the command too quickly after starting riak, or if there is another issue, you may see an output such as below, which would require further investigation:

```bash
Failed to read test value: {error,{insufficient_vnodes,0,need,1}}
```

## Testing with Curl

You can also test whether OpenRiak is working by using the curl command-line tool. When you have OpenRiak running, run the following command, replacing the IP address with your Nodes address to retrieve the the properties associated with the bucket type `test`:

```bash
*   Trying 127.0.0.1:8098...
* Connected to 127.0.0.1 (127.0.0.1) port 8098 (#0)
> GET /types/default/props HTTP/1.1
> Host: 127.0.0.1:8098
> User-Agent: curl/7.76.1
> Accept: */*
>
* Mark bundle as not supporting multiuse
< HTTP/1.1 200 OK
< Vary: Accept-Encoding
< Server: MochiWeb/3.0.0 WebMachine/0.0.0+build.698.refadbf4a6 (greased slide to failure)
< Date: Fri, 31 Oct 2025 11:01:07 GMT
< Content-Type: application/json
< Content-Length: 503
<
* Connection #0 to host 127.0.0.1 left intact
{"props":{"allow_mult":false,"basic_quorum":false,"big_vclock":50,"chash_keyfun":{"mod":"riak_core_util","fun":"chash_std_keyfun"},"dvv_enabled":false,"dw":"quorum","last_write_wins":false,"linkfun":{"mod":"riak_kv_wm_link_walker","fun":"mapreduce_linkfun"},"n_val":3,"node_confirms":0,"notfound_ok":true,"old_vclock":86400,"postcommit":[],"pr":0,"precommit":[],"pw":0,"r":"quorum","repl":true,"rw":"quorum","small_vclock":50,"sync_on_write":"backend","w":"quorum","write_once":false,"young_vclock":20}}
```

The output above shows a successful response (HTTP 200 OK) and additional details from the verbose option. The response also contains the bucket properties for the default bucket type.

If all of the above was successful, then you have a functioning OpenRiak node and can move on!

