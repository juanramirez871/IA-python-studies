from fastapi import APIRouter, Request
from pinecone import Pinecone
from app.services import text_processing_services
from langchain_pinecone import PineconeVectorStore
from langchain_openai import ChatOpenAI
from langchain.chains.question_answering import load_qa_chain
from langchain_huggingface import HuggingFaceEmbeddings
import os

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
    docs = vectorstore.similarity_search(query, 10)
    respuesta = chain.run(input_documents=docs, question=query)
    
    return {
        "messages": respuesta,
        "query": query,
        "number_phone": number_phone,
        "docs": docs
    }