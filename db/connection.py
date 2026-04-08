from pymongo import MongoClient
import os
import sys

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")

db = None
sessions_collection = None
logs_collection = None

try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    # Trigger connection to check if URI is valid
    client.server_info()
    db = client["debt_env"]
    sessions_collection = db["sessions"]
    logs_collection = db["logs"]
except Exception as e:
    print(f"CRITICAL: Failed to connect to MongoDB at {MONGO_URI}: {e}")
    # In some environments (like HF Spaces), we might want to fall back to a mock or just log
    # The collections remain None, which the repositories gracefully handle.