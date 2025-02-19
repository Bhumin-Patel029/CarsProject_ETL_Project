# Databricks notebook source
# MAGIC %md 
# MAGIC # Creating Flag Paramameter
# MAGIC

# COMMAND ----------

#Since we want to know if it is an inital run or incremental run, need to create a flag parameter

# COMMAND ----------

dbutils.widgets.text("incremental_flag", "0")

# COMMAND ----------

incremental_flag = dbutils.widgets.get("incremental_flag")
print(incremental_flag  )

# COMMAND ----------

# MAGIC %md
# MAGIC #Creating Dimension Model
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ### Fetch Relative Columns

# COMMAND ----------

df_src = spark.sql('''
select distinct(Dealer_ID) as Dealer_ID, DealerName
from parquet.`abfss://silver@carsdatalake369.dfs.core.windows.net/carsales`
''')

# COMMAND ----------

df_src.display()

# COMMAND ----------

# MAGIC %md
# MAGIC ### dim_model sink - Initial and Incremetnal

# COMMAND ----------

if not spark.catalog.tableExists('cars_catalog.gold.dim_dealer'):

    df_sink=spark.sql('''
    select 1 as dim_Dealer_key,Dealer_ID,DealerName
    from parquet.`abfss://silver@carsdatalake369.dfs.core.windows.net/carsales`
    where 1=0
    ''')
else:
    df_sink=spark.sql('''
    select dim_Dealer_key,Dealer_ID,DealerName
    from cars_catalog.gold.dim_dealer
    ''')




# COMMAND ----------

# MAGIC %md 
# MAGIC ### Filtering new records and old records
# MAGIC

# COMMAND ----------

df_filter = df_src.join(df_sink, df_src.Dealer_ID == df_sink.Dealer_ID, 'left').select(df_src.Dealer_ID, df_src.DealerName, df_sink.dim_Dealer_key)

# COMMAND ----------

# MAGIC %md
# MAGIC **df_filter_old**

# COMMAND ----------

df_filter_old = df_filter.filter(df_filter.dim_Dealer_key.isNotNull())

# COMMAND ----------

df_filter_old.display()

# COMMAND ----------

# MAGIC %md
# MAGIC **df_filter_new**

# COMMAND ----------

df_filter_new = df_filter.filter(df_filter.dim_Dealer_key.isNull()).select(df_filter.Dealer_ID, df_filter.DealerName)

# COMMAND ----------

df_filter_new.display()

# COMMAND ----------

# MAGIC %md
# MAGIC ### Create Surrogate Keys

# COMMAND ----------

# MAGIC %md
# MAGIC ### Fetch the max Surrogate Key

# COMMAND ----------

if incremental_flag == '0':
    max_value = 1
else:
    max_value = spark.sql("select max(dim_Dealer_key) from cars_catalog.gold.dim_Dealer").collect()[0][0]

# COMMAND ----------

print(max_value)    

# COMMAND ----------

# MAGIC %md
# MAGIC ### Create Surrogate Key column and add surrogate key

# COMMAND ----------

from pyspark.sql.functions import monotonically_increasing_id
df_filter_new = df_filter_new.withColumn('dim_Dealer_key', max_value + monotonically_increasing_id())

# COMMAND ----------

df_filter_new.display()

# COMMAND ----------

# MAGIC %md
# MAGIC ### Create Final df = df_filter_old + df_filter_new

# COMMAND ----------

df_final = df_filter_new.union(df_filter_old)

# COMMAND ----------

# MAGIC %md
# MAGIC # SCD TYPE - 1 UPSERT (update + insert)

# COMMAND ----------

from delta.tables import DeltaTable

# COMMAND ----------

#incremental run
if spark.catalog.tableExists('cars_catalog.gold.dim_dealer'):
    delta_tbl = DeltaTable.forPath(spark, "abfss://gold@carsdatalake369.dfs.core.windows.net/dim_dealer")

    delta_tbl.alias("trg").merge(df_final.alias("src"), "trg.dim_Dealer_key = src.dim_Dealer_key")\
        .whenMatchedUpdateAll()\
            .whenNotMatchedInsertAll()\
                .execute()
             
#initial run
else:
    df_final.write.format("delta")\
          .mode("overwrite")\
              .option("path","abfss://gold@carsdatalake369.dfs.core.windows.net/dim_dealer")\
              .saveAsTable("cars_catalog.gold.dim_dealer")

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from cars_catalog.gold.dim_dealer;