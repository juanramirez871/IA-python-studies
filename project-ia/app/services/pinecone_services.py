from pinecone import ServerlessSpec
import time

def create_index(index_name, pinecone):
    try:
        pinecone.describe_index(index_name)
    except:
        pinecone.create_index(
            index_name,
            dimension=384,
            metric='cosine',
            spec=ServerlessSpec(
                cloud='aws', 
                region='us-east-1'
            ) 
        )
        
def insert_vector(index, vector, metadata):
    upsert_response = index.upsert(
        vectors=[
            {
                'id': str(time.time() * 1000),
                'values': vector.tolist(),
                'metadata': metadata
            }
        ]
    )
    
    return upsert_response