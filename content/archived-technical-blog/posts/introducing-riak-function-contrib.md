---
title: "Introducing Riak Function Contrib"
date: "2010-12-02T06:00:08+00:00"
author: "Mark Phillips"
original_url: "http://basho.com/posts/technical/introducing-riak-function-contrib/"
archive_url: "https://web.archive.org/web/20170801115040http://basho.com/posts/technical/introducing-riak-function-contrib/"
categories:
  - "Developer Tools"
  - "Community & Events"
---
*December 2, 2010*

A short while ago I [made it known on the Riak Mailing list](http://lists.basho.com/pipermail/riak-users_lists.basho.com/2010-October/002082.html) that the Basho Dev team was working on getting “more resources out the door to help the community better use Riak.” Today we are pleased to announce that [Riak Function Contrib](http://contrib.basho.com), one of these resources, is now live and awaiting your usage and code contributions.

## What is Riak Function Contrib?

Riak Function Contrib is a home for MapReduce, Pre- and Post-Commit, and “Other” Functions or pieces of code that developers are using or might have a need for in their applications or testing. Put another way, it’s a Riak-specific function repository and library. Riak developers are using a lot of functions in a ton of different ways. So, we built Function Contrib to promote efficient development of Riak apps and to encourage a deeper level of community interaction through the use of this code.

## How do I use it?

There are two primary ways to make use of Riak Function Contrib:

1. Find a function – If, for instance, you needed a Pre-Commit Hook to validate a JSON document before you store it in Riak, [you could use or adapt this to your needs](http://contrib.basho.com/validate_json.html). No need to write it yourself!
2. Contribute a Function – There are a lot of use cases for Riak. This leads to many different functions and code bits that are written to extend Riak’s functionality. It you have one (or 20) functions that you think might be of use to someone other than you, contribute it. You’ll be helping developers everywhere. Francisco Treacy and [Widescript](http://widescript.com/), for example, did their part when [they contributed this JavaScript reduce function for Sorting by Fields](http://contrib.basho.com/sorting-by-field.html).

## What’s Next?

Riak Function Contrib is far from being a complete library. That’s where you come in. If you have a function, script, or some other piece of code that you think may be beneficial to someone using Riak (or Riak Search for that matter), we want it. Head over to the [Riak Function Contrib Repo on GitHub](https://github.com/basho/riak_function_contrib) and check out the README for details.

In the meantime, the Basho Dev team will continue polishing up the site and GitHub repo to make it easier to use and contribute to.

We are excited about this. We hope you are, too. As usual, thanks for being a part of Riak.

More to come…

[Mark](http://twitter.com/pharkmillups)

Community Manager
