\# Healthcare Data Integration Platform



A healthcare data integration and ETL platform built using Python, SQL/T-SQL, Azure SQL Database, and Synthea synthetic healthcare data.



\## Project Overview



This project simulates an enterprise healthcare data integration workflow where synthetic healthcare data is ingested, profiled, validated, transformed, and loaded into a relational data platform.



The project demonstrates practical data engineering concepts including:



\* Data ingestion

\* Data profiling and validation

\* Source-to-staging processing

\* Relational data modeling

\* ETL transformations

\* Data quality checks

\* Source-to-target reconciliation

\* Error handling and reprocessing

\* Pipeline monitoring



\## Current Progress



\### 1. Synthetic Healthcare Data



\[Synthea](https://github.com/synthetichealth/synthea) is used as the source of synthetic healthcare data.



The following raw datasets have been generated and added to the project:



| Dataset    | Approx. Records | Purpose                               |

| ---------- | --------------: | ------------------------------------- |

| Patients   |              12 | Patient/member information            |

| Encounters |           4,870 | Healthcare visits and clinical events |

| Providers  |              42 | Healthcare provider information       |

| Payers     |              10 | Insurance/payer information           |



The record counts are intentionally different because each dataset represents a different healthcare entity and has different relationships. For example, one patient can have multiple encounters, while multiple patients can be associated with the same provider or payer.



\### 2. Data Profiling



Python and pandas are being used to profile the raw healthcare CSV files before they enter the ETL pipeline.



Current profiling checks include:



\* Row and column counts

\* Column names

\* Data types

\* Missing-value counts

\* Duplicate-row checks

\* Duplicate identifier checks



Current profiling scripts:



```text

scripts/

├── inspect\_patients.py

├── inspect\_encounters.py

├── inspect\_providers.py

└── inspect\_payers.py

```



The profiling stage identifies potential data-quality issues without modifying the original raw datasets.



\## Project Structure



```text

Healthcare-Data-Integration-Platform/

│

├── data/

│   └── raw/                  # Raw Synthea CSV files

│

├── scripts/                  # Python ingestion and profiling scripts

│

├── sql/                      # SQL/T-SQL schemas and transformations

│

├── tests/                    # Data and pipeline tests

│

├── docs/                     # Architecture and project documentation

│

├── .gitignore

└── README.md

```



\## Planned ETL Architecture



```text

Synthea

&#x20;  ↓

Raw CSV Files

&#x20;  ↓

Python Ingestion \& Profiling

&#x20;  ↓

Azure SQL Staging Layer

&#x20;  ↓

Data Validation \& Transformation

&#x20;  ↓

Relational Healthcare Model

&#x20;  ↓

Azure SQL Database

&#x20;  ↓

Data Quality \& Source-to-Target Reconciliation

&#x20;  ↓

Monitoring / Error Handling / Reprocessing

```



\## Planned Healthcare Data Model



The project will progressively model relationships between healthcare entities such as:



```text

Patient

&#x20;  │

&#x20;  ├──────────────→ Encounter

&#x20;  │                    │

&#x20;  │                    └──────────────→ Provider

&#x20;  │

&#x20;  └──────────────→ Coverage / Payer

&#x20;                          



Patient

&#x20;  │

&#x20;  └──────────────→ Claim

&#x20;                        │

&#x20;                        └──────────────→ Claim Line

```



The relational model will be designed to support healthcare data integration, transformation, validation, and downstream reporting/analytics.



\## Planned ETL Components



The project will progressively implement:



1\. Raw healthcare data ingestion

2\. Staging tables in Azure SQL

3\. Data validation and quality checks

4\. Data transformation

5\. Relational healthcare data model

6\. Source-to-target reconciliation

7\. Error detection and reprocessing

8\. Load and pipeline logging

9\. Monitoring of ETL processing



\## Technology Stack



\* \*\*Python\*\*

\* \*\*pandas\*\*

\* \*\*SQL / T-SQL\*\*

\* \*\*Azure SQL Database\*\*

\* \*\*Bash / Linux\*\*

\* \*\*Git / GitHub\*\*

\* \*\*Synthea\*\*



\## Project Status



The project is being developed incrementally.



\### Completed



\* Set up Synthea as a synthetic healthcare data source

\* Generated patient, encounter, provider, and payer datasets

\* Added raw CSV files to the project

\* Created Python/pandas profiling scripts

\* Implemented basic data-quality profiling checks

\* Set up project version control with Git/GitHub



\### In Progress / Planned



\* Analyze relationships and identifiers between healthcare datasets

\* Design relational healthcare schema

\* Create Azure SQL staging tables

\* Implement Python-based ingestion

\* Implement transformations and validation

\* Add claims and claim-line data

\* Implement source-to-target reconciliation

\* Add error handling and reprocessing

\* Add ETL logging and monitoring



