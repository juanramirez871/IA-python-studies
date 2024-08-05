from fastapi import APIRouter, Request
from pinecone import Pinecone
from langchain_pinecone import PineconeVectorStore
from langchain_openai import ChatOpenAI
from langchain.chains.question_answering import load_qa_chain
from langchain_huggingface import HuggingFaceEmbeddings
from app.services import pinecone_services
import os
import random
import requests

router = APIRouter()

@router.get("/search/info/{number_phone}/{query}")
async def get_conversation(number_phone, query, request: Request):
    
    index_name = os.getenv("INDEX_SENTIMENT_NAME")
    vectorstore = PineconeVectorStore(
        index_name=index_name,
        embedding=HuggingFaceEmbeddings(model_name="sentence-transformers/paraphrase-multilingual-mpnet-base-v2"),
        namespace=number_phone
        )
    llm = ChatOpenAI(model_name='gpt-3.5-turbo')
    chain = load_qa_chain(llm, chain_type="stuff")
    docs = vectorstore.similarity_search(query, 5)
    respuesta = chain.run(input_documents=docs, question=query)
    
    return {
        "messages": respuesta,
        "query": query,
        "number_phone": number_phone,
        "docs": docs
    }
    
@router.get("/all/numbers")
async def get_all_numbers(request: Request):
    url = f"https://waapi.app/api/v1/instances/{os.environ['ID_INSTANCE_WHATSAPP']}/client/action/get-contacts"
    headers = {
        "accept": "application/json",
        "authorization": "Bearer " + os.getenv("API_KEY_WHATSAPP")
    }
    response = requests.post(url, headers=headers)
    contacts = (response.json())['data']['data']
    data = []
    images = [
      "https://i.pinimg.com/736x/c3/9b/76/c39b7637c1c2069e44775383768c7d1f.jpg",
      "https://i.pinimg.com/564x/de/a3/25/dea325f568138dc0909fe0f5410e8e2b.jpg",
      "https://64.media.tumblr.com/9c07dffff53b9c429c338e19672b8b19/b6346d08680485d5-cc/s1280x1920/04e84f5019ef50abf5103c64a189855bdc6aff57.jpg",
      "https://i.pinimg.com/736x/c9/97/4f/c9974fd47769e4787aa84843d9bb510b.jpg",
      "https://i.pinimg.com/736x/66/58/25/665825d2af6224853083e111f2c00fc6.jpg",
      "https://i.pinimg.com/736x/71/c8/13/71c813deb4cd1dcbf22c473c68fe8398.jpg",
      "https://i.pinimg.com/736x/ae/fb/32/aefb32e7f7812102cf2e5756169b13db.jpg",
      "https://avatarfiles.alphacoders.com/322/322979.png",
      "https://avatarfiles.alphacoders.com/915/91501.jpg",
      "https://i.pinimg.com/236x/4b/eb/ae/4bebae19b406ab46c59f62f2c35f978a.jpg",
      "https://i.pinimg.com/originals/c6/e5/18/c6e518bc0ff173610f8eb4b4b929140a.png",
      "https://avatarfiles.alphacoders.com/182/182640.jpg",
      "https://i.pinimg.com/1200x/4d/08/85/4d0885341f054cb6f482997555a925a4.jpg",
      "https://pm1.aminoapps.com/6979/11bd68fd9afda48f101b2071fa0255893d0d4cc0r1-750-742v2_uhq.jpg",
      "https://i.pinimg.com/736x/c1/b7/4f/c1b74f94455ef3f263af5d6c250cf192.jpg",
      "https://pbs.twimg.com/media/F-abA_IaQAEP9yC.jpg",
      "https://i.pinimg.com/originals/19/85/27/1985270ce4fe87c73fed359f10529e7a.jpg"
    ];
    for contact in contacts:
        
        if contact['isUser'] == True and len(contact['number']) <= 12:
            random_image = images[random.randint(0, len(images) - 1)]
            data.append({
                "name": contact['name'] if 'name' in contact else contact['number'],
                "number": contact['number'],
                "image": random_image
            })

    return {
        "contacts": data
    }
    

@router.get("/conversation/{number_phone}")
async def get_conversation(number_phone, request: Request):
    
    pc = Pinecone()
    index = pc.Index(os.getenv("INDEX_SENTIMENT_NAME"))
    messages = pinecone_services.get_all_vectors_by_number(index, number_phone)
    
    return {
        "messages": messages,
        "number_phone": number_phone,
        "status": "success 🧙‍♂️"
    }