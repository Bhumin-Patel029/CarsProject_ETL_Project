# Databricks notebook source
# MAGIC %md
# MAGIC
# MAGIC # Create Fact Table

# COMMAND ----------

# MAGIC %md
# MAGIC Reading Silver Data

# COMMAND ----------

df_silver = spark.sql("SELECT * FROM PARQUET.`abfss://silver@carsdatalake369.dfs.core.windows.net/carsales`")

# COMMAND ----------

df_silver.display()

# COMMAND ----------

# MAGIC %md
# MAGIC ### Reading all the DIMS

# COMMAND ----------

df_dealer = spark.sql("SELECT * FROM cars_catalog.gold.dim_dealer")

df_branch = spark.sql("SELECT * FROM cars_catalog.gold.dim_branch")

df_date= spark.sql("SELECT * FROM cars_catalog.gold.dim_date")

df_model = spark.sql("SELECT * FROM cars_catalog.gold.dim_model")

# COMMAND ----------

# MAGIC %md
# MAGIC ### Bringing Keys to the fact table

# COMMAND ----------

df_fact = df_silver.join(df_branch, df_silver.Branch_Id == df_branch.Branch_ID, 'left')\
    .join(df_dealer, df_silver.Dealer_ID == df_dealer.Dealer_ID, 'left')\
        .join(df_date, df_silver.Date_ID == df_date.Date_ID, 'left')\
            .join(df_model, df_silver.Model_ID == df_model.Model_ID, 'left')\
                .select(df_silver['Revenue'], df_silver['Units_Sold'], df_silver['RevPerUnit'], df_branch.dim_branch_key, df_dealer.dim_Dealer_key, df_date.dim_date_key, df_model.dim_model_key)
                

# COMMAND ----------

df_fact.display()   

# COMMAND ----------

# MAGIC %md
# MAGIC ### Writing Fact Table

# COMMAND ----------

from delta.tables import DeltaTable

# COMMAND ----------

if spark.catalog.tableExists("cars_catalog.gold.fact_sales"):
    deltatbl = DeltaTable.forName(spark, "cars_catalog.gold.fact_sales")

    deltatbl.alias("trg").merge(df_fact.alias("src"), "trg.dim_branch_key = src.dim_branch_key AND trg.dim_Dealer_key = src.dim_Dealer_key AND trg.dim_date_key = src.dim_date_key AND trg.dim_model_key = src.dim_model_key")\
        .whenMatchedUpdateAll()\
            .whenNotMatchedInsertAll()\
                .execute()


else:
    df_fact.write.format("delta").mode("overwrite")\
        .option("path","abfss://gold@carsdatalake369.dfs.core.windows.net/fact_sales")\
            .saveAsTable("cars_catalog.gold.fact_sales")

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from cars_catalog.gold.fact_sales