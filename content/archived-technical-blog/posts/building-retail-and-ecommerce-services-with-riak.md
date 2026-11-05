---
title: "Building Retail and eCommerce Services with Riak"
date: "2013-01-31T22:18:08+00:00"
author: "Basho"
original_url: "http://basho.com/posts/technical/building-retail-and-ecommerce-services-with-riak/"
archive_url: "https://web.archive.org/web/20170407131911http://basho.com/posts/technical/building-retail-and-ecommerce-services-with-riak/"
categories:
  - "Use Cases"
---
*January 31, 2013*

This is the second in a series of blog posts covering Riak for retail and eCommerce platforms. To learn more, join our “[Retail on Riak](http://info.basho.com/RiakonRetailWebcast.html)” webcast on Friday, February 8th or download the “[Riak for Retail](http://info.basho.com/RiakonRetail.html)” whitepaper.

In our [last post](http://basho.com/posts/business/riak-in-production-retail-and-ecommerce-stories/), we looked at three Riak users in the eCommerce/retail space. In this post, we will look at some common use cases for Riak and how to start building them with Riak’s key/value model and querying features.

## Use Cases

- **Shopping Carts:** Riak’s focus on availability makes it attractive to retailers offering shopping carts and other “buy now” functionality. If the shopping cart is unavailable, loses product additions, or responds slowly to users, it has a direct impact on revenue and user trust.
- **Product Catalogs:** Retailers need to store anywhere from thousands to tens of thousands of inventory items and associated information – such as photos, descriptions, prices, and category information. Riak’s flexible, fast storage makes it a good fit for this type of data.
- **User Information:** As mobile, web, and multi-channel shopping become more social and personalized, retailers have to manage increasing amounts of user information. Riak scales efficiently to meet increased data and traffic needs and ensures user data is always available for online shopping experiences.
- **Session Data:** Riak provides a highly reliable platform for session storage. User/session IDs are usually stored in cookies or otherwise known at lookup time, a good fit for Riak’s key/value mode.

## Data Modeling

In Riak, objects are comprised of key/value pairs, which are stored in flat namespaces called “buckets.” Riak is content-type agnostic, and stores all objects on disk as binaries, giving retailers lots of flexibility to store anything they want. Here are some common approaches to modeling the data and services discussed above in Riak:

![](../images/building-retail-and-ecommerce-services-with-riak/blog_retail_data_table.png)

## Querying

Riak provides several features for querying data:

**Riak Search:** Riak Search is a distributed, full-text search engine. It provides support for various MIME types & analyzers, and robust querying.  
*Possible Use Cases: Searching product information or product descriptions.*

**Secondary Indexing:** Secondary Indexing (2i) gives developers the ability, at write time, to tag an object stored in Riak with one or more values, queryable by exact matches or ranges of an index.  
*Possible Use Cases: Tagging products with categories, special promotion identifiers, date ranges, price or other metadata.*

**MapReduce:** Riak offers MapReduce for analytic and aggregation tasks with support for JavaScript and Erlang.  
*Possible Use Cases: Filtering product information by tag, counting items, and extracting links to related products.*

Check out our docs for more information on [building applications and services with Riak](http://docs.basho.com/riak/latest/tutorials/querying/Basic-Operations/).

For more details and examples of common Riak use cases, register for our “[Retail on Riak](http://info.basho.com/RiakonRetailWebcast.html)” webcast on February 8th or download the “[Riak for Retail](http://info.basho.com/RiakonRetail.html)” whitepaper.

[Basho](http://twitter.com/basho)
