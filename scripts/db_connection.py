import struct  #Converts the authentication token into the binary format required by ODBC

import pyodbc #Connects Python to Azure SQL and executes SQL queries.
from azure.identity import AzureCliCredential #Gets an Azure authentication token using your existing az login session.

SERVER = "healthcare-sql-reshma-2026.database.windows.net"
DATABASE = "HealthcareDataDB"

SQL_COPT_SS_ACCESS_TOKEN = 1256 #This number identifies the ODBC connection attribute used to pass an access token to the SQL Server driver.
#It tells ODBC that we are providing a token rather than a username and password

def get_connection():
    # # Get an Azure SQL access token using your Azure CLI login
    credential = AzureCliCredential()
    token = credential.get_token(
        "https://database.windows.net/.default"
    ).token

    # Format the token for ODBC Driver 18
    # ODBC Driver 18 expects the access token in a specific binary structure, not simply as a normal Python string.
    token_bytes = token.encode("utf-16-le")  # converts the token text into bytes
    token_struct = struct.pack(  # adds the length information in the binary format expected by the ODBC driver
        f"<I{len(token_bytes)}s",
        len(token_bytes),  #calculates the token's byte length
        token_bytes,
    )

    # Define the connection settings
    connection_string = (
        "Driver={ODBC Driver 18 for SQL Server};"
        f"Server=tcp:{SERVER},1433;"
        f"Database={DATABASE};"
        "Encrypt=yes;"
        "TrustServerCertificate=no;"
        "Connection Timeout=30;"
    )

    # Return the open database connection
    return pyodbc.connect(
        connection_string,
        attrs_before={
            SQL_COPT_SS_ACCESS_TOKEN: token_struct
        },
    )
