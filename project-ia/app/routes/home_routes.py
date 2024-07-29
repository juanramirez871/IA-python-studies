from fastapi import APIRouter
from pinecone import Pinecone, ServerlessSpec
from transformers import AutoTokenizer, AutoModel
import time

router = APIRouter()

@router.get("/")
def read_root():
    return {
            "title": "My first IA project 🧠",
            "description": "i dont know what to do 🧐",
            "author": "Juan 🧙‍♂️",
            "server": f"Server is running done 🤖"
            }
    
@router.get("/test")
def test():
    
    pc = Pinecone()
    indexes = (pc.list_indexes()).indexes
    
    ## example data (test)
    message_created_at = "11/02/2024 07:02:01"
    message_content = "what's up my lover, i miss you so much"
    message_from = "juan"
    message_to = "silvia"
    
    
    ## create index
    try:
        pc.describe_index(message_from)
    except:
        pc.create_index(
            message_from,
            dimension=384,
            metric='cosine',
            spec=ServerlessSpec(
                cloud='aws', 
                region='us-east-1'
            ) 
        )
        
    
    ## Tokenizer message
    tokenizer = AutoTokenizer.from_pretrained('sentence-transformers/all-MiniLM-L6-v2')
    model = AutoModel.from_pretrained('sentence-transformers/all-MiniLM-L6-v2')
    
    inputs = tokenizer(message_content, return_tensors='pt', padding=True, truncation=True, max_length=128)
    embeddings = model(**inputs).last_hidden_state.mean(dim=1).squeeze()
    vector_message = embeddings.detach().numpy()
    

    ## Insert message to index
    index = pc.Index(message_from)    
    upsert_response = index.upsert(
        vectors=[
            {
                'id': str(time.time() * 1000),
                'values': vector_message.tolist(),
                'metadata': {
                    'to': message_to,
                    'created_at': message_created_at
                }
            }
        ]
    )
    
    
    return "Test done 🧙‍♂️"