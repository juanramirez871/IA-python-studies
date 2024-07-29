from transformers import AutoTokenizer, AutoModel

def text_vectorizer(message_content):
    tokenizer = AutoTokenizer.from_pretrained('sentence-transformers/all-MiniLM-L6-v2')
    model = AutoModel.from_pretrained('sentence-transformers/all-MiniLM-L6-v2')
    
    inputs = tokenizer(message_content, return_tensors='pt', padding=True, truncation=True, max_length=128)
    embeddings = model(**inputs).last_hidden_state.mean(dim=1).squeeze()
    vector_message = embeddings.detach().numpy()
    return vector_message