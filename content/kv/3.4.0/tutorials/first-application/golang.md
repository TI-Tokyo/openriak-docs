---
title: 'Build a first OpenRiak application with Go'
description: 'Guide a developer through modeling, storing, retrieving, querying, and updating a small dataset with Go.'
weight: 4
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
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\developing\getting-started\golang.md'
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\developing\getting-started\golang\crud-operations.md'
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\developing\getting-started\golang\object-modeling.md'
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\developing\getting-started\golang\querying.md'
tags: ['diataxis', 'kv', 'tutorial']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Guide a developer through modeling, storing, retrieving, querying, and updating a small dataset with Go.

## Overview

### Getting Started with Go

If you haven't set up an OpenRiak node and started it, please visit [Running A Cluster]({{< baseurl >}}kv/3.4.0/how-to/operate/) first and ensure you have
[a working installation of Go](http://golang.org/doc/install).

#### Client Setup

First install the [Riak Go client](https://github.com/basho/riak-go-client):

```bash
go get github.com/basho/riak-go-client
```

Next download the [Taste of Riak - Go](https://github.com/basho/taste-of-riak/tree/master/go) utilities:

```bash
go get github.com/basho/taste-of-riak/go/util
```

If you are using a single local OpenRiak node, use the following to create a
new client instance:

```golang
package main

import (
  "encoding/binary"
  "encoding/json"
  "sync"

riak "github.com/basho/riak-go-client"
  util "github.com/basho/taste-of-riak/go/util"
)

func main() {
  var err error

// un-comment-out to enable debug logging
  // riak.EnableDebugLogging = true

o := &riak.NewClientOptions{
    RemoteAddresses: []string{util.GetRiakAddress()},
  }

var c *riak.Client
  c, err = riak.NewClient(o)
  if err != nil {
    util.ErrExit(err)
  }

defer func() {
    if err := c.Stop(); err != nil {
      util.ErrExit(err)
    }
  }()
}
```

We are now ready to start interacting with Riak.

#### Next Steps

[CRUD Operations]({{< baseurl >}}kv/3.4.0/tutorials/first-application/golang/)

### Crud Operations

#### Creating Objects

First let’s create a few objects and a bucket to keep them in:

```golang
  val1 := uint32(1)
  val1buf := make([]byte, 4)
  binary.LittleEndian.PutUint32(val1buf, val1)

val2 := "two"

val3 := struct{ MyValue int }{3} // NB: ensure that members are exported (i.e. capitalized)
  var val3json []byte
  val3json, err = json.Marshal(val3)
  if err != nil {
    util.ErrExit(err)
  }

bucket := "test"

util.Log.Println("Creating Objects In Riak...")

objs := []*riak.Object{
    {
      Bucket:      bucket,
      Key:         "one",
      ContentType: "application/octet-stream",
      Value:       val1buf,
    },
    {
      Bucket:      bucket,
      Key:         "two",
      ContentType: "text/plain",
      Value:       []byte(val2),
    },
    {
      Bucket:      bucket,
      Key:         "three",
      ContentType: "application/json",
      Value:       val3json,
    },
  }

var cmd riak.Command
  wg := &sync.WaitGroup{}

for _, o := range objs {
    cmd, err = riak.NewStoreValueCommandBuilder().
      WithContent(o).
      Build()
    if err != nil {
      util.ErrLog.Println(err)
      continue
    }
    a := &riak.Async{
      Command: cmd,
      Wait:    wg,
    }
    if err := c.ExecuteAsync(a); err != nil {
      util.ErrLog.Println(err)
    }
  }

wg.Wait()
```

In our first object, we have stored the integer 1 with the lookup key
of `one`:

```golang
{
  Bucket:      bucket,
  Key:         "one",
  ContentType: "application/octet-stream",
  Value:       val1buf,
}
```

For our second object, we stored a simple string value of `two` with a
matching key:

```golang
{
  Bucket:      bucket,
  Key:         "two",
  ContentType: "text/plain",
  Value:       []byte(val2),
}
```

Finally, the third object we stored was a bit of JSON:

```golang
{
  Bucket:      bucket,
  Key:         "three",
  ContentType: "application/json",
  Value:       val3json,
}
```

#### Reading Objects

Now that we have a few objects stored, let’s retrieve them and make sure
they contain the values we expect.

Requesting the objects by key:

```golang
var cmd riak.Command
wg := &sync.WaitGroup{}

wg.Wait()

util.Log.Println("Reading Objects From Riak...")

d := make(chan riak.Command, len(objs))

for _, o := range objs {
  cmd, err = riak.NewFetchValueCommandBuilder().
    WithBucket(bucket).
    WithKey(o.Key).
    Build()
  if err != nil {
    util.ErrLog.Println(err)
    continue
  }
  a := &riak.Async{
    Command: cmd,
    Wait:    wg,
    Done:    d,
  }
  if err := c.ExecuteAsync(a); err != nil {
    util.ErrLog.Println(err)
  }
}

wg.Wait()
close(d)
```

Converting to JSON to compare a string key to a symbol
key:

```golang
for done := range d {
  f := done.(*riak.FetchValueCommand)
  /* un-comment to dump fetched object as JSON
  if json, jerr := json.MarshalIndent(f.Response, "", "  "); err != nil {
    util.ErrLog.Println(jerr)
  } else {
    util.Log.Println("fetched value: ", string(json))
  }
  */
  obj := f.Response.Values[0]
  switch obj.Key {
  case "one":
    if actual, expected := binary.LittleEndian.Uint32(obj.Value), val1; actual != expected {
      util.ErrLog.Printf("key: %s, actual %v, expected %v", obj.Key, actual, expected)
    }
  case "two":
    if actual, expected := string(obj.Value), val2; actual != expected {
      util.ErrLog.Printf("key: %s, actual %v, expected %v", obj.Key, actual, expected)
    }
  case "three":
    obj3 = obj
    val3.MyValue = 0
    if jerr := json.Unmarshal(obj.Value, &val3); jerr != nil {
      util.ErrLog.Println(jerr)
    } else {
      if actual, expected := val3.MyValue, int(3); actual != expected {
        util.ErrLog.Printf("key: %s, actual %v, expected %v", obj.Key, actual, expected)
      }
    }
  default:
    util.ErrLog.Printf("unrecognized key: %s", obj.Key)
  }
}
```

#### Updating Objects

While some data may be static, other forms of data need to be
updated.

Let’s update some values:

```golang
util.Log.Println("Updating Object Three In Riak...")

val3.MyValue = 42
obj3.Value, err = json.Marshal(val3)
if err != nil {
  util.ErrExit(err)
}

cmd, err = riak.NewStoreValueCommandBuilder().
  WithContent(obj3).
  WithReturnBody(true).
  Build()
if err != nil {
  util.ErrLog.Println(err)
} else {
  if err := c.Execute(cmd); err != nil {
    util.ErrLog.Println(err)
  }
}

svcmd := cmd.(*riak.StoreValueCommand)
svrsp := svcmd.Response
obj3 = svrsp.Values[0]
val3.MyValue = 0
if jerr := json.Unmarshal(obj3.Value, &val3); jerr != nil {
  util.ErrLog.Println(jerr)
} else {
  if actual, expected := val3.MyValue, int(42); actual != expected {
    util.ErrLog.Printf("key: %s, actual %v, expected %v", obj3.Key, actual, expected)
  }
}
util.Log.Println("updated object key: ", obj3.Key)
util.Log.Println("updated object value: ", val3.MyValue)
```

#### Deleting Objects

As a last step, we’ll demonstrate how to delete data. You’ll see that
the delete message can be called against either the bucket or the
object.

```golang
for _, o := range objs {
  cmd, err = riak.NewDeleteValueCommandBuilder().
    WithBucket(o.Bucket).
    WithKey(o.Key).
    Build()
  if err != nil {
    util.ErrLog.Println(err)
    continue
  }
  a := &riak.Async{
    Command: cmd,
    Wait:    wg,
  }
  if err := c.ExecuteAsync(a); err != nil {
    util.ErrLog.Println(err)
  }
}

wg.Wait()
```

#### Working With Complex Objects

Since the world is a little more complicated than simple integers and
bits of strings, let’s see how we can work with more complex objects.

For example, this `struct` that represents some information about
a book:

```golang
type Book struct {
  ISBN        string
  Title       string
  Author      string
  Body        string
  CopiesOwned uint16
}

book := &Book{
    ISBN:        "1111979723",
    Title:       "Moby Dick",
    Author:      "Herman Melville",
    Body:        "Call me Ishmael. Some years ago...",
    CopiesOwned: 3,
}
```

We now have some information about our Moby Dick collection
that we want to save. Storing this to Riak should look familiar by now:

```golang
var jbook []byte
jbook, err = json.Marshal(book)
if err != nil {
  util.ErrExit(err)
}

bookObj := &riak.Object{
  Bucket:      "books",
  Key:         book.ISBN,
  ContentType: "application/json",
  Value:       jbook,
}

cmd, err = riak.NewStoreValueCommandBuilder().
  WithContent(bookObj).
  WithReturnBody(false).
  Build()
if err != nil {
  util.ErrLog.Println(err)
} else {
  if err := c.Execute(cmd); err != nil {
    util.ErrLog.Println(err)
  }
}
```

If we fetch our book back and print the data:

```golang
cmd, err = riak.NewFetchValueCommandBuilder().
  WithBucket("books").
  WithKey(book.ISBN).
  Build()
if err != nil {
  util.ErrExit(err)
}
if err := c.Execute(cmd); err != nil {
  util.ErrLog.Println(err)
}

fcmd := cmd.(*riak.FetchValueCommand)
bookObj = fcmd.Response.Values[0]
util.Log.Println(string(bookObj.Value))
```

The result is:

```json
{"isbn":"1111979723","title":"Moby Dick","author":"Herman Melville",
"body":"Call me Ishmael. Some years ago...","copies_owned":3}
```

Now, let’s delete the book:

```golang
...
```

### Object Modeling with Go

**Code Download**
You can download the code for this chapter at
[Github](https://github.com/basho/taste-of-riak/tree/master/go/ch03/models).

To get started, let's create the models that we'll be using:

```model.go
package models

type Model interface {
  GetId() string
  SetId(id string)
}

type modelImpl struct {
  id string
}

func (m *modelImpl) SetId(id string) {
  m.id = id
}
```

Our user model:

```user.go
package models

type User struct {
  modelImpl
  UserName string
  FullName string
  Email    string
}

func NewUser(userName, fullName, email string) *User {
  u := &User{
    UserName: userName,
    FullName: fullName,
    Email:    email,
  }
  u.SetId(userName)
  return u
}

func (u *User) GetId() string {
  return u.UserName
}
```

And our message model:

```msg.go
package models

import (
  "fmt"
  "time"

util "github.com/basho/taste-of-riak/go/util"
)

type Msg struct {
  modelImpl
  Sender    string
  Recipient string
  Text      string
  Created   time.Time
}

func NewMsg(sender, recipient, text string) *Msg {
  m := &Msg{
    Sender:    sender,
    Recipient: recipient,
    Text:      text,
    Created:   time.Now(),
  }
  m.SetId(m.GetId())
  return m
}

func (m *Msg) GetId() string {
  return fmt.Sprintf("%s_%v", m.Sender, util.Iso8601(m.Created))
}
```

Our timeline model:

```timeline.go
package models

type Timeline struct {
  modelImpl
  MsgKeys []string
}

type TimelineType byte

const (
  TimelineType_INBOX TimelineType = iota
  TimelineType_SENT
)

func NewTimeline(id string) *Timeline {
  t := &Timeline{}
  t.id = id
  return t
}

func (t *Timeline) AddMsg(msgKey string) {
  t.MsgKeys = append(t.MsgKeys, msgKey)
}

func (t *Timeline) GetId() string {
  return t.id
}
````

We'll be using the bucket `Users` to store our data. We won't be [using bucket types]({{< baseurl >}}kv/3.4.0/how-to/develop/use-bucket-types/) here, so we don't need to specify one.

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
`Timelines`. The key names, however, are a little trickier. In past
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
users and `<groupname>_Inbox_<date>` for groups, which will look like
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

```repository.go
package repositories

import (
  "encoding/json"
  "errors"

riak "github.com/basho/riak-go-client"
  models "github.com/basho/taste-of-riak/go/ch03/models"
)

var ErrUnexpectedSiblings = errors.New("Unexpected siblings in response!")

type Repository interface {
  Get(key string, notFoundOk bool) (models.Model, error)
  Save(models.Model) (models.Model, error)
  getBucketName() string
  getModel() models.Model
  getClient() *riak.Client
}

type repositoryImpl struct {
  client *riak.Client
}

func (ri *repositoryImpl) getClient() *riak.Client {
  return ri.client
}

func get(r Repository, key string, notFoundOk bool) (models.Model, error) {
  client := r.getClient()
  bucket := r.getBucketName()
  cmd, err := riak.NewFetchValueCommandBuilder().
    WithBucket(bucket).
    WithKey(key).
    WithNotFoundOk(notFoundOk).
    Build()
  if err != nil {
    return nil, err
  }
  if err = client.Execute(cmd); err != nil {
    return nil, err
  }

fcmd := cmd.(*riak.FetchValueCommand)

if notFoundOk && len(fcmd.Response.Values) == 0 {
    return nil, nil
  }

if len(fcmd.Response.Values) > 1 {
    // Siblings present that need resolution
    // Here we'll just return an unexpected error
    return nil, ErrUnexpectedSiblings
  } else {
    return buildModel(r.getModel(), fcmd.Response.Values[0])
  }
}

func save(r Repository, m models.Model) (models.Model, error) {
  client := r.getClient()
  bucket := r.getBucketName()
  key := m.GetId()

cmd, err := riak.NewFetchValueCommandBuilder().
    WithBucket(bucket).
    WithKey(key).
    WithNotFoundOk(true).
    Build()
  if err != nil {
    return nil, err
  }
  if err = client.Execute(cmd); err != nil {
    return nil, err
  }

modelJson, err := json.Marshal(m)
  if err != nil {
    return nil, err
  }

var objToInsertOrUpdate *riak.Object
  fcmd := cmd.(*riak.FetchValueCommand)
  if len(fcmd.Response.Values) > 1 {
    // Siblings present that need resolution
    // Here we'll just assume the first sibling is the "correct" one
    // with which to update with the new Model data
    // A conflict resolver can also be part of the options to fetchValue above
    objToInsertOrUpdate = fcmd.Response.Values[0]
    objToInsertOrUpdate.Value = modelJson
  } else {
    objToInsertOrUpdate = &riak.Object{
      Bucket:      bucket,
      Key:         key,
      ContentType: "application/json",
      Charset:     "utf8",
      Value:       modelJson,
    }
  }

cmd, err = riak.NewStoreValueCommandBuilder().
    WithContent(objToInsertOrUpdate).
    WithReturnBody(true).
    Build()
  if err != nil {
    return nil, err
  }
  if err = client.Execute(cmd); err != nil {
    return nil, err
  }

scmd := cmd.(*riak.StoreValueCommand)
  if len(scmd.Response.Values) > 1 {
    return nil, ErrUnexpectedSiblings
  }
  obj := scmd.Response.Values[0]
  return buildModel(r.getModel(), obj)
}

func buildModel(m models.Model, obj *riak.Object) (models.Model, error) {
  err := json.Unmarshal(obj.Value, m)
  m.SetId(obj.Key)
  return m, err
}
```

<br/>

```user-repository.go
package repositories

import (
  riak "github.com/basho/riak-go-client"
  models "github.com/basho/taste-of-riak/go/ch03/models"
)

type UserRepository struct {
  repositoryImpl
}

func NewUserRepository(c *riak.Client) *UserRepository {
  r := &UserRepository{}
  r.client = c
  return r
}

func (u *UserRepository) Get(key string, notFoundOk bool) (models.Model, error) {
  return get(u, key, notFoundOk)
}

func (u *UserRepository) Save(m models.Model) (models.Model, error) {
  return save(u, m)
}

func (u *UserRepository) getBucketName() string {
  return "Users"
}

func (u *UserRepository) getModel() models.Model {
  return &models.User{}
}
```

<br/>

```msg-repository.go
package repositories

type MsgRepository struct {
  repositoryImpl
}

func NewMsgRepository(c *riak.Client) *MsgRepository {
  m := &MsgRepository{}
  m.client = c
  return m
}

func (m *MsgRepository) Get(key string, notFoundOk bool) (models.Model, error) {
  return get(m, key, notFoundOk)
}

func (m *MsgRepository) Save(model models.Model) (models.Model, error) {
  return save(m, model)
}

func (m *MsgRepository) getBucketName() string {
  return "Msgs"
}

func (m *MsgRepository) getModel() models.Model {
  return &models.Msg{}
}
```

<br/>

```timeline-repository.go
package repositories

type TimelineRepository struct {
  repositoryImpl
}

func NewTimelineRepository(c *riak.Client) *TimelineRepository {
  t := &TimelineRepository{}
  t.client = c
  return t
}

func (t *TimelineRepository) Get(key string, notFoundOk bool) (models.Model, error) {
  return get(t, key, notFoundOk)
}

func (t *TimelineRepository) Save(m models.Model) (models.Model, error) {
  return save(t, m)
}

func (t *TimelineRepository) getBucketName() string {
  return "Timelines"
}

func (t *TimelineRepository) getModel() models.Model {
  return &models.Timeline{}
}
```

Finally, let's test them:

import (
  "time"

mgrs "github.com/basho/taste-of-riak/go/ch03/managers"
  models "github.com/basho/taste-of-riak/go/ch03/models"
  repos "github.com/basho/taste-of-riak/go/ch03/repositories"

util.Log.Println("Starting Client")

o := &riak.NewClientOptions{
    RemoteAddresses: util.GetRiakAddresses(),
  }

var client *riak.Client
  client, err = riak.NewClient(o)
  if err != nil {
    util.ErrExit(err)
  }

defer func() {
    if err := client.Stop(); err != nil {
      util.ErrExit(err)
    }
  }()

userRepo := repos.NewUserRepository(client)
  msgRepo := repos.NewMsgRepository(client)
  timelineRepo := repos.NewTimelineRepository(client)
  timelineMgr := mgrs.NewTimelineManager(timelineRepo, msgRepo)

util.Log.Println("Creating and saving users")

marleen := models.NewUser("marleenmgr", "Marleen Manager", "marleen.manager@basho.com")
  joe := models.NewUser("joeuser", "Joe User", "joe.user@basho.com")

var m models.Model
  m, err = userRepo.Save(marleen)
  if err != nil {
    util.ErrExit(err)
  }
  marleen = m.(*models.User)

m, err = userRepo.Save(joe)
  if err != nil {
    util.ErrExit(err)
  }
  joe = m.(*models.User)

util.Log.Println("Posting message")

msg := models.NewMsg(marleen.UserName, joe.UserName, "Welcome to the company!")
  if terr := timelineMgr.PostMsg(msg); terr != nil {
    util.ErrExit(terr)
  }

util.Log.Println("Getting Joe's inbox for today")

// Get Joe's inbox for today, get first message
  now := time.Now()
  joe_tl, terr := timelineMgr.GetTimeline(joe.UserName, models.TimelineType_INBOX, now)
  if terr != nil {
    util.ErrExit(terr)
  }

for _, msgKey := range joe_tl.MsgKeys {
    m, merr := msgRepo.Get(msgKey, false)
    if merr != nil {
      util.ErrExit(merr)
    }
    tl_msg := m.(*models.Msg)
    util.Log.Println("From: ", tl_msg.Sender)
    util.Log.Println("Msg: ", tl_msg.Text)
  }
}
```

As you can see, the repository pattern helps us with a few things:

* It helps us to see if an object exists before creating a new one.
* It keeps our buckets and key names consistent.
* It provides us with a consistent interface to work with.

While this set of repositories solves many of our problems, it is very
minimal and doesn't cover all the edge cases. For instance, what happens
if two different people try to create a user with the same username?

Also, we can easily compute key names now, but how do we quickly look
up the last 10 messages a user sent? Many of these answers will be
application-dependent. If your application shows the last 10 messages in
reverse order, for example, you may want to store that set of data in
another collection object to make lookup faster. There are drawbacks to
every solution, but we recommend seeking out the key/value-based
solution first, as it will likely be the quickest.

So to recap, in this chapter we learned:

* How to choose bucket names.
* How to choose natural keys based on how we want to partition our data.

### Querying with Go

#### Go Version Setup

For the Go version, please download the source from GitHub by either [cloning](https://github.com/basho/taste-of-riak) the source code repository or downloading the [current zip of the master branch](https://github.com/basho/taste-of-riak/archive/master.zip). Ensure that the source is located in your `GOPATH`. The code for this chapter is in `go/ch02/ch02.go`. You may import this code into your favorite editor, or just run it from the command line using the `Makefile` if you are running on a *nix* OS.

>A Quick Note on Querying and Schemas:
>
>Even with a key/value store, you will still have a logical database schema of how all the data relates to one another. This can be as simple as using the same key across multiple buckets for different types of data, to having fields in your data that are related by name. These querying methods will introduce you to some ways of laying out your data in Riak, along with how to query it back.

##### Denormalization

If you're coming from a relational database, the easiest way to get your application started with NoSQL is to denormalize your data into related chunks. For example with a customer database, you might have separate tables for Customers, Addresses, Preferences, etc. In OpenRiak KV, you can denormalize all that associated data into a single object and store it into a `Customer` bucket.  You can keep pulling in associated data until you hit one of the big denormalization walls:

* Size Limits (objects greater than 1MB)
* Shared/Referential Data (data that the object doesn't "own")
* Differences in Access Patterns (objects that get read/written once vs. often)

At one of these points we will have to split the model.

##### Same Keys - Different Buckets

The simplest way to split up data would be to use the same identity key across different buckets. A good example of this would be a `Customer` object, an `Order` object, and an `OrderSummaries` object that keeps rolled up info about orders such as Total, etc. Let's put some data into OpenRiak KV so we can play with it.

import (
  "encoding/json"
  "errors"
  "fmt"
  "reflect"
  "sync"
  "time"

const (
  timeFmt              = "2006-01-02 15:04:05"
  customersBucket      = "Customers"
  ordersBucket         = "Orders"
  orderSummariesBucket = "OrderSummaries"
)

type Customer struct {
  Name        string
  Address     string
  City        string
  State       string
  Zip         string
  Phone       string
  CreatedDate time.Time
}

type Order struct {
  Id            string
  CustomerId    string
  SalespersonId string
  Items         []*OrderItem
  Total         float32
  Date          time.Time
}

type OrderItem struct {
  Id    string
  Title string
  Price float32
}

type OrderSummary struct {
  CustomerId string
  Summaries  []*OrderSummaryItem
}

type OrderSummaryItem struct {
  Id    string
  Total float32
  Date  time.Time
}

func main() {
  var err error
  var customerId string

util.Log.Println("Creating Data")

var cd time.Time
  cd, err = time.Parse(timeFmt, "2013-10-01 14:30:26")
  if err != nil {
    util.ErrExit(err)
  }

customer := &Customer{
    Name:        "John Smith",
    Address:     "123 Main Street",
    City:        "Columbus",
    State:       "Ohio",
    Zip:         "43210",
    Phone:       "+1-614-555-5555",
    CreatedDate: cd,
  }

util.Log.Printf("customer: %v", customer)

defer func() {
    if err := c.Stop(); err != nil {
      util.ErrExit(err)
    }
  }()

util.Log.Println("Storing Customer")

var cmd riak.Command
  var customerJson []byte

customerJson, err = json.Marshal(customer)
  if err != nil {
    util.ErrExit(err)
  }

obj := &riak.Object{
    Bucket:      customersBucket,
    ContentType: "application/json",
    Value:       customerJson,
  }

cmd, err = riak.NewStoreValueCommandBuilder().
    WithContent(obj).
    WithReturnBody(true).
    Build()
  if err != nil {
    util.ErrExit(err)
  }
  if eerr := c.Execute(cmd); eerr != nil {
    util.ErrExit(eerr)
  }

svc := cmd.(*riak.StoreValueCommand)
  customerId = svc.Response.GeneratedKey
  if customerId == "" {
    util.ErrExit(errors.New("expected generated customer Id"))
  } else {
    util.Log.Println("Customer ID:", customerId)
  }

util.Log.Println("Storing Data")

var orders []*Order
  orders, err = createOrders(customerId)
  if err != nil {
    util.ErrExit(err)
  }

var orderSummary *OrderSummary
  var orderSummaryJson []byte
  orderSummary = createOrderSummary(customerId, orders)

ccmds := 1 + len(orders)
  cmds := make([]riak.Command, ccmds)

// command to store OrderSummary
  orderSummaryJson, err = json.Marshal(orderSummary)
  if err != nil {
    util.ErrExit(err)
  }
  obj = &riak.Object{
    Bucket:      orderSummariesBucket,
    Key:         customerId,
    ContentType: "application/json",
    Value:       orderSummaryJson,
  }
  cmds[0], err = riak.NewStoreValueCommandBuilder().
    WithContent(obj).
    Build()
  if err != nil {
    util.ErrExit(err)
  }

for i, order := range orders {
    // command to store Order
    var orderJson []byte
    orderJson, err = json.Marshal(order)
    if err != nil {
      util.ErrExit(err)
    }
    obj = &riak.Object{
      Bucket:      ordersBucket,
      Key:         order.Id,
      ContentType: "application/json",
      Value:       orderJson,
    }
    cmds[i+1], err = riak.NewStoreValueCommandBuilder().
      WithContent(obj).
      Build()
    if err != nil {
      util.ErrExit(err)
    }
  }

errored := false
  wg := &sync.WaitGroup{}
  for _, cmd := range cmds {
    a := &riak.Async{
      Command: cmd,
      Wait:    wg,
    }
    if eerr := c.ExecuteAsync(a); eerr != nil {
      errored = true
      util.ErrLog.Println(eerr)
    }
  }
  wg.Wait()
  if errored {
    util.ErrExit(errors.New("error, exiting!"))
  }
}

func createOrders(customerId string) ([]*Order, error) {
  o := make([]*Order, 3)

d, err := time.Parse(timeFmt, "2013-10-01 14:42:26")
  if err != nil {
    return nil, err
  }
  o[0] = &Order{
    Id:            "1",
    CustomerId:    customerId,
    SalespersonId: "9000",
    Items: []*OrderItem{
      {
        Id:    "TCV37GIT4NJ",
        Title: "USB 3.0 Coffee Warmer",
        Price: 15.99,
      },
      {
        Id:    "PEG10BBF2PP",
        Title: "eTablet Pro, 24GB; Grey",
        Price: 399.99,
      },
    },
    Total: 415.98,
    Date:  d,
  }

d, err = time.Parse(timeFmt, "2013-10-15 16:43:16")
  if err != nil {
    return nil, err
  }
  o[1] = &Order{
    Id:            "2",
    CustomerId:    customerId,
    SalespersonId: "9001",
    Items: []*OrderItem{
      {
        Id:    "OAX19XWN0QP",
        Title: "GoSlo Digital Camera",
        Price: 359.99,
      },
    },
    Total: 359.99,
    Date:  d,
  }

d, err = time.Parse(timeFmt, "2013-11-03 17:45:28")
  if err != nil {
    return nil, err
  }
  o[2] = &Order{
    Id:            "3",
    CustomerId:    customerId,
    SalespersonId: "9000",
    Items: []*OrderItem{
      {
        Id:    "WYK12EPU5EZ",
        Title: "Call of Battle : Goats - Gamesphere 4",
        Price: 69.99,
      },
      {
        Id:    "TJB84HAA8OA",
        Title: "Bricko Building Blocks",
        Price: 4.99,
      },
    },
    Total: 74.98,
    Date:  d,
  }

return o, nil
}

func createOrderSummary(customerId string, orders []*Order) *OrderSummary {

s := &OrderSummary{
    CustomerId: customerId,
    Summaries:  make([]*OrderSummaryItem, len(orders)),
  }

for i, o := range orders {
    s.Summaries[i] = &OrderSummaryItem{
      Id:    o.Id,
      Total: o.Total,
      Date:  o.Date,
    }
  }

return s
}
```

While individual `Customer` and `Order` objects don't change much (or shouldn't change), the `Order Summaries` object will likely change often. It will do double duty by acting as an index for all a customer's orders and also holding some relevant data, such as the order total, etc. If we showed this information in our application often, it's only one extra request to get all the info.

```golang
util.Log.Println("Fetching related data by shared key")

cmds = cmds[:0]

// fetch customer
cmd, err = riak.NewFetchValueCommandBuilder().
  WithBucket(customersBucket).
  WithKey(customerId).
  Build()
if err != nil {
  util.ErrExit(err)
}
cmds = append(cmds, cmd)

// fetch OrderSummary
cmd, err = riak.NewFetchValueCommandBuilder().
  WithBucket(orderSummariesBucket).
  WithKey(customerId).
  Build()
if err != nil {
  util.ErrExit(err)
}
cmds = append(cmds, cmd)

doneChan := make(chan riak.Command)
errored = false
for _, cmd := range cmds {
  a := &riak.Async{
    Command: cmd,
    Done:    doneChan,
  }
  if eerr := c.ExecuteAsync(a); eerr != nil {
    errored = true
    util.ErrLog.Println(eerr)
  }
}
if errored {
  util.ErrExit(errors.New("error, exiting!"))
}

for i := 0; i < len(cmds); i++ {
  select {
  case d := <-doneChan:
    if fv, ok := d.(*riak.FetchValueCommand); ok {
      obj := fv.Response.Values[0]
      switch obj.Bucket {
      case customersBucket:
        util.Log.Printf("Customer     1: %v", string(obj.Value))
      case orderSummariesBucket:
        util.Log.Printf("OrderSummary 1: %v", string(obj.Value))
      }
    } else {
      util.ErrExit(fmt.Errorf("unknown response command type: %v", reflect.TypeOf(d)))
    }
  case <-time.After(5 * time.Second):
    util.ErrExit(errors.New("fetch operations took too long"))
  }
}
```

Which returns our amalgamated objects:

```sh
2015/12/29 09:44:10 OrderSummary 1: {"CustomerId":"I4R9AdTpJ7RL13qj14ED9Qjzbyy","Summaries":[{"Id":"1","Total":415.98,"Date":"2013-10-01T14:42:26Z"},{"Id":"2","Total":359.99,"Date":"2013-10-15T16:43:16Z"},{"Id":"3","Total":74.98,"Date":"2013-11-03T17:45:28Z"}]}
2015/12/29 09:44:10 Customer     1: {"Name":"John Smith","Address":"123 Main Street","City":"Columbus","State":"Ohio","Zip":"43210","Phone":"+1-614-555-5555","CreatedDate":"2013-10-01T14:30:26Z"
```

While this pattern is very easy and extremely fast with respect to queries and complexity, it's up to the application to know about these intrinsic relationships.

##### Secondary Indexes

**Note:**
Secondary indexes in OpenRiak KV require a sorted backend: [Memory]({{< baseurl >}}kv/3.4.0/explanation/storage/memory/) or [LevelDB]({{< baseurl >}}kv/3.4.0/explanation/storage/leveldb/). [Bitcask]({{< baseurl >}}kv/3.4.0/explanation/storage/bitcask/) does not support secondary indexes.

See [Using Secondary Indexes (2i)]({{< baseurl >}}kv/3.4.0/how-to/develop/query-secondary-indexes/) for more information on developing with secondary indexes.

If you're coming from a SQL world, Secondary Indexes (2i) are a lot like SQL indexes. They are a way to quickly look up objects based on a secondary key, without scanning through the whole dataset. This makes it very easy to find groups of related data by values or ranges of values. To properly show this off, we will add some more data to our application, and add some secondary index entries at the same time:

```golang
util.Log.Println("Adding Index Data")

// fetch orders to add index data
cmds = cmds[:0]

for _, order := range orders {
  cmd, err = riak.NewFetchValueCommandBuilder().
    WithBucket(ordersBucket).
    WithKey(order.Id).
    Build()
  if err != nil {
    util.ErrExit(err)
  }
  cmds = append(cmds, cmd)
}

errored = false
for _, cmd := range cmds {
  a := &riak.Async{
    Command: cmd,
    Done:    doneChan,
  }
  if eerr := c.ExecuteAsync(a); eerr != nil {
    errored = true
    util.ErrLog.Println(eerr)
  }
}
if errored {
  util.ErrExit(errors.New("error, exiting!"))
}

errored = false
for i := 0; i < len(cmds); i++ {
  select {
  case d := <-doneChan:
    if fv, ok := d.(*riak.FetchValueCommand); ok {
      obj := fv.Response.Values[0]
      switch obj.Key {
      case "1":
        obj.AddToIntIndex("SalespersonId_int", 9000)
        obj.AddToIndex("OrderDate_bin", "2013-10-01")
      case "2":
        obj.AddToIntIndex("SalespersonId_int", 9001)
        obj.AddToIndex("OrderDate_bin", "2013-10-15")
      case "3":
        obj.AddToIntIndex("SalespersonId_int", 9000)
        obj.AddToIndex("OrderDate_bin", "2013-11-03")
      }
      scmd, serr := riak.NewStoreValueCommandBuilder().
        WithContent(obj).
        Build()
      if serr != nil {
        util.ErrExit(serr)
      }
      a := &riak.Async{
        Command: scmd,
        Wait:    wg,
      }
      if eerr := c.ExecuteAsync(a); eerr != nil {
        errored = true
        util.ErrLog.Println(eerr)
      }
    } else {
      util.ErrExit(fmt.Errorf("unknown response command type: %v", reflect.TypeOf(d)))
    }
  case <-time.After(5 * time.Second):
    util.ErrExit(errors.New("fetch operations took too long"))
  }
}

if errored {
  util.ErrExit(errors.New("error, exiting!"))
}

wg.Wait()
close(doneChan)
```

As you may have noticed, ordinary key/value data is opaque to 2i, so we have to add entries to the indexes at the application level.

Now let's find all of Jane Appleseed's processed orders. We'll lookup the orders by searching the `saleperson_id_int` index for Jane's id of `9000`:

```golang
util.Log.Println("Index Queries")

cmd, err = riak.NewSecondaryIndexQueryCommandBuilder().
  WithBucket(ordersBucket).
  WithIndexName("SalespersonId_int").
  WithIndexKey("9000").
  Build()
if err != nil {
  util.ErrExit(err)
}

if eerr := c.Execute(cmd); eerr != nil {
  util.ErrExit(eerr)
}

qcmd := cmd.(*riak.SecondaryIndexQueryCommand)
for _, rslt := range qcmd.Response.Results {
  util.Log.Println("Jane's Orders, key: ", string(rslt.ObjectKey))
}
```

Which returns:

```sh
2015/12/29 09:44:10 Jane's Orders, key:  3
2015/12/29 09:44:10 Jane's Orders, key:  1
```

Jane processed orders 1 and 3.  We used an *integer* index to reference Jane's id, next let's use a *binary* index.

Let's say that the VP of Sales wants to know how many orders came in during October 2013. In this case, we can exploit 2i's range queries. Let's search the `order_date_bin` index for entries between `20131001` and `20131031`:

```golang
cmd, err = riak.NewSecondaryIndexQueryCommandBuilder().
  WithBucket(ordersBucket).
  WithIndexName("OrderDate_bin").
  WithRange("2013-10-01", "2013-10-31").
  Build()
if err != nil {
  util.ErrExit(err)
}

qcmd = cmd.(*riak.SecondaryIndexQueryCommand)
for _, rslt := range qcmd.Response.Results {
  util.Log.Println("October's Orders, key: ", string(rslt.ObjectKey))
}
```

Which returns:

```sh
2015/12/29 09:44:10 October's Orders, key:  1
2015/12/29 09:44:10 October's Orders, key:  2
```

Easy!  We used 2i's range feature to search for a range of values, and demonstrated binary indexes.

So to recap:

* You can use Secondary Indexes to quickly lookup an object based on a secondary id other than the object's key.
* Indexes can have either Integer or Binary(String) keys.
* You can search for specific values or a range of values.
* Riak will return a list of keys that match the index query.

## What you will learn

By completing this tutorial, you will build the workflow described above and learn how to validate each stage before moving on.

## Before you begin

Use a disposable OpenRiak KV environment that matches this documentation version, and keep cluster status and logs available while you work.

## Verify the result

Repeat the completed workflow, inspect the stored or operational result, and confirm that the cluster remains healthy.
