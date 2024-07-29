from fastapi import HTTPException
from datetime import datetime

def message_create(event_data):
    
    message_data = event_data.get("message")
    if not message_data:
        return {"status": "error", "message": "Invalid message data ❗❗❗"}

    message_type = message_data.get("type")
    if message_type == "chat":
        
        timestamp = message_data.get("timestamp")
        date_created = datetime.fromtimestamp(timestamp)
        message_created_at = date_created.strftime("%d/%m/%Y %H:%M:%S")
        message_content = message_data.get("body")
        message_from = message_data.get("from", "").replace("@c.us", "")
        message_to = message_data.get("to", "").replace("@c.us", "")
        
        return {
            "message_from": message_from,
            "message_to": message_to,
            "message_created_at": message_created_at,
            "message_content": message_content
        }