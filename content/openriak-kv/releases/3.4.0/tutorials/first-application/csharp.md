---
title: 'Build a first OpenRiak application with C#'
description: 'Guide a developer through modeling, storing, retrieving, querying, and updating a small dataset with C#.'
weight: 2
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
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\developing\getting-started\csharp.md'
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\developing\getting-started\csharp\crud-operations.md'
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\developing\getting-started\csharp\object-modeling.md'
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\developing\getting-started\csharp\querying.md'
tags: ['diataxis', 'kv', 'tutorial']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Guide a developer through modeling, storing, retrieving, querying, and updating a small dataset with C#.

## Overview

### Getting Started with C Sharp

If you haven't set up an OpenRiak node and started it, please visit [Running A Cluster]({{< product-version-root >}}how-to/operate/) first.

To try this flavor of Riak, a working installation of the .NET Framework or Mono is required.

#### Client Setup

Install [the Riak .NET Client](https://github.com/basho/riak-dotnet-client/wiki/Installation) through [NuGet](http://nuget.org/packages/RiakClient) or the Visual Studio NuGet package manager.

**Configuring for a remote cluster**
By default, the Riak .NET Client will add a section to your `app.config` file
for a four node local cluster. If you are using a remote cluster, open up
`app.config` and change the `hostAddress` values to point to nodes in your
remote cluster.

##### Connecting to Riak

Connecting to Riak with the Riak .NET Client requires creating a cluster object and then creating a new client object.

```csharp
using System;
using RiakClient;

namespace TasteOfRiak
{
    class Program
    {
        static void Main(string[] args)
        {
          // don't worry, we'll use this string later
          const string contributors = "contributors";
            IRiakEndpoint cluster = RiakCluster.FromConfig("riakConfig");
            IRiakClient client = cluster.CreateClient();
        }
    }
}
```

This creates a new `RiakCluster` which is used to create a new `RiakClient`. A `RiakCluster` object handles all the details of tracking active nodes and also provides load balancing. The `RiakClient` is used to send commands to Riak. *Note:* the `IRiakEndpoint` object implements `IDisposable` and should be correctly disposed when you're done communicating with Riak.

Let's make sure the cluster is online. Add this to your `Main` method:

```csharp
var pingResult = client.Ping();

if (pingResult.IsSuccess)
{
    Console.WriteLine("pong");
}
else
{
    Console.WriteLine("Are you sure Riak is running?");
    Console.WriteLine("{0}: {1}", pingResult.ResultCode, pingResult.ErrorMessage);
}
```

This is some simple code to test that a node in an OpenRiak cluster is online - we send a simple ping message. Even if the cluster isn't present, the Riak .NET Client will return a response message. It's important to check that your activity was successful by using the `IsSuccess` property and then checking any errors and result codes.

We are now ready to start interacting with Riak.

#### Next Steps

[CRUD Operations]({{< product-version-root >}}tutorials/first-application/csharp/)

### CRUD Operations with C Sharp

#### Creating Objects In Riak

Pinging an OpenRiak cluster sounds like a lot of fun, but eventually someone is going to want us to do productive work. Let's create a class to represent some data and save some objects into Riak.

The Riak .NET Client makes use of a `RiakObject` class to encapsulate Riak key/value objects. At the most basic, a `RiakObject` is responsible for identifying your object and for translating it into a format that can be easily saved to Riak.

Add the `RiakClient.Models` namespace to your using directive. Your usings should look like this:

```csharp
using System;
using System.Collections.Generic;
using RiakClient;
using RiakClient.Models;
```

Add the `Person` class to the `TasteOfRiak` namespace:

```csharp
public class Person
{
    public string EmailAddress { get; set; }
    public string FirstName { get; set; }
    public string LastName { get; set; }
}
```

Now let's create some people!

```csharp
var people = new[]
{
    new Person {
        EmailAddress = "bashoman@basho.com",
        FirstName = "Basho",
        LastName = "Man"
    },
    new Person {
        EmailAddress = "johndoe@gmail.com",
        FirstName = "John",
        LastName = "Doe"
    }
};

foreach (var person in people)
{
    var o = new RiakObject(contributors, person.EmailAddress, person);
    var putResult = client.Put(o);

if (putResult.IsSuccess)
    {
        Console.WriteLine("Successfully saved {1} to bucket {0}", o.Key, o.Bucket);
    }
    else
    {
        Console.WriteLine("Are you *really* sure Riak is running?");
        Console.WriteLine("{0}: {1}", putResult.ResultCode, putResult.ErrorMessage);
    }
}
```

In this sample, we create a collection of `Person` objects and then save each `Person` to Riak.

Before saving, we need to create a `RiakObject` that encapsulates the bucket, key, and object to be saved. Once we've created a `RiakObject` from our `Person` object, we can save it to Riak using `Client.Put()`.

Once again, we check the response from Riak. If things are successful, you'll see a helpful message letting you know that your object has been saved to Riak. If things didn't go as planned, there will be an error message displaying the result code and a helpful error message.

#### Reading from Riak

Let's find a person!

```csharp
var result = client.Get(contributors, "bashoman@basho.com");
if (result.IsSuccess)
{
    bashoman = result.Value.GetObject<Person>();
    Console.WriteLine("I found {0} in {1}", bashoman.EmailAddress, contributors);
}
else
{
    Console.WriteLine("Something went wrong!");
    Console.WriteLine("{0}: {1}", result.ResultCode, result.ErrorMessage);
}
```

We use `RiakClient.Get` to retrieve an object from Riak. This returns a `RiakResult<RiakObject>` which, like other RiakResults, helpfully encapsulates the communication with Riak.

After verifying that we've been able to communicate with Riak *and* that we have a successful result, we use `GetObject<T>` to deserialize our object.

#### Modifying Existing Data

Let's say that Basho Man has decided to be known as Riak Man:

```csharp
bashoman.FirstName = "Riak";

var o = new RiakObject(contributors, bashoman.EmailAddress, bashoman);
var updateResult = client.Put(o);
if (updateResult.IsSuccess)
{
    Console.WriteLine("Successfully updated {0} in {1}", bashoman.EmailAddress, contributors);
}
else
{
    Console.WriteLine("Something went wrong!");
    Console.WriteLine("{0}: {1}", updateResult.ResultCode, updateResult.ErrorMessage);
}
```

Updating an object involves creating a new `RiakObject` then using `RiakClient.Put` to save the existing object.

#### Deleting Data

```csharp
var deleteResult = client.Delete(contributors, "johndoe@gmail.com");
if (deleteResult.IsSuccess)
{
    Console.WriteLine("Successfully got rid of John Doe");
}
else
{
    Console.WriteLine("Something went wrong!");
    Console.WriteLine("{0}: {1}", deleteResult.ResultCode, deleteResult.ErrorMessage);
}
```

Just like other operations, we check the results that have come back from Riak to make sure the object was successfully deleted.

The Riak .NET Client has a lot of additional functionality that makes it easy to build rich, complex applications with Riak. Check out the [documentation](https://github.com/basho/riak-dotnet-client/wiki) to learn more about working with the Riak .NET Client and Riak.

### Object Modeling with C Sharp

To get started, refer to [this source code][1] for the models that we'll
be using.

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
| `Msgs` | `<username>_<datetime>` | `joeuser_2014-03-06T02:05:13`
| `Timelines` | `<username>_<type>_<date>` | `joeuser_Sent_2014-03-06`<br /> `marketing_group_Inbox_2014-03-06` |

For the `Users` bucket, we can be certain that we will want each
username to be unique, so let's use the `username` as the key.

For the `Msgs` bucket, let's use a combination of the username and the
posting UTC datetime in an [ISO 8601][iso_8601]
format. This combination gives us the pattern `<username>_<datetime>`,
which produces keys like `joeuser_2014-03-05T23:20:28`.

Now for `Timelines`, we need to differentiate between `Inbox` and `Sent`
timelines, so we can simply add that type into the key name. We will
also want to partition each collection object into some time period,
that way the object doesn't grow too large (see note below).

For `Timelines`, let's use the pattern `<username>_<type>_<date>` for
users, and `<groupname>_Inbox_<date>` for groups, which will look like
`joeuser_Sent_2014-03-06` or `marketing_group_Inbox_2014-03-05`,
respectively.

**Note**
Riak performs best with objects under 1-2MB. Objects larger than that can hurt
performance, especially when many siblings are being created. We will cover
siblings, sibling resolution, and sibling explosions in the next chapter.

#### Keeping our story straight with repositories

Now that we've figured out our object model, please refer to
[this source code][2] for the repositories that we'll be using.

[This console application][3] exercises the code that we've written.

The repository pattern and `TimelineManager` help with a few things:

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

[1]: https://github.com/basho/taste-of-riak/tree/master/csharp/Ch03-Msgy-Schema/Models
[2]: https://github.com/basho/taste-of-riak/tree/master/csharp/Ch03-Msgy-Schema/Repositories
[3]: https://github.com/basho/taste-of-riak/blob/master/csharp/Ch03-Msgy-Schema/Program.cs
[iso_8601]: http://en.wikipedia.org/wiki/ISO_8601

### Querying with C Sharp

#### C Sharp Version Setup

For the C# version, please download the source from GitHub by either
[cloning][taste_of_riak] the source code repository or downloading the
[current zip of the master branch][master_zip]. The code for this
chapter is in `/csharp`. Open up `TasteOfRiak.sln` in Visual Studio or
your IDE of choice.

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
rolled up info about orders such as total, etc. You can find the source
for these POCOs in `Customer.cs`, `Order.cs` and
`OrderSummaries.cs`.  Let's put some data into Riak so we can play
with it.

```csharp
Console.WriteLine("Creating Data");
Customer customer = CreateCustomer();
IEnumerable<Order> orders = CreateOrders(customer);
OrderSummary orderSummary = CreateOrderSummary(customer, orders);

Console.WriteLine("Starting Client");
using (IRiakEndPoint endpoint = RiakCluster.FromConfig("riakConfig"))
{
    IRiakClient client = endpoint.CreateClient();

Console.WriteLine("Storing Data");

client.Put(ToRiakObject(customer));

foreach (Order order in orders)
    {
        // NB: this adds secondary index data as well
        client.Put(ToRiakObject(order));
    }

client.Put(ToRiakObject(orderSummary));

...
    ...
    ...
}
```

While individual `Customer` and `Order` objects don't change much (or
shouldn't change), the `OrderSummaries` object will likely change often.
It will do double duty by acting as an index for all a customer's
orders, and also holding some relevant data such as the order total,
etc. If we showed this information in our application often, it's only
one extra request to get all the info.

```csharp
Console.WriteLine("Fetching related data by shared key");
string key = "1";

var result = client.Get(customersBucketName, key);
CheckResult(result);
Console.WriteLine("Customer     1: {0}\n", GetValueAsString(result));

result = client.Get(orderSummariesBucketName, key);
CheckResult(result);
Console.WriteLine("OrderSummary 1: {0}\n", GetValueAsString(result));
```

Which returns our amalgamated objects:

```bash
Fetching related data by shared key
Customer     1: {"CustomerId":1,"Name":"John Smith","Address":"123 Main Street","City":"Columbus","State":"Ohio","Zip":"43210","Phone":"+1-614-555-5555","CreatedDate":"2013-10-01 14:30:26"}
OrderSummary 1: {"CustomerId":1,"Summaries":[{"OrderId":1,"Total":415.98,"OrderDate":"2013-10-01 14:42:26"},{"OrderId":2,"Total":359.99,"OrderDate":"2013-10-15 16:43:16"},{"OrderId":3,"Total":74.98,"OrderDate":"2013-11-03 17:45:28"}]}
```

While this pattern is very easy and extremely fast with respect to
queries and complexity, it's up to the application to know about these
intrinsic relationships.

#### Secondary Indexes

**Note:**
Secondary indexes in OpenRiak KV require a sorted backend: [Memory]({{< product-version-root >}}explanation/storage/memory/) or [LevelDB]({{< product-version-root >}}explanation/storage/leveldb/). [Bitcask]({{< product-version-root >}}explanation/storage/bitcask/) does not support secondary indexes.

See [Using Secondary Indexes (2i)]({{< product-version-root >}}how-to/develop/query-secondary-indexes/) for more information on developing with secondary indexes.

If you're coming from an SQL world, Secondary Indexes (2i) are a lot
like SQL indexes. They are a way to quickly look up objects based on a
secondary key, without scanning through the whole dataset. This makes it
very easy to find groups of related data by values, or even ranges of
values. To properly show this off, we will make a note of where
secondary index data is added to our model objects.

```csharp
private static RiakObject ToRiakObject(Order order)
{
    var orderRiakObjectId = new RiakObjectId(ordersBucketName, order.Id.ToString());
    var riakObject = new RiakObject(orderRiakObjectId, order);

IntIndex salesPersonIdIndex = riakObject.IntIndex(ordersSalesPersonIdIndexName);
    salesPersonIdIndex.Add(order.SalesPersonId.ToString());

BinIndex orderDateIndex = riakObject.BinIndex(ordersOrderDateIndexName);
    orderDateIndex.Add(order.OrderDate.ToString("yyyy-MM-dd"));

return riakObject;
}
```

As you may have noticed, ordinary key/value data is opaque to 2i, so we
have to add entries to the indexes at the application level. Now let's
find all of Jane Appleseed's processed orders, we'll look up the orders
by searching the `SalespersonId` integer index for Jane's id of `9000`.

```csharp
// Query for order keys where the SalesPersonId index is set to 9000
var riakIndexId = new RiakIndexId(ordersBucketName, ordersSalesPersonIdIndexName);
RiakResult<RiakIndexResult> indexRiakResult = client.GetSecondaryIndex(riakIndexId, 9000); // NB: *must* use 9000 as integer here.
CheckResult(indexRiakResult);
RiakIndexResult indexResult = indexRiakResult.Value;
Console.WriteLine("Jane's orders (key values): {0}", string.Join(", ", indexResult.IndexKeyTerms.Select(ikt => ikt.Key)));
```

Which returns:

```text
Jane's orders (key values): 1, 3
```

Jane processed orders 1 and 3. We used an "integer" index to reference
Jane's ID, next let's use a "binary" index. Now, let's say that the VP
of Sales wants to know how many orders came in during October 2013. In
this case, we can exploit 2i's range queries. Let's search the
`OrderDate` binary index for entries between `2013-10-01` and
`2013-10-31`.

```csharp
// Query for orders where the OrderDate index is between 2013-10-01 and 2013-10-31
riakIndexId = new RiakIndexId(ordersBucketName, ordersOrderDateIndexName);
indexRiakResult = client.GetSecondaryIndex(riakIndexId, "2013-10-01", "2013-10-31"); // NB: *must* use strings here.
CheckResult(indexRiakResult);
indexResult = indexRiakResult.Value;
Console.WriteLine("October orders (key values): {0}", string.Join(", ", indexResult.IndexKeyTerms.Select(ikt => ikt.Key)));
```

Which returns:

```text
October orders (key values): 1, 2
```

We used 2i's range feature to search for a range of values, and demonstrated binary indexes.

So to recap:

* You can use Secondary Indexes to quickly look up an object based on a
  secondary id other than the object's key.
* Indexes can have either Integer or Binary(String) keys
* You can search for specific values, or a range of values
* Riak will return a list of keys that match the index query

[taste_of_riak]: https://github.com/basho/taste-of-riak
[master_zip]: https://github.com/basho/taste-of-riak/archive/master.zip

## What you will learn

By completing this tutorial, you will build the workflow described above and learn how to validate each stage before moving on.

## Before you begin

Use a disposable OpenRiak KV environment that matches this documentation version, and keep cluster status and logs available while you work.

## Verify the result

Repeat the completed workflow, inspect the stored or operational result, and confirm that the cluster remains healthy.
