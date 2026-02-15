# models.py
from pymongo import MongoClient
from config import MONGO_URI, DB_NAME

client = MongoClient(MONGO_URI)
db = client[DB_NAME]

leads_collection = db["leads"]

emails_collection = db["emails"]
