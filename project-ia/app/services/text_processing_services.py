from langchain_huggingface import HuggingFaceEmbeddings
from sentence_transformers import SentenceTransformer
from transformers import pipeline

model_embeddings = False

def text_tokenizer(message_content):
    
    global model_embeddings
    if(model_embeddings == False):
        HuggingFaceEmbeddings(model_name="sentence-transformers/paraphrase-multilingual-mpnet-base-v2")
        model_embeddings = SentenceTransformer('sentence-transformers/paraphrase-multilingual-mpnet-base-v2')
        
    sentence_embeddings = model_embeddings.encode(message_content)
    return sentence_embeddings 

def text_transfom_sentiment(message_content):
    pipe_sentiment = pipeline("text-classification", model="nlptown/bert-base-multilingual-uncased-sentiment")
    feeling = pipe_sentiment(message_content)
    return feeling