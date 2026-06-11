import mysql.connector
import pandas as pd

# 1. Connect to the MySQL server
conn = mysql.connector.connect(
    host="18.136.157.135",
    port=3306,
    user="dm_team2",
    password="DM!$Team&27@9!20!",
    database="project_sales"
)

# 2. Run SQL and load into pandas
query = "SELECT * FROM data;"
df = pd.read_sql(query, conn)   # [web:54][web:60][web:66]

# 3. Close the connection
conn.close()

# 4. Save to CSV locally (optional but recommended)
df.to_csv("project_sales_data.csv", index=False)

print(df.shape)
print(df.head())