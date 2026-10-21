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

- Created an Azure SQL Database named `HealthcareDataDB`.
- Designed and created five staging tables.
- Added the table definitions to `sql/01_create_staging_tables.sql`.

Staging tables:

- `stg_patients`
- `stg_providers`
- `stg_payers`
- `stg_encounters`
- `stg_claims`

**Note:** The staging tables have been created. Loading the CSV data into them is the next step.

## Project Structure

```text
## Project Structure

```text
Healthcare-Data-Integration-Platform/
├── data/
│   └── raw/                         # Raw Synthea CSV files
├── scripts/
│   ├── inspect_patients.py          # Profile patient data
│   ├── inspect_encounters.py        # Profile encounter data
│   ├── inspect_providers.py         # Profile provider data
│   ├── inspect_payers.py            # Profile payer data
│   └── inspect_relationships.py     # Validate relationships between datasets
├── sql/
│   └── 01_create_staging_tables.sql # Create five staging tables
├── tests/                           # Data and pipeline tests
├── docs/                            # Project documentation
├── .gitignore
└── README.md
```

The profiling scripts inspect individual datasets, while `inspect_relationships.py` checks whether identifiers referenced across datasets match the corresponding records.


```

## ETL Architecture

The planned pipeline is:

```text

Synthea

  ↓

Raw CSV Files

  ↓

Python Ingestion \& Profiling

  ↓

Azure SQL Staging Layer

  ↓

Data Validation \& Transformation

  ↓

Relational Healthcare Model

  ↓

Azure SQL Database

  ↓

Data Quality \& Source-to-Target Reconciliation

  ↓

Monitoring / Error Handling / Reprocessing

```

## Next Steps

1. Load the raw CSV data into Azure SQL staging tables.
2. Validate loaded record counts and data quality.
3. Develop the relational healthcare data model.
4. Implement transformations and source-to-target reconciliation.
5. Add load logging, error handling, and reprocessing.
6. Explore pipeline orchestration and reporting tools as the project progresses.

## Project Status

The project is being developed incrementally, with an emphasis on understanding and implementing each stage of the data integration process.
