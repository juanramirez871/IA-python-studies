from fastapi import APIRouter, Request
from pinecone import Pinecone
from app.services import text_processing_services
from langchain_pinecone import PineconeVectorStore
from langchain_openai import ChatOpenAI
from langchain.chains.question_answering import load_qa_chain
from langchain_huggingface import HuggingFaceEmbeddings
import openai
import pandas as pd
import os

router = APIRouter()

@router.get("/preddict/message/{number_phone}/{prediccion}")
async def predict_message(number_phone, prediccion, request: Request):
    
    pc = Pinecone()
    index_name = os.getenv("INDEX_SENTIMENT_NAME")
    index = pc.Index(index_name)
    my_number = os.getenv("MY_NUMBER")
    
    data = index.query(
            vector=text_processing_services.text_tokenizer('').tolist(),
            top_k=20,
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
            
    print(f"Conversations: {conversations}")
    print('-'*100)
    df = pd.DataFrame(conversations)
    df['created_at'] = pd.to_datetime(df['created_at'], format='%d/%m/%Y %H:%M:%S')
    df_sorted = df.sort_values(by='created_at')
    
    context = []
    for _, row in df_sorted.iterrows():
        context.append(f"{row['from']}: {row['message']}, creado en {row['created_at']}, ")
    
    context = "\n".join(context)
    messages = []
    if prediccion == True:
        messages = [
            {"role": "system", "content": "Eres un modelo de IA que predice el siguiente mensaje en una conversación, sin importar que das tu mayor esfuerzo y das la mejor prediccion."},
            {"role": "user", "content": f"Predice el siguiente mensaje de esta conversación:\n{context}"}
        ]
    else:
        messages = [
            {"role": "system", "content": "Eres un modelo de IA, segun la conversacion dame consejos que responder, siempre das por lo minimo un consejo y hablas natural como un chico de 18 años."},
            {"role": "user", "content": f"yo soy {my_number}, dame consejos que responder segun:\n{context}"}
        ]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=100,
        temperature=0.7,
    )
    
    next_message = response['choices'][0]['message']['content']
    return {
            "message": next_message,
            "context": context
        }