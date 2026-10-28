--Step 1: Check all four tables having unique Id's
SELECT
    'stg_patients' AS table_name,
    COUNT(*) AS total_rows,
    COUNT(Id) AS non_null_ids,
    COUNT(DISTINCT Id) AS unique_ids
FROM dbo.stg_patients

UNION ALL

SELECT
    'stg_payers',
    COUNT(*),
    COUNT(Id),
    COUNT(DISTINCT Id)
FROM dbo.stg_payers

UNION ALL

SELECT
    'stg_encounters',
    COUNT(*),
    COUNT(Id),
    COUNT(DISTINCT Id)
FROM dbo.stg_encounters

UNION ALL

SELECT
    'stg_providers',
    COUNT(*),
    COUNT(Id),
    COUNT(DISTINCT Id)
FROM dbo.stg_providers;

UNION ALL

SELECT
    'stg_providers',
    COUNT(*),
    COUNT(Id),
    COUNT(DISTINCT Id)
FROM dbo.stg_claims;

--Step 2: Check whether Id allows NULL
SELECT
    TABLE_NAME,
    COLUMN_NAME,
    IS_NULLABLE,
    DATA_TYPE,
    CHARACTER_MAXIMUM_LENGTH
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_SCHEMA = 'dbo'
  AND TABLE_NAME IN (
      'stg_patients',
      'stg_payers',
      'stg_encounters',
      'stg_providers'
  )
  AND COLUMN_NAME = 'Id';

--Step 3: Alyet ID col from nullable to not nullable and add primary key to the ID col

ALTER TABLE dbo.stg_claims
ALTER COLUMN Id NVARCHAR(36) NOT NULL;

Add the primary key
ALTER TABLE dbo.stg_claims
ADD CONSTRAINT PK_stg_claims
PRIMARY KEY (Id);

ALTER TABLE dbo.stg_patients
ALTER COLUMN Id NVARCHAR(36) NOT NULL;

ALTER TABLE dbo.stg_patients
ADD CONSTRAINT PK_stg_patients
PRIMARY KEY (Id);


ALTER TABLE dbo.stg_payers
ALTER COLUMN Id NVARCHAR(36) NOT NULL;

ALTER TABLE dbo.stg_payers
ADD CONSTRAINT PK_stg_payers
PRIMARY KEY (Id);


ALTER TABLE dbo.stg_encounters
ALTER COLUMN Id NVARCHAR(36) NOT NULL;

ALTER TABLE dbo.stg_encounters
ADD CONSTRAINT PK_stg_encounters
PRIMARY KEY (Id);


ALTER TABLE dbo.stg_providers
ALTER COLUMN Id NVARCHAR(36) NOT NULL;

ALTER TABLE dbo.stg_providers
ADD CONSTRAINT PK_stg_providers
PRIMARY KEY (Id);

--Step 4:Verify the primary keys

SELECT
    OBJECT_NAME(parent_object_id) AS table_name,
    name AS primary_key_name,
    type_desc
FROM sys.key_constraints
WHERE type = 'PK'
  AND parent_object_id IN (
      OBJECT_ID('dbo.stg_patients'),
      OBJECT_ID('dbo.stg_payers'),
      OBJECT_ID('dbo.stg_encounters'),
      OBJECT_ID('dbo.stg_providers'),
      OBJECT_ID('dbo.stg_claims')
  )
ORDER BY table_name;