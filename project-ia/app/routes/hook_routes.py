from fastapi import APIRouter, HTTPException, Request
from app.services import event_message_services, text_processing_services, pinecone_services
from pinecone import Pinecone
import os

security_tokens = { 16728: os.environ['API_KEY_WHATSAPP'] }
router = APIRouter()


@router.post("/webhooks/whatsapp/{security_token}")
async def whatsapp_webhook(security_token, request: Request):
    
    body = await request.json()
    instance_id = body.get("instanceId")
    event_name = body.get("event")
    event_data = body.get("data")
    pc = Pinecone()

    if security_token is None or instance_id is None or event_name is None or event_data is None:
        print("Invalid request ❗❗❗")
        raise HTTPException(status_code=400, detail="Invalid request")

    if event_name == "message_create":
        data_message = event_message_services.message_create(event_data)
        pinecone_services.create_index(os.getenv("INDEX_WHATSAPP_NAME"), pc)
        vector_tokenized = text_processing_services.text_tokenizer(data_message['message_content'])
        index = pc.Index(os.getenv("INDEX_WHATSAPP_NAME"))
        metadata = {
            "to": data_message['message_to'],
            "from": data_message['message_from'],
            "created_at": data_message['message_created_at'],
            "message": data_message['message_content']
        }
        pinecone_services.insert_vector(index, vector_tokenized, metadata)
        
    print("Webhook received successfully ✅✅✅")
    return {"status": "success", "message": "Webhook received successfully"}
