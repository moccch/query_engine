from transformers import BertTokenizer, T5Tokenizer
from transformers import pipeline

ner_tokenizer_name = "dbmdz/bert-large-cased-finetuned-conll03-english"
ner_tokenizer = BertTokenizer.from_pretrained(ner_tokenizer_name, model_max_length=512)

summarizer_tokenizer_name = "t5-base"
summarizer_tokenizer = T5Tokenizer.from_pretrained(summarizer_tokenizer_name, model_max_length=512)


ner = pipeline("ner", model="dbmdz/bert-large-cased-finetuned-conll03-english", tokenizer=ner_tokenizer)
summarizer = pipeline("summarization", model="t5-base", tokenizer=summarizer_tokenizer)


def summarizer_model(id, text):
    text = summarizer(text)
    text = text[0]['summary_text']
    return (id, text)



def ner_model(id, sentence):
    entities = []
    results = ner(sentence)
    for res in results:
        entities.append((id, res['word'],res['entity']))
    return entities
