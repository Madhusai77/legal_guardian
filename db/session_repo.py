from db.connection import sessions_collection, db
from bson import ObjectId
from datetime import datetime

def create_session(state):
    if sessions_collection is None:
        return "mock_session_id"
    
    # state is a State Pydantic model
    session_data = {
        "state": state.dict() if hasattr(state, "dict") else state,
        "done": False,
        "created_at": datetime.utcnow()
    }
    result = sessions_collection.insert_one(session_data)
    return str(result.inserted_id)

def get_session(session_id):
    if sessions_collection is None:
        return None
    try:
        session = sessions_collection.find_one({"_id": ObjectId(session_id)})
        if session:
            session["_id"] = str(session["_id"])
        return session
    except Exception:
        return None

def list_sessions(limit=10):
    if sessions_collection is None:
        return []
    try:
        sessions = list(sessions_collection.find().sort("created_at", -1).limit(limit))
        for s in sessions:
            s["_id"] = str(s["_id"])
        return sessions
    except Exception as e:
        print(f"Error listing sessions: {e}")
        return []

def get_latest_session():
    if sessions_collection is None:
        return None
    try:
        session = sessions_collection.find_one(sort=[("created_at", -1)])
        if session:
            session["_id"] = str(session["_id"])
        return session
    except Exception as e:
        print(f"Error getting latest session: {e}")
        return None

def update_session(session_id, state, done):
    if sessions_collection is None:
        return
    try:
        sessions_collection.update_one(
            {"_id": ObjectId(session_id)},
            {"$set": {
                "state": state.dict() if hasattr(state, "dict") else state, 
                "done": done,
                "updated_at": datetime.utcnow()
            }}
        )
    except Exception as e:
        print(f"Error updating session {session_id}: {e}")