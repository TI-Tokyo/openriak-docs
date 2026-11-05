---
title: "Understanding riak_core: Building Handoff"
date: "2015-05-19T05:11:18+00:00"
author: "Mark Allen"
original_url: "http://basho.com/posts/technical/understanding-riak_core-building-handoff/"
archive_url: "https://web.archive.org/web/20170801115249http://basho.com/posts/technical/understanding-riak_core-building-handoff/"
categories:
  - "Architecture & Distributed Systems"
  - "Operations"
---
At Erlang Factory 2015, I presented a talk entitled “[How to build applications on top of riak\_core](https://www.youtube.com/watch?v=LKsNbYf9mLw&index=1&list=PLWbHc_FXPo2h0sJW6X2RZDtT1ndw6KKpQ).” I wanted to do this talk because there is a serious lack of “one-stop” documentation around riak\_core. In particular, implementing handoffs has been underdocumented and not well disseminated. To help, I have a few blog posts to share.

In my first post, *[Understanding riak\_core: Handoff](http://basho.com/understanding-riak_core-handoff/)*, I explored some background, defined a handoff and answer the question of “should I use riak\_core?” In this post, we’ll walk through building an application that uses riak\_core as its foundation.

## Build your first riak\_core application

Building an application on riak\_core means leveraging the powerful toolset that makes writing this code easier. You will benefit from using rebar: a self-contained script designed to minimize the amount of build configuration work you have to do. One of the lesser known talents that the rebar build tool possesses is the ability to stamp out new Erlang/OTP applications using a set of template files. Conveniently, Basho has a set of template files available for riak\_core applications, which you will find in the [rebar\_riak\_core](https://github.com/basho/rebar_riak_core) github repository.

```
$ git clone https://github.com/basho/rebar_riak_core
Cloning into 'rebar_riak_core'...
remote: Counting objects: 230, done.
remote: Total 230 (delta 0), reused 0 (delta 0), pack-reused 230
Receiving objects: 100% (230/230), 53.38 KiB | 0 bytes/s, done.
Resolving deltas: 100% (114/114), done.
Checking connectivity... done.
$ cd rebar_riak_core; make
mkdir -p /Users/mallen/.rebar/templates
cp riak* /Users/mallen/.rebar/templates
$ cd ..; mkdir demoapp; cd demoapp
$ rebar create template=riak_core appid=demoapp
==> demoapp (create)
Writing .gitignore
Writing Makefile
Writing README.md
Writing rebar.config
Writing rel/reltool.config
Writing rel/vars.config
Writing rel/gen_dev
Writing rel/files/app.config
Writing rel/files/erl
Writing rel/files/demoapp
Writing rel/files/demoapp-admin
Writing rel/files/nodetool
Writing rel/files/vm.args
Writing rel/vars/dev_vars.config.src
Writing src/demoapp_app.erl
Writing src/demoapp_console.erl
Writing src/demoapp_node_event_handler.erl
Writing src/demoapp_ring_event_handler.erl
Writing src/demoapp_sup.erl
Writing src/demoapp_vnode.erl
Writing src/demoapp.app.src
Writing src/demoapp.erl
Writing src/demoapp.hrl
$ cp $(which rebar) .
$ make devrel
```

Although you haven’t done much work, this is a fully functional riak\_core application! Let’s start it up and see what it can do.

```
$ dev/dev1/bin/demoapp console
Exec: /Users/mallen/github/basho/demoapp/dev/dev1/erts-5.10.3/bin/erlexec -boot /Users/mallen/github/basho/demoapp/dev/dev1/releases/1/demoapp -embedded -config /Users/mallen/github/basho/demoapp/dev/dev1/etc/app.config -args_file /Users/mallen/github/basho/demoapp/dev/dev1/etc/vm.args -- console
Root: /Users/mallen/github/basho/demoapp/dev/dev1
Erlang R16B02-basho6 (erts-5.10.3) [source] [64-bit] [smp:8:8] [async-threads:5] [hipe] [kernel-poll:true]

17:30:32.462 [info] Application lager started on node 'demoapp1@127.0.0.1'
17:30:32.463 [info] Application crypto started on node 'demoapp1@127.0.0.1'
17:30:32.465 [info] Application riak_sysmon started on node 'demoapp1@127.0.0.1'
17:30:32.472 [info] Application os_mon started on node 'demoapp1@127.0.0.1'
17:30:32.472 [info] Application basho_stats started on node 'demoapp1@127.0.0.1'
17:30:32.472 [info] Application eleveldb started on node 'demoapp1@127.0.0.1'
17:30:32.472 [info] Application pbkdf2 started on node 'demoapp1@127.0.0.1'
17:30:32.472 [info] Application poolboy started on node 'demoapp1@127.0.0.1'
17:30:32.490 [info] Starting reporters with []
17:30:32.490 [info] Application exometer_core started on node 'demoapp1@127.0.0.1'
17:30:32.498 [info] Application clique started on node 'demoapp1@127.0.0.1'
17:30:32.538 [warning] No ring file available.
17:30:32.648 [info] New capability: {riak_core,vnode_routing} = proxy
17:30:32.654 [info] New capability: {riak_core,staged_joins} = true
17:30:32.658 [info] New capability: {riak_core,resizable_ring} = true
17:30:32.664 [info] New capability: {riak_core,fold_req_version} = v2
17:30:32.669 [info] New capability: {riak_core,security} = true
17:30:32.675 [info] New capability: {riak_core,bucket_types} = true
17:30:32.681 [info] New capability: {riak_core,net_ticktime} = true
Eshell V5.10.3  (abort with ^G)
(demoapp1@127.0.0.1)1> demoapp:ping().
{pong,639406966332270026714112114313373821099470487552}
(demoapp1@127.0.0.1)2> demoapp:ping().
{pong,1438665674247607560106752257205091097473808596992}
(demoapp1@127.0.0.1)3> demoapp:ping().
{pong,1324485858831130769622089379649131486563188867072}
(demoapp1@127.0.0.1)4> demoapp:ping().
{pong,159851741583067506678528028578343455274867621888}
```

Alright. “Out of the box” we get the ping() function for free. Let’s see what it does.

```
ping() ->
    DocIdx = riak_core_util:chash_key({<<"ping">>, term_to_binary(now())}),
    PrefList = riak_core_apl:get_primary_apl(DocIdx, 1, demoapp),
    [{IndexNode, _Type}] = PrefList,
    riak_core_vnode_master:sync_spawn_command(IndexNode, ping, demoapp_vnode_master).
```

On line 2, the code takes the Erlang “now” counter value and sends it to riak\_core’s built in consistent hash function. On line 3, we take the hash value and use it to build a “preference list” or a list of one or more {Node, VnodeType} tuples. On line 4, we use the Node value to send a command to the (possibly) remote VNode to execute the ping method. Since this is a synchronous command, the call will wait until it returns from the (possibly remote) vnode method call or the call times out. So that should give you a pretty decent idea how you would implement other vnode based API calls. (Some of the details that are omitted include writing replicas to different vnodes – if you’re interested in that topic, then I will refer you to the [example code in the udon application](https://github.com/mrallen1/udon/blob/master/src/udon.erl#L34-L42) which covers how to implement that using a [finite state machine](https://github.com/mrallen1/udon/blob/master/src/udon_op_fsm.erl) and the actual code that [writes bits to disk](https://github.com/mrallen1/udon/blob/master/src/udon_vnode.erl#L47-L57) in the vnode callback module.)

## Writing handoff code

Although there are different scenarios when a handoff might occur for a vnode, each of these different types of handoff uses the same code to implement it. Fortunately, riak\_core does a lot of the hard work for you – it manages all of the network connections, keeps track of what keys and values it has transmitted and so forth – so implementation comes down to a few things:

- Is a vnode empty? (if a vnode is empty, we don’t need to do any handoffs over the network)

- How do we collect the data for each key and value?

- How do we serialize the vnode data?

- How do we deserialize the vnode data at the receiver?

If you’re already familiar with the OTP [gen\_server](http://www.erlang.org/doc/man/gen_server.html) behavior, then implementing handoffs will feel very familiar. Handoffs are implemented by writing a series of function callbacks. Let’s look at the callbacks as defined in the demoapp we created above.

```
handle_handoff_command(_Message, _Sender, State) ->
    {noreply, State}.

handoff_starting(_TargetNode, State) ->
    {true, State}.

handoff_cancelled(State) ->
    {ok, State}.

handoff_finished(_TargetNode, State) ->
    {ok, State}.

handle_handoff_data(_Data, State) ->
    {reply, ok, State}.

encode_handoff_item(_ObjectName, _ObjectValue) ->
    <<>>.
    
is_empty(State) ->
    {true, State}.
```

Those are the callbacks which need to be implemented. As you can see, in the demoapp they’re just stubs which return valid (but likely incorrect) values. If you’re using riak\_core as a mechanism to distribute work among a set of workers (and don’t need to worry about vnode migration) then these stubs are all you need to have for your application.

**The bare minimum**  
Most of you who are reading this far are interested in writing handoff code to move data from one (physical) node to another. So let’s take a look at the `handle_handoff_command/3` callback. Here’s the function head from my udon application.

```
handle_handoff_command(?FOLD_REQ{foldfun=VisitFun, acc0=Acc0}, _Sender, State) ->
    %% eliding details for now. Don't worry, we'll get to them shortly.
    Final = lists:foldl(fun magic/2, Acc0, object_list()),
    {reply, Final, State}.
```

Whoa. What’s that `?FOLD_REQ macro`?  
How do I implement `magic/2`?!  
Let’s break this down step by step before we fill in the details.

As noted above, at the big picture level, we need a way to find all of the objects (that is, each key and each value) that a particular vnode owns. So we need a way to get all of them – that’s what the `object_list()` function is supposed to do. By the way, `object_list()` is not a callback supplied by riak\_core – that’s a function you need to write yourself. (Also, the function **name** in the fold parameters is not important, only the property that this function returns a list of the keys to fold over.)

Next, we need a way to take each object and serialize it. That’s the purpose of the `encode_handoff_item/2` function callback.

After that, we need to send that data over the wire to the (probably remote) node. And that’s what the mysterious VisitFun() in the function head does. More on VisitFun() in a moment, but for now, it’s part of riak\_core that handles all of the messy details around network connections, sockets, and pumping serialized data out on the wire.

And on the receiving end, we need a way to deserialize and store the incoming vnode data. That is the purpose of `handle_handoff_data/2`.

So at a bare minimum, you must write four callbacks to implement vnode handoffs. These are:

- `is_empty/1`
- `encode_handoff_data/2`
- `handle_handoff_data/2`
- `handle_handoff_command/3`

## Next Steps

At this point, you should have a good understanding on the basics of handoff, as coordinated by riak\_core, and an understanding of the steps involved in implementing handoff. In my final post in this series, we will delve into the mysterious world of VisitFun().

Mark Allen  
[Speakerdeck](https://speakerdeck.com/mrallen1)  
[GitHub](https://github.com/mrallen1)  
[Twitter](https://twitter.com/bytemeorg)
