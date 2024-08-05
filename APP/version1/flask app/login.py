from pymongo import MongoClient
import bcrypt

# MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client['AlgeriaData']
users_collection = db.users

# User data
username = 'karima'
password = '123456'

# Hash the password
hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

# Insert user into the database
users_collection.insert_one({
    'username': username,
    'password': hashed_password
})

print('User inserted successfully')
