import csv
from datetime import datetime

import mysql.connector


mydb = mysql.connector.connect(
    host="mysql",
    user="root",
    password="password"
)

cur = mydb.cursor()
cur.execute("USE openADR")

cur.execute("Show tables;")

myresult = cur.fetchall()

print("Show table ----- ")
for x in myresult:
    print(x)

print("----------")


data_file = 'measurements.csv'

with open(data_file, "r") as f:
    csv_reader = csv.DictReader(f)
    records = list(csv_reader)


for record in records:
    print(record)
    # data
    data_id = record['data_id']
    meter_id = record['meter_id']
    ven_id = record['ven_id']
    measurement = record['measurement']
    value = record['value']
    device_id = record['device_id']

    record_time = record['time']
    date_obj = datetime.strptime(record_time, '%Y-%m-%d %H:%M:%S.%f')

    sql_stmt = f"INSERT INTO measurements(data_id, meter_id,ven_id,measurement,value,device_id,time) VALUES('{data_id}', '{meter_id}', ' {ven_id}',' {measurement}',' {value}',' {device_id}',' {date_obj}')"
    cur.execute(sql_stmt)
    mydb.commit()

cur.execute("select * from measurements;")

myresult = cur.fetchall()
print("Show result ----- ")
for x in myresult:
    print(x)
cur.close()
mydb.close()
print("Save to DB success")
