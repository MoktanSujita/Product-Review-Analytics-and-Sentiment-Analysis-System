import spacy
from collections import Counter

nlp = spacy.load("en_core_web_sm")

def extract_key_phrases(reviews, top_n = 5):
    phrases = []

    for review in reviews:
        doc = nlp(review)

        for chunk in doc.noun_chunks:
            text = chunk.text.lower().strip()

            if len(text) > 2:
                phrases.append(text)

    return Counter(phrases).most_common(top_n)