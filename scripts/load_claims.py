
import time
import pandas as pd
from decimal import Decimal
from db_connection import get_connection

CSV_PATH = (
    r"D:\Reshma Personal\Reshma Capstone Project\Healthcare-Data-Integration-Platform\data\raw\claims.csv"
)

TABLE = "dbo.stg_claims"
BATCH_SIZE = 500
MAX_RETRIES = 5


# Read code-like and decimal columns as strings to prevent
# pandas from changing their values or using scientific notation.
string_columns = [
    "DEPARTMENTID",
    "PATIENTDEPARTMENTID",
    "DIAGNOSIS1",
    "DIAGNOSIS2",
    "DIAGNOSIS3",
    "DIAGNOSIS4",
    "DIAGNOSIS5",
    "DIAGNOSIS6",
    "DIAGNOSIS7",
    "DIAGNOSIS8",
    "REFERRINGPROVIDERID",
    "HEALTHCARECLAIMTYPEID1",
    "HEALTHCARECLAIMTYPEID2",
    "OUTSTANDING1",
    "OUTSTANDING2",
    "OUTSTANDINGP",
]

df = pd.read_csv(
    CSV_PATH,
    dtype={column: "string" for column in string_columns},
)

total_rows = len(df)
print("Source rows:", total_rows)

# Claim Id must uniquely identify each source record.
if df["Id"].isna().any():
    raise ValueError("Source claims contain missing Id values.")

if df["Id"].duplicated().any():
    raise ValueError("Source claims contain duplicate Id values.")


# Convert date columns.
date_columns = [
    "CURRENTILLNESSDATE",
    "SERVICEDATE",
    "LASTBILLEDDATE1",
    "LASTBILLEDDATE2",
    "LASTBILLEDDATEP",
]

for column in date_columns:
    df[column] = pd.to_datetime(
        df[column],
        errors="raise",
        utc=True,
    ).dt.date


# Convert outstanding amounts to Decimal for SQL DECIMAL columns.
decimal_columns = [
    "OUTSTANDING1",
    "OUTSTANDING2",
    "OUTSTANDINGP",
]

for column in decimal_columns:
    df[column] = df[column].apply(
        lambda value: (
            Decimal(str(value))
            if pd.notna(value) and str(value).strip()
            else None
        )
    )

# Convert pandas missing values to Python None for SQL NULL.
df = df.astype(object).where(pd.notna(df), None)


def connect_and_get_existing_ids():
    """Connect to Azure SQL and retrieve claim IDs already loaded."""
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(f"SELECT [Id] FROM {TABLE}")
    existing_ids = {
        str(row[0]).strip()
        for row in cursor.fetchall()
        if row[0] is not None
    }

    cursor.close()
    return connection, existing_ids


connection = None

try:
    # Discover the target columns instead of hardcoding their order.
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT COLUMN_NAME
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_SCHEMA = 'dbo'
          AND TABLE_NAME = 'stg_claims'
        ORDER BY ORDINAL_POSITION;
    """)

    target_columns = [
        row[0]
        for row in cursor.fetchall()
        if row[0].lower() != "stg_load_log_key"
    ]

    cursor.close()
    connection.close()
    connection = None

    # Match CSV columns to SQL columns, ignoring case.
    csv_column_map = {
        column.lower(): column
        for column in df.columns
    }

    if set(csv_column_map) != {
        column.lower() for column in target_columns
    }:
        raise ValueError(
            "CSV columns do not match the target SQL columns."
        )

    df = df[
        [csv_column_map[column.lower()] for column in target_columns]
    ]

    id_index = next(
        index
        for index, column in enumerate(target_columns)
        if column.lower() == "id"
    )

    columns_sql = ", ".join(
        f"[{column}]" for column in target_columns
    )
    placeholders = ", ".join("?" for _ in target_columns)

    insert_sql = (
        f"INSERT INTO {TABLE} ({columns_sql}) "
        f"VALUES ({placeholders})"
    )

    # Read existing IDs before loading. This also supports reruns.
    connection, existing_ids = connect_and_get_existing_ids()

    print("Claims already loaded:", len(existing_ids))

    for start in range(0, total_rows, BATCH_SIZE):
        batch = df.iloc[start:start + BATCH_SIZE]
        batch_rows = list(batch.itertuples(index=False, name=None))

        # Retry the current batch if the connection fails.
        for attempt in range(MAX_RETRIES):
            try:
                # Exclude claims committed during earlier runs/batches.
                pending_rows = [
                    row
                    for row in batch_rows
                    if str(row[id_index]).strip() not in existing_ids
                ]

                if not pending_rows:
                    break

                cursor = connection.cursor()

                for row in pending_rows:
                    cursor.execute(insert_sql, row)

                # Commit each batch, not the entire file at once.
                connection.commit()
                cursor.close()

                # Record committed IDs in memory.
                existing_ids.update(
                    str(row[id_index]).strip()
                    for row in pending_rows
                )

                break

            except Exception as error:
                print(
                    f"Batch starting at source row {start + 1} "
                    f"failed on attempt {attempt + 1}: {error}"
                )

                # The connection may be broken. Do not rely on
                # rollback succeeding on a failed connection.
                try:
                    connection.close()
                except Exception:
                    pass

                connection = None

                if attempt == MAX_RETRIES - 1:
                    raise

                # Exponential backoff: 5, 10, 20, 40 seconds.
                wait_seconds = min(5 * (2 ** attempt), 60)
                print(f"Retrying in {wait_seconds} seconds...")
                time.sleep(wait_seconds)

                # Reconnect and refresh IDs. This determines whether
                # the previous batch was committed before the failure.
                connection, existing_ids = (
                    connect_and_get_existing_ids()
                )

        processed = min(start + BATCH_SIZE, total_rows)
        print(
            f"Processed source rows {start + 1}-{processed} "
            f"of {total_rows}; loaded IDs: {len(existing_ids)}"
        )

    # Final source-to-target reconciliation.
    cursor = connection.cursor()
    cursor.execute(f"SELECT COUNT(*) FROM {TABLE}")
    target_rows = cursor.fetchone()[0]
    cursor.close()

    print("\nSource rows:", total_rows)
    print("Target rows:", target_rows)
    print("Row counts match:", total_rows == target_rows)

    if target_rows != total_rows:
        raise RuntimeError(
            "Source and target row counts do not match. "
            "Check for pre-existing or unrelated target records."
        )

    print("Claims CSV load completed successfully.")

finally:
    if connection is not None:
        try:
            connection.close()
        except Exception:
            pass
