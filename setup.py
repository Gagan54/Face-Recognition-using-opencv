import sqlite3 as sql
import os
import pandas as pd

db = sql.connect('database.db')
cur = db.cursor()
sql_command = '''create table records(roll_no int(10) PRIMARY KEY,name varchar(12));'''
cur.execute(sql_command)
print('Database created Sucessfully')
print('Table Created Sucessfully.')
db.commit()
db.close()

os.mkdir('train_data')
os.mkdir('records')
df=pd.DataFrame()
df['Rollno']=''
df['Names']=''
df.to_excel('records\\Records.xls')
#os.mkdir('attendance')
print('Training Folder Created Successfully.')
print('Records File and Folder Created Successfully.')
#print('Attendance Folder Created Successfully.')
input('Press any key to continue...\n')



