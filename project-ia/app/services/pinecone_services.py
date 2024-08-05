from pinecone import ServerlessSpec
import time
import pandas as pd
import os

def create_index(index_name, pinecone):
    try:
        pinecone.describe_index(index_name)
    except:
        pinecone.create_index(
            index_name,
            dimension=768,
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
        ],
        namespace=metadata['from']
    )
    
    return upsert_response

def get_all_vectors_by_number(index, number_phone):
    
        my_number = my_number = os.getenv("MY_NUMBER")
        conversations = [] 
        response_1 = index.query(
            vector=[0] * 768,
            top_k=100,
            include_metadata=True,
            filter={
                'from': my_number,
                'to': number_phone
            },
            namespace=my_number,
            sort={"metadata.created_at": "desc"}
        )
        
        response_2 = index.query(
            vector=[0] * 768,
            top_k=100,
            include_metadata=True,
            namespace=number_phone,
            sort={"metadata.created_at": "desc"}
        )
        
        responses = response_1['matches'] + response_2['matches']
        unique_results = {match['id']: match for match in responses}.values()
        
        for match in unique_results:
            metadata = match['metadata']
            if (metadata['from'] == my_number and metadata['to'] == number_phone) or (metadata['from'] == number_phone and metadata['to'] == my_number):
                conversations.append({
                    "from": metadata['from'],
                    "to": metadata['to'],
                    "created_at": metadata['created_at'],
                    "message": metadata['text'],
                    "id": match['id']
                })

        df = pd.DataFrame(conversations)
        if df.empty:
            return []
        
        df['created_at'] = pd.to_datetime(df['created_at'], format='%d/%m/%Y %H:%M:%S')
        df_sorted = df.sort_values(by='created_at')
        messages = df_sorted.to_dict(orient='records')
        return messages
    
def get_lastest_vectors_by_number(index, number_phone, amount_vectors):
    
        all_ids = [id_vector for id_vector in index.list(namespace=number_phone)][0]
        vectors = index.fetch(ids=all_ids, namespace=number_phone)['vectors']
        conversations = []
        for id_vector in all_ids:
            metadata = vectors[id_vector]['metadata']
            conversations.append({
                "from": metadata['from'],
                "to": metadata['to'],
                "created_at": metadata['created_at'],
                "message": metadata['text'],
                "starts": metadata['starts'].split(' ')[0],
                "score": metadata['score']
            })
        
        last_message = conversations[-amount_vectors:]
        return last_message