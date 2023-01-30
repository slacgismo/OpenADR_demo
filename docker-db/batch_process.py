

import csv
from datetime import datetime

import mysql.connector


mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password"
)

cur = mydb.cursor()
cur.execute("USE openADR")


# data_file = 'orders.csv'
data_file = 'measurement.csv'

with open(data_file, "r") as f:
    csv_reader = csv.DictReader(f)
    records = list(csv_reader)


#   `meter_id` VARCHAR(100) NOT NULL primary key,
#   `ven_id` INT NOT NULL,
#   `measurement` VARCHAR(45) NOT NULL,
#   `value` REAL NOT NULL,
#   `time` DATETIME NOT NULL,
#   `device_id` VARCHAR(45) NOT NULL,
for record in records:
    print(record)
    time = record['time']
    date_obj = datetime.strptime(time, '%Y-%m-%d %H:%M:%S.%f')
    ven_id = record['ven_id']
    measurement = record['measurement']
    value = record['value']
    device_id = record['device_id']
    meter_id = record['meter_id']
    sql_stmt = f"INSERT INTO meter(meter_id, ven_id,measurement,value,date_obj,device_id) VALUES('{meter_id}', '{ven_id}', '{measurement}', '{value}', '{date_obj}', '{device_id}')"
    cur.execute(sql_stmt)
    mydb.commit()

cur.close()
mydb.close()
