import asyncio
import websockets
import os
import pandas as pd
import json
from dotenv import load_dotenv
from pinecone import Pinecone

load_dotenv()
port_ws = 8765

async def get_all_vectors_by_number(index, number_phone):
    
        my_number = my_number = os.getenv("MY_NUMBER")
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
        conversations = []
        
        for match in unique_results:
            metadata = match['metadata']
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
        messages = await get_all_vectors_by_number(index, number)
        
        await websocket.send(messages)
        await asyncio.sleep(0.5)        


server_socket = websockets.serve(websocket_conversation, "localhost", port_ws)
asyncio.get_event_loop().run_until_complete(server_socket)
asyncio.get_event_loop().run_forever()