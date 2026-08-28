---
title: 'Build a first OpenRiak application with Node.js'
description: 'Guide a developer through modeling, storing, retrieving, querying, and updating a small dataset with Node.js.'
weight: 6
diataxis: 'tutorial'
product: 'OpenRiak KV'
product_version: '3.4.1'
status: 'editorially-rewritten'
draft: true
audience:
  - 'new-developers'
source_material:
  - 'legacy-3.2.5'
  - 'live-3.2.5'
  - 'proposed-kv'
legacy_3_2_5_sources:
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\developing\getting-started\nodejs.md'
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\developing\getting-started\nodejs\crud-operations.md'
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\developing\getting-started\nodejs\object-modeling.md'
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\developing\getting-started\nodejs\querying.md'
tags: ['diataxis', 'kv', 'tutorial']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Guide a developer through modeling, storing, retrieving, querying, and updating a small dataset with Node.js.

## Overview

### Getting Started with NodeJS

[introduction.js]: https://github.com/basho/riak-nodejs-client-examples/blob/master/dev/taste-of-riak/introduction.js
[npm]: https://www.npmjs.com/package/basho-riak-client
[node_js_installation]: https://github.com/basho/riak-nodejs-client/wiki/Installation
[nodejs_wiki]: https://github.com/basho/riak-nodejs-client/wiki

If you haven't set up an OpenRiak node and started it, please visit [Running A Cluster](/kv/3.4.1/how-to/operate/) first.

To try this flavor of Riak, a working installation of Node.js 0.12 or later is
required.

Code for these examples is available [here][introduction.js]. To run, follow
these directions:

```bash
git clone git://github.com/basho/riak-nodejs-client-examples
cd riak-nodejs-client-examples
npm install
node ./app.js
```

#### Client Setup

Install [the OpenRiak node.js Client][node_js_installation] through [NPM][npm].

##### Connecting to Riak

Connecting to Riak with the OpenRiak node.js Client requires creating a new client
object and using the callback argument to know when the client is fully
initialized:

```javascript
var Riak = require('basho-riak-client');
var nodes = [
    'riak-test:10017',
    'riak-test:10027',
    'riak-test:10037',
    'riak-test:10047'
];
var client = new Riak.Client(nodes, function (err, c) {
    // NB: at this point the client is fully initialized, and
    // 'client' and 'c' are the same object
});
```

This creates a new `Riak.Client` object which handles all the details of
tracking active nodes and also provides load balancing. The `Riak.Client` object
is used to send commands to Riak. When your application is completely done with
Riak communications, the following method can be used to gracefully shut the
client down and exit Node.js:

```javascript
client.stop(function (err, rslt) {
    // NB: you may wish to check err
    process.exit();
});
```

Let's make sure the cluster is online with a `Ping` request:

```javascript
var assert = require('assert');

client.ping(function (err, rslt) {
    if (err) {
        throw new Error(err);
    } else {
        // On success, ping returns true
        assert(rslt === true);
    }
});
```

This is some simple code to test that a node in an OpenRiak cluster is online - we
send a simple ping message. Even if the cluster isn't present, the OpenRiak node.js
Client will return a response message. In the callback it is important to check
that your activity was successful by checking the `err` variable.

We are now ready to start interacting with Riak.

#### Next Steps

[CRUD Operations](/kv/3.4.1/tutorials/first-application/nodejs/)

### CRUD Operations with NodeJS

[nodejs_wiki]: https://github.com/basho/riak-nodejs-client/wiki

#### Creating Objects In OpenRiak KV

Pinging an OpenRiak cluster sounds like a lot of fun, but eventually someone is going
to want us to do productive work. Let's create some data to save in Riak.

The OpenRiak node.js Client makes use of a `RiakObject` class to encapsulate Riak
key/value objects. At the most basic, a `RiakObject` is responsible for
identifying your object and for translating it into a format that can be easily
saved to Riak.

```javascript
var async = require('async');

var people = [
    {
        emailAddress: "bashoman@basho.com",
        firstName: "Basho",
        lastName: "Man"
    },
    {
        emailAddress: "johndoe@gmail.com",
        firstName: "John",
        lastName: "Doe"
    }
];

var storeFuncs = [];
people.forEach(function (person) {
    // Create functions to execute in parallel to store people
    storeFuncs.push(function (async_cb) {
        client.storeValue({
                bucket: 'contributors',
                key: person.emailAddress,
                value: person
            },
            function(err, rslt) {
                async_cb(err, rslt);
            }
        );
    });
});

async.parallel(storeFuncs, function (err, rslts) {
    if (err) {
        throw new Error(err);
    }
});
```

In this sample, we create a collection of `Person` objects and then save each
`Person` to Riak. Once again, we check the response from Riak.

#### Reading from Riak

Let's find a person!

```javascript
var logger = require('winston');

client.fetchValue({ bucket: 'contributors', key: 'bashoman@basho.com', convertToJs: true },
    function (err, rslt) {
        if (err) {
            throw new Error(err);
        } else {
            var riakObj = rslt.values.shift();
            var bashoman = riakObj.value;
            logger.info("I found %s in 'contributors'", bashoman.emailAddress);
        }
    }
);
```

We use `client.fetchValue` to retrieve an object from Riak. This returns an
array of `RiakObject` objects which helpfully encapsulates the communication
with Riak.

After verifying that we've been able to communicate with Riak *and* that we have
a successful result, we use the `value` property to get the object, which has
already been converted to a javascript object due to the use of `convertToJs:
true` in the options.

#### Modifying Existing Data

Let's say that Basho Man has decided to be known as Riak Man:

```javascript
bashoman.FirstName = "Riak";
riakObj.setValue(bashoman);

client.storeValue({ value: riakObj }, function (err, rslt) {
    if (err) {
        throw new Error(err);
    }
});
```

Updating an object involves modifying a `RiakObject` then using
`client.storeValue` to save the existing object.

#### Deleting Data

```javascript
client.deleteValue({ bucket: 'contributors', key: 'johndoe@gmail.com' }, function (err, rslt) {
    if (err) {
        throw new Error(err);
    }
});
```

Just like other operations, we check the results that have come back from Riak
to make sure the object was successfully deleted.

The OpenRiak node.js Client has a lot of additional functionality that makes it easy
to build rich, complex applications with Riak. Check out the
[documentation][nodejs_wiki] to learn more about working with the OpenRiak node.js
Client and Riak.

### Object Modeling with NodeJS

To get started, let's create the models that we'll be using.

