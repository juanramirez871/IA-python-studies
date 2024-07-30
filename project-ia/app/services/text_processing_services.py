from langchain_huggingface import HuggingFaceEmbeddings
from sentence_transformers import SentenceTransformer

def text_tokenizer(message_content):
    HuggingFaceEmbeddings(model_name="sentence-transformers/paraphrase-multilingual-mpnet-base-v2")
    model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-mpnet-base-v2')
    sentence_embeddings = model.encode(message_content)
    return sentence_embeddings 