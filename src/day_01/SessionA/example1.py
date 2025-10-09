import pyodbc

# Replace with your server & database
conn = pyodbc.connect(
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=localhost,1433;"
    "DATABASE=AdventureWorks2022;"
    "UID=sa;"
    "PWD=passw0rd;"
)

cursor = conn.cursor()

cursor.execute("select top 10 [AddressID], [AddressLine1] from [Person].[Address]")
rows = cursor.fetchall()

for row in rows:
    print(row)