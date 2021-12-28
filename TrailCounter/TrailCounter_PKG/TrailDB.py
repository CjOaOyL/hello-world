'''
Created on Sep 5, 2021

@author: jaqua
'''

import os
import sqlalchemy
from sqlalchemy import MetaData
import pandas as pd

#import mysql.connector




def ConnToSQL(dbname):
    # Remember - storing secrets in plaintext is potentially unsafe. Consider using
    # something like https://cloud.google.com/secret-manager/docs/overview to help keep
    # secrets secret.
    db_user = "myUser"
    db_pass = "k4l4ni4Mysql"
    db_name = dbname
    db_host = ["35.232.112.8","3306"]
    
    
    # Extract host and port from db_host
    #host_args = db_host.split(":")
    db_hostname = "35.232.112.8"
    db_port = 3306
    
    #db_port = host_args[0], int(host_args[1])
    
    
    
    
    pool = sqlalchemy.create_engine(
        # Equivalent URL:
        # mysql+pymysql://<db_user>:<db_pass>@<db_host>:<db_port>/<db_name>
        sqlalchemy.engine.url.URL.create(
            drivername="mysql+pymysql",
            username=db_user,  # e.g. "my-database-user"
            password=db_pass,  # e.g. "my-database-password"
            host=db_hostname,  # e.g. "127.0.0.1"
            port=db_port,  # e.g. 3306
            database=db_name,  # e.g. "my-database-name"
        ),
        #**db_config
    )
    

    return pool


    
def readGSheet(sheet_name,sheet_id):
    

    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
    df = pd.read_csv(url)
    df.columns = df.columns.str.replace(' ','')
    
    return df

dbname = 'guestbook'
table1 = 'entries'
table2 = 'trailDB'
engine = ConnToSQL(dbname)   

metadata = MetaData()
metadata.reflect(engine)
print(metadata.tables.keys())

di = pd.read_sql(table1,engine)
print(di)

sheet_id = '1zIH1K7ohxNSgnZW4KOGfHEMFzHRayWyj'
sheet_name = 'Management_Sheet_Simplified'

df = readGSheet(sheet_name,sheet_id)
print(df)
print(df.columns)


'''eliminate empty rows'''
dg = df[df['Property'].notnull()]


print(dg)

 '''upload as new table to database'''
# 
# dg.to_sql(table2,engine,index=False)
# 
# dh = pd.read_sql(table2,engine)
# print(dh)

# dbname = 'guestbook'
# dbtable = 'entries'
# pool = ConnToSQL(dbname)
# df = pd.read_sql(dbtable,pool)
# 
# print(df)
# df2 = pd.DataFrame([{'guestName':'Carlos', 'content':'made up','entryID':3}])
# df.loc[len(df.index)] = ['Carlos', 'made up',3]
# print(df)
# 
# df2.to_sql(dbtable,pool, if_exists='append', index = False)
# pd.read_sql(dbtable,pool)
# 
# Trail_Char = ['trail_name', 'loc', 'length', 'parking', 'partners' ]
# Trail_Facts = ['year_obtained', 'Donated_by', 'Cost']

