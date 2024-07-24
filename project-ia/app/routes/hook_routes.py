from fastapi import APIRouter, HTTPException, Request
from app.services import event_message_services
import os

security_tokens = { 16174: os.environ['API_KEY_WHATSAPP'] }
router = APIRouter()


@router.post("/webhooks/whatsapp/{security_token}")
async def whatsapp_webhook(security_token, request: Request):
    
    body = await request.json()
    instance_id = body.get("instanceId")
    event_name = body.get("event")
    event_data = body.get("data")

    if security_token is None or instance_id is None or event_name is None or event_data is None:
        print("Invalid request ❗❗❗")
        raise HTTPException(status_code=400, detail="Invalid request")

    if event_name == "message_create":
        response = event_message_services.message_create(event_data)
        return response
