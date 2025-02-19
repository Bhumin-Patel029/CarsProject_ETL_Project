# Databricks notebook source
# MAGIC %md
# MAGIC # DATA READING
# MAGIC

# COMMAND ----------

df = spark.read.format('parquet')\
    .option('inferSchema',True)\
        .load('abfss://bronze@carsdatalake369.dfs.core.windows.net/rawdata')

# COMMAND ----------

df.display()

# COMMAND ----------

# MAGIC %md
# MAGIC # DATA TRANSFORMATION

# COMMAND ----------

from pyspark.sql.functions import split, col

df = df.withColumn('model_category', split(col('Model_ID'), '-')[0])
display(df)

# COMMAND ----------

from pyspark.sql.types import StringType
from pyspark.sql.functions import col

df = df.withColumn('Units_Sold', col('Units_Sold').cast(StringType()))
display(df)

# COMMAND ----------

df = df.withColumn('RevPerUnit',col('Revenue')/col('Units_Sold'))
display(df)

# COMMAND ----------

# MAGIC %md
# MAGIC # AD-HOC
# MAGIC

# COMMAND ----------

from pyspark.sql.functions import sum

display(df.groupBy('Year', 'BranchName').agg(sum('Units_Sold').alias('Total_Units_Sold')).sort('Year','Total_Units_Sold',ascending=[1,0]))

# COMMAND ----------

# MAGIC %md 
# MAGIC # DATA WRITING

# COMMAND ----------

df.write.format('parquet')\
    .mode('overwrite')\
        .option('path','abfss://silver@carsdatalake369.dfs.core.windows.net/carsales')\
            .save()

# COMMAND ----------

# MAGIC %md
# MAGIC # Querying Data

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM parquet.`abfss://silver@carsdatalake369.dfs.core.windows.net/carsales`