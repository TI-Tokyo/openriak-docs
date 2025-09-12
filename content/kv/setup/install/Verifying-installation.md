---
sidebar_position: 2
title:Verifying an OpenRiak installation
sidebar_label: "Verifying Install"
---

Once OpenRiak has been installed, we would recommend that each node be check to ensure it is responding properly. There are a number of steps you can take for this.

 ## 1. Checking OpenRiak configuration files
 
 It is generally recommended to check your configuration files with `riak chkconfig` before you start your node for the first time.
 
 You should seen an output of `config is OK` plus the files that were checked.
 If something is wrong with the syntax, the command will provide an error output with the details of what is wrong.
 
 Once you've done this, you can start the node and move onto the next steps!
 
 
## 2. Starting an OpenRiak node

To start a OpenRiak node:

```
riak start
```

If the node started successfully you should see no output.

Once the node has started, you can check whether the node responds with:

```
riak ping
```
If the node is running, you should see a response of:

```
pong
```


## 3. Checking OpenRiak's readiness

You can check whether an individual node is able to read and write with the following command:

```
riak admin test
```

If successful, you should see the following output:

```
Successfully completed 1 read/write cycle to 'riak@127.0.0.1'
```

Alternatively, you can test a node by using the following command to get the properties of the bucket type `test`:

```
curl -v http://127.0.0.1:8098/types/default/props
```

Just swap out 127.0.0.1 in the example above with the IP address or fully qualified domain name of your Riak node. Once you've done that, you should see a response similar to the one shown.

```
* About to connect() to 127.0.0.1 port 8098 (#0)
*   Trying 127.0.0.1... connected
* Connected to 127.0.0.1 (127.0.0.1) port 8098 (#0)
> GET /riak/test HTTP/1.1
> User-Agent: curl/7.21.6 (x86_64-pc-linux-gnu)
> Host: 127.0.0.1:8098
> Accept: */*
>
< HTTP/1.1 200 OK
< Vary: Accept-Encoding
< Server: MochiWeb/1.1 WebMachine/1.9.0 (someone had painted it blue)
< Date: Wed, 26 Dec 2012 15:50:20 GMT
< Content-Type: application/json
< Content-Length: 422
<
* Connection #0 to host 127.0.0.1 left intact
* Closing connection #0
{"props":{"name":"test","allow_mult":false,"basic_quorum":false,
 "big_vclock":50,"chash_keyfun":{"mod":"riak_core_util",
 "fun":"chash_std_keyfun"},"dw":"quorum","last_write_wins":false,
 "linkfun":{"mod":"riak_kv_wm_link_walker","fun":"mapreduce_linkfun"},
 "n_val":3,"notfound_ok":true,"old_vclock":86400,"postcommit":[],"pr":0,
 "precommit":[],"pw":0,"r":"quorum","rw":"quorum","small_vclock":50,
 "w":"quorum","young_vclock":20}}
 ```
 
 The output above includes a `HTTP 200 OK`r response and further details from the -v (verbose) flag. It also outputs the default bucket properties for the `test` bucket.
 
