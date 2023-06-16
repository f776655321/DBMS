import csv
import os
import json
import mysql.connector

with open('.config.json') as f:
    config = json.load(f)

host = config['host']
user = config['user']
passwd = config['passwd']

db = mysql.connector.connect(host = host, user = user, passwd = passwd)
cursor = db.cursor()

cursor.execute("CREATE DATABASE IF NOT EXISTS Source")
cursor.execute("CREATE DATABASE IF NOT EXISTS Target")

topic = 'us cities'
folder = f'./data/autojoin-Benchmark/{topic}'

for table in os.listdir(folder):
    if(table == 'source.csv'):   
        cursor.execute("USE Source")
        # Create table
        table_path = os.path.join(folder, table)
        table_name = topic.replace(" ", "_")
        with open(table_path, 'r') as f:
            reader = csv.reader(f)
            column_names = next(reader)
            create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ("
            for column_name in column_names:
                column_name = column_name.replace(" ", "_")
                create_table_query += f"`{column_name}` VARCHAR(512), "
            create_table_query = create_table_query.rstrip(", ") + ")"
            cursor.execute(create_table_query)
            
            for row in reader:
                insert_query = f"INSERT INTO {table_name} VALUES {tuple(row)}"
                insert_query = insert_query.rstrip(",)") + ")"
                print(insert_query)
                cursor.execute(insert_query)
        
    elif(table == 'target.csv'):
        cursor.execute("USE Target")
        # Create table
        table_path = os.path.join(folder, table)
        table_name = topic.replace(" ", "_")
        with open(table_path, 'r') as f:
            reader = csv.reader(f)
            column_names = next(reader)
            create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ("
            for column_name in column_names:
                column_name = column_name.replace(" ", "_")
                create_table_query += f"`{column_name}` VARCHAR(512), "
            create_table_query = create_table_query.rstrip(", ") + ")"
            cursor.execute(create_table_query)
            
            for row in reader:
                insert_query = f"INSERT INTO {table_name} VALUES {tuple(row)}"
                insert_query = insert_query.rstrip(",)") + ")"
                print(insert_query)
                cursor.execute(insert_query)

db.commit()
cursor.close()
db.close()
print("Success!")