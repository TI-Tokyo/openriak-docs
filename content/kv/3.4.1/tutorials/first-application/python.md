---
title: 'Build a first OpenRiak application with Python'
description: 'Guide a developer through modeling, storing, retrieving, querying, and updating a small dataset with Python.'
weight: 8
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
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\developing\getting-started\python.md'
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\developing\getting-started\python\crud-operations.md'
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\developing\getting-started\python\object-modeling.md'
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\developing\getting-started\python\querying.md'
tags: ['diataxis', 'kv', 'tutorial']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Guide a developer through modeling, storing, retrieving, querying, and updating a small dataset with Python.

## Overview

### Getting Started with Python

If you haven't set up an OpenRiak node and started it, please visit [Running A Cluster](/kv/3.4.1/how-to/operate/) first.

To try this flavor of Riak, a working installation of Python is
required, with Python 2.7 preferred. One of the Python package managers,
e.g. `setuptools` or `pip`, is also required to install the client
package.

You may install `setuptools` on OS X through MacPorts by running `sudo
port install py-distribute`. `setuptools` and `pip` are included in the
Homebrew formula for Python on OS X as well. Just run `brew install
python`.

#### Prerequisites

First, you must install some packages needed by the Riak Python client:

* `python-dev` - Header files and a static library for Python
* `libffi-dev` - Foreign function interface library
* `libssl-dev` - libssl and libcrypto development libraries

##### Ubuntu (12.04 & 14.04)

```bash
sudo apt-get install python-dev libffi-dev libssl-dev
```

##### Client Setup

The easiest way to install the client is with `easy_install` or `pip`.
Either of the commands below will ensure that the client and all its
dependencies are installed and on the load path. Depending on where your
Python libraries are held, these may require `sudo`.

```bash
easy_install riak
pip install riak
```

To install from source, download the latest Python client from GitHub
([zip](https://github.com/basho/riak-python-client/archive/master.zip),
[GitHub repository](https://github.com/basho/riak-python-client)), and
extract it to your working directory.

Now, let's build the client.

```bash
python setup.py install
```

##### Connecting to Riak

Now, let's start the Python REPL and get set up. Enter the following
into the Python REPL:

```python
import riak
```
If you are using a single local OpenRiak node, use the following to create a
new client instance:

```python
myClient = riak.RiakClient(pb_port=8087, protocol='pbc')

#### Because the Python client uses the Protocol Buffers interface by
#### default, the following will work the same:
myClient = riak.RiakClient(pb_port=8087)
```

If you set up a local OpenRiak cluster using the [[five-minute install]]
method, use this code snippet instead:

```python
myClient = riak.RiakClient(pb_port=10017, protocol='pbc')
```

We are now ready to start interacting with Riak.

##### Next Steps

[CRUD Operations](/kv/3.4.1/tutorials/first-application/python/)

### CRUD Operations with Python

#### Creating Objects In Riak

First, let’s create a few objects and a bucket to keep them in.

```python
myBucket = myClient.bucket('test')

val1 = 1
key1 = myBucket.new('one', data=val1)
key1.store()
```

In this first example, we have stored the integer 1 with the lookup key
of `one`.  Next let’s store a simple string value of `two` with a
matching key.

```python
val2 = "two"
key2 = myBucket.new('two', data=val2)
key2.store()
```

That was easy. Finally, let’s store a bit of JSON. You will probably
recognize the pattern by now.

```python
val3 = {"myValue": 3}
key3 = myBucket.new('three', data=val3)
key3.store()
```

#### Reading Objects From Riak

Now that we have a few objects stored, let’s retrieve them and make sure
they contain the values we expect.

```python
fetched1 = myBucket.get('one')
fetched2 = myBucket.get('two')
fetched3 = myBucket.get('three')

assert val1 == fetched1.data
assert val2 == fetched2.data
assert val3 == fetched3.data
```

That was easy. We simply request the objects by key.

#### Updating Objects In Riak

While some data may be static, other forms of data may need to be
updated. This is also easy to accomplish. Let’s update the value of
myValue in the 3rd example to `42`.

```python
fetched3.data["myValue"] = 42
fetched3.store()
```

#### Deleting Objects From Riak

Nothing is complete without a delete. Fortunately, that's easy too.

```python
fetched1.delete()
fetched2.delete()
fetched3.delete()
```

Now we can verify that the objects have been removed from Riak.

```python
assert myBucket.get('one').exists == False
assert myBucket.get('two').exists == False
assert myBucket.get('three').exists == False
```

#### Working With Complex Objects

Since the world is a little more complicated than simple integers and
bits of strings, let’s see how we can work with more complex objects.
Take for example, this object that encapsulates some knowledge about a
book.

```python
book = {
  'isbn': "1111979723",
  'title': "Moby Dick",
  'author': "Herman Melville",
  'body': "Call me Ishmael. Some years ago...",
  'copies_owned': 3
}
```

All right, so we have some information about our Moby Dick collection
that we want to save. Storing this to Riak should look familiar by now:

```python
booksBucket = myClient.bucket('books')
newBook = booksBucket.new(book['isbn'], data=book)
newBook.store()
```

Some of you may be thinking, "But how does the Python Riak client
encode/decode my object?" If we fetch our book back and print the raw
encoded data, we shall know:

```python
fetchedBook = booksBucket.get(book['isbn'])

print(fetchedBook.encoded_data)
```

JSON! The Riak Python client library encodes things as JSON when it can.

```json
{"body": "Call me Ishmael. Some years ago...",
"author": "Herman Melville", "isbn": "1111979723",
"copies_owned": 3, "title": "Moby Dick"}
```

If we wanted to get a deserialized object back we would just use the
regular `fetchedBook.data` method.

Finally, let’s clean up our mess:

```python
fetchedBook.delete()
```

### Object Modeling with Python

To get started, let's create the data structures that we'll be using.

```python
from datetime import datetime
import string
import riak

marleen = {'user_name': 'marleenmgr',
           'full_name': 'Marleen Manager',
           'email': 'marleen.manager@basho.com'}

joe = {'user_name': 'joeuser',
       'full_name': 'Joe User',
       'email': 'joe.user@basho.com'}

msg = {'sender': marleen['user_name'],
       'recipient': joe['user_name'],
       'created': datetime.utcnow().isoformat(),
       'text': 'Welcome to the company!'}
```

As you can see, we first create a user, and then we can use that user to
create a message. To send this message we can append it to one or more
`Timeline`s. If it's a private message, we'll append it to the
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
`Timelines` | `<username>_<type>_<date>` | `joeuser_Sent_2014-03-06`<br /> `marketing_group_Inbox_2014-03-06` |

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
users, and `<groupname>_<type>_<date>` for groups, which will look like
`joeuser_Sent_2014-03-06` or `marketing_group_Inbox_2014-03-06`,
respectively.

**Note**
Riak performs best with objects under 1-2MB. Objects larger than that can hurt
performance, especially if many siblings are being created. We will cover
siblings, sibling resolution, and sibling explosions in the next chapter.

##### Keeping our story straight with repositories

Now that we've figured out our object model, let's write some
repositories to help create and work with these objects in Riak:

```python
class UserRepository:
    BUCKET = 'Users'

def __init__(self, client):
        self.client = client

def save(self, user):
        riak_obj = self.client.bucket(self.BUCKET).get(user['user_name'])
        riak_obj.data = user
        return riak_obj.store()

def get(self, user_name):
        riak_obj = self.client.bucket(self.BUCKET).get(user_name)
        return riak_obj.data

class MsgRepository:
    BUCKET = 'Msgs'

def save(self, msg):
        msgs = self.client.bucket(self.BUCKET)
        key = self._generate_key(msg)

riak_obj = msgs.get(key)

if not riak_obj.exists:
            riak_obj.data = msg
            riak_obj.store(if_none_match=True)

return riak_obj

def get(self, key):
        riak_obj = self.client.bucket(self.BUCKET).get(key)
        return riak_obj.data

def _generate_key(self, msg):
        return msg['sender'] + '_' + msg['created']

class TimelineRepository:
    BUCKET = 'Timelines'
    SENT = 'Sent'
    INBOX = 'Inbox'

def __init__(self, client):
        self.client = client
        self.msg_repo = MsgRepository(client)

def post_message(self, msg):
        # Save the canonical copy
        saved_message = self.msg_repo.save(msg)
        msg_key = saved_message.key

# Post to sender's Sent timeline
        self._add_to_timeline(msg, self.SENT, msg_key)

# Post to recipient's Inbox timeline
        self._add_to_timeline(msg, self.INBOX, msg_key)

def get_timeline(self, owner, msg_type, date):
        key = self._generate_key(owner, msg_type, date)
        riak_obj = self.client.bucket(self.BUCKET).get(key)
        return riak_obj.data

def _add_to_timeline(self, msg, msg_type, msg_key):
        timeline_key = self._generate_key_from_msg(msg, msg_type)
        riak_obj = self.client.bucket(self.BUCKET).get(timeline_key)

if riak_obj.exists:
            riak_obj = self._add_to_existing_timeline(riak_obj,
                                                      msg_key)
        else:
            riak_obj = self._create_new_timeline(riak_obj,
                                                 msg, msg_type,
                                                 msg_key)

return riak_obj.store()

def _create_new_timeline(self, riak_obj, msg, msg_type, msg_key):
        owner = self._get_owner(msg, msg_type)
        new_timeline = {'owner': owner,
                        'msg_type': msg_type,
                        'msgs': [msg_key]}

riak_obj.data = new_timeline
        return riak_obj

def _add_to_existing_timeline(self, riak_obj, msg_key):
        riak_obj.data['msgs'].append(msg_key)
        return riak_obj

def _get_owner(self, msg, msg_type):
        if msg_type == self.INBOX:
            return msg['recipient']
        else:
            return msg['sender']

def _generate_key_from_msg(self, msg, msg_type):
        owner = self._get_owner(msg, msg_type)
        return self._generate_key(owner, msg_type, msg['created'])

def _generate_key(self, owner, msg_type, datetimestr):
        dateString = string.split(datetimestr, 'T', 1)[0]
        return owner + '_' + msg_type + '_' + dateString

```

Finally, let's test them:

```python
#### Setup our repositories
client = riak.RiakClient(pb_port=10017, protocol='pbc')
userRepo = UserRepository(client)
msgsRepo = MsgRepository(client)
timelineRepo = TimelineRepository(client)

#### Save users
userRepo.save(marleen)
userRepo.save(joe)

#### Post msg to timelines
timelineRepo.post_message(msg)

#### Get Joe's inbox for today, get first message
joes_inbox_today = timelineRepo.get_timeline(
    joe['user_name'],
    TimelineRepository.INBOX,
    datetime.utcnow().isoformat())

joes_first_message = msgsRepo.get(joes_inbox_today['msgs'][0])

print 'From: {0}\nMsg : {1}\n\n'.format(
    joes_first_message['sender'],
    joes_first_message['text'])

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

### Querying with Python

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

```python
import riak

#### Creating Data

customer = {
    'customer_id': 1,
    'name': "John Smith",
    'address': "123 Main Street",
    'city': "Columbus",
    'state': "Ohio",
    'zip': "43210",
    'phone': "+1-614-555-5555",
    'created_date': "2013-10-01 14:30:26"
}

orders = [
    {
        'order_id': 1,
        'customer_id': 1,
        'salesperson_id': 9000,
        'items': [
            {
                'item_id': "TCV37GIT4NJ",
                'title': "USB 3.0 Coffee Warmer",
                'price': 15.99
            },
            {
                'item_id': "PEG10BBF2PP",
                'title': "eTablet Pro, 24GB, Grey",
                'price': 399.99
            }
        ],
        'total': 415.98,
        'order_date': "2013-10-01 14:42:26"
    },
    {
        'order_id': 2,
        'customer_id': 1,
        'salesperson_id': 9001,
        'items': [
            {
                'item_id': "OAX19XWN0QP",
                'title': "GoSlo Digital Camera",
                'price': 359.99
            }
        ],
        'total': 359.99,
        'order_date': "2013-10-15 16:43:16"
    },
    {
        'order_id': 3,
        'customer_id': 1,
        'salesperson_id': 9000,
        'items': [
            {
                'item_id': "WYK12EPU5EZ",
                'title': "Call of Battle: Goats - Gamesphere 4",
                'price': 69.99
            },
            {
                'item_id': "TJB84HAA8OA",
                'title': "Bricko Building Blocks",
                'price': 4.99
            }
        ],
        'total': 74.98,
        'order_date': "2013-11-03 17:45:28"
    }]

order_summary = {
    'customer_id': 1,
    'summaries': [
        {
            'order_id': 1,
            'total': 415.98,
            'order_date': "2013-10-01 14:42:26"
        },
        {
            'order_id': 2,
            'total': 359.99,
            'order_date': "2013-10-15 16:43:16"
        },
        {
            'order_id': 3,
            'total': 74.98,
            'order_date': "2013-11-03 17:45:28"
        }
    ]
}

#### Starting Client
client = riak.RiakClient(pb_port=10017, protocol='pbc')

#### Creating Buckets
customer_bucket = client.bucket('Customers')
order_bucket = client.bucket('Orders')
order_summary_bucket = client.bucket('OrderSummaries')

#### Storing Data
cr = customer_bucket.new(str(customer['customer_id']),
                         data=customer)
cr.store()

for order in orders:
    order_riak = order_bucket.new(str(order['order_id']),
                                  data=order)
    order_riak.store()

os = order_summary_bucket.new(str(order_summary['customer_id']),
                              data=order_summary)
os.store()
```

While individual `Customer` and `Order` objects don't change much (or shouldn't change), the `Order Summaries` object will likely change often.  It will do double duty by acting as an index for all customer orders, and also holding some relevant data such as the order total, etc.  If we showed this information in our application often, it's only one extra request to get all the info.

```python
customer = customer_bucket.get('1').data
customer['order_summary'] = order_summary_bucket.get('1').data
customer
```

Which returns our amalgamated objects:

```python
{
  u'city': u'Columbus', u'name': u'John Smith', u'zip': u'43210',
  u'created_date': u'2013-10-01 14:30:26',
  'order_summary': {
    u'customer_id': 1, u'summaries': [
      {u'order_id': 1, u'order_date': u'2013-10-01 14:42:26', u'total': 415.98},
      {u'order_id': 2, u'order_date': u'2013-10-15 16:43:16', u'total': 359.99},
      {u'order_id': 3, u'order_date': u'2013-11-03 17:45:28', u'total': 74.98}
    ]},
  u'phone': u'+1-614-555-5555', u'state': u'Ohio', u'address': u'123 Main Street',
  u'customer_id': 1
}
```

While this pattern is very easy and extremely fast with respect to queries and complexity, it's up to the application to know about these intrinsic relationships.

###### Secondary Indexes

**Note:**
Secondary indexes in OpenRiak KV require a sorted backend: [Memory](/kv/3.4.1/explanation/storage/memory/) or [LevelDB](/kv/3.4.1/explanation/storage/leveldb/). [Bitcask](/kv/3.4.1/explanation/storage/bitcask/) does not support secondary indexes.

See [Using Secondary Indexes (2i)](/kv/3.4.1/how-to/develop/query-secondary-indexes/) for more information on developing with secondary indexes.

If you're coming from a SQL world, Secondary Indexes (2i) are a lot like SQL indexes.  They are a way to quickly lookup objects based on a secondary key, without scanning through the whole dataset.  This makes it very easy to find groups of related data by values, or even ranges of values.  To properly show this off, we will now add some more data to our application, and add some secondary index entries at the same time.

```python
for i in range(1, 4):
    order = order_bucket.get(str(i))
    # Initialize our secondary indices
    order.add_index('salesperson_id_int', order.data['salesperson_id'])
    order.add_index('order_date_bin', order.data['order_date'])
    order.store()
```

As you may have noticed, ordinary Key/Value data is opaque to 2i, so we have to add entries to the indexes at the application level.
Now let's find all of Jane Appleseed's processed orders, we'll lookup the orders by searching the `saleperson_id_int` index for Jane's id of `9000`.

```python
janes_orders = order_bucket.get_index("salesperson_id_int", 9000)
janes_orders.results
```

Which returns:

```text
['1', '3']
```

Jane processed orders 1 and 3.  We used an "integer" index to reference Jane's id, next let's use a "binary" index.
Now, let's say that the VP of Sales wants to know how many orders came in during October 2013.  In this case, we can exploit 2i's range queries.  Let's search the `order_date_bin` index for entries between `2013-10-01` and `2013-10-31`.

```python
october_orders = order_bucket.get_index("order_date_bin",
                                        "2013-10-01", "2013-10-31")
october_orders.results
```

Which returns:

```text
['1', '2']
```

Boom, easy-peasy.  We used 2i's range feature to search for a range of values, and demonstrated binary indexes.

So to recap:

* You can use Secondary Indexes to quickly lookup an object based on a secondary id other than the object's key.
* Indexes can have either Integer or Binary(String) keys
* You can search for specific values, or a range of values
* Riak will return a list of keys that match the index query

## What you will learn

By completing this tutorial, you will build the workflow described above and learn how to validate each stage before moving on.

## Verify the result

Repeat the completed workflow, inspect the stored or operational result, and confirm that the cluster remains healthy.
