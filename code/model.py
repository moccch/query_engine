from transformers import pipeline

# Create a NER pipeline using the "distilbert-base-cased" model
ner_pipeline = pipeline("ner", model="dbmdz/bert-large-cased-finetuned-conll03-english", tokenizer="dbmdz/bert-large-cased-finetuned-conll03-english")

# # # Input text
# text = "John Doe is a software engineer at Google in Mountain View, California."

# # # Perform NER
# entities = ner_pipeline(text)

# # Display the recognized named entities
# print(entities)
# for entity in entities:
#     print(f"{entity['word']}: {entity['entity']} ({entity['score']:.4f})")



def model(id, sentence):
    entities = []
    results = ner_pipeline(sentence)
    for res in results:
        entities.append((id, res['word'],res['entity']))
    return entities

