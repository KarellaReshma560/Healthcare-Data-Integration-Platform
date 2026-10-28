--1. Check Patients table col's and record count
SELECT COLUMN_NAME, DATA_TYPE
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_SCHEMA = 'dbo'
  AND TABLE_NAME = 'stg_patients'
ORDER BY ORDINAL_POSITION;

Select count(*) from stg_patients;

--2. Check providers table col's and record count
SELECT
    COLUMN_NAME,
    DATA_TYPE,
    IS_NULLABLE
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_SCHEMA = 'dbo'
  AND TABLE_NAME = 'stg_providers'
ORDER BY ORDINAL_POSITION;

SELECT COUNT(*) AS existing_rows
FROM dbo.stg_providers;

--3. Check encounters table col's and record count
SELECT
    COLUMN_NAME,
    DATA_TYPE,
    IS_NULLABLE
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_SCHEMA = 'dbo'
  AND TABLE_NAME = 'stg_encounters'
ORDER BY ORDINAL_POSITION;

SELECT COUNT(*) AS existing_rows
FROM dbo.stg_encounters;

--4. Check payers table col's and record count
SELECT
    COLUMN_NAME,
    DATA_TYPE,
    IS_NULLABLE
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_SCHEMA = 'dbo'
  AND TABLE_NAME = 'stg_payers'
ORDER BY ORDINAL_POSITION;

SELECT *
FROM dbo.stg_payers;

--5. Check Claims table col's and record count
SELECT
    COLUMN_NAME,
    DATA_TYPE,
    IS_NULLABLE
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_SCHEMA = 'dbo'
  AND TABLE_NAME = 'stg_claims'
ORDER BY ORDINAL_POSITION;

SELECT
    COLUMN_NAME,
    DATA_TYPE,
    CHARACTER_MAXIMUM_LENGTH
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_SCHEMA = 'dbo'
  AND TABLE_NAME = 'stg_claims'
ORDER BY ORDINAL_POSITION;

SELECT count(*) as total_row_counts
FROM dbo.stg_claims;

SELECT
    COLUMN_NAME,
    DATA_TYPE,
    IS_NULLABLE
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_SCHEMA = 'dbo'
  AND TABLE_NAME = 'stg_claims'
  AND COLUMN_NAME = 'Id';

  EXEC sp_help 'dbo.stg_claims';

  SELECT
    name AS constraint_name,
    type_desc
FROM sys.key_constraints
WHERE parent_object_id = OBJECT_ID('dbo.stg_claims');

--Check the current Id definition
SELECT
    COLUMN_NAME,
    DATA_TYPE,
    CHARACTER_MAXIMUM_LENGTH,
    IS_NULLABLE
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_SCHEMA = 'dbo'
  AND TABLE_NAME = 'stg_claims'
  AND COLUMN_NAME = 'Id';


SELECT name, type_desc
FROM sys.key_constraints
WHERE parent_object_id = OBJECT_ID('dbo.stg_claims');
