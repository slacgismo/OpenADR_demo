import mysql.connector


mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password"
)

cur = mydb.cursor()
cur.execute("USE DB")

sql_stmt = f"SELECT * FROM Orders"

cur.execute(sql_stmt)
response = cur.fetchall()

for row in response:
    print(row[0], row[1])

cur.close()
mydb.close()
