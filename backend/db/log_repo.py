from db.connection import logs_collection
from bson import ObjectId
from datetime import datetime

def add_log(session_id, step_id, ai_output, lender_output, reward):
    if logs_collection is None:
        return
    
    log_entry = {
        "session_id": ObjectId(session_id) if ObjectId.is_valid(session_id) else session_id,
        "step_id": step_id,
        "ai_output": ai_output,
        "lender_output": lender_output,
        "reward": reward,
        "timestamp": datetime.utcnow()
    }
    logs_collection.insert_one(log_entry)

def get_logs(session_id):
    if logs_collection is None:
        return []
    
    query = {"session_id": ObjectId(session_id)} if ObjectId.is_valid(session_id) else {"session_id": session_id}
    logs = list(logs_collection.find(query).sort("step_id", 1))
    for log in logs:
        log["_id"] = str(log["_id"])
        log["session_id"] = str(log["session_id"])
    return logs