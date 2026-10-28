# Healthcare Data Integration Platform

A healthcare data integration and ETL project built with Python, pandas, SQL/T-SQL, Azure SQL Database, and Synthea synthetic healthcare data.

## Project Overview

This project simulates a healthcare data pipeline that prepares, validates, and integrates synthetic healthcare data into a relational database.

The goal is to demonstrate practical data engineering skills, including data profiling, relational data modeling, ETL processing, data quality validation, and source-to-target reconciliation.

## Technology Stack

- **Programming:** Python, pandas
- **Database:** Azure SQL Database, SQL/T-SQL
- **Data Source:** [Synthea](https://github.com/synthetichealth/synthea)
- **Tools:** Bash/Linux, Git, GitHub

## Completed Work

### 1. Synthetic Healthcare Data

Generated synthetic healthcare data using Synthea and added the raw CSV files to the project.

Datasets include:

- Patients
- Providers
- Payers
- Encounters
- Claims

### 2. Data Profiling and Validation

Created Python and pandas scripts to inspect source datasets and identify potential data-quality issues.

Checks include:

- Row and column counts
- Column names and data types
- Missing values
- Duplicate rows and identifiers
- Relationships between datasets

Validated the available relationships between patients, providers, payers, encounters, and claims. All checked references matched their corresponding source records.

### 3. Azure SQL Staging Tables

Created an Azure SQL Database named HealthcareDataDB.

Designed and created five staging tables.

Stored the table definitions in sql/01_create_staging_tables.sql.

Loaded the raw CSV data into the corresponding staging tables.

Added a primary key to dbo.stg_claims on the Id column.

Implemented a Python claims loader with batch commits, duplicate-ID checks, retry handling, and source-to-target row-count validation.

Staging tables:

- **dbo.stg_patients**

- **dbo.stg_providers**

- **dbo.stg_payers**

- **dbo.stg_encounters**

- **dbo.stg_claims**

The staging layer provides a foundation for subsequent data-quality checks, transformations, and relational modeling.

4. SQL Development

Created SQL scripts to define and manage the staging tables and support database development.

The sql/ directory contains the project's SQL scripts for table creation, schema changes, and other database operations.

5. Python ETL Scripts

Developed Python scripts to profile source data, validate relationships, connect to Azure SQL Database, and load data into staging tables.

The claims loader supports batch processing and resuming interrupted loads by checking claim IDs already present in the target table.

## Project Structure

```text
## Project Structure

```text
Healthcare-Data-Integration-Platform/
├── data/
│   └── raw/                              # Raw Synthea CSV files
├── scripts/
│   ├── check_connection.py
│   ├── db_connection.py
│   ├── inspect_claims.py
│   ├── inspect_encounters.py
│   ├── inspect_patients.py
│   ├── inspect_payers.py
│   ├── inspect_providers.py
│   ├── inspect_relationships.py
│   ├── load_claims.py
│   ├── load_encounters.py
│   ├── load_patients.py
│   ├── load_payers.py
│   ├── load_providers.py
│   └── main.py
├── sql/
│   ├── 01_create_staging_tables.sql
│   ├── 02_check_and_add_primary_keys.sql
│   └── 03_Checking Data after loading.sql
├── tests/
├── docs/
├── .gitignore
└── README.md
```

```

## ETL Architecture

The planned pipeline is:

```text

Synthea
   ↓
Raw CSV Files
   ↓
Python Data Profiling and Validation
   ↓
Azure SQL Staging Tables
   ↓
Data Quality Checks and Reconciliation
   ↓
Relational Healthcare Data Model
   ↓
Production Data Loading
   ↓
Monitoring and Error Handling

```
The source-data generation, profiling, staging-table creation, and staging loads are implemented. Further validation, production-layer modeling, and monitoring capabilities will be developed incrementally.

## Next Steps

1.Validate staging-table row counts and data quality.
2.Implement comprehensive source-to-target reconciliation.
3.Design the relational healthcare data model.
4.Create production tables and appropriate foreign-key relationships.
5.Implement transformations and production-layer loading.
6.Add load logging, error handling, and reprocessing.
7.Explore pipeline orchestration and reporting tools.


## Project Status

All five synthetic healthcare datasets have been loaded into Azure SQL staging tables, and each staging table has a primary key on its Id column.

The project is progressing toward a complete healthcare data integration pipeline, with a focus on data quality, reliable ETL processing, and relational data modeling.
