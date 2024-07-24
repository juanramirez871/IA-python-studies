from fastapi import FastAPI, HTTPException, Request
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()
app = FastAPI()
port = 3000

security_tokens = {
    16174: os.environ['API_KEY_WHATSAPP'],
}


@app.get("/")
def read_root():
    return {
            "title": "My first IA project 🧠",
            "description": "i dont know what to do 🧐",
            "author": "Juan 🧙‍♂️",
            "server": f"Server is running on port {port} 🤖"
            }

@app.post("/webhooks/whatsapp/{security_token}")
async def whatsapp_webhook(security_token, request: Request):
    
    print("🚀🚀🚀 New message 🚀🚀🚀")
    body = await request.json()
    instance_id = body.get("instanceId")
    event_name = body.get("event")
    event_data = body.get("data")

    if security_token is None or instance_id is None or event_name is None or event_data is None:
        print("Invalid request ❗❗❗")
        raise HTTPException(status_code=400, detail="Invalid request")

    if event_name == "message_create":
        
        message_data = event_data.get("message")
        if not message_data:
            raise HTTPException(status_code=400, detail="Invalid request")

        message_type = message_data.get("type")
        if message_type == "chat":
            
            timestamp = message_data.get("timestamp")
            date_created = datetime.fromtimestamp(timestamp)
            message_created_at = date_created.strftime("%d/%m/%Y %H:%M:%S")
            message_content = message_data.get("body")
            message_from = message_data.get("from", "").replace("@c.us", "")
            message_to = message_data.get("to", "").replace("@c.us", "")
            author = message_data.get("author")

            print("-----------------------------------")
            print(f"Message created at: {message_created_at}")
            print(f"Message content: {message_content}")
            print(f"Message to: {message_to}")
            print(f"Message from: {message_from}")
            print(f"Author: {author}")
            print("-----------------------------------")

        return {"status": "success"}

    else:
        raise HTTPException(status_code=404, detail=f"Cannot handle this event: {event_name}")

if __name__ == "__main__":
    import uvicorn
    print(f"Server is running on port {port} 🤖")
    uvicorn.run(app, host="0.0.0.0", port=port)
