---
title: 'Build a first OpenRiak application with PHP'
description: 'Guide a developer through modeling, storing, retrieving, querying, and updating a small dataset with PHP.'
weight: 7
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
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\developing\getting-started\php.md'
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\developing\getting-started\php\crud-operations.md'
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\developing\getting-started\php\querying.md'
tags: ['diataxis', 'kv', 'tutorial']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Guide a developer through modeling, storing, retrieving, querying, and updating a small dataset with PHP.

## Overview

### Getting Started with PHP

If you haven't set up an OpenRiak node and started it, please visit [Running A Cluster]({{< baseurl >}}kv/3.4.0/how-to/operate/) first.

To try this flavor of Riak, a working installation of PHP is required, and [Composer](https://getcomposer.org/) is required to be installed to fetch the client library package.

#### Client Setup

Download and unzip, or clone the Taste of Riak Sample Code Repository from GitHub ([zip](https://github.com/basho/taste-of-riak/archive/master.zip), [github repository](https://github.com/basho/taste-of-riak)).

From the `taste-of-riak` directory, use composer to install the Riak PHP 2.0 Client`.

```bash
php path/to/your/composer.phar install

#### If you did a global install of composer, run this instead:
composer install
```

If you set up a local OpenRiak cluster using the [[five minute install]] method, change line 11 from `->onPort(8098)` to `->onPort(10018)`.

Next, run `php Ch01-CRUD/taste-of-riak.php` to run this chapter's example code. It should output:

```json
Reading Objects From Riak...
Updating Objects In Riak...
Deleting Objects From Riak...
Working With Complex Objects...
Serialized Object:
{"title":"Moby Dick","author":"Herman Melville","body":"Call me Ishmael. Some years ago...","isbn":"1111979723","copiesOwned":3}
```

Yay, success!

Since we didn't use PHP's REPL environment, let's walk through the code
to see what it actually did at each step.

##### Setting up the PHP Client and connections

```php
include_once 'vendor/autoload.php';

use Basho\Riak;
use Basho\Riak\Node;
use Basho\Riak\Command;

$node = (new Node\Builder)
        ->atHost('127.0.0.1')
        ->onPort(8098)
        ->build();

$riak = new Riak([$node]);
```

This code will load the library, declare the necessary `use` statements for our code, and then initialize and configure a [Node Builder](http://basho.github.io/riak-php-client/class-Basho.Riak.Node.Builder.html).
Once we call `build()` on the builder, it will return to us a [Node](http://basho.github.io/riak-php-client/class-Basho.Riak.Node.html) object, which we use when building our Riak commands.

We are now ready to start interacting with Riak.

##### Next Steps

[CRUD Operations]({{< baseurl >}}kv/3.4.0/tutorials/first-application/php/)

### CRUD Operations with PHP

#### Creating Objects In Riak

First, let’s create a few objects and a bucket to keep them in.

```php
$bucket = new Riak\Bucket('testBucket');

$val1 = 1;
$location1 = new Riak\Location('one', $bucket);

$storeCommand1 = (new Command\Builder\StoreObject($riak))
                    ->buildObject($val1)
                    ->atLocation($location1)
                    ->build();
$storeCommand1->execute();
```

In this first example we have stored the integer 1 with the lookup key of ‘one’.  Next let’s store a simple string value of “two” with a matching key.

```php
$val2 = 'two';
$location2 = new Riak\Location('two', $bucket);

$storeCommand2 = (new Command\Builder\StoreObject($riak))
                    ->buildObject($val2)
                    ->atLocation($location2)
                    ->build();
$storeCommand2->execute();
```

That was easy.  Finally, let’s store an associative array.  You will probably recognize the pattern by now.

```php
$val3 = ['myValue' => 3];
$location3 = new Riak\Location('three', $bucket);

$storeCommand3 = (new Command\Builder\StoreObject($riak))
                    ->buildJsonObject($val3)
                    ->atLocation($location3)
                    ->build();
$storeCommand3->execute();
```

#### Reading Objects From Riak

Now that we have a few objects stored, let’s retrieve them and make sure they contain the values we expect.

```php
$response1 = (new Command\Builder\FetchObject($riak))
                ->atLocation($location1)
                ->build()
                ->execute();

$response2 = (new Command\Builder\FetchObject($riak))
                ->atLocation($location2)
                ->build()
                ->execute();

$response3 = (new Command\Builder\FetchObject($riak))
                ->atLocation($location3)
                ->withDecodeAsAssociative()
                ->build()
                ->execute();

print_r($response1->getObject()->getData());
print_r($response2->getObject()->getData());
print_r($response3->getObject()->getData());
```

That was easy.  We create a [Fetch Command](http://basho.github.io/riak-php-client/class-Basho.Riak.Command.Object.Fetch.html) from a [FetchObject Builder](http://basho.github.io/riak-php-client/class-Basho.Riak.Command.Builder.FetchObject.html).
For our object that is an associative array, we also add [`withDecodeAsAssociative()`](http://basho.github.io/riak-php-client/class-Basho.Riak.Command.Builder.FetchObject.html#_withDecodeAsAssociative) to the builder so it returns the object as an associative array instead of an stdClass object.

In either case, we'll get a [Response](http://basho.github.io/riak-php-client/class-Basho.Riak.Command.Object.Response.html) object back, which holds information about the operation, and the result data.

#### Updating Objects In Riak

While some data may be static, other forms of data may need to be updated.  This is also easy to accomplish.  Let’s update the value of myValue in the 3rd example to 42.

```php
$object3 = $response3->getObject();
$data3 = $object3->getData();

$data3['myValue'] = 42;
$object3 = $object3->setData(json_encode($data3));

$updateCommand = (new Command\Builder\StoreObject($riak))
    ->withObject($object3)
    ->atLocation($location3)
    ->build();

$updateCommand->execute();
```

First we get the Riak [Object](http://basho.github.io/riak-php-client/class-Basho.Riak.Object.html) from the [Response](http://basho.github.io/riak-php-client/class-Basho.Riak.Command.Object.Response.html), then we get the stored data with [`getData()`](http://basho.github.io/riak-php-client/class-Basho.Riak.Object.html#_getData). We update the data to our liking, then use [`setData()`](http://basho.github.io/riak-php-client/class-Basho.Riak.Object.html#_setData) to set the new data back to the Riak Object.
To store it we use the same pattern as before, but this time we use the [`withObject()`](http://basho.github.io/riak-php-client/class-Basho.Riak.Command.Builder.ObjectTrait.html#_withObject) method to tell it to store our updated Riak Object.

#### Deleting Objects From Riak

As a last step, we’ll demonstrate how to delete data.  We just build a [Delete Command](http://basho.github.io/riak-php-client/class-Basho.Riak.Command.Object.Delete.html) from a [DeleteObject Builder](http://basho.github.io/riak-php-client/class-Basho.Riak.Command.Builder.DeleteObject.html), and execute it.

```php
(new Command\Builder\DeleteObject($riak))->atLocation($location1)->build()->execute();
(new Command\Builder\DeleteObject($riak))->atLocation($location2)->build()->execute();
(new Command\Builder\DeleteObject($riak))->atLocation($location3)->build()->execute();
```

##### Working With Complex Objects

Since the world is a little more complicated than simple integers and bits of strings, let’s see how we can work with more complex objects.  Take for example, this plain old PHP object(POPO) that encapsulates some knowledge about a book.

```php
class Book
{
    var $title;
    var $author;
    var $body;
    var $isbn;
    var $copiesOwned;
}

$book = new Book();
$book->isbn = '1111979723';
$book->title = 'Moby Dick';
$book->author = 'Herman Melville';
$book->body = 'Call me Ishmael. Some years ago...';
$book->copiesOwned = 3;
```

Ok, so we have some information about our Moby Dick collection that we want to save.  Storing this to Riak should look familiar by now:

```php
$bookLocation = new Riak\Location($book->isbn, new Riak\Bucket('books'));

$storeCommand1 = (new Command\Builder\StoreObject($riak))
    ->buildJsonObject($book)
    ->atLocation($bookLocation)
    ->build();

$storeCommand1->execute();
```

Some of you may be thinking “But how does the Riak client encode/decode my object”?  If we fetch the binary version of our book back and print it as a string, we shall know:

```php
$fetchBookResponse = (new Command\Builder\FetchObject($riak))
                        ->atLocation($bookLocation)
                        ->build()
                        ->execute();

print('Serialized Object:' . PHP_EOL);
print($fetchBookResponse->getBody() . PHP_EOL);
```

```json
Serialized Object:
{"title":"Moby Dick","author":"Herman Melville","body":"Call me Ishmael. Some years ago...","isbn":"1111979723","copiesOwned":3}
```

JSON!  The library encodes PHP objects as JSON strings when you use the [`buildJsonObject()`](http://basho.github.io/riak-php-client/class-Basho.Riak.Command.Builder.ObjectTrait.html#_buildJsonObject) method on the StoreObject builder.

Now that we’ve ruined the magic of object encoding, let’s clean up our mess:

```php
(new Command\Builder\DeleteObject($riak))
    ->atLocation($bookLocation)
    ->build()
    ->execute();
```

#### Next Steps

More complex use cases can be composed from these initial create, read, update, and delete (CRUD) operations. [In the next chapter]({{< baseurl >}}kv/3.4.0/tutorials/first-application/php/) we will look at how to store and query more complicated and interconnected data, such as documents.

### Querying with PHP

#### A Quick Note on Querying and Schemas

_Schemas_? Yes we said that correctly, S-C-H-E-M-A-S. It's not a dirty word.
Even with a Key/Value store, you will still have a logical database schema of how all the data relates to one another. This can be as simple as using the same key across multiple buckets for different types of data, to having fields in your data that are related by name.  These querying methods will introduce you to some ways of laying out your data in Riak, along with how to query it back.

#### Denormalization

If you're coming from a relational database, the easiest way to get your application's feet wet with NoSQL is to denormalize your data into related chunks.  For example with a customer database, you might have separate tables for Customers, Addresses, Preferences, etc.  In Riak, you can denormalize all that associated data into a single object and store it into a `Customer` bucket.  You can keep pulling in associated data until you hit one of the big denormalization walls:

* Size Limits (objects greater than 1MB)
* Shared/Referential Data (data that the object doesn't "own")
* Differences in Access Patterns (objects that get read/written once vs. often)

At one of these points we will have to split the model.

#### Same Keys - Different Buckets

The simplest way to split up data would be to use the same identity key across different buckets. A good example of this would be a `Customer` object, an `Order` object, and an `OrderSummaries` object that keeps rolled up info about orders such as Total, etc. Let's put some data into Riak so we can play with it.

```php
<?php

include_once 'vendor/autoload.php';

use Basho\Riak;
use Basho\Riak\Location;
use Basho\Riak\Node;
use Basho\Riak\Command;

$riak = new Riak([$node]);

// Class definitions for our models

class Customer
{
    var $customerId;
    var $name;
    var $address;
    var $city;
    var $state;
    var $zip;
    var $phone;
    var $createdDate;
}

class Order
{
    public function __construct()
    {
        $this->items = array();
    }
    var $orderId;
    var $customerId;
    var $salespersonId;
    var $items;
    var $total;
    var $orderDate;
}

class Item
{
    public function __construct($itemId, $title, $price)
    {
        $this->itemId = $itemId;
        $this->title = $title;
        $this->price = $price;
    }
    var $itemId;
    var $title;
    var $price;
}

class OrderSummary
{
    public function __construct()
    {
        $this->summaries = array();
    }
    var $customerId;
    var $summaries;
}

class OrderSummaryItem
{
    public function __construct(Order $order)
    {
        $this->orderId = $order->orderId;
        $this->total = $order->total;
        $this->orderDate = $order->orderDate;
    }
    var $orderId;
    var $total;
    var $orderDate;
}

// Creating Data
$customer = new Customer();
$customer->customerId = 1;
$customer->name = 'John Smith';
$customer->address = '123 Main Street';
$customer->city = 'Columbus';
$customer->state = 'Ohio';
$customer->zip = '43210';
$customer->phone = '+1-614-555-5555';
$customer->createdDate = '2013-10-01 14:30:26';

$orders = [];

$order1 = new Order();
$order1->orderId = 1;
$order1->customerId = 1;
$order1->salespersonId = 9000;
$order1->items = [
    new Item(
        'TCV37GIT4NJ',
        'USB 3.0 Coffee Warmer',
        15.99
    ),
    new Item(
        'PEG10BBF2PP',
        'eTablet Pro; 24GB; Grey',
        399.99
    )
];
$order1->total = 415.98;
$order1->orderDate = '2013-10-01 14:42:26';
$orders[] = $order1;

$order2 = new Order();
$order2->orderId = 2;
$order2->customerId = 1;
$order2->salespersonId = 9001;
$order2->items = [
    new Item(
        'OAX19XWN0QP',
        'GoSlo Digital Camera',
        359.99
    )
];
$order2->total = 359.99;
$order2->orderDate = '2013-10-15 16:43:16';
$orders[] = $order2;

$order3 = new Order();
$order3->orderId = 3;
$order3->customerId = 1;
$order3->salespersonId = 9000;
$order3->items = [
    new Item(
        'WYK12EPU5EZ',
        'Call of Battle = Goats - Gamesphere 4',
        69.99
    ),
    new Item(
        'TJB84HAA8OA',
        'Bricko Building Blocks',
        4.99
    )
];
$order3->total = 74.98;
$order3->orderDate = '2013-11-03 17:45:28';
$orders[] = $order3;

$orderSummary = new OrderSummary();
$orderSummary->customerId = 1;
foreach ($orders as $order) {
    $orderSummary->summaries[] = new OrderSummaryItem($order);
}
unset($order);

// Starting Client
$node = (new Node\Builder)
    ->atHost('127.0.0.1')
    ->onPort(8098)
    ->build();

// Creating Buckets
$customersBucket = new Riak\Bucket('Customers');
$ordersBucket = new Riak\Bucket('Orders');
$orderSummariesBucket = new Riak\Bucket('OrderSummaries');

// Storing Data
$storeCustomer = (new Command\Builder\StoreObject($riak))
    ->buildJsonObject($customer)
    ->atLocation(new Location($customer->customerId, $customersBucket))
    ->build();
$storeCustomer->execute();

foreach ($orders as $order) {
    $storeOrder = (new Command\Builder\StoreObject($riak))
        ->buildJsonObject($order)
        ->atLocation(new Location($order->orderId, $ordersBucket))
        ->build();
    $storeOrder->execute();
}
unset($order);

$storeSummary = (new Command\Builder\StoreObject($riak))
    ->buildJsonObject($orderSummary)
    ->atLocation(new Location($orderSummary->customerId, $orderSummariesBucket))
    ->build();
$storeSummary->execute();
```

While individual `Customer` and `Order` objects don't change much (or shouldn't change), the `Order Summaries` object will likely change often.  It will do double duty by acting as an index for all a customer's orders, and also holding some relevant data such as the order total, etc.  If we showed this information in our application often, it's only one extra request to get all the info.

```php
// Fetching related data by shared key
$fetched_customer = (new Command\Builder\FetchObject($riak))
                    ->atLocation(new Location('1', $customersBucket))
                    ->build()->execute()->getObject()->getData();

$fetched_customer->orderSummary =
    (new Command\Builder\FetchObject($riak))
    ->atLocation(new Location('1', $orderSummariesBucket))
    ->build()->execute()->getObject()->getData();

print("Customer with OrderSummary data: \n");
print_r($fetched_customer);
```

Which returns our amalgamated objects:

```text
Customer with OrderSummary data:
stdClass Object
(
    [customerId] => 1
    [name] => John Smith
    [address] => 123 Main Street
    [city] => Columbus
    [state] => Ohio
    [zip] => 43210
    [phone] => +1-614-555-5555
    [createdDate] => 2013-10-01 14:30:26
    [orderSummary] => stdClass Object
        (
            [customerId] => 1
            [summaries] => Array
                (
                    [0] => stdClass Object
                        (
                            [orderId] => 1
                            [total] => 415.98
                            [orderDate] => 2013-10-01 14:42:26
                        )

[1] => stdClass Object
                        (
                            [orderId] => 2
                            [total] => 359.99
                            [orderDate] => 2013-10-15 16:43:16
                        )

[2] => stdClass Object
                        (
                            [orderId] => 3
                            [total] => 74.98
                            [orderDate] => 2013-11-03 17:45:28
                        )
                )
        )
)
```

While this pattern is very easy and extremely fast with respect to queries and complexity, it's up to the application to know about these intrinsic relationships.

#### Secondary Indexes

**Note:**
Secondary indexes in OpenRiak KV require a sorted backend: [Memory]({{< baseurl >}}kv/3.4.0/explanation/storage/memory/) or [LevelDB]({{< baseurl >}}kv/3.4.0/explanation/storage/leveldb/). [Bitcask]({{< baseurl >}}kv/3.4.0/explanation/storage/bitcask/) does not support secondary indexes.

See [Using Secondary Indexes (2i)]({{< baseurl >}}kv/3.4.0/how-to/develop/query-secondary-indexes/) for more information on developing with secondary indexes.

If you're coming from a SQL world, Secondary Indexes (2i) are a lot like SQL indexes.  They are a way to quickly lookup objects based on a secondary key, without scanning through the whole dataset.  This makes it very easy to find groups of related data by values, or even ranges of values.  To properly show this off, we will now add some more data to our application, and add some secondary index entries at the same time.

```php
// Adding Index Data
$keys = array(1,2,3);
foreach ($keys as $key) {
    $orderLocation = new Location($key, $ordersBucket);
    $orderObject = (new Command\Builder\FetchObject($riak))
                    ->atLocation($orderLocation)
                    ->build()->execute()->getObject();

$order = $orderObject->getData();

$orderObject->addValueToIndex('SalespersonId_int', $order->salespersonId);
    $orderObject->addValueToIndex('OrderDate_bin', $order->orderDate);

$storeOrder = (new Command\Builder\StoreObject($riak))
                    ->withObject($orderObject)
                    ->atLocation($orderLocation)
                    ->build();
    $storeOrder->execute();
}
unset($key);

```

As you may have noticed, ordinary Key/Value data is opaque to 2i, so we have to add entries to the indexes at the application level.
Now let's find all of Jane Appleseed's processed orders, we'll lookup the orders by searching the `saleperson_id_int` index for Jane's id of `9000`.

```php
// Query for orders where the SalespersonId int index is set to 9000
$fetchIndex = (new Command\Builder\QueryIndex($riak))
                ->inBucket($ordersBucket)
                ->withIndexName('SalespersonId_int')
                ->withScalarValue(9000)->build();
$janes_orders = $fetchIndex->execute()->getResults();

print("\n\nJane's Orders: \n");
print_r($janes_orders);
```

Which returns:

```text
Jane's Orders:
Array
(
    [0] => 3
    [1] => 1
)

```

Jane processed orders 1 and 3.  We used an "integer" index to reference Jane's id, next let's use a "binary" index.
Now, let's say that the VP of Sales wants to know how many orders came in during October 2013.  In this case, we can exploit 2i's range queries.  Let's search the `order_date_bin` index for entries between `20131001` and `20131031`.

```php
// Query for orders where the OrderDate bin index is
// between 2013-10-01 and 2013-10-31
$fetchOctoberOrders = (new Command\Builder\QueryIndex($riak))
                        ->inBucket($ordersBucket)
                        ->withIndexName('OrderDate_bin')
                        ->withRangeValue('2013-10-01','2013-10-31')
                        ->withReturnTerms(true)
                        ->build();

$octobers_orders = $fetchOctoberOrders->execute()->getResults();

print("\n\nOctober's Orders: \n");
print_r($octobers_orders);
?>
```

Which returns:

```text
October's Orders:
Array
(
    [0] => Array
        (
            [2013-10-01 14:42:26] => 1
        )

[1] => Array
        (
            [2013-10-15 16:43:16] => 2
        )
)
```

Boom, easy-peasy.  We used 2i's range feature to search for a range of values, and demonstrated binary indexes.  With the October's Orders query we also used the `->withReturnTerms(true)` option, which as you can see will return the values of the matching 2i terms.

So to recap:

* You can use Secondary Indexes to quickly lookup an object based on a secondary id other than the object's key.
* Indexes can have either Integer or Binary(String) keys
* You can search for specific values, or a range of values
* Riak will return a list of keys (and terms if needed) that match the index query

## What you will learn

By completing this tutorial, you will build the workflow described above and learn how to validate each stage before moving on.

## Before you begin

Use a disposable OpenRiak KV environment that matches this documentation version, and keep cluster status and logs available while you work.

## Verify the result

Repeat the completed workflow, inspect the stored or operational result, and confirm that the cluster remains healthy.