* [`Msg`](https://github.com/basho/taste-of-riak/blob/master/nodejs/Ch03-Msgy-Schema/models/msg.js)
* [`Timeline`](https://github.com/basho/taste-of-riak/blob/master/nodejs/Ch03-Msgy-Schema/models/timeline.js)
* [`User`](https://github.com/basho/taste-of-riak/blob/master/nodejs/Ch03-Msgy-Schema/models/user.js)

To use these classes to store data, we will first have to create a user.
Then, when a user creates a message, we will append that message to one
or more timelines. If it's a private message, we'll append it to the
Recipient's `Inbox` timeline and the User's own `Sent` timeline. If it's
a group message, we'll append it to the Group's timeline, as well as to
the User's `Sent` timeline.

#### Buckets and Keys Revisited

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

| Bucket | Key Pattern | Example Key
|:-------|:------------|:-----------
| `Users` | `<user_name>` | `joeuser`
| `Msgs` | `<username>_<datetime>` | `joeuser_2014-03-06T02:05:13.556Z`
| `Timelines` | `<username>_<type>_<date>` | `joeuser_SENT_2014-03-06`<br /> `marketing_group_INBOX_2014-03-06` |

For the `Users` bucket, we can be certain that we will want each
username to be unique, so let's use the `userName` as the key.

[*Example:* `userName` as key](https://github.com/basho/taste-of-riak/blob/master/nodejs/Ch03-Msgy-Schema/models/user.js#L19-L20)

For the `Msgs` bucket, let's use a combination of the username and the
posting datetime in an [ISO 8601
Long](http://en.wikipedia.org/wiki/ISO_8601) format. This combination
gives us the pattern `<username>_<datetime>`, which produces keys like
`joeuser_2014-03-05T23:20:28Z`.

[*Example:* `Msg` key](https://github.com/basho/taste-of-riak/blob/master/nodejs/Ch03-Msgy-Schema/models/msg.js#L25-L27)

Now for `Timelines`, we need to differentiate between `Inbox` and `Sent`
timelines, so we can simply add that type into the key name. We will
also want to partition each collection object into some time period,
that way the object doesn't grow too large (see note below).

For `Timelines`, let's use the pattern `<username>_<type>_<date>` for
users, and `<groupname>_Inbox_<date>` for groups, which will look like
`joeuser_SENT_2014-03-06` or `marketing_group_INBOX_2014-03-05`,
respectively.

**Note**
Riak performs best with objects under 1-2MB. Objects larger than that can hurt
performance, especially many siblings are being created. We will cover
siblings, sibling resolution, and sibling explosions in the next chapter.

#### Keeping our story straight with repositories

Now that we've figured out our object model, let's write some
repositories to help create and work with these objects in Riak:

* [Base `Repository` class](https://github.com/basho/taste-of-riak/blob/master/nodejs/Ch03-Msgy-Schema/repositories/repository.js)
* [`UserRepository` class](https://github.com/basho/taste-of-riak/blob/master/nodejs/Ch03-Msgy-Schema/repositories/user-repository.js)
* [`MsgRepository` class](https://github.com/basho/taste-of-riak/blob/master/nodejs/Ch03-Msgy-Schema/repositories/msg-repository.js)
* [`TimelineRepository` class](https://github.com/basho/taste-of-riak/blob/master/nodejs/Ch03-Msgy-Schema/repositories/timeline-repository.js)
* [`TimelineManager` class that manages `Msg` and `Timeline` objects](https://github.com/basho/taste-of-riak/blob/master/nodejs/Ch03-Msgy-Schema/timeline-manager.js)

Finally, let's test them:

[*Example:* Putting it all together](https://github.com/basho/taste-of-riak/blob/master/nodejs/Ch03-Msgy-Schema/app.js)

As you can see, the repository pattern helps us with a few things:

- It helps us to see if an object exists before creating a new one
 - It keeps our buckets and key names consistent
 - It provides us with a consistent interface to work with.

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
* How to choose natural keys based on how we want to partition our data

### Querying with NodeJS

#### Node.js Version Setup

For the Node.js version, please download the source from GitHub by either
[cloning](https://github.com/basho/taste-of-riak) the source code
repository or downloading the [current zip of the master
branch](https://github.com/basho/taste-of-riak/archive/master.zip).
The code for this chapter is in `nodejs/Ch02-Schemas-and-Indexes`. Be
sure to run `npm install` in this directory prior to running `node
./app.js` to run the code.

#### A Quick Note on Querying and Schemas

_Schemas_? Yes, we said that correctly: S-C-H-E-M-A-S. It's not a dirty
word. Even in a key/value store, you will still have a logical database
schema of how all the data relates to other data. This can be as simple
as using the same key across multiple buckets for different types of
data to having fields in your data that are related by name. These
querying methods will introduce you to some ways of laying out your data
in Riak, along with how to query it back.

#### Denormalization

If you're coming from a relational database, the easiest way to get your
application's feet wet with NoSQL is to denormalize your data into
related chunks. For example, with a customer database, you might have
separate tables for customers, addresses, preferences, etc. In Riak,
you can denormalize all that associated data into a single object and
store it into a `Customer` bucket. You can keep pulling in associated
data until you hit one of the big denormalization walls:

* Size Limits (objects greater than 1MB)
* Shared/Referential Data (data that the object doesn't "own")
* Differences in Access Patterns (objects that get read/written once vs.
  often)

At one of these points we will have to split the model.

#### Same Keys, Different Buckets

The simplest way to split up data would be to use the same identity key
across different buckets. A good example of this would be a `Customer`
object, an `Order` object, and an `OrderSummaries` object that keeps
rolled up info about orders such as total, etc. Let's put some data into
Riak so we can play with it.

* [*Example:* Creating a customer](https://github.com/basho/taste-of-riak/blob/master/nodejs/Ch02-Schemas-and-Indexes/app.js#L24-L33)
* [*Example:* Creating orders and order summaries](https://github.com/basho/taste-of-riak/blob/master/nodejs/Ch02-Schemas-and-Indexes/app.js#L193-L262)

While individual Customer and Order objects don't change much (or
shouldn't change), the "Order Summary" object will likely change often.
It will do double duty by acting as an index for all a customer's
orders, and also holding some relevant data such as the order total,
etc. If we showed this information in our application often, it's only
one extra request to get all the info.

[*Example:* Fetching by shared key](https://github.com/basho/taste-of-riak/blob/master/nodejs/Ch02-Schemas-and-Indexes/app.js#L78-L96)

Which returns our amalgamated objects:

```bash
info: Customer     1: {"id":"1","name":"John Smith","address":"123 Main Street","city":"Columbus","state":"Ohio","zip":"43210","phone":"+1-614-555-5555","createdDate":"2013-10-01 14:30:26"}
info: OrderSummary 1: {"customerId":"1","summaries":[{"orderId":"1","total":415.98,"orderDate":"2013-10-01 14:42:26"},{"orderId":"2","total":359.99,"orderDate":"2013-10-15 16:43:16"},{"orderId":"3","total":74.98,"orderDate":"2013-11-03 17:45:28"}]}
```

While this pattern is very easy and extremely fast with respect to
queries and complexity, it's up to the application to know about these
intrinsic relationships.

#### Secondary Indexes

**Note:**
Secondary indexes in OpenRiak KV require a sorted backend: [Memory](/kv/3.4.1/explanation/storage/memory/) or [LevelDB](/kv/3.4.1/explanation/storage/leveldb/). [Bitcask](/kv/3.4.1/explanation/storage/bitcask/) does not support secondary indexes.

See [Using Secondary Indexes (2i)](/kv/3.4.1/how-to/develop/query-secondary-indexes/) for more information on developing with secondary indexes.

If you're coming from an SQL world, Secondary Indexes (2i) are a lot
like SQL indexes. They are a way to quickly look up objects based on a
secondary key, without scanning through the whole dataset. This makes it
very easy to find groups of related data by values, or even ranges of
values. To properly show this off, we will now add some more data to our
application, and add some secondary index entries at the same time.

[*Example:* Adding index data](https://github.com/basho/taste-of-riak/blob/master/nodejs/Ch02-Schemas-and-Indexes/app.js#L98-L141)

As you may have noticed, ordinary key/value data is opaque to 2i, so we
have to add entries to the indexes at the application level. Now let's
find all of Jane Appleseed's processed orders, we'll look up the orders
by searching the `SalespersonId` integer index for Jane's id of `9000`.

[*Example:* Query for orders where the SalespersonId index is set to 9000](https://github.com/basho/taste-of-riak/blob/master/nodejs/Ch02-Schemas-and-Indexes/app.js#L143-L159)

Which returns:

```text
Jane's Orders: 1, 3
```

Jane processed orders 1 and 3. We used an "integer" index to reference
Jane's ID, next let's use a "binary" index. Now, let's say that the VP
of Sales wants to know how many orders came in during October 2013. In
this case, we can exploit 2i's range queries. Let's search the
`OrderDate` binary index for entries between `2013-10-01` and
`2013-10-31`.

[*Example:* Query for orders where the OrderDate index is between 2013-10-01 and
2013-10-31](https://github.com/basho/taste-of-riak/blob/master/nodejs/Ch02-Schemas-and-Indexes/app.js#L161-175)

Which returns:

```text
October's Orders: 1, 2
```

Boom! Easy-peasy. We used 2i's range feature to search for a range of
values, and demonstrated binary indexes.

So to recap:

* You can use Secondary Indexes to quickly look up an object based on a
  secondary id other than the object's key.
* Indexes can have either Integer or Binary(String) keys
* You can search for specific values, or a range of values
* Riak will return a list of keys that match the index query

## What you will learn

By completing this tutorial, you will build the workflow described above and learn how to validate each stage before moving on.

## Before you begin

Use a disposable OpenRiak KV environment that matches this documentation version, and keep cluster status and logs available while you work.

## Verify the result

Repeat the completed workflow, inspect the stored or operational result, and confirm that the cluster remains healthy.
