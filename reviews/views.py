from django.shortcuts import render, redirect
import re
from .services.daraz_service import fetch_all_reviews
from .services.daraz_service import analyze_sentiment_batch
from .utils.text_cleaner import clean_text
from .utils.helpers import get_overall_sentiment

# MAIN VIEW
def perform_analysis(product_url):
    match = re.search(r'i(\d+)', product_url)
    if not match: return {"error": "Invalid Daraz URL"}

    reviews = fetch_all_reviews(match.group(1))
    if not reviews: return {"error": "No reviews found"}

    sentiments = analyze_sentiment_batch(reviews)
    counts = {"positive": 0, "negative": 0, "neutral": 0}
    lists = {"positive": [], "negative": [], "neutral": []}

    for i, sentiment in enumerate(sentiments):
        label = sentiment['label'].lower()
        counts[label] += 1
        lists[label].append(reviews[i])

    total = len(reviews)

    return {
        "total_reviews": total,
        "positive": counts["positive"],
        "negative": counts["negative"],
        "neutral": counts["neutral"],
        "positive_percentage": round((counts["positive"] / total) * 100, 2),
        "negative_percentage": round((counts["negative"] / total) * 100, 2),
        "neutral_percentage": round((counts["neutral"] / total) * 100, 2),
        "overall": get_overall_sentiment(counts),
        "top_positive_words": get_top_words([clean_text(r) for r in lists["positive"]]),
        "top_negative_words": get_top_words([clean_text(r) for r in lists["negative"]]),
        "top_neutral_words": get_top_words([clean_text(r) for r in lists["neutral"]]),
    }
    
    def analyze_revie(request):
        if request.method == 'POST':
            url_a = request.POST.get("url_a")
            url_b = request.POST.get("url_b")

            results = {}
            if url_a: results['a'] = perform_analysis(url_a)
        if url_b: results['b'] = perform_analysis(url_b)

        request.session["results"] = results
        return redirect("chart_page")

    return render(request, "reviews_list.html")

# Keep only specialized logic here, or move it to helpers too!
def get_top_words(cleaned_review_list):
    from collections import Counter
    words = []
    for review in cleaned_review_list:
        words.extend(review.split())
    # Filter out your stop_words list here
    return Counter(words).most_common(3)
