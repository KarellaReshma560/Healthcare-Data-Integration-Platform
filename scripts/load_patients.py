
import struct

import pandas as pd
import pyodbc
from azure.identity import AzureCliCredential

# Azure SQL details
SERVER = "healthcare-sql-reshma-2026.database.windows.net"
DATABASE = "HealthcareDataDB"
CSV_PATH = r"D:\Reshma Personal\Reshma Capstone Project\Healthcare-Data-Integration-Platform\data\raw\patients.csv"
# Read the CSV
df = pd.read_csv(CSV_PATH)
print("Source rows:", len(df))

# Convert missing values to SQL NULL
df = df.astype(object).where(pd.notna(df), None)

# Get Azure SQL access token
credential = AzureCliCredential()
token = credential.get_token(
    "https://database.windows.net/.default"
).token

token_bytes = token.encode("utf-16-le")
token_struct = struct.pack(
    f"<I{len(token_bytes)}s",
    len(token_bytes),
    token_bytes,
)

# Connect to Azure SQL
connection_string = (
    "Driver={ODBC Driver 18 for SQL Server};"
    f"Server=tcp:{SERVER},1433;"
    f"Database={DATABASE};"
    "Encrypt=yes;"
    "TrustServerCertificate=no;"
)

with pyodbc.connect(
    connection_string,
    attrs_before={1256: token_struct},
) as connection:

    cursor = connection.cursor()

    # Stop if data already exists to avoid duplicate inserts
    cursor.execute("SELECT COUNT(*) FROM dbo.stg_patients")
    existing_rows = cursor.fetchone()[0]

    if existing_rows > 0:
        raise Exception(
            f"Table already contains {existing_rows} rows. "
            "Load stopped."
        )

    # Insert only the 28 CSV columns
    columns = ", ".join(f"[{col}]" for col in df.columns)
    placeholders = ", ".join("?" for _ in df.columns)

    sql = (
        f"INSERT INTO dbo.stg_patients ({columns}) "
        f"VALUES ({placeholders})"
    )

    cursor.fast_executemany = True
    cursor.executemany(
        sql,
        list(df.itertuples(index=False, name=None)),
    )

    connection.commit()

    # Verify inserted rows
    cursor.execute("SELECT COUNT(*) FROM dbo.stg_patients")
    target_rows = cursor.fetchone()[0]

    print("Target rows:", target_rows)
    print("Row counts match:", len(df) == target_rows)
    print("Patients CSV load completed.")