import pandas as pd
from pymongo import MongoClient

# Correct paths with raw strings
wilayas_path = r'C:\Users\k_ben\OneDrive\Desktop\inserting data in the db\data\wilayas.csv'
dairas_path = r'C:\Users\k_ben\OneDrive\Desktop\inserting data in the db\data\dairas.csv'
baladias_path = r'C:\Users\k_ben\OneDrive\Desktop\inserting data in the db\data\baladias.csv'

# Read the CSV files
wilayas_df = pd.read_csv(wilayas_path)
dairas_df = pd.read_csv(dairas_path)
baladias_df = pd.read_csv(baladias_path)

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['AlgeriaData']

# Clear previous data in collections if any
db.wilayas.delete_many({})
db.dairas.delete_many({})
db.baladias.delete_many({})

# Insert wilayas and keep track of wilaya_ids
wilaya_id_map = {}
for _, row in wilayas_df.iterrows():
    wilaya_doc = row.to_dict()
    wilaya_id = db.wilayas.insert_one(wilaya_doc).inserted_id
    wilaya_id_map[wilaya_doc['ID']] = wilaya_id  # Update with correct column name

# Insert dairas and keep track of daira_ids
daira_id_map = {}
for _, row in dairas_df.iterrows():
    daira_doc = row.to_dict()
    daira_doc['wilaya_id'] = wilaya_id_map[daira_doc['ID_Wilaya']]  # Add reference to wilaya
    daira_id = db.dairas.insert_one(daira_doc).inserted_id
    daira_id_map[daira_doc['ID']] = daira_id  # Update with correct column name

# Insert baladias with references to daira and wilaya
for _, row in baladias_df.iterrows():
    baladia_doc = row.to_dict()
    baladia_doc['daira_id'] = daira_id_map[baladia_doc['ID_Daira']]  # Add reference to daira
    baladia_doc['wilaya_id'] = wilaya_id_map[daira_doc['ID_Wilaya']]  # Add reference to wilaya
    db.baladias.insert_one(baladia_doc)

print("Data has been successfully inserted into MongoDB with relationships!")
