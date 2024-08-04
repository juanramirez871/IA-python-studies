from fastapi import APIRouter, Request
from pinecone import Pinecone
from app.services import text_processing_services
import openai
import pandas as pd
from openai import OpenAI
import os

router = APIRouter()

@router.get("/preddict/message/{number_phone}/type/{typeQuery}")
async def predict_message(number_phone, typeQuery, request: Request):
    
    pc = Pinecone()
    index_name = os.getenv("INDEX_SENTIMENT_NAME")
    index = pc.Index(index_name)
    my_number = os.getenv("MY_NUMBER")
    
    data = index.query(
            vector=text_processing_services.text_tokenizer('').tolist(),
            top_k=30,
            include_metadata=True,
            namespace=number_phone
        )
    messages = data['matches']
    conversations  = []
    
    for message in messages:
        metadata = message.get('metadata', {})
        if metadata:
            conversations .append({
                "from": metadata.get("from"),
                "to": metadata.get("to"),
                "created_at": metadata.get("created_at"),
                "message": metadata.get("text")
            })
            
    df = pd.DataFrame(conversations)
    df['created_at'] = pd.to_datetime(df['created_at'], format='%d/%m/%Y %H:%M:%S')
    df_sorted = df.sort_values(by='created_at')
    
    context = []
    for _, row in df_sorted.iterrows():
        context.append(f"{row['from']}: {row['message']}, creado en {row['created_at']}, ")
    
    context = "\n".join(context)
    messages = []
    temperatura = 0
    if typeQuery == 'predict':
        print("prediccion")
        temperatura = 0.2
        messages = [
            {"role": "system", "content": "Eres un modelo de IA que predice el siguiente mensaje en una conversación, siempre das una prediccion del proximo mensaje, siempre lo haces sin importar nada."},
            {"role": "user", "content": f"Predice el siguiente mensaje de esta conversación:\n{context}"}
        ]
    else:
        print("consejo")
        temperatura = 0.5
        messages = [
            {"role": "system", "content": "Eres un modelo de IA, segun la conversacion dame consejos que responder, siempre das por lo minimo un consejo y hablas natural como un chico de 18 años."},
            {"role": "user", "content": f"en la conversacion mis mensajes son el numero {my_number} y de la otra persona es el de {number_phone}, dame consejos que responder segun:\n{context}"}
        ]
        
    client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY"),
    )
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=100,
        temperature=temperatura,
    )
    
    next_message = response.choices[0].message.content
    return {
            "message": next_message,
            "context": context
        }