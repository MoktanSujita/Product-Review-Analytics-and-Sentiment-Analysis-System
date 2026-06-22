import re

def clean_text(text):
    if not text:
        return ""
    
    #remove special characters, URLs, and extra whitespaces
    text = re.sub(r'http\S+', '', text)
    text = re.sub(r'[^\w\s]', '', text) #keep only words/spaces
    return text.lower().strip()

def remove_stop_words(text, stop_words):
    words = text.split()
    return [w for w in words if w not in stop_words]