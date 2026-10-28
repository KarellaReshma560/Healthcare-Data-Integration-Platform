
import pandas as pd
from db_connection import get_connection

CSV_PATH = r"D:\Reshma Personal\Reshma Capstone Project\Healthcare-Data-Integration-Platform\data\raw\encounters.csv"
TABLE = "dbo.stg_encounters"

# Read the source CSV
df = pd.read_csv(CSV_PATH)
print("Source rows:", len(df))

# Convert UTC timestamp strings to Python datetime values
for column in ["START", "STOP"]:
    df[column] = (
        pd.to_datetime(df[column], utc=True)
        .dt.tz_localize(None)
        .apply(lambda value: value.to_pydatetime() if pd.notna(value) else None)
    )

# Convert remaining missing values (NaN/NaT) to None
df = df.astype(object).where(pd.notna(df), None)
#Received Error's while loading type cast error. in order to find used below lines to find out datatypes
# print("\nCSV data types:")
# print(df.dtypes)
#
# print("\nSample records:")
# print(df.head(5).to_string())
#
# print("\nEmpty strings by column:")
# print((df == "").sum())

# Convert REASONCODE to strings for Azure SQL NVARCHAR
df["REASONCODE"] = df["REASONCODE"].apply(
    lambda value: (
        str(int(value))
        if pd.notna(value) and float(value).is_integer()
        else str(value) if pd.notna(value)
        else None
    )
)

# Convert missing values to SQL NULL
df = df.astype(object).where(pd.notna(df), None)

with get_connection() as connection:
    cursor = connection.cursor()

    # Prevent duplicate loading
    cursor.execute(f"SELECT COUNT(*) FROM {TABLE}")
    existing_rows = cursor.fetchone()[0]

    if existing_rows > 0:
        raise RuntimeError(
            f"{TABLE} already contains {existing_rows} rows. "
            "Load stopped to prevent duplicate inserts."
        )

    # Get target table columns, excluding the load-log key
    cursor.execute("""
        SELECT COLUMN_NAME
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_SCHEMA = 'dbo'
          AND TABLE_NAME = 'stg_encounters'
        ORDER BY ORDINAL_POSITION;
    """)

    target_columns = [
        row[0] for row in cursor.fetchall()
        if row[0].lower() != "stg_load_log_key"
    ]

    # Validate CSV and SQL column names
    csv_column_map = {col.lower(): col for col in df.columns}

    if set(csv_column_map) != {col.lower() for col in target_columns}:
        raise ValueError(
            "CSV columns do not match the target table columns.\n"
            f"CSV: {df.columns.tolist()}\n"
            f"SQL: {target_columns}"
        )

    # Arrange CSV columns in target table order
    df = df[
        [csv_column_map[col.lower()] for col in target_columns]
    ]

    columns_sql = ", ".join(f"[{col}]" for col in target_columns)
    placeholders = ", ".join("?" for _ in target_columns)

    insert_sql = (
        f"INSERT INTO {TABLE} ({columns_sql}) "
        f"VALUES ({placeholders})"
    )

    # Insert records
    cursor.fast_executemany = True
    cursor.executemany(
        insert_sql,
        list(df.itertuples(index=False, name=None)),
    )

    connection.commit()

    # Verify target row count
    cursor.execute(f"SELECT COUNT(*) FROM {TABLE}")
    target_rows = cursor.fetchone()[0]

    print("Target rows:", target_rows)
    print("Row counts match:", len(df) == target_rows)
    print("Encounters CSV load completed.")
