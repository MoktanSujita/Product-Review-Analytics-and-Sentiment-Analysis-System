from transformers import pipeline

classifier = pipeline('sentiment-analysis', 
                      model='nlptown/bert-base-multilingual-uncased-sentiment'
                    )

def map_label(label):
    stars = int(label.split()[0])
    if stars >= 4: return 'POSITIVE'
    if stars <= 2: return 'NEGATIVE'
    return 'NEUTRAL'

def analyze_sentiment(text):
    if not text or not text.strip():
        return {'label': 'NEUTRAL', 'score': 0.0}
    
    result = classifier(text[:512])[0]
    return {
        'label': map_label(result['label']),
        'score': round(result['score'],4)
    }

def analyze_sentiment_batch(reviews):
    valid_reviews = [r[:512] for r in reviews if r and r.strip()]
    if not valid_reviews:
        return []
    
    results = classifier(valid_reviews)
    return[
        {
            'label': map_label(r['label']),
            'score': round(r['score'],4)
        } for r in results ]