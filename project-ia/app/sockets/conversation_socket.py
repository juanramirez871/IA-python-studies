import asyncio
import websockets
import os
import pandas as pd
import json
from dotenv import load_dotenv
from pinecone import Pinecone

load_dotenv()
port_ws = 8765

def get_all_vectors_by_number(index, number_phone):
    
        my_number = my_number = os.getenv("MY_NUMBER")
        ids_from = [id_vector for id_vector in index.list(namespace=number_phone)][0][-5:]
        ids_to = [id_vector for id_vector in index.list(namespace=my_number)][0][-5:]
        
        vectors_from = index.fetch(ids=ids_from, namespace=number_phone)['vectors']
        vectors_to = index.fetch(ids=ids_to, namespace=my_number)['vectors']
        vectors = {**vectors_from, **vectors_to}
        conversations = []
        
        for id_vector, vector_data in vectors.items():
            metadata = vector_data['metadata']
            if (metadata['from'] == my_number and metadata['to'] == number_phone) or (metadata['from'] == number_phone and metadata['to'] == my_number):
                conversations.append({
                    "from": metadata['from'],
                    "to": metadata['to'],
                    "created_at": metadata['created_at'],
                    "message": metadata['text']
                })

        df = pd.DataFrame(conversations)
        df['created_at'] = pd.to_datetime(df['created_at'], format='%d/%m/%Y %H:%M:%S')
        df_sorted = df.sort_values(by='created_at')
        last_five_messages = df_sorted.tail(5)
        messages = last_five_messages.to_json(orient='records')
        return messages

async def websocket_conversation(websocket, path):
    
    number = await websocket.recv()
    print(f"Received (server) {number}")
    while True:
        pc = Pinecone()
        index = pc.Index(os.getenv("INDEX_SENTIMENT_NAME"))
        messages = get_all_vectors_by_number(index, number)
        
        await websocket.send(messages)
        await asyncio.sleep(5)        


server_socket = websockets.serve(websocket_conversation, "localhost", port_ws)
asyncio.get_event_loop().run_until_complete(server_socket)
asyncio.get_event_loop().run_forever()