import pymongo
import pandas as pd
import json


url = "mongodb+srv://pwskills:pwskills@cluster0.mf0wr.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

#create a new client to connect with server
client = pymongo.MongoClient(url)

DATABASE_NAME = "sensor_fault_DB"
COLLECTION_NAME = "sensor_fault"

df = pd.read_csv(r"notebooks/wafer_23012020_041211.csv")

df.drop(columns=["Unnamed: 0"],inplace=True)

#convert df to json to store in db 
json_record = list(json.loads(df.T.to_json()).values())

collection1 = client[DATABASE_NAME][COLLECTION_NAME]

collection1.insert_many(json_record)

