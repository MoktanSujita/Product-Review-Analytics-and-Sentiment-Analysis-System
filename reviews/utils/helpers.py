def get_sentiment_label(polarity):
    if polarity > 0.2: return "Positive"
    if polarity < -0.2: return "Negative"
    return "Neutral"

def get_overall_sentiment(counts):
    return max(counts, key=counts.get).replace('-',' ').title()