from transformers import pipeline
from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer, MarianMTModel

model_sentence = None

def text_tokenizer(message_content):
    
    global model_sentence
    if model_sentence is None:
        model_sentence = SentenceTransformer("sentence-transformers/paraphrase-multilingual-mpnet-base-v2")
        
    sentence_embeddings = model_sentence.encode(message_content)
    return sentence_embeddings  

def text_transfom_sentiment(message_content):
    model_name = f"Helsinki-NLP/opus-mt-es-en"
    model = MarianMTModel.from_pretrained(model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    batch = tokenizer([message_content], return_tensors="pt")

    generated_ids = model.generate(**batch)
    translate = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
    print(translate)
    
    model_path = "cardiffnlp/twitter-xlm-roberta-base-sentiment"
    sentiment_task = pipeline("sentiment-analysis", model=model_path, tokenizer=model_path)    
    feeling = sentiment_task(translate)
    return feeling