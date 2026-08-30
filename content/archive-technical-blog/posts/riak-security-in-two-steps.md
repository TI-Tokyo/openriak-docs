---
title: "Riak Security in Two Steps"
date: "2017-01-25T15:48:30+00:00"
author: "Justin Pease"
original_url: "http://basho.com/posts/technical/riak-security-in-two-steps/"
archive_url: "https://web.archive.org/web/20170211194009http://basho.com/posts/technical/riak-security-in-two-steps/"
categories:
  - "Security"
---
In recent weeks, security compromises have been reported against [MongoDB](http://www.eweek.com/security/mongodb-ransomware-impacts-over-10000-databases.html), [ElasticSearch](http://www.zdnet.com/article/first-came-mass-mongodb-ransacking-now-copycat-ransoms-hit-elasticsearch/), [CouchDB](http://www.csoonline.com/article/3159534/security/attackers-start-wiping-data-from-couchdb-and-hadoop-databases.html) and [Hadoop](http://windowsitpro.com/database-administration/db-ransom-attacks-spread-couchdb-and-hadoop) installations. These attacks are costly to businesses and present real risks to user data. A similar scenario prompted us to publish a blog post detailing the [Fundamentals of NoSQL Security](./fundamentals-of-nosql-security.md) back in February 2015.

System attacks are an ever-present threat in today’s business world. We urge all Riak operators to take the time to implement these best practices to secure their Riak clusters. Here is a quick checklist of the two areas to review:

1. **Secure your network**
   - SSL
     - Generate SSL certificates
     - Enable SSL
     - Establish a certificate configuration
   - Firewall
     - Configure appropriate ports for Riak usage
2. **Setup Riak authentication and authorization**
   - Define users and, optionally, groups
   - Define an authentication source for each user
   - Grant the necessary permissions to each user (and/or group)

The above checklist is just that: a checklist. It is not intended to provide complete coverage on the important and expansive topic of security. For detailed information on the specifics of Riak security, we highly recommend you review our relevant documentation:

- Riak KV
  - [Security Basics](http://docs.basho.com/riak/kv/latest/using/security/basics/)
  - [Managing Security Sources](http://docs.basho.com/riak/kv/latest/using/security/managing-sources/)
  - [Security & Firewalls](http://docs.basho.com/riak/kv/latest/using/security/)
- Riak TS
  - [Security Checklist](http://docs.basho.com/riak/ts/latest/using/security/checklist/)
  - [Enable & Disable](http://docs.basho.com/riak/ts/latest/using/security/enable-disable/)
  - [User Management](http://docs.basho.com/riak/ts/latest/using/security/user-management/)
  - [Sources Management](http://docs.basho.com/riak/ts/latest/using/security/sources-management/)
  - [Notifying Basho](http://docs.basho.com/riak/ts/latest/using/security/notify-basho/)
  - [Security Overview](http://docs.basho.com/riak/ts/latest/using/security/)
- Riak CS
  - [Account Management](http://docs.basho.com/riak/cs/latest/cookbooks/account-management/)
  - [Access Control Lists](http://docs.basho.com/riak/cs/latest/cookbooks/access-control-lists/)
  - [Authentication](http://docs.basho.com/riak/cs/latest/cookbooks/authentication/)
  - [Accounts and Administration](http://docs.basho.com/riak/cs/latest/references/appendices/http-admin/)
- Riak Clients
  - [Java](http://docs.basho.com/riak/kv/latest/developing/usage/security/java/)
  - [Python](http://docs.basho.com/riak/kv/latest/developing/usage/security/python/)
  - [Ruby](http://docs.basho.com/riak/kv/latest/developing/usage/security/ruby/)
  - [Erlang](http://docs.basho.com/riak/kv/latest/developing/usage/security/erlang/)
  - [PHP](http://docs.basho.com/riak/kv/latest/developing/usage/security/php/)
  - [Client Security](http://docs.basho.com/riak/kv/latest/developing/usage/security/)

As always, we welcome you to reach out if you have any questions. Customers may do so by opening a support ticket via our [online help desk](https://help.basho.com). The community is invited to do so via our [mailing list](http://lists.basho.com/mailman/listinfo/riak-users_lists.basho.com).

Justin Pease  
VP, Services  
[@jpease](https://twitter.com/jpease)
