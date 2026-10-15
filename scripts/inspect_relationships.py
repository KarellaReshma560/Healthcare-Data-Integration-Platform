
import pandas as pd
from pathlib import Path

# Step 1: Find the raw data folder
data_folder = Path(__file__).resolve().parent.parent / "data" / "raw"

# Step 2: Load the CSV files
patients = pd.read_csv(data_folder / "patients.csv", dtype="string")
encounters = pd.read_csv(data_folder / "encounters.csv", dtype="string")
providers = pd.read_csv(data_folder / "providers.csv", dtype="string")
payers = pd.read_csv(data_folder / "payers.csv", dtype="string")
claims = pd.read_csv(data_folder / "claims.csv", dtype="string")


# Step 3: Create a function to check IDs between two datasets
def check_relationship(source_df, source_column,
                       target_df, target_column, relationship_name):

    print("\nChecking:", relationship_name)

    # Get IDs from the source dataset
    source_ids = source_df[source_column].dropna().str.strip()
    source_ids = source_ids[source_ids != ""]

    # Get IDs from the target dataset
    target_ids = target_df[target_column].dropna().str.strip()

    # Find source IDs that do not exist in the target
    unmatched_ids = set(source_ids) - set(target_ids)

    print("Number of source references:", len(source_ids))
    print("Number of unmatched IDs:", len(unmatched_ids))

    if unmatched_ids:
        print("Sample unmatched IDs:", list(unmatched_ids)[:5])
    else:
        print("All non-empty references matched.")


# Step 4: Check patient relationships
check_relationship(
    encounters, "PATIENT", patients, "Id",
    "Encounters -> Patients"
)

check_relationship(
    claims, "PATIENTID", patients, "Id",
    "Claims -> Patients"
)


# Step 5: Check provider relationships
check_relationship(
    encounters, "PROVIDER", providers, "Id",
    "Encounters -> Providers"
)

check_relationship(
    claims, "PROVIDERID", providers, "Id",
    "Claims -> Providers"
)


# Step 6: Check payer relationships
check_relationship(
    encounters, "PAYER", payers, "Id",
    "Encounters -> Payers"
)

check_relationship(
    claims, "PRIMARYPATIENTINSURANCEID", payers, "Id",
    "Claims -> Primary Payer"
)

check_relationship(
    claims, "SECONDARYPATIENTINSURANCEID", payers, "Id",
    "Claims -> Secondary Payer"
)


# Step 7: Check claim appointment references against encounters
check_relationship(
    claims, "APPOINTMENTID", encounters, "Id",
    "Claims -> Encounters (appointment reference)"
)

print("\nFirst 10 patient IDs:")
print(patients["Id"].head(10).to_list())

print("\nFirst 10 patient IDs referenced by claims:")
print(claims["PATIENTID"].head(10).to_list())

print("\nFirst 10 patient IDs referenced by encounters:")
print(encounters["PATIENT"].head(10).to_list())