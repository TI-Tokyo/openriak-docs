---
title: 'Build a first OpenRiak application with Java'
description: 'Guide a developer through modeling, storing, retrieving, querying, and updating a small dataset with Java.'
weight: 5
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
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\developing\getting-started\java.md'
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\developing\getting-started\java\crud-operations.md'
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\developing\getting-started\java\object-modeling.md'
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\developing\getting-started\java\querying.md'
tags: ['diataxis', 'kv', 'tutorial']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Guide a developer through modeling, storing, retrieving, querying, and updating a small dataset with Java.

## Overview

### Getting Started with Java

If you haven't set up an OpenRiak node and started it, please visit [Running A Cluster]({{< baseurl >}}kv/3.4.0/how-to/operate/) first.

To try this flavor of Riak, a working installation of Java is required.

#### Client Setup

To include the Riak Java client in your project, add it to your
project's dependencies. Here is a Maven example:

```xml
<dependencies>
  <dependency>
    <groupId>com.basho.riak</groupId>
    <artifactId>riak-client</artifactId>
    <version>2.1.1</version>
  </dependency
</dependencies>
```

Next, download
[`TasteOfRiak.java`](https://github.com/basho/basho_docs/raw/master/extras/code-examples/TasteOfRiak.java)
source code for this tutorial, and save it to your working directory.

**Configuring for a local cluster**
The `TasteOfRiak.java` file that you downloaded is set up to communicate with
a 1-node OpenRiak cluster listening on `localhost` port 10017. We recommend
modifying the connection info directly within the `setUpCluster()` method.

If you execute the `TasteOfRiak.java` file within your IDE, you should
see the following:

```
Basic object created
Location object created for quote object
StoreValue operation created
Client object successfully created
Object storage operation successfully completed
Success! The object we created and the object we fetched have the same value
Quote object successfully deleted
Book object created
Moby Dick information now stored in Riak
Book object successfully fetched
Success! All of our tests check out
```

Since Java doesn’t have a REPL environment, let's walk through the code
to see what it actually did at each step.

#### Setting Up the Cluster

The first step in using the Riak Java client is to create a cluster
object to facilitate all interactions with Riak. You'll see this on line
72:

```java
RiakCluster cluster = setUpCluster();
```

This calls the private `setUpCluster` method which begins on line 25.
Using that `cluster` object, we can instantiate a client object which
will execute all Riak interactions:

```java
RiakClient client = new RiakClient(cluster);
```

#### Next Steps

[CRUD Operations]({{< baseurl >}}kv/3.4.0/tutorials/first-application/java/)

### CRUD Operations with Java

#### Creating Objects in Riak

The first object that we create is a very basic object with a content
type of `text/plain`. Once that object is created, we create a
`StoreValue` operation that will store the object later on down the line

```java
RiakObject quoteObject = new RiakObject()
        .setContentType("text/plain")
        .setValue(BinaryValue.create("You're dangerous, Maverick"));
Namespace quotesBucket = new Namespace("quotes");
Location quoteObjectLocation = new Location(quotesBucket, "Icemand");
StoreValue storeOp = new StoreValue.Builder(quoteObject)
        .withLocation(quoteObjectLocation)
        .build();
```

We then use our `client` object to execute the storage operation:

```java
StoreValue.Response response = client.execute(storeOp);
```

#### Reading Objects from Riak

After that, we check to make sure that the stored object has the same
value as the object that we created. This requires us to fetch the
object by way of a `FetchValue` operation:

```java
FetchValue fetchOp = new FetchValue.Builder(quoteObjectLocation)
        .build();
RiakObject fetchedObject = client.execute(fetchOp).getValue(RiakObject.class);
assert(fetchedObject.getValue.equals(quoteObject.getValue()));
```

If the values are equal, as they should be, the Java client will say
`Success!  The object we created and the object we fetched have the same
value`. If not, then the client will throw an exception.

#### Updating Objects

Once we've read the object back in from Riak, we can update the object
and store it back as we did before with the `StoreValue` object:

```java
fetchedObject.setValue(BinaryValue.create("You can be my wingman any time."));
StoreValue updateOp = new StoreValue.Builder(fetchedObject)
        .withLocation(quoteObjectLocation)
        .build();
StoreValue.Response updateOpResp = client.execute(updateOp);
```

For more in depth information on updating objects and sibling resolution in
Riak, see [Updating Objects]({{< baseurl >}}kv/3.4.0/how-to/develop/update-object/)
and [Conflict Resolution]({{< baseurl >}}kv/3.4.0/how-to/develop/resolve-conflicts/)
documentation.

#### Deleting Objects

Now that we've stored and then fetched the object, we can delete it by
creating and executing a `DeleteValue` operation:

```java
DeleteValue deleteOp = new DeleteValue.Builder(quoteObjectLocation)
        .build();
client.execute(deleteOp);
```

#### Working With Complex Objects

Since the world is a little more complicated than simple integers and
bits of strings, let’s see how we can work with more complex objects.
Take for example, this plain old Java object (POJO) that encapsulates
some knowledge about a book.

```java
public class Book {
    public String title;
    public String author;
    public String body;
    public String isbn;
    publict Integer copiesOwned;
}
```

By default, the Java Riak client serializes POJOs as JSON. Let's create
a new `Book` object to store:

```java
Book mobyDick = new Book();
modyDick.title = "Moby Dick";
mobyDick.author = "Herman Melville";
mobyDick.body = "Call me Ishmael. Some years ago...";
mobyDick.isbn = "11119799723";
mobyDick.copiesOwned = 3;
```

Now we can store that POJO object just like we stored the more simple
object earlier:

```java
Namespace booksBucket = new Namespace("books");
Location mobyDickLocation = new Location(booksBucket, "moby_dick");
StoreValue storeBookOp = new StoreValue.Builder(mobyDick)
        .withLocation(mobyDickLocation)
        .build();
client.execute(storeBookOp);
```

If we fetch the object (using the same method we showed up above and in
`TasteOfRiak.java`), we should get the following:

```json
{
  "title": "Moby Dick",
  "author": "Herman Melville",
  "body": "Call me Ishmael. Some years ago...",
  "isbn": "1111979723",
  "copiesOwned": 3
}
```

Since we really like Moby Dick, let's buy a couple more copies
and update the POJO.

To update the POJO, we would use `UpdateValue` by
extending a new `BookUpdate` class as follows:

```java
public static class BookUpdate extends UpdateValue.Update<Book> {
    private final Book update;
    public BookUpdate(Book update){
        this.update = update;
    }

@Override
    public Book apply(Book t) {
        if(t == null) {
            t = new Book();
        }

t.author = update.author;
        t.body = update.body;
        t.copiesOwned = update.copiesOwned;
        t.isbn = update.isbn;
        t.title = update.title;

return t;
    }
}
```

Then using the `BookUpdate` class with our `mobyDick` object:

```java
mobyDick.copiesOwned = 5;
BookUpdate updatedBook = new BookUpdate(mobyDick);

UpdateValue updateValue = new UpdateValue.Builder(mobyDickLocation)
    .withUpdate(updatedBook).build();
UpdateValue.Response response = client.execute(updateValue);
```

For more in depth information on updating objects and sibling resolution in
Riak, see [Updating Objects]({{< baseurl >}}kv/3.4.0/how-to/develop/update-object/)
and [Conflict Resolution]({{< baseurl >}}kv/3.4.0/how-to/develop/resolve-conflicts/)
documention.

### Object Modeling with Java

To get started, let's create the models that we'll be using.

```java
package com.basho.msgy.Models;

import java.text.DateFormat;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.TimeZone;

public class Msg {
    public String Sender;
    public String Recipient;
    public String Created;
    public String Text;

public static Msg createNew(String sender, String recipient, String text) {
        Msg msg = new Msg();
        msg.Sender = sender;
        msg.Recipient = recipient;
        msg.Text = text;
        msg.Created = GetCurrentISO8601Timestamp();
        return msg;
    }

private static String GetCurrentISO8601Timestamp() {
        TimeZone tz = TimeZone.getTimeZone("UTC");
        // Java Dates don't have microsecond resolution :(
        // Pad out to microseconds to match other examples.
        DateFormat df = new SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss.SSS'000'");
        df.setTimeZone(tz);
        return df.format(new Date());
    }
}

// ----------------------------------------------------------------------------

import java.util.ArrayList;

public class Timeline {

public enum TimelineType
    {
        Inbox,
        Sent;

@Override
        public String toString() {
            if(this == Inbox)
                return "Inbox";
            else
                return "Sent";
        }
    }

public Timeline() {
        Msgs = new ArrayList<String>();
    }

public String Owner;
    public String Type;
    public ArrayList<String> Msgs;
}

package com.basho.msgy.Models;

import com.basho.riak.client.convert.RiakKey;

public class User {
    @RiakKey
    public String UserName;

@RiakBucketName
    final String bucketName = "msgs";

public String FullName;
    public String Email;

public User() {}

public User(String userName, String fullName, String email) {
        this.UserName = userName;
        this.FullName = fullName;
        this.Email = email;
    }
}
```

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
| `Msgs` | `<username>_<datetime>` | `joeuser_2014-03-06T02:05:13.223556Z`
| `Timelines` | `<username>_<type>_<date>` | `joeuser_Sent_2014-03-06Z`<br /> `marketing_group_Inbox_2014-03-06Z` |

For the `Users` bucket, we can be certain that we will want each
username to be unique, so let's use the `username` as the key.  With the
Java client, we can use the `@RiakKey` annotation to tell the client
that we want to use the `UserName` member as the key. It will
automatically use that value in the future, instead of having to pass the
key in as another parameter when storing a value.

For the `Msgs` bucket, let's use a combination of the username and the
posting datetime in an [ISO 8601
Long](http://en.wikipedia.org/wiki/ISO_8601) format. This combination
gives us the pattern `<username>_<datetime>`, which produces keys like
`joeuser_2014-03-05T23:20:28Z`.

Now for `Timelines`, we need to differentiate between `Inbox` and `Sent`
timelines, so we can simply add that type into the key name. We will
also want to partition each collection object into some time period,
that way the object doesn't grow too large (see note below).

For `Timelines`, let's use the pattern `<username>_<type>_<date>` for
users, and `<groupname>_Inbox_<date>` for groups, which will look like
`joeuser_Sent_2014-03-06Z` or `marketing_group_Inbox_2014-03-05Z`,
respectively.

**Note**
Riak performs best with objects under 1-2MB. Objects larger than that can hurt
performance, especially many siblings are being created. We will cover
siblings, sibling resolution, and sibling explosions in the next chapter.

#### Keeping our story straight with repositories

Now that we've figured out our object model, let's write some
repositories to help create and work with these objects in Riak:

```java
package com.basho.msgy.Repositories;

import com.basho.msgy.Models.Msg;
import com.basho.riak.client.IRiakClient;
import com.basho.riak.client.RiakRetryFailedException;
import com.basho.riak.client.bucket.Bucket;

public class MsgRepository {

static final String BUCKET_NAME = "Msgs";
    protected RiakClient client;

public MsgRepository(RiakClient client) {
        this.client = client;
    }

public Msg get(String msgKey) throws Exception {
        Location key = new Location(new Namespace(BUCKET_NAME), msgKey);
        FetchValue fetch = new FetchValue.Builder(key).build();
        FetchValue.Response response = client.execute(fetch);
        return response.getValue(Msg.class);
    }

public String save(Msg msg) throws Exception {
        StoreValue store = new StoreValue.Builder(msg).build();
        client.execute(store);
        return generateKey(msg);
    }

private String generateKey(Msg msg) {
        return msg.Sender + "_" + msg.Created;
    }
}

package com.basho.msgy.Repositories;

import com.basho.msgy.Models.Msg;
import com.basho.msgy.Models.Timeline;
import com.basho.riak.client.IRiakClient;
import com.basho.riak.client.RiakRetryFailedException;
import com.basho.riak.client.bucket.Bucket;

public class TimelineRepository {

static final String BUCKET_NAME = "Timelines";
    protected RiakClient client;
    protected MsgRepository msgRepo;

public TimelineRepository(RiakClient client) {
        this.client = client;
        this.msgRepo = new MsgRepository(this.client);
    }

public void postMsg(Msg msg) throws Exception {
        String msgKey = msgRepo.save(msg);

// Post to recipient's Inbox timeline
        addToTimeline(msg, Timeline.TimelineType.Inbox, msgKey);

// Post to sender's Sent timeline
        addToTimeline(msg, Timeline.TimelineType.Sent, msgKey);
    }

private void addToTimeline(Msg msg, Timeline.TimelineType type, String msgKey) throws Exception {
        String timelineKey = generateKeyFromMsg(msg, type);

Location loc = new Location(new Namespace(BUCKET_NAME), timelineKey);
        FetchValue fetch = new FetchValue.Builder(loc).build();
        Timeline timeline = client.execute(fetch).getValue(Timeline.class);

if (timeline != null) {
            timeline = addToExistingTimeline(timeline,msgKey);
        } else {
            timeline = createNewTimeline(msg, type, msgKey);
        }

StoreValue store = new StoreValue.Builder(timeline).build();
        client.execute(store);
    }

public Timeline createNewTimeline(Msg msg, Timeline.TimelineType type, String msgKey) {
        String owner = getOwner(msg, type);

Timeline newTimeline = new Timeline();
        newTimeline.Owner = owner;
        newTimeline.Type = type.toString();
        newTimeline.Msgs.add(msgKey);

return newTimeline;
    }

public Timeline addToExistingTimeline(Timeline timeline, String msgKey) {
        timeline.Msgs.add(msgKey);
        return timeline;
    }

public Timeline getTimeline(String ownerUsername, Timeline.TimelineType type, Date date) throws RiakRetryFailedException {
        String timelineKey = generateKey(ownerUsername, type, date);
        Bucket bucket = client.fetchBucket(BUCKET_NAME).execute();
        return bucket.fetch(timelineKey, Timeline.class).execute();
    }

private String generateKeyFromMsg(Msg msg, Timeline.TimelineType type) {
        String owner = getOwner(msg, type);
        String dateString = msg.Created.substring(0, 10);
        return generateKey(owner, type, dateString);
    }

private String getOwner(Msg msg, Timeline.TimelineType type) {
        if(type == Timeline.TimelineType.Inbox)
            return msg.Recipient;
        else
            return msg.Sender;
    }

private String generateKey(String ownerUsername, Timeline.TimelineType type, Date date) {
        String dateString = getIso8601DateStringFromDate(date);
        return generateKey(ownerUsername, type, dateString);
    }

private String generateKey(String ownerUsername, Timeline.TimelineType type, String dateString) {
        return ownerUsername + "_" + type.toString() + "_" + dateString;
    }

private String getIso8601DateStringFromDate(Date date) {
        TimeZone tz = TimeZone.getTimeZone("UTC");
        DateFormat df = new SimpleDateFormat("yyyy-MM-dd");
        df.setTimeZone(tz);
        return df.format(date);
    }

}

import com.basho.msgy.Models.User;
import com.basho.riak.client.IRiakClient;
import com.basho.riak.client.RiakRetryFailedException;
import com.basho.riak.client.bucket.Bucket;

public class UserRepository {
    static final String BUCKET_NAME = "Users";
    protected IRiakClient client;

public UserRepository(IRiakClient client) {
        this.client = client;
    }

public void save(User user) throws RiakRetryFailedException {
        Bucket bucket = client.fetchBucket(BUCKET_NAME).execute();
        bucket.store(user).execute();
    }

public User get(String UserName) throws RiakRetryFailedException {
        Bucket bucket = client.fetchBucket(BUCKET_NAME).execute();
        return bucket.fetch(UserName, User.class).execute();
    }
}

```

Finally, let's test them:

```java
package com.basho.msgy;

import com.basho.msgy.Models.Msg;
import com.basho.msgy.Models.Timeline;
import com.basho.msgy.Models.User;
import com.basho.msgy.Repositories.MsgRepository;
import com.basho.msgy.Repositories.TimelineRepository;
import com.basho.msgy.Repositories.UserRepository;
import com.basho.riak.client.IRiakClient;
import com.basho.riak.client.RiakException;
import com.basho.riak.client.RiakFactory;

import java.util.Date;

public class MsgyMain {

public static void main(String[] args) throws RiakException {
        // Setup our repositories
        IRiakClient client = RiakFactory.pbcClient("127.0.0.1", 10017);

UserRepository userRepo = new UserRepository(client);
        MsgRepository msgRepo = new MsgRepository(client);
        TimelineRepository timelineRepo = new TimelineRepository(client);

// Create and save users
        User marleen = new User("marleenmgr",
                "Marleen Manager",
                "marleen.manager@basho.com");

User joe = new User("joeuser",
                "Joe User",
                "joe.user@basho.com");

userRepo.save(marleen);
        userRepo.save(joe);

// Create new Msg, post to timelines
        Msg msg = Msg.createNew(marleen.UserName,
                joe.UserName,
                "Welcome to the company!");

timelineRepo.postMsg(msg);

// Get Joe's inbox for today, get first message
        Timeline joesInboxToday = timelineRepo.getTimeline(joe.UserName,
                                                           Timeline.TimelineType.Inbox,
                                                           new Date());

Msg joesFirstMsg = msgRepo.get(joesInboxToday.Msgs.get(0));

System.out.println("From: " + joesFirstMsg.Sender);
        System.out.println("Msg : " + joesFirstMsg.Text);
        System.out.println("");

client.shutdown();
    }
}
```

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

### Querying with Java

#### Java Version Setup

For the Java version, please download the source from GitHub by either
[cloning](https://github.com/basho/taste-of-riak) the source code
repository or downloading the [current zip of the master
branch](https://github.com/basho/taste-of-riak/archive/master.zip).
The code for this chapter is in `/java/Ch02-Schemas-and-Indexes`. You
may import this code into your favorite editor, or just run it from the
command line using the commands in `BuildAndRun.sh` if you are running
on a *nix* OS.

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
for these POJO's in `Customer.java`, `Order.java` and
`OrderSummaries.java`.  Let's put some data into Riak so we can play
with it.

```java
// From SipOfRiak.java

private static Customer createCustomer() {
    Customer customer = new Customer();
    customer.CustomerId = 1;
    customer.Name = "John Smith";
    customer.Address = "123 Main Street";
    customer.City = "Columbus";
    customer.State = "Ohio";
    customer.Zip = "43210";
    customer.Phone = "+1-614-555-5555";
    customer.CreatedDate = "2013-10-01 14:30:26";
    return customer;
}

private static ArrayList<Order> createOrders() {
    ArrayList<Order> orders = new ArrayList<Order>();

Order order1 = new Order();
    order1.OrderId = 1;
    order1.CustomerId = 1;
    order1.SalespersonId = 9000;
    order1.Items.add(
            new Item("TCV37GIT4NJ",
                    "USB 3.0 Coffee Warmer",
                    15.99));
    order1.Items.add(
            new Item("PEG10BBF2PP",
                    "eTablet Pro; 24GB; Grey",
                    399.99));
    order1.Total = 415.98;
    order1.OrderDate = "2013-10-01 14:42:26";
    orders.add(order1);

Order order2 = new Order();
    order2.OrderId = 2;
    order2.CustomerId = 1;
    order2.SalespersonId = 9001;
    order2.Items.add(
            new Item("OAX19XWN0QP",
                    "GoSlo Digital Camera",
                    359.99));
    order2.Total = 359.99;
    order2.OrderDate = "2013-10-15 16:43:16";
    orders.add(order2);

Order order3 = new Order();
    order3.OrderId = 3;
    order3.CustomerId = 1;
    order3.SalespersonId = 9000;
    order3.Items.add(
            new Item("WYK12EPU5EZ",
                    "Call of Battle = Goats - Gamesphere 4",
                    69.99));
    order3.Items.add(
            new Item("TJB84HAA8OA",
                    "Bricko Building Blocks",
                    4.99));
    order3.Total = 74.98;
    order3.OrderDate = "2013-11-03 17:45:28";
    orders.add(order3);
    return orders;
}

private static OrderSummary createOrderSummary(ArrayList<Order> orders) {
    OrderSummary orderSummary = new OrderSummary();
    orderSummary.CustomerId = 1;
    for(Order order: orders)
    {
        orderSummary.Summaries.add(new OrderSummaryItem(order));
    }
    return orderSummary;
}

public static void main(String[] args) throws RiakException {

System.out.println("Creating Data");
    Customer customer = createCustomer();
    ArrayList<Order> orders = createOrders();
    OrderSummary orderSummary = createOrderSummary(orders);

System.out.println("Starting Client");
    IRiakClient client = RiakFactory.pbcClient("127.0.0.1", 10017);

System.out.println("Creating Buckets");
    Bucket customersBucket = client.fetchBucket("Customers").lazyLoadBucketProperties().execute();
    Bucket ordersBucket = client.fetchBucket("Orders").lazyLoadBucketProperties().execute();
    Bucket orderSummariesBucket = client.fetchBucket("OrderSummaries").lazyLoadBucketProperties().execute();

System.out.println("Storing Data");
    customersBucket.store(String.valueOf(customer.CustomerId), customer).execute();
    for (Order order : orders) {
        ordersBucket.store(String.valueOf(order.OrderId), order).execute();
    }
    orderSummariesBucket.store(String.valueOf(orderSummary.CustomerId), orderSummary).execute();
```

While individual `Customer` and `Order` objects don't change much (or
shouldn't change), the `OrderSummaries` object will likely change often.
It will do double duty by acting as an index for all a customer's
orders, and also holding some relevant data such as the order total,
etc. If we showed this information in our application often, it's only
one extra request to get all the info.

```java
    System.out.println("Fetching related data by shared key");
    String key = "1";
    String fetchedCust = customersBucket.fetch(key).execute().getValueAsString();
    String fetchedOrdSum = orderSummariesBucket.fetch(key).execute().getValueAsString();
    System.out.format("Customer     1: %s\n", fetchedCust);
    System.out.format("OrderSummary 1: %s\n", fetchedOrdSum);
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
Secondary indexes in OpenRiak KV require a sorted backend: [Memory]({{< baseurl >}}kv/3.4.0/explanation/storage/memory/) or [LevelDB]({{< baseurl >}}kv/3.4.0/explanation/storage/leveldb/). [Bitcask]({{< baseurl >}}kv/3.4.0/explanation/storage/bitcask/) does not support secondary indexes.

See [Using Secondary Indexes (2i)]({{< baseurl >}}kv/3.4.0/how-to/develop/query-secondary-indexes/) for more information on developing with secondary indexes.

If you're coming from an SQL world, Secondary Indexes (2i) are a lot
like SQL indexes. They are a way to quickly look up objects based on a
secondary key, without scanning through the whole dataset. This makes it
very easy to find groups of related data by values, or even ranges of
values. To properly show this off, we will now add some more data to our
application, and add some secondary index entries at the same time.

```java
    System.out.println("Adding Index Data");
    IRiakObject riakObj = ordersBucket.fetch("1").execute();
    riakObj.addIndex("SalespersonId", 9000);
    riakObj.addIndex("OrderDate", "2013-10-01");
    ordersBucket.store(riakObj).execute();

IRiakObject riakObj2 = ordersBucket.fetch("2").execute();
    riakObj2.addIndex("SalespersonId", 9001);
    riakObj2.addIndex("OrderDate", "2013-10-15");
    ordersBucket.store(riakObj2).execute();

IRiakObject riakObj3 = ordersBucket.fetch("3").execute();
    riakObj3.addIndex("SalespersonId", 9000);
    riakObj3.addIndex("OrderDate", "2013-11-03");
    ordersBucket.store(riakObj3).execute();
```

As you may have noticed, ordinary key/value data is opaque to 2i, so we
have to add entries to the indexes at the application level. Now let's
find all of Jane Appleseed's processed orders, we'll look up the orders
by searching the `SalespersonId` integer index for Jane's id of `9000`.

```java
    // Query for orders where the SalespersonId index is set to 9000
    List<String> janesOrders = ordersBucket.fetchIndex(IntIndex.named("SalespersonId"))
                                           .withValue(9000).execute();

System.out.format("Jane's Orders: %s\n", StringUtil.Join(", ", janesOrders));
```

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

```java
    // Query for orders where the OrderDate index is between 2013-10-01 and 2013-10-31
    List<String> octoberOrders = ordersBucket.fetchIndex(BinIndex.named("OrderDate"))
                                             .from("2013-10-01").to("2013-10-31").execute();

System.out.format("October's Orders: %s\n", StringUtil.Join(", ", octoberOrders));
```

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
