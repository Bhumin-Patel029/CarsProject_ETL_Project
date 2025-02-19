# **Azure End-to-End Data Engineering Project-CarSales: Medallion Architecture**

This project is a data engineering solution built on Microsoft Azure, focused on processing car sales data using the Medallion Architecture (Bronze, Silver, and Gold layers). It automates data workflows to provide scalable and efficient processing from raw data to analytics-ready insights.

## **System Architecture Overview**

The Medallion Architecture guides the data transformation, where the raw data flows through the following stages:

1. **Bronze Layer** - Raw, unrefined data
2. **Silver Layer** - Cleaned and enriched data
3. **Gold Layer** - Analytics-ready data


![architecture image](https://github.com/user-attachments/assets/4fe90069-f8e9-4658-abcf-1e0264518172)

---

## **Project Overview**

This project implements a robust data pipeline for car sales data using the Medallion framework. By leveraging Azure tools, the pipeline is designed to handle large-scale data processing and provide structured insights at the end.

### **Key Features**

- **Three-Tier Architecture:** Data is processed and stored in separate stages (Bronze, Silver, Gold) for easy management and optimization.
- **Automated Pipeline:** Azure Data Factory orchestrates the entire pipeline, moving and transforming data automatically.
- **Incremental Loading:** Data is added incrementally to the Bronze layer, ensuring efficient processing.
- **Data Cleanup:** Databricks handles data transformations, making the final dataset ready for analytics.
- **Star Schema & SCD Type-1:** A star schema is used to structure the final dataset, with Slowly Changing Dimension (SCD) Type-1 for updating historical data.

---

## **Technologies Used**

- **Azure Data Factory** for orchestrating data movement.
- **Azure SQL Database** for storing raw data.
- **Azure Data Lake Gen 2** for tiered storage (Bronze, Silver, Gold).
- **Azure Databricks** for data transformation and enrichment.
- **Star Schema & SCD Type-1** for efficient data modeling.

---

## **Project Workflow**

### **Step 1: Raw Data Ingestion**
Data is fetched from an external source (e.g., GitHub) and loaded into Azure SQL Database using Azure Data Factory.

### **Step 2: Incremental Data Loading**
New data is loaded incrementally into the Bronze layer of Azure Data Lake Gen 2. Azure Data Factory automates this process.

### **Step 3: Data Transformation**
Databricks processes the data, cleans it, and applies necessary transformations to build the Silver and Gold layers, structured into a star schema.

### **Step 4: Reporting-Ready Data**
The Gold layer is the final output—cleaned and enriched data that can be used for business intelligence or reporting.

---

## **Pipeline Details**

### **Pipeline 1: Data Ingestion**

This pipeline fetches data from GitHub and loads it into the Azure SQL Database.

![ingestion pipeline](https://github.com/user-attachments/assets/55ef7742-7be6-496b-8141-3596286c377d)

### **Pipeline 2: Incremental Data Loading**

This pipeline ensures that only new data is appended to the Bronze layer in Azure Data Lake Gen 2.

![incremental loading](https://github.com/user-attachments/assets/4ff1d24b-b6d5-40a3-842f-358552270969)

### **Databricks Workflow: Building the Star Schema**

The raw data is transformed into structured tables with a star schema in Databricks.

![databricks workflow](https://github.com/user-attachments/assets/fa3c1295-5e00-42ce-aedc-d3b47a558f02)

### **SQL Procedures and Data Transformation**

SQL tables and procedures are created to facilitate data cleaning and transformations.

![sql procedures](https://github.com/user-attachments/assets/abea55b8-9a30-48f4-b633-c200d312fcbc)

### **Azure Resource Group**

Overview of the deployed resources within Azure for this project.

![resource group](https://github.com/user-attachments/assets/d7068f49-eec5-45cc-a891-24b8e9d2da85)

---

## **How to Deploy and Run the Project**

Follow these steps to deploy and run the project in your Azure environment.

### **Prerequisites**
- **Azure Subscription** for access to Azure services (Data Factory, Databricks, Data Lake).
- **Basic knowledge of Azure Data Factory** for pipeline creation.
- **Azure Databricks Workspace** setup and cluster configuration.
- **GitHub Repository Access** for fetching the raw data.
- **Azure SQL Database** for storing raw data.

### **Step-by-Step Instructions**

1. **Configure Data Factory Pipelines:**
   - Pipeline 1: Set up data ingestion from GitHub to SQL Database.
   - Pipeline 2: Automate incremental data loading into the Bronze layer of Data Lake.

2. **Set Up Databricks:**
   - Create a Databricks workspace and set up the cluster.
   - Import Databricks notebooks that handle data transformation and schema creation.

3. **Verify Data Flow:**
   - Ensure raw data is stored in SQL Database.
   - Verify that data flows correctly through the Bronze, Silver, and Gold layers in Data Lake.

4. **Star Schema Construction:**
   - Run Databricks jobs to generate the star schema for reporting, implementing SCD Type-1 for historical updates.

5. **Optional Customizations:**
   - Modify workflows and notebooks as needed, including adding custom monitoring or error handling mechanisms.

---

### **Post-Execution**

After the pipeline completes, the Gold layer will contain clean, enriched data. This data can be accessed and used for analytics or reporting.

---

This code version of the README follows the same structure and clarity as the one I provided earlier, but with unique phrasing and fresh content throughout. Let me know if you'd like further modifications!
