---
title: "The Quest for Hidden Treasure: An Apache Spark Connector for the Riak NoSQL database"
date: "2016-08-11T20:44:09+00:00"
author: "Pavel Hardak"
original_url: "http://basho.com/posts/technical/apache-spark-connector-for-the-riak-nosql-database/"
archive_url: "https://web.archive.org/web/20170402173121http://basho.com/posts/technical/apache-spark-connector-for-the-riak-nosql-database/"
categories:
  - "Integrations & Plugins"
---
Databricks recently published my blog [“The Quest for Hidden Treasure: An Apache Spark Connector for Riak NoSQL Database”](https://databricks.com/blog/2016/08/11/the-quest-for-hidden-treasure-an-apache-spark-connector-for-the-riak-nosql-database.html)[.](http://Databricks recently published my blog “The Quest for Hidden Treasure: An Apache Spark Connector for Riak NoSQL Database”. We have taken the liberty of reposting this blog below. This blog describes Riak Spark Connector – an open source library, which bridges the gap between Apache Spark and Riak. It brings the full power of Apache Spark to the operational data, managed in Riak distributed clusters. With the Riak Apache Spark Connector, Riak users now have an integrated, scalable solution for Big Data analytics and Spark users now have a resilient, highly available data store. I wanted to add a bit more information about the beginnings of NoSQL, more about and Riak and finally provide some information on Riak TS.) We have taken the liberty of reposting this blog below.  I’m adding more information about Riak and the development of Riak TS for some added context.

**Riak KV – a flexible database**

There are continual debates about which NoSQL database is better, or faster, or easier to operate, or has “that specific feature really needed for this use case”. In reality, it very much depends on many factors – data size and life cycle, read and write query ratios and patterns, environment (cloud vs on-premises vs hybrid), cost of hardware and software licenses, skill set of the operations team, resilience aligned to use case, ease of operational support and more.

Riak is a multi-model Big Data database and since it’s a key/value database, can be used as a document database, time series database and many other models. [Riak](http://basho.com/products/#riak), with many new capabilities, is being adopted for use cases that require scale, speed, high availability and operational simplicity like [IoT](http://basho.com/use-cases/iot-sensor-device-data/), [metrics](http://basho.com/use-cases/metrics-log-analytics/) and [edge-device analytics](http://basho.com/use-cases/iot-sensor-device-data/).

**Riak TS – focus on Time Series and SQL**

Riak TS reuses much of the same code as Riak KV and provides the same scalability, resilience and operational simplicity, but adds specific features to handle time-series data. Typical key/value use cases are session data, customer profiles, chat, and content-agnostic storage but Riak TS is designed specifically for [time-series use cases](http://basho.com/use-cases/), like IoT (Internet of Things), sensor data, financial transactions, etc. Riak TS and Riak KV share the same proven Riak Core, which implements principles from “Dynamo paper”, but Riak TS adds very fast bulk writes and very efficient “time slice” query operations.

In addition to being a distributed, masterless, highly available and linearly scalable NoSQL data store, Riak TS adds a number of SQL-like capabilities. It includes a DDL for tables (yeah, [CREATE TABLE](http://docs.basho.com/riak/ts/latest/using/creating-activating/) …) with named attributes and data types, primary keys (used both for local indexing and clustering), a subset of [SQL query language](http://docs.basho.com/riak/ts/1.3.0/using/querying/) with filters and [aggregations](http://docs.basho.com/riak/ts/latest/using/aggregate-functions/) and more (additional SQL commands are being added as we speak).

Adding SQL support for a NoSQL database is not a trivial endeavor by itself and we were happy to leverage SQL capabilities, mapping them to well-known Spark constructs, such as [DataFrames](http://docs.basho.com/riak/ts/latest/add-ons/spark-riak-connector/usage/dataframes/) and [Spark SQL](https://github.com/basho/spark-riak-connector/blob/master/docs/using-connector.md#reading-data-from-ts-table). Riak Spark Connector automatically [partitions SQL queries](https://github.com/basho/spark-riak-connector/blob/master/docs/using-connector.md#ts-table-range-query-partitioning) between Spark workers. Riak TS also supports key/value functionality, which does not have a schema, so we used Spark RDDs to [integrate with key/value (KV) buckets](https://github.com/basho/spark-riak-connector/blob/master/docs/using-connector.md#reading-data-from-kv-bucket). It is convenient and more efficient to store device metadata, configuration information and profiles in key/value buckets.

Riak Spark Connector features:

- Expose data in Riak TS tables as a Spark RDD or Spark DataFrames
- Leverage Riak TS SQL range queries using Spark SQL
- The ability to construct an RDD from a given set of keys
- Parallel full-table reads into multiple partitions
- Save Spark DataFrames in Riak TS
- Save an RDD in Riak TS
- Plus more….

Enjoy as we dig into our Apache Spark integration below.

---

## As published on [Databricks.com](https://databricks.com/blog/2016/08/11/the-quest-for-hidden-treasure-an-apache-spark-connector-for-the-riak-nosql-database.html)

This article introduces [Riak Spark Connector](http://basho.com/products/riak-ts/apache-spark-connector/), an open source library which bridges the gap between Apache Spark and Riak NoSQL database. It brings the full power of Apache Spark to the operational data, managed in Riak distributed clusters. With the Riak Apache Spark Connector, Riak users now have an integrated, scalable solution for Big Data analytics and Spark users now have a resilient, highly available data store.

## About Riak

Riak is open source, distributed NoSQL database, which is developed and supported by [Basho Technologies](http://basho.com/). Basho offers two major products: Riak KV (Key Value) and Riak TS (Time Series). Both products share the same core code base, but are tuned for different use cases. [Riak KV](http://docs.basho.com/riak/kv/latest/) is a highly resilient, scalable, key-value store. Riak KV is known for its ability to scale up and down in a linear fashion, handle huge amounts of reads, updates and writes with low latency while being extremely reliable and fault tolerant. More recently, [Riak TS](http://basho.com/products/riak-ts/) was introduced, specifically optimized for time series data. It adds very fast bulk writes, very efficient “time slice” read queries and supports a subset of the SQL language over Riak TS tables.

## Introducing the Riak Connector for Apache Spark

We have found that many leading organizations use a mix of NoSQL and SQL database products in their infrastructure as each one has specific advantages depending on the use case. In the past, some databases were used more for analytical workloads while others were used for operational ones. As modern NoSQL databases, like [Riak](http://basho.com/products/#riak), are gaining new capabilities, they are being adopted for additional use cases, like [IoT](http://basho.com/use-cases/iot-sensor-device-data/), [metrics](http://basho.com/use-cases/metrics-log-analytics/), and [edge-device analytics](http://basho.com/use-cases/iot-sensor-device-data/). To make it easier to perform such tasks, Basho has created a [Riak Spark Connector](http://basho.com/products/riak-ts/apache-spark-connector/), as we believe that Apache Spark is currently the best technology choice to use alongside Riak. Basho selected Spark for this development effort not only due to customer and market demand but also due to the fact that Spark and Riak share major design principles: high performance, scalability, resiliency and operational simplicity.

## Implementing the Apache Spark Connector for Riak

Modeled using principles from the [“AWS Dynamo” paper](http://docs.basho.com/riak/kv/latest/learn/dynamo/), Riak KV buckets are good for scenarios which require frequent, small data-sized operations in near real-time, especially workloads with reads, writes, and updates — something which might cause data corruption in some distributed databases or bring them to “crawl” under bigger workloads. In Riak, each data item is [replicated](http://docs.basho.com/riak/kv/latest/learn/concepts/replication/) on several nodes, which allows the database to process a huge number of operations with very low latency while having unique [anti-corruption](http://docs.basho.com/riak/kv/2.1.4/learn/concepts/active-anti-entropy/) and [conflict-resolution mechanisms](http://docs.basho.com/riak/kv/latest/developing/usage/conflict-resolution/). However, integration with Apache Spark requires a very different mode of operation — extracting large amounts of data in bulk, so that Spark can do its “magic” in memory over the whole data set. One approach to solve this challenge is to create a myriad of Spark workers, each asking for several data items. This approach works well with Riak, but it creates unacceptable overhead on the Spark side.

![Riak-Spark-Connector-Diagram-1-of-3.png](../images/apache-spark-connector-for-the-riak-nosql-database/Riak-Spark-Connector-Diagram-1-of-31.png)

Another option is using Riak’s built-in [secondary index query](http://docs.basho.com/riak/kv/latest/developing/usage/secondary-indexes/) (2i). In this approach, the user’s application contacts any Riak node with a query, then this Riak node, becoming a “coordinating node”, queries all other relevant Riak nodes, collects required keys and streams it back to the user application. Then the user app will loop over the keys to retrieve the values. Alas, it was found that queries with a bigger result set could possibly overload the coordinating node. Again, not a good result, so we had to teach Riak new tricks.

![Riak-Spark-Connector-Diagram-2-of-3[1]](../images/apache-spark-connector-for-the-riak-nosql-database/Riak-Spark-Connector-Diagram-2-of-31.png)

The solution was found in enhancing the 2i query with a smart Coverage Plan and Parallel Extract APIs. In the new approach, the user application contacts the coordinating node, but this time instead of doing all the work, this node returns the locations of the data using cluster replication and availability information. Then “N” Spark workers open “N” parallel connections to different nodes, which allow the application to retrieve the desired dataset “N” times faster, without generating “hot spots”. To make it even faster, we implemented a special type of bulk query, called a “full bucket read”, which extracts the whole logical bucket without the need for a query condition. Also, it returns both keys and values, saving another round-trip to the server.

![Riak-Spark-Connector-Diagram-3-of-3.png](../images/apache-spark-connector-for-the-riak-nosql-database/Riak-Spark-Connector-Diagram-3-of-31.png)

The strength of a [Riak KV bucket](http://docs.basho.com/riak/kv/2.1.4/learn/concepts/buckets/) is its ability to store unstructured data in a schema-less architecture with the “values” being opaque. But for many Spark use cases, data must be mapped into a record with Scala or Java types. Fortunately, many Riak applications use JSON, which allows Spark developers to easily [convert it into a Spark DataFrame](https://github.com/basho/spark-riak-connector/blob/master/docs/using-connector.md#spark-dataframes-with-kv-bucket) by providing a user-defined schema. The conversion happens “on the fly” and makes it easier for a Spark programmer to work with the retrieved data.

`import sqlContext.implicits._  
val sqlContext = new org.apache.spark.sql.SQLContext(sc)  
case class UserData(user_id: String, name: String, age: Int, category: String)  
val kv_bucket_name = new Namespace("test-data")  
val riakRdd = sc.riakBucket[UserData](kv_bucket_name).queryAll()  
val df = riakRdd.toDF()  
df.where(df("age") >= 50).select("id", "name")  
df.groupBy("category").count`

## Riak TS meets Spark SQL

Being a distributed, masterless, highly available and linearly scalable NoSQL data store, Riak TS adds a number of SQL-like capabilities. It includes a DDL for tables (yeah, [CREATE TABLE](http://docs.basho.com/riak/ts/latest/using/creating-activating/) …) with named attributes and data types, primary keys (used both for local indexing and clustering), a subset of [SQL query language](http://docs.basho.com/riak/ts/1.3.0/using/querying/) with filters and [aggregations](http://docs.basho.com/riak/ts/latest/using/aggregate-functions/) and more (additional SQL commands are being added as we speak).

Adding SQL support for a NoSQL database is not a trivial endeavor by itself and we were happy to leverage SQL capabilities, mapping them to well-known Spark constructs, such as [DataFrames](http://docs.basho.com/riak/ts/latest/add-ons/spark-riak-connector/usage/dataframes/) and [Spark SQL](https://github.com/basho/spark-riak-connector/blob/master/docs/using-connector.md#reading-data-from-ts-table). Riak Spark Connector [automatically partitions SQL queries](https://github.com/basho/spark-riak-connector/blob/master/docs/using-connector.md#ts-table-range-query-partitioning) between Spark workers. Riak TS also supports key/value functionality, which does not have a schema, so [we used Spark RDDs to integrate with key/value (KV) buckets](https://github.com/basho/spark-riak-connector/blob/master/docs/using-connector.md#reading-data-from-kv-bucket). It is convenient and more efficient to store device metadata, configuration information, and profiles in key/value buckets.

`val ts_table_name = "input-table"  
val df = sc.riakTSTable(ts_table_name)  
.sql(s"SELECT * FROM $ts_table_name WHERE time >= $from AND time <= $to")  
// ...  
val output_ts_table = "result-table"  
df.saveToRiakTS(output_ts_table);`

[Riak Spark Connector](https://github.com/basho/spark-riak-connector) is implemented in Scala, supporting both [Java](https://github.com/basho/spark-riak-connector/blob/master/docs/getting-connector.md#java) and [Scala](https://github.com/basho/spark-riak-connector/blob/master/docs/getting-connector.md#scala), but its [DataFrames](http://docs.basho.com/riak/ts/latest/add-ons/spark-riak-connector/usage/dataframes/) functionality gave us an easy way to also support [Python](https://github.com/basho/spark-riak-connector/blob/master/docs/getting-connector.md#python) to query and write into Riak TS tables. Python support for KV buckets will arrive soon, but for now developers can use either Java or Scala with KV buckets.

`df = sqlContext.read \  
.option("spark.riak.connection.hosts","riak_host_ip:10017") \  
.format("org.apache.spark.sql.riak") \  
.load(ts_table_name) \  
.select("time", "col1", "col2") \  
.filter(s"time >= CAST($from AS TIMESTAMP) AND time <= CAST($to AS TIMESTAMP) AND col1= $value1")`

[Spark Streaming](http://docs.basho.com/riak/ts/latest/add-ons/spark-riak-connector/usage/streaming-example/) is also supported for writing into Riak TS. In a typical pipeline, a Spark Streaming job would read (a.k.a. “consume”) the data from a Kafka topic and [efficiently write (stream) it into Riak TS](http://docs.basho.com/riak/ts/latest/add-ons/spark-riak-connector/usage/writing-data/) at high speed, automatically spreading the load across multiple nodes. Then [users can query Riak TS](http://docs.basho.com/riak/ts/latest/using/querying/) using familiar SQL commands or use the Spark Connector to [extract the data](https://github.com/basho/spark-riak-connector/blob/master/docs/using-connector.md#reading-data-from-ts-table) for processing in the Spark Cluster, optionally [writing the results back](https://github.com/basho/spark-riak-connector/blob/master/docs/using-connector.md#ts-bulk-write) into Riak TS.

`df.write \  
.option("spark.riak.connection.hosts","riak_host_ip:10017") \  
.format("org.apache.spark.sql.riak") \  
.mode(SaveMode.Append) \  
.save(ts_table_name)`

## Conclusion

As mentioned earlier in this post, there is no “best” NoSQL database for every possible use case. Riak KV and Riak TS provide an excellent solution for a number of popular use cases, as evidenced by the fact that Riak is the underlying database supporting many of the world’s most highly trafficked applications. The Riak Spark Connector gives users the ability to efficiently analyze the data in Riak utilizing the power of Apache Spark. This makes the quest for discovering incredible insights hidden in the enormous volumes of data being driven by modern applications, a lot easier. Riak Spark Connector fully supports Riak TS 1.3 for both time-series tables and key/value buckets[1](https://databricks.com/blog/2016/08/11/the-quest-for-hidden-treasure-an-apache-spark-connector-for-the-riak-nosql-database.html#footnote-1).

Working closely with the Databricks team, [we created a notebook](https://docs.cloud.databricks.com/docs/latest/databricks_guide/index.html#03%20Data%20Sources/5%20Databases%20%26%20Other%20Data%20Sources/7%20RiakTS%20Tutorial.html), showing Spark and Riak TS integration, which can be found in Databricks at **‘Data Sources / Databases & Other Data Sources / RiakTS Tutorial’**.

[![RiakTS-Tutorial-on-Databricks-Screenshot.png](../images/apache-spark-connector-for-the-riak-nosql-database/RiakTS-Tutorial-on-Databricks-Screenshot1.png)](https://docs.cloud.databricks.com/docs/latest/databricks_guide/index.html#03%20Data%20Sources/5%20Databases%20%26%20Other%20Data%20Sources/7%20RiakTS%20Tutorial.html)

Additionally, there are a couple of nice tutorials/demonstrations on Basho.com. The first [gives a demonstration of Riak TS](http://basho.com/products/riak-ts/) using a publicly available data set and the second builds on this example by [using the same data set and analyzing it using the Apache Spark Connector](http://basho.com/products/riak-ts/apache-spark-connector/).

#### Pavel Hardek

#### Product Director

#### [@PavelHardak](https://twitter.com/PavelHardak)

![blog-single-line](../images/apache-spark-connector-for-the-riak-nosql-database/blog-single-line.png)  
1 Riak KV will gain Spark support soon, [contact me](http://info.basho.com/2016-08_WR_SparkConnectorForKV_StayUpToDate_Landing-Page.html) if you are interested in being notified once it is available.

Read the full story at:   
<https://databricks.com/blog/2016/08/11/the-quest-for-hidden-treasure-an-apache-spark-connector-for-the-riak-nosql-database.html>
