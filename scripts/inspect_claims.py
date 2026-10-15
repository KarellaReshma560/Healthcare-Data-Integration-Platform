import pandas as pd

file_path = "D:/Reshma Personal/Reshma Capstone Project/Healthcare-Data-Integration-Platform/data/raw/claims.csv"
df = pd.read_csv(file_path) #Load data from csv file

print("Number of rows:", len(df))
print("Number of columns:", len(df.columns))

print("\nColumn names:", df.columns.tolist())
print("\nData types:", df.dtypes)
print("\nMissing values:", df.isnull().sum())
print("\nDuplicate rows:", df.duplicated().sum())
print("\nDuplicate claim IDs:", df["Id"].duplicated().sum())
print("Duplicate patient IDs:", df["PATIENTID"].duplicated().sum())

print("Total claims:", len(df))
print("Unique claim IDs:", df["Id"].nunique())
print("Unique patient IDs in claims:", df["PATIENTID"].nunique())