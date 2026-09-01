---
title: 'Build a first OpenRiak application with Ruby'
description: 'Guide a developer through modeling, storing, retrieving, querying, and updating a small dataset with Ruby.'
weight: 9
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
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\developing\getting-started\ruby.md'
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\developing\getting-started\ruby\crud-operations.md'
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\developing\getting-started\ruby\object-modeling.md'
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\developing\getting-started\ruby\querying.md'
tags: ['diataxis', 'kv', 'tutorial']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Guide a developer through modeling, storing, retrieving, querying, and updating a small dataset with Ruby.

## Overview

### Getting Started with Ruby

If you haven't set up an OpenRiak node and started it, please visit [Running A Cluster]({{< product-version-root >}}how-to/operate/) first. To try this flavor
of Riak, a working installation of Ruby is required.

#### Client Setup

First, install the Riak Ruby client via RubyGems.

```bash
gem install riak-client
```

Start IRB, the Ruby REPL, and let’s get set up. Enter the following into
IRB:

```ruby
require 'riak'
```

If you are using a single local OpenRiak node, use the following to create a
new client instance, assuming that the node is running on `localhost`
port 8087:

```ruby
client = Riak::Client.new(:protocol => "pbc", :pb_port => 8087)

#### Since the Ruby Riak client uses the Protocol Buffers API by default,
#### you can also just enter this:
client = Riak::Client.new(:pb_port => 8087)
```

If you set up a local OpenRiak cluster using the [[five-minute install]]
method, use this code snippet instead:

```ruby
client = Riak::Client.new(:protocol => "pbc", :pb_port => 10017)

#### For the reasons explain in the snippet above, this will also work:
client = Riak::Client.new(:pb_port => 10017)
```

We are now ready to start interacting with Riak.

##### Next Steps

[CRUD Operations]({{< product-version-root >}}tutorials/first-application/ruby/)

### CRUD Operations with Ruby

#### Creating Objects In Riak

First, let’s create a few objects and a bucket to keep them in.

```ruby
my_bucket = client.bucket("test")

val1 = 1
obj1 = my_bucket.new('one')
obj1.data = val1
obj1.store()
```

In this first example we have stored the integer 1 with the lookup key
of `one`. Next, let’s store a simple string value of `two` with a
matching key.

```ruby
val2 = "two"
obj2 = my_bucket.new('two')
obj2.data = val2
obj2.store()
```

That was easy. Finally, let’s store a bit of JSON. You will probably
recognize the pattern by now.

```ruby
val3 = { myValue: 3 }
obj3 = my_bucket.new('three')
obj3.data = val3
obj3.store()
```

#### Reading Objects From Riak

Now that we have a few objects stored, let’s retrieve them and make sure
they contain the values we expect.

```ruby
fetched1 = my_bucket.get('one')
fetched2 = my_bucket.get('two')
fetched3 = my_bucket.get('three')

fetched1.data == val1
fetched2.data == val2
fetched3.data.to_json == val3.to_json
```

That was easy. we simply request the objects by key. in the last
example, we converted to JSON so we can compare a string key to a symbol
key.

#### Updating Objects In Riak

While some data may be static, other forms of data may need to be
updated. This is also easy to accomplish. Let’s update the value of
myValue in the 3rd example to 42.

```ruby
fetched3.data["myValue"] = 42
fetched3.store()
```

#### Deleting Objects From Riak

As a last step, we’ll demonstrate how to delete data. You’ll see that
the delete message can be called either against the bucket or the
object.

```ruby
my_bucket.delete('one')
obj2.delete()
obj3.delete()
```

#### Working With Complex Objects

Since the world is a little more complicated than simple integers and
bits of strings, let’s see how we can work with more complex objects.
Take, for example, this Ruby hash that encapsulates some knowledge about
a book.

```ruby
book = {
  :isbn => '1111979723',
  :title => 'Moby Dick',
  :author => 'Herman Melville',
  :body => 'Call me Ishmael. Some years ago...',
  :copies_owned => 3
}
```

All right, so we have some information about our Moby Dick collection
that we want to save. Storing this to Riak should look familiar by now.

```ruby
books_bucket = client.bucket('books')
new_book = books_bucket.new(book[:isbn])
new_book.data = book
new_book.store()
```

Some of you may be thinking, "But how does the Ruby Riak client
encode/decode my object?" If we fetch our book back and print the raw
data, we shall know:

```ruby
fetched_book = books_bucket.get(book[:isbn])
puts fetched_book.raw_data
```

Raw Data:

```json
{"isbn":"1111979723","title":"Moby Dick","author":"Herman Melville",
"body":"Call me Ishmael. Some years ago...","copies_owned":3}
```

JSON! The Ruby Riak client will serialize objects to JSON when it comes
across structured data like hashes.  For more advanced control over
serialization you can use a library called
[Ripple](https://github.com/basho/ripple), which is a rich Ruby modeling
layer over the basic riak client. Ripple falls outside the scope of
this document but we shall visit it later.

Now, let’s clean up our mess:

```ruby
new_book.delete()
```

### Object Modeling with Ruby

To get started, let's create the models that we'll be using. Since the
[Ruby Riak Client](https://github.com/basho/riak-ruby-client) uses
hashes when converting to and from JSON, we'll use the library
[Hashie](http://rdoc.info/github/intridea/hashie) to help automatically
coerce class properties to and from hashes. You can install this library
with `gem install hashie`.

```ruby
#### Encoding: utf-8

require 'riak'
require 'hashie'
require 'time'

class User < Hashie::Dash
  property :user_name
  property :full_name
  property :email
end

class Msg < Hashie::Dash
  property :from
  property :to
  property :created
  property :text
end

class Timeline < Hashie::Dash
  property :owner
  property :type
  property :msgs
end
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
which produces keys like `joeuser_2014-03-05T23:20:28`.

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

##### Keeping our story straight with repositories

Now that we've figured out our object models, let's write some
repositories to help create and work with these objects in Riak:

```ruby
class UserRepository
  BUCKET = 'Users'

def initialize(client)
    @client = client
  end

def save(user)
    users = @client.bucket(BUCKET)
    key = user.user_name

riak_obj = users.get_or_new(key)
    riak_obj.data = user
    riak_obj.content_type = 'application/json'
    riak_obj.store
  end

def get(user_name)
    riak_obj = @client.bucket(BUCKET)[user_name]
    User.new(riak_obj.data)
  end
end

class MsgRepository
  BUCKET = 'Msgs'

def save(msg)
    msgs = @client.bucket(BUCKET)
    key = generate_key(msg)

return msgs.get(key) if msgs.exists?(key)
    riak_obj = msgs.new(key)
    riak_obj.data = msg
    riak_obj.content_type = 'application/json'
    riak_obj.prevent_stale_writes = true
    riak_obj.store(returnbody: true)
  end

def get(key)
    riak_obj = @client.bucket(BUCKET).get(key)
    Msg.new(riak_obj.data)
  end

def generate_key(msg)
    msg.from + '_' + msg.created.utc.iso8601(6)
  end
end

class TimelineRepository
  BUCKET = 'Timelines'
  SENT = 'Sent'
  INBOX = 'Inbox'

def initialize(client)
    @client = client
    @msg_repo = MsgRepository.new(client)
  end

def post_message(msg)
    # Save the canonical copy
    saved_message = @msg_repo.save(msg)
    # Post to sender's Sent timeline
    add_to_timeline(msg, SENT, saved_message.key)
    # Post to recipient's Inbox timeline
    add_to_timeline(msg, INBOX, saved_message.key)
  end

def get_timeline(owner, type, date)
    riak_obj = @client.bucket(BUCKET).get(generate_key(owner, type, date))
    Timeline.new(riak_obj.data)
  end

private

def add_to_timeline(msg, type, msg_key)
    timeline_key = generate_key_from_msg(msg, type)
    riak_obj = nil

if @client.bucket(BUCKET).exists?(timeline_key)
      riak_obj = add_to_existing_timeline(timeline_key, msg_key)
    else
      riak_obj = create_new_timeline(timeline_key, msg, type, msg_key)
    end

riak_obj.store
  end

def create_new_timeline(key, msg, type, msg_key)
    owner = get_owner(msg, type)
    riak_obj = @client.bucket(BUCKET).new(key)
    riak_obj.data = Timeline.new(owner: owner,
                                 type: type,
                                 msgs: [msg_key])
    riak_obj.content_type = 'application/json'
    riak_obj
  end

def add_to_existing_timeline(key, msg_key)
    riak_obj = @client.bucket(BUCKET).get(key)
    timeline = Timeline.new(riak_obj.data)
    timeline.msgs << msg_key
    riak_obj.data = timeline
    riak_obj
  end

def get_owner(msg, type)
    type == INBOX ? msg.to : msg.from
  end

def generate_key_from_msg(msg, type)
    owner = get_owner(msg, type)
    generate_key(owner, type, msg.created)
  end

def generate_key(owner, type, date)
    owner + '_' + type + '_' + date.utc.strftime('%F')
  end
end
```

Finally, let's test them:

```ruby
#### Setup our repositories
client = Riak::Client.new(protocol: 'pbc', pb_port: 10017)
user_repo = UserRepository.new(client)
msgs_repo = MsgRepository.new(client)
timeline_repo = TimelineRepository.new(client)

#### Create and save users
marleen = User.new(user_name: 'marleenmgr',
                   full_name: 'Marleen Manager',
                   email: 'marleen.manager@basho.com')

joe = User.new(user_name: 'joeuser',
               full_name: 'Joe User',
               email: 'joe.user@basho.com')

user_repo.save(marleen)
user_repo.save(joe)

#### Create new Msg, post to timelines
msg = Msg.new(from: marleen.user_name,
              to: joe.user_name,
              created: Time.now,
              text: 'Welcome to the company!')

timeline_repo.post_message(msg)

#### Get Joe's inbox for today, get first message
joes_inbox_today = timeline_repo.get_timeline(joe.user_name, 'Inbox', Time.now)
joes_first_message = msgs_repo.get(joes_inbox_today.msgs.first)

puts "From: #{joes_first_message.from}\nMsg : #{joes_first_message.text}"
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

### Querying with Ruby

#### A Quick Note on Querying and Schemas

_Schemas_? Yes we said that correctly, S-C-H-E-M-A-S. It's not a dirty word.
Even with a Key/Value store, you will still have a logical database schema of how all the data relates to one another. This can be as simple as using the same key across multiple buckets for different types of data, to having fields in your data that are related by name.  These querying methods will introduce you to some ways of laying out your data in Riak, along with how to query it back.

##### Denormalization

If you're coming from a relational database, the easiest way to get your application's feet wet with NoSQL is to denormalize your data into related chunks.  For example with a customer database, you might have separate tables for Customers, Addresses, Preferences, etc.  In Riak, you can denormalize all that associated data into a single object and store it into a `Customer` bucket.  You can keep pulling in associated data until you hit one of the big denormalization walls:

* Size Limits (objects greater than 1MB)
* Shared/Referential Data (data that the object doesn't "own")
* Differences in Access Patterns (objects that get read/written once vs. often)

At one of these points we will have to split the model.

###### Same Keys - Different Buckets

The simplest way to split up data would be to use the same identity key across different buckets. A good example of this would be a `Customer` object, an `Order` object, and an `OrderSummaries` object that keeps rolled up info about orders such as Total, etc. Let's put some data into Riak so we can play with it.

require 'riak'
require 'pp'

#### Starting Client
client = Riak::Client.new protocol: 'pbc', pb_port: 10017

#### Creating Data
customer = {
    customer_id: 1,
    name: 'John Smith',
    address: '123 Main Street',
    city: 'Columbus',
    state: 'Ohio',
    zip: '43210',
    phone: '+1-614-555-5555',
    created_date: Time.parse('2013-10-1 14:30:26')
}

orders = [
  {
      order_id: 1,
      customer_id: 1,
      salesperson_id: 9000,
      items: [
          {
            item_id: 'TCV37GIT4NJ',
            title: 'USB 3.0 Coffee Warmer',
            price: 15.99
          },
          {
            item_id: 'PEG10BBF2PP',
            title: 'eTablet Pro, 24GB, Grey',
            price: 399.99
          }
      ],
      total: 415.98,
      order_date: Time.parse('2013-10-1 14:42:26')
  },
  {
      order_id: 2,
      customer_id: 1,
      salesperson_id: 9001,
      items: [
          {
            item_id: 'OAX19XWN0QP',
            title: 'GoSlo Digital Camera',
            price: 359.99
          }
      ],
      total: 359.99,
      order_date: Time.parse('2013-10-15 16:43:16')
  },
  {
      order_id: 3,
      customer_id: 1,
      salesperson_id: 9000,
      items: [
          {
            item_id: 'WYK12EPU5EZ',
            title: 'Call of Battle: Goats - Gamesphere 4',
            price: 69.99
          },
          {
            item_id: 'TJB84HAA8OA',
            title: 'Bricko Building Blocks',
            price: 4.99
          }
      ],
      total: 74.98,
      order_date: Time.parse('2013-11-3 17:45:28')
  }]

order_summary = {
    customer_id: 1,
    summaries: [
        {
            order_id: 1,
            total: 415.98,
            order_date: Time.parse('2013-10-1 14:42:26')
        },
        {
            order_id: 2,
            total: 359.99,
            order_date: Time.parse('2013-10-15 16:43:16')
        },
        {
            order_id: 3,
            total: 74.98,
            order_date: Time.parse('2013-11-3 17:45:28')
        }
    ]
}

#### Creating Buckets and Storing Data
customer_bucket = client.bucket('Customers')
cr = customer_bucket.new(customer[:customer_id].to_s)
cr.data = customer
cr.store

order_bucket = client.bucket('Orders')
orders.each do |order|
  order_riak = order_bucket.new(order[:order_id].to_s)
  order_riak.data = order
  order_riak.store
end

order_summary_bucket = client.bucket('OrderSummaries')
os = order_summary_bucket.new(order_summary[:customer_id].to_s)
os.data = order_summary
os.store
```

While individual `Customer` and `Order` objects don't change much (or shouldn't change), the `Order Summaries` object will likely change often.  It will do double duty by acting as an index for all a customer's orders, and also holding some relevant data such as the order total, etc.  If we showed this information in our application often, it's only one extra request to get all the info.

```ruby
shared_key = '1'
customer = customer_bucket.get(shared_key).data
customer[:order_summary] = order_summary_bucket.get(shared_key).data
puts "Combined Customer and Order Summary: "
pp customer
```

Which returns our amalgamated objects:

```ruby
#### Combined Customer and Order Summary:
{"customer_id"=>1,
 "name"=>"John Smith",
 "address"=>"123 Main Street",
 "city"=>"Columbus",
 "state"=>"Ohio",
 "zip"=>"43210",
 "phone"=>"+1-614-555-5555",
 "created_date"=>"2013-10-01 14:30:26 -0400",
 :order_summary=>
  {"customer_id"=>1,
   "summaries"=>
    [{"order_id"=>1,
      "total"=>415.98,
      "order_date"=>"2013-10-01 14:42:26 -0400"},
     {"order_id"=>2,
      "total"=>359.99,
      "order_date"=>"2013-10-15 16:43:16 -0400"},
     {"order_id"=>3,
      "total"=>74.98,
      "order_date"=>"2013-11-03 17:45:28 -0500"}]}}
```

While this pattern is very easy and extremely fast with respect to queries and complexity, it's up to the application to know about these intrinsic relationships.

###### Secondary Indexes

**Note:**
Secondary indexes in OpenRiak KV require a sorted backend: [Memory]({{< product-version-root >}}foundations/storage/memory/) or [LevelDB]({{< product-version-root >}}foundations/storage/leveldb/). [Bitcask]({{< product-version-root >}}foundations/storage/bitcask/) does not support secondary indexes.

See [Using Secondary Indexes (2i)]({{< product-version-root >}}how-to/develop/query-secondary-indexes/) for more information on developing with secondary indexes.

If you're coming from a SQL world, Secondary Indexes (2i) are a lot like SQL indexes.  They are a way to quickly lookup objects based on a secondary key, without scanning through the whole dataset.  This makes it very easy to find groups of related data by values, or even ranges of values.  To properly show this off, we will now add some more data to our application, and add some secondary index entries at the same time.

```ruby
(1..3).each do |i|
  order = order_bucket.get(i.to_s)
  # Initialize our secondary indices
  order.indexes['salesperson_id_int'] = []
  order.indexes['order_date_bin'] = []

order.indexes['salesperson_id_int'] <<  order.data['salesperson_id']
  order.indexes['order_date_bin'] << Time.parse(order.data['order_date'])
                                         .strftime('%Y%m%d')
  order.store
end
```

As you may have noticed, ordinary Key/Value data is opaque to 2i, so we have to add entries to the indexes at the application level.
Now let's find all of Jane Appleseed's processed orders, we'll lookup the orders by searching the `saleperson_id_int` index for Jane's id of `9000`.

```ruby
puts "#Jane's Orders: "
pp order_bucket.get_index('salesperson_id_int', 9000)
```

Which returns:

```ruby
#### Jane's Orders:
["1", "3"]
```

Jane processed orders 1 and 3.  We used an "integer" index to reference Jane's id, next let's use a "binary" index.
Now, let's say that the VP of Sales wants to know how many orders came in during October 2013.  In this case, we can exploit 2i's range queries.  Let's search the `order_date_bin` index for entries between `20131001` and `20131031`.

```ruby
puts "#October's Orders: "
pp order_bucket.get_index('order_date_bin', '20131001'..'20131031')
```

Which returns:

```ruby
#### October's Orders:
["1", "2"]
```

Boom, easy-peasy.  We used 2i's range feature to search for a range of values, and demonstrated binary indexes.

So to recap:

* You can use Secondary Indexes to quickly lookup an object based on a secondary id other than the object's key.
* Indexes can have either Integer or Binary(String) keys
* You can search for specific values, or a range of values
* Riak will return a list of keys that match the index query

## What you will learn

By completing this tutorial, you will build the workflow described above and learn how to validate each stage before moving on.

## Before you begin

Use a disposable OpenRiak KV environment that matches this documentation version, and keep cluster status and logs available while you work.

## Verify the result

Repeat the completed workflow, inspect the stored or operational result, and confirm that the cluster remains healthy.
