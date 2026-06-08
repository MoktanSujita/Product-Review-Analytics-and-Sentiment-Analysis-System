from transformers import pipeline

classifier = pipeline('sentiment-analysis', 
                      model='distilbert-base-uncased-finetuned-sst-2-english'
                    )
def analyze_sentiment(text):
    """
    analyze sentiment using Huggingface transformer.
    Returns:{
        'label':'POSITIVE' | 'NEGATIVE' | 'NEUTRAL',
        'score':float
    }
    """

    if not text or not text.strip():
        return{
            'label':'NEUTRAL',
            'score':0.0
        }
    result = classifier(text[:512])[0]

    return{
        'label':result['label'],
        'score':round(result['score'],4)
    }

def analyze_sentiment_batch(reviews):
    cleaned_reviews = [
        review[:512]
        for review in reviews
        if review and review.strip()
    ]
    return classifier(cleaned_reviews)