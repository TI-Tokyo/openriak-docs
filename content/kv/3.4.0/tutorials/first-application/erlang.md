---
title: 'Build a first OpenRiak application with Erlang'
description: 'Guide a developer through modeling, storing, retrieving, querying, and updating a small dataset with Erlang.'
weight: 3
diataxis: 'tutorial'
product: 'OpenRiak KV'
product_version: '3.4.0'
status: 'editorially-rewritten'
draft: true
audience:
  - 'new-developers'
source_material:
  - 'legacy-3.2.5'
  - 'live-3.2.5'
  - 'proposed-kv'
legacy_3_2_5_sources:
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\developing\getting-started\erlang.md'
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\developing\getting-started\erlang\crud-operations.md'
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\developing\getting-started\erlang\object-modeling.md'
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\developing\getting-started\erlang\querying.md'
tags: ['diataxis', 'kv', 'tutorial']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Guide a developer through modeling, storing, retrieving, querying, and updating a small dataset with Erlang.

## Overview

### Getting Started with Erlang

If you haven't set up an OpenRiak node and started it, please visit [Running A Cluster](/kv/3.4.0/how-to/operate/) first.

To try this flavor of Riak, a working installation of Erlang is
required. You can also use the `erts` Erlang installation that comes
with Riak.

#### Client Setup

Download the latest Erlang client from GitHub
([zip](https://github.com/basho/riak-erlang-client/archive/master.zip),
[GitHub repository](https://github.com/basho/riak-erlang-client/)) and
extract it to your working directory.

Next, open the Erlang console with the client library paths included.

```bash
erl -pa CLIENT_LIBRARY_PATH/ebin/ CLIENT_LIBRARY_PATH/deps/*/ebin
```

Now let’s create a link to the OpenRiak node. If you are using a single
local OpenRiak node, use the following to create the link:

```erlang
{ok, Pid} = riakc_pb_socket:start("127.0.0.1", 8087).
```

If you set up a local OpenRiak cluster using the [[five-minute install]]
method, use this code snippet instead:

```erlang
{ok, Pid} = riakc_pb_socket:start_link("127.0.0.1", 10017).
```

We are now ready to start interacting with Riak.

#### Next Steps

[CRUD Operations](/kv/3.4.0/tutorials/first-application/erlang/)

### CRUD Operations with Erlang

#### Creating Objects In Riak

First, let’s create a few Riak objects. For these examples we'll be
using the bucket `test`.

```erlang
MyBucket = <<"test">>.

Val1 = 1.
Obj1 = riakc_obj:new(MyBucket, <<"one">>, Val1).
riakc_pb_socket:put(Pid, Obj1).
```

In this first example, we have stored the integer 1 with the lookup key
of `one`. Next, let’s store a simple string value of `two` with a
matching key.

```erlang
Val2 = <<"two">>.
Obj2 = riakc_obj:new(MyBucket, <<"two">>, Val2).
riakc_pb_socket:put(Pid, Obj2).
```

That was easy. Finally, let’s store something more complex, a tuple this
time. You will probably recognize the pattern by now.

```erlang
Val3 = {value, 3}.
Obj3 = riakc_obj:new(MyBucket, <<"three">>, Val3).
riakc_pb_socket:put(Pid, Obj3).
```

#### Reading Objects From Riak

Now that we have a few objects stored, let’s retrieve them and make sure
they contain the values we expect.

```erlang
{ok, Fetched1} = riakc_pb_socket:get(Pid, MyBucket, <<"one">>).
{ok, Fetched2} = riakc_pb_socket:get(Pid, MyBucket, <<"two">>).
{ok, Fetched3} = riakc_pb_socket:get(Pid, MyBucket, <<"three">>).

Val1 =:= binary_to_term(riakc_obj:get_value(Fetched1)). %% true
Val2 =:= riakc_obj:get_value(Fetched2).                 %% true
Val3 =:= binary_to_term(riakc_obj:get_value(Fetched3)). %% true
```

That was easy. We simply request the objects by bucket and key.

#### Updating Objects In Riak

While some data may be static, other forms of data may need to be
updated. This is also easy to do. Let’s update the value in the third
example to 42, update the Riak object, and then save it.

```erlang
NewVal3 = setelement(2, Val3, 42).
UpdatedObj3 = riakc_obj:update_value(Fetched3, NewVal3).
{ok, NewestObj3} = riakc_pb_socket:put(Pid, UpdatedObj3, [return_body]).
```

We can verify that our new value was saved by looking at the value
returned.

```erlang
rp(binary_to_term(riakc_obj:get_value(NewestObj3))).
```

#### Deleting Objects From Riak

Nothing is complete without a delete, as they say. Fortunately, that's
easy too.

```erlang
riakc_pb_socket:delete(Pid, MyBucket, <<"one">>).
riakc_pb_socket:delete(Pid, MyBucket, <<"two">>).
riakc_pb_socket:delete(Pid, MyBucket, <<"three">>).
```

Now we can verify that the objects have been removed from Riak.

```erlang
{error,notfound} =:= riakc_pb_socket:get(Pid, MyBucket, <<"one">>).
{error,notfound} =:= riakc_pb_socket:get(Pid, MyBucket, <<"two">>).
{error,notfound} =:= riakc_pb_socket:get(Pid, MyBucket, <<"three">>).
```

#### Working With Complex Objects

Since the world is a little more complicated than simple integers and
bits of strings, let’s see how we can work with more complex objects.
Take, for example, this record that encapsulates some information about
a book.

```erlang
rd(book, {title, author, body, isbn, copies_owned}).

MobyDickBook = #book{title="Moby Dick",
                     isbn="1111979723",
                     author="Herman Melville",
                     body="Call me Ishmael. Some years ago...",
                     copies_owned=3}.
```

So we have some information about our Moby Dick collection that we want
to save. Storing this to Riak should look familiar by now:

```erlang
MobyObj = riakc_obj:new(<<"books">>,
                        list_to_binary(MobyDickBook#book.isbn),
                        MobyDickBook).

riakc_pb_socket:put(Pid, MobyObj).
```

Some of you may be thinking: "How does the Erlang Riak client
encode/decode my object?" If we fetch our book back and print the value,
we shall know:

```erlang
{ok, FetchedBook} = riakc_pb_socket:get(Pid,
                                        <<"books">>,
                                        <<"1111979723">>).

rp(riakc_obj:get_value(FetchedBook)).
```

The response:

```
<<131,104,6,100,0,4,98,111,111,107,107,0,9,77,111,98,121,
  32,68,105,99,107,107,0,15,72,101,114,109,97,110,32,77,
  101,108,118,105,108,108,101,107,0,34,67,97,108,108,32,
  109,101,32,73,115,104,109,97,101,108,46,32,83,111,109,
  101,32,121,101,97,114,115,32,97,103,111,46,46,46,107,0,
  10,49,49,49,49,57,55,57,55,50,51,97,3>>
```

Erlang binaries! The Riak Erlang client library encodes everything as
binaries. If we wanted to get a `book` object back we could use
`binary_to_term/1` to get our original object back:

```erlang
rp(binary_to_term(riakc_obj:get_value(FetchedBook))).
```

Next let’s clean up our mess:

```erlang
riakc_pb_socket:delete(Pid, <<"books">>, <<"1111979723">>).
riakc_pb_socket:stop(Pid).
```

### Object Modeling with Erlang

To get started, let's create the records that we'll be using.

**Code Download**
You can also download the code for this chapter at
[Github](https://github.com/basho/taste-of-riak/tree/am-dem-erlang-modules/erlang/Ch03-Msgy-Schema).

The Github version includes Erlang type specifications which have been omitted
here for brevity.

```erlang
%% msgy.hrl

-define(USER_BUCKET, <<"Users">>).
-define(MSG_BUCKET, <<"Msgs">>).
-define(TIMELINE_BUCKET, <<"Timelines">>).
-define(INBOX, "Inbox").
-define(SENT, "Sent").

-record(user, {user_name, full_name, email}).

-record(msg, {sender, recipient, created, text}).

-record(timeline, {owner, msg_type, msgs}).
```

We'll be using the bucket `Users` to store our data. We won't be [using bucket types](/kv/3.4.0/how-to/develop/use-bucket-types/) here, so we don't need to specify one.

To use these records to store data, we will first have to create a user
record. Then, when a user creates a message, we will append that message
to one or more timelines. If it's a private message, we'll append it to
the Recipient's `Inbox` timeline and to the User's own `Sent` timeline.
If it's a group message, we'll append it to the Group's timeline, as
well as to the User's `Sent` timeline.

#### Buckets and keys revisited

Now that we've worked out how we will differentiate data in the system,
let's figure out our bucket and key names.

The bucket names are straightforward. We can use `Users`, `Msgs`, and
`Timelines`. The key names, however, are a little more tricky. In past
examples we've used sequential integers, but this presents a problem: we
would need a secondary service to hand out these IDs. This service could
easily be a future bottleneck in the system, so let's use a natural key.
Natural keys are a great fit for key/value systems because both humans
and computers can easily construct them when needed, and most of the
time they can be made unique enough for a KV store.

Bucket | Key Pattern | Example Key
:------|:------------|:-----------
`Users` | `<user_name>` | `joeuser`
`Msgs` | `<username>_<datetime>` | `joeuser_2014-03-06T02:05:13.223556Z`
`Timelines` | `<username>_<type>_<date>` | `joeuser_Sent_2014-03-06Z`<br /> `marketing_group_Inbox_2014-03-06Z` |

For the `Users` bucket, we can be certain that we will want each
username to be unique, so let's use the `username` as the key.  For the
`Msgs` bucket, let's use a combination of the username and the posting
datetime in an [ISO 8601 Long](http://en.wikipedia.org/wiki/ISO_8601)
format. This combination gives us the pattern `<username>_<datetime>`,
which produces keys like `joeuser_2014-03-05T23:20:28Z`.

Now for `Timelines`, we need to differentiate between `Inbox` and `Sent`
timelines, so we can simply add that type into the key name. We will
also want to partition each collection object into some time period,
that way the object doesn't grow too large (see note below).

For `Timelines`, let's use the pattern `<username>_<type>_<date>` for
users, and `<groupname>_Inbox_<date>` for groups, which will look like
`joeuser_Sent_2014-03-06Z` or `marketing_group_Inbox_2014-03-05Z`,
respectively.

**Note**
Riak performs best with objects under 1-2 MB. Objects larger than that can
hurt performance, especially if many siblings are being created. We will cover
siblings, sibling resolution, and sibling explosions in the next chapter.

#### Keeping our story straight with repositories

Now that we've figured out our object model, let's write some modules to
act as repositories that will help us create and work with these records
in Riak:

```erlang
%% user_repository.erl

-module(user_repository).
-export([save_user/2,
         get_user/2]).
-include("msgy.hrl").

save_user(ClientPid, User) ->
    RUser = riakc_obj:new(?USER_BUCKET,
                          list_to_binary(User#user.user_name),
                          User),
    riakc_pb_socket:put(ClientPid, RUser).

get_user(ClientPid, UserName) ->
    {ok, RUser} = riakc_pb_socket:get(ClientPid,
                                      ?USER_BUCKET,
                                      list_to_binary(UserName)),
    binary_to_term(riakc_obj:get_value(RUser)).
```

<br />

```erlang
%% msg_repository.erl

-module(msg_repository).
-export([create_msg/3,
         get_msg/2]).
-include("msgy.hrl").

-spec create_msg(user_name(), user_name(), text()) -> msg().
create_msg(Sender, Recipient, Text) ->
    #msg{sender=Sender,
         recipient=Recipient,
         created=get_current_iso_timestamp(),
         text = Text}.

-spec get_msg(pid(), riakc_obj:key()) -> msg().
get_msg(ClientPid, MsgKey) ->
    {ok, RMsg} = riakc_pb_socket:get(ClientPid,
                                     ?MSG_BUCKET,
                                     MsgKey),
    binary_to_term(riakc_obj:get_value(RMsg)).

%% @private
-spec get_current_iso_timestamp() -> datetimestamp().
get_current_iso_timestamp() ->
    {_,_,MicroSec} = DateTime = erlang:now(),
    {{Year,Month,Day},{Hour,Min,Sec}} = calendar:now_to_universal_time(DateTime),
    lists:flatten(
        io_lib:format("~4..0B-~2..0B-~2..0BT~2..0B:~2..0B:~2..0B.~6..0B",
            [Year, Month, Day, Hour, Min, Sec, MicroSec])).

```

<br />

```erlang
%% timeline_repository.erl

-module(timeline_repository).
-export([post_msg/2,
         get_timeline/4]).
-include("msgy.hrl").

post_msg(ClientPid, Msg) ->
     %% Save the canonical copy
    SavedMsg = save_msg(ClientPid, Msg),
    MsgKey = binary_to_list(riakc_obj:key(SavedMsg)),

%% Post to sender's Sent timeline
    add_to_timeline(ClientPid, Msg, sent, MsgKey),

%% Post to recipient's Inbox timeline
    add_to_timeline(ClientPid, Msg, inbox, MsgKey),
    ok.

get_timeline(ClientPid, Owner, MsgType, Date) ->
    TimelineKey = generate_key(Owner, MsgType, Date),
    {ok, RTimeline} = riakc_pb_socket:get(ClientPid,
                                          ?TIMELINE_BUCKET,
                                          list_to_binary(TimelineKey)),
    binary_to_term(riakc_obj:get_value(RTimeline)).

%% --------------------------------------------------------------------

%% @private
save_msg(ClientPid, Msg) ->
    MsgKey = Msg#msg.sender ++ "_" ++ Msg#msg.created,
    ExistingMsg = riakc_pb_socket:get(ClientPid,
                                      ?MSG_BUCKET,
                                      list_to_binary(MsgKey)),
    SavedMsg = case ExistingMsg of
        {error, notfound} ->
            NewMsg = riakc_obj:new(?MSG_BUCKET, list_to_binary(MsgKey), Msg),
            {ok, NewSaved} = riakc_pb_socket:put(ClientPid,
                                                 NewMsg,
                                                 [if_none_match, return_body]),
            NewSaved;
        {ok, Existing} -> Existing
    end,
    SavedMsg.

%% @private
add_to_timeline(ClientPid, Msg, MsgType, MsgKey) ->
    TimelineKey = generate_key_from_msg(Msg, MsgType),
    ExistingTimeline = riakc_pb_socket:get(ClientPid,
                                           ?TIMELINE_BUCKET,
                                           list_to_binary(TimelineKey)),
    UpdatedTimeline = case ExistingTimeline of
        {error, notfound} ->
            create_new_timeline(Msg, MsgType, MsgKey, TimelineKey);
        {ok, Existing} ->
            add_to_existing_timeline(Existing, MsgKey)
    end,

{ok, SavedTimeline} = riakc_pb_socket:put(ClientPid,
                                              UpdatedTimeline,
                                              [return_body]),
    SavedTimeline.

%% @private
create_new_timeline(Msg, MsgType, MsgKey, TimelineKey) ->
    Owner = get_owner(Msg, MsgType),
    Timeline = #timeline{owner=Owner,
                         msg_type=MsgType,
                         msgs=[MsgKey]},
    riakc_obj:new(?TIMELINE_BUCKET, list_to_binary(TimelineKey), Timeline).

%% @private
add_to_existing_timeline(ExistingRiakObj, MsgKey) ->
    ExistingTimeline = binary_to_term(riakc_obj:get_value(ExistingRiakObj)),
    ExistingMsgList = ExistingTimeline#timeline.msgs,
    UpdatedTimeline = ExistingTimeline#timeline{msgs=[MsgKey|ExistingMsgList]},
    riakc_obj:update_value(ExistingRiakObj, UpdatedTimeline).

%% @private
get_owner(Msg, inbox) ->  Msg#msg.recipient;
get_owner(Msg, sent) ->  Msg#msg.sender.

%% @private
generate_key_from_msg(Msg, MsgType) ->
    Owner = get_owner(Msg, MsgType),
    generate_key(Owner, MsgType, Msg#msg.created).

%% @private
generate_key(Owner, MsgType, Date) when is_tuple(Date) ->
    DateString = get_iso_datestamp_from_date(Date),
    generate_key(Owner, MsgType, DateString);

generate_key(Owner, MsgType, Datetimestamp) ->
    DateString = get_iso_datestamp_from_iso_timestamp(Datetimestamp),
    MsgTypeString = case MsgType of
        inbox -> ?INBOX;
        sent -> ?SENT
    end,
    Owner ++ "_" ++ MsgTypeString ++ "_" ++ DateString.

%% @private
get_iso_datestamp_from_date(Date) ->
    {Year,Month,Day} = Date,
    lists:flatten(io_lib:format("~4..0B-~2..0B-~2..0B", [Year, Month, Day])).

%% @private
get_iso_datestamp_from_iso_timestamp(CreatedString) ->
    {Date, _} = lists:split(10,CreatedString),
    Date.

```

Finally, let's test them:

```erlang
%% msgy.erl

-module(msgy).
-export([main/0]).
-include("msgy.hrl").

main() ->
  %% Setup our repositories
  {ok, Pid} = riakc_pb_socket:start_link("127.0.0.1", 10017),

%% Create and save users
  Joe = #user{user_name="joeuser",
              full_name="Joe User",
              email="joe.user@basho.com"},

Marleen = #user{user_name="marleenmgr",
                  full_name="Marleen Manager",
                  email="marleen.manager@basho.com"},

user_repository:save_user(Pid, Joe),
  user_repository:save_user(Pid, Marleen),

%% Create new Msg, post to timelines
  Msg = msg_repository:create_msg(Marleen#user.user_name, Joe#user.user_name, "Welcome to the company!"),
  timeline_repository:post_msg(Pid, Msg),

%% Get Joe's inbox for today, get first message
  {TodaysDate,_} = calendar:now_to_universal_time(erlang:now()),
  JoesInboxToday = timeline_repository:get_timeline(Pid, Joe#user.user_name, inbox, TodaysDate),

JoesFirstMessage = msg_repository:get_msg(Pid, hd(JoesInboxToday#timeline.msgs)),

io:format("From: ~s~nMsg : ~s~n~n", [JoesFirstMessage#msg.sender, JoesFirstMessage#msg.text]),
  ok.
```

As you can see, the repository pattern helps us with a few things:

* It helps us to see if an object exists before creating a new one
* It keeps our buckets and key names consistent
* It provides us with a consistent interface to work with.

While this set of repositories solves many of our problems, it is very
minimal and doesn't cover all the edge cases. For instance, what happens
if two different people try to create a user with the same username?

We can also easily "compute" key names now, but how do we quickly look
up the last 10 messages a user sent? Many of these answers will be
application dependent. If your application shows the last 10 messages in
reverse order, for example, you may want to store that set of data in
another collection object to make lookup faster. There are drawbacks to
every solution, but we recommend seeking out the key/value-based
solution first, as it will likely be the quickest.

So to recap, in this chapter we learned:

* How to choose bucket names
* How to choose natural keys based on how we want to partition our data.

### Querying with Erlang

#### A Quick Note on Querying and Schemas

_Schemas_? Yes, we said that correctly: S-C-H-E-M-A-S. It's not a dirty
word. Even in a key/value store, you will still have a logical database
schema of how all the data relates to other data. This can be as simple
as using the same key across multiple buckets for different types of
data to having fields in your data that are related by name. These
querying methods will introduce you to some ways of laying out your data
in Riak, along with how to query it back.

A more comprehensive discussion can be found in [Key/Value Modeling](/kv/3.4.0/how-to/plan/map-data-to-objects/).

#### Denormalization

If you're coming from a relational database, the easiest way to get your
application's feet wet with NoSQL is to denormalize your data into
related chunks. For example, with a customer database, you might have
separate tables for customers, addresses, preferences, etc. In Riak, you
can denormalize all that associated data into a single object and store
it into a `Customer` bucket. You can keep pulling in associated
data until you hit one of the big denormalization walls:

* Size limits (objects greater than 1MB)
* Shared/referential Data (data that the object doesn't "own")
* Differences in access patterns (objects that get read/written once vs.
  often)

At one of these points we will have to split the model.

#### Same Keys, Different Buckets

The simplest way to split up data would be to use the same identity key
across different buckets. A good example of this would be a `Customer`
object, an `Order` object, and an `OrderSummaries` object that keeps
rolled up info about orders such as total, etc.

Let's put some data into Riak so we can play with it. Fire up your
Erlang REPL with the client library in the path, and enter in the
following:

```erlang
rd(customer, {customer_id, name, address, city, state, zip, phone, created_date}).
rd(item, {item_id, title, price}).
rd(order, {order_id, customer_id, salesperson_id, items, total, order_date}).
rd(order_summary_entry, {order_id, total, order_date}).
rd(order_summary, {customer_id, summaries}).

Customer = #customer{ customer_id= 1,
                      name= "John Smith",
                      address= "123 Main Street",
                      city= "Columbus",
                      state= "Ohio",
                      zip= "43210",
                      phone= "+1-614-555-5555",
                      created_date= {{2013,10,1},{14,30,26}}}.

Orders =  [ #order{
              order_id= 1,
              customer_id= 1,
              salesperson_id= 9000,
              items= [
                #item{
                  item_id= "TCV37GIT4NJ",
                  title= "USB 3.0 Coffee Warmer",
                  price= 15.99 },
                #item{
                  item_id= "PEG10BBF2PP",
                  title= "eTablet Pro, 24GB, Grey",
                  price= 399.99 }],
              total= 415.98,
              order_date= {{2013,10,1},{14,42,26}}},

#order{
              order_id= 2,
              customer_id= 1,
              salesperson_id= 9001,
              items= [
                #item{
                  item_id= "OAX19XWN0QP",
                  title= "GoSlo Digital Camera",
                  price= 359.99 }],
              total= 359.99,
              order_date= {{2013,10,15},{16,43,16}}},

#order {
              order_id= 3,
              customer_id= 1,
              salesperson_id= 9000,
              items= [
                #item{
                  item_id= "WYK12EPU5EZ",
                  title= "Call of Battle= Goats - Gamesphere 4",
                  price= 69.99 },
                #item{
                  item_id= "TJB84HAA8OA",
                  title= "Bricko Building Blocks",
                  price= 4.99 }],
              total= 74.98,
              order_date= {{2013,11,3},{17,45,28}}}
          ].

OrderSummary =  #order_summary{
                  customer_id= 1,
                  summaries= [
                    #order_summary_entry{
                      order_id= 1,
                      total= 415.98,
                      order_date= {{2013,10,1},{14,42,26}}
                    },
                    #order_summary_entry{
                      order_id= 2,
                      total= 359.99,
                      order_date= {{2013,10,15},{16,43,16}}
                    },
                    #order_summary_entry{
                      order_id= 3,
                      total= 74.98,
                      order_date= {{2013,11,3},{17,45,28}}}]}.

#### Remember to replace the ip and port parameters with those that match your cluster.

{ok, Pid} = riakc_pb_socket:start_link("127.0.0.1", 10017).

CustomerBucket = <<"Customers">>.
OrderBucket = <<"Orders">>.
OrderSummariesBucket = <<"OrderSummaries">>.

CustObj = riakc_obj:new(CustomerBucket,
                        list_to_binary(
                          integer_to_list(
                            Customer#customer.customer_id)),
                        Customer).

riakc_pb_socket:put(Pid, CustObj).

StoreOrder = fun(Order) ->
  OrderObj = riakc_obj:new(OrderBucket,
                           list_to_binary(
                             integer_to_list(
                               Order#order.order_id)),
                           Order),
  riakc_pb_socket:put(Pid, OrderObj)
end.

lists:foreach(StoreOrder, Orders).

OrderSummaryObj = riakc_obj:new(OrderSummariesBucket,
                                list_to_binary(
                                  integer_to_list(
                                    OrderSummary#order_summary.customer_id)),
                                OrderSummary).

riakc_pb_socket:put(Pid, OrderSummaryObj).

```

While individual `Customer` and `Order` objects don't change much (or
shouldn't change), the `OrderSummaries` object will likely change often.
It will do double duty by acting as an index for all a customer's
orders, and also holding some relevant data such as the order total,
etc. If we showed this information in our application often, it's only
one extra request to get all the info.

```erlang
{ok, FetchedCustomer} = riakc_pb_socket:get(Pid,
                                            CustomerBucket,
                                            <<"1">>).
{ok, FetchedSummary} = riakc_pb_socket:get(Pid,
                                           OrderSummariesBucket,
                                           <<"1">>).
rp({binary_to_term(riakc_obj:get_value(FetchedCustomer)),
    binary_to_term(riakc_obj:get_value(FetchedSummary))}).
```

Which returns our amalgamated objects:

```erlang
{#customer{customer_id = 1,name = "John Smith",
           address = "123 Main Street",city = "Columbus",
           state = "Ohio",zip = "43210",phone = "+1-614-555-5555",
           created_date = {{2013,10,1},{14,30,26}}},
 #order_summary{customer_id = 1,
                summaries = [#order_summary_entry{order_id = 1,
                                                  total = 415.98,
                                                  order_date = {{2013,10,1},{14,42,26}}},
                             #order_summary_entry{order_id = 2,total = 359.99,
                                                  order_date = {{2013,10,15},{16,43,16}}},
                             #order_summary_entry{order_id = 3,total = 74.98,
                                                  order_date = {{2013,11,3},{17,45,28}}}]}}
```

While this pattern is very easy and extremely fast with respect to
queries and complexity, it's up to the application to know about these
intrinsic relationships.

#### Secondary Indexes

**Note:**
Secondary indexes in OpenRiak KV require a sorted backend: [Memory](/kv/3.4.0/explanation/storage/memory/) or [LevelDB](/kv/3.4.0/explanation/storage/leveldb/). [Bitcask](/kv/3.4.0/explanation/storage/bitcask/) does not support secondary indexes.

See [Using Secondary Indexes (2i)](/kv/3.4.0/how-to/develop/query-secondary-indexes/) for more information on developing with secondary indexes.

If you're coming from an SQL world, Secondary Indexes (2i) are a lot
like SQL indexes. They are a way to quickly look up objects based on a
secondary key, without scanning through the whole dataset. This makes it
very easy to find groups of related data by values, or even ranges of
values. To properly show this off, we will now add some more data to our
application, and add some secondary index entries at the same time.

```erlang
FormatDate = fun(DateTime) ->
  {{Year, Month, Day}, {Hour, Min, Sec}} = DateTime,
  lists:concat([Year,Month,Day,Hour,Min,Sec])
end.

AddIndicesToOrder = fun(OrderKey) ->
  {ok, Order} = riakc_pb_socket:get(Pid, OrderBucket,
                                    list_to_binary(integer_to_list(OrderKey))),

OrderData = binary_to_term(riakc_obj:get_value(Order)),
  OrderMetadata = riakc_obj:get_update_metadata(Order),

MD1 = riakc_obj:set_secondary_index(OrderMetadata,
                                      [{{binary_index, "order_date"},
                                        [FormatDate(OrderData#order.order_date)]}]),

MD2 = riakc_obj:set_secondary_index(MD1,
                                      [{{integer_index, "salesperson_id"},
                                        [OrderData#order.salesperson_id]}]),

Order2 = riakc_obj:update_metadata(Order,MD2),
  riakc_pb_socket:put(Pid,Order2)
end.

lists:foreach(AddIndicesToOrder, [1,2,3]).

```

As you may have noticed, ordinary Key/Value data is opaque to 2i, so we
have to add entries to the indices at the application level. Now let's
find all of Jane Appleseed's processed orders, we'll lookup the orders
by searching the `saleperson_id_int` index for Jane's id of `9000`.

```erlang
riakc_pb_socket:get_index_eq(Pid, OrderBucket, {integer_index, "salesperson_id"}, 9000).
```

Which returns:

```erlang
{ok,{index_results_v1,[<<"1">>,<<"3">>],
                      undefined,undefined}}
```

Jane processed orders 1 and 3. We used an "integer" index to reference
Jane's id, next let's use a "binary" index. Now, let's say that the VP
of Sales wants to know how many orders came in during October 2013. In
this case, we can exploit 2i's range queries. Let's search the
`order_date_bin` index for entries between `20131001` and `20131031`.

```erlang
riakc_pb_socket:get_index_range(Pid, OrderBucket,
                                {binary_index, "order_date"},
                                <<"20131001">>, <<"20131031">>).
```

Which returns:

```erlang
{ok,{index_results_v1,[<<"1">>,<<"2">>],
                      undefined,undefined}}
```

Boom! Easy-peasy. We used 2i's range feature to search for a range of
values, and demonstrated binary indexes.

So, to recap:

* You can use Secondary Indexes to quickly lookup an object based on a
  secondary id other than the object's key.
* Indices can have either Integer or Binary(String) keys
* You can search for specific values, or a range of values
* Riak will return a list of keys that match the index query

## What you will learn

By completing this tutorial, you will build the workflow described above and learn how to validate each stage before moving on.

## Before you begin

Use a disposable OpenRiak KV environment that matches this documentation version, and keep cluster status and logs available while you work.

## Verify the result

Repeat the completed workflow, inspect the stored or operational result, and confirm that the cluster remains healthy.
