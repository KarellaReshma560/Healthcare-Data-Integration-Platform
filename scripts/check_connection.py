
from db_connection import get_connection

try:
    with get_connection() as connection:
        cursor = connection.cursor()

        cursor.execute("SELECT DB_NAME(), SUSER_SNAME();")
        database, account = cursor.fetchone()

        print("Connection successful!")
        print("Database:", database)
        print("Connected account:", account)

except Exception as error:
    print("Connection failed:")
    print(error)
