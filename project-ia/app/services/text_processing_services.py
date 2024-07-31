from transformers import pipeline
from sentence_transformers import SentenceTransformer

model_sentence = None

def text_tokenizer(message_content):
    
    global model_sentence
    if model_sentence is None:
        print("Loading model 🤖")
        model_sentence = SentenceTransformer("sentence-transformers/paraphrase-multilingual-mpnet-base-v2")
        
    sentence_embeddings = model_sentence.encode(message_content)
    return sentence_embeddings  

def text_transfom_sentiment(message_content):
    pipe_sentiment = pipeline("text-classification", model="nlptown/bert-base-multilingual-uncased-sentiment")
    feeling = pipe_sentiment(message_content)
    return feeling