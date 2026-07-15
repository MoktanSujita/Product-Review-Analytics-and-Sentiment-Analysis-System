from django.shortcuts import render, redirect
import re
from collections import Counter

from .services.daraz_service import fetch_all_reviews
from .services.sentiment_service import analyze_sentiment_batch
from .utils.text_cleaner import clean_text
from .utils.helpers import get_overall_sentiment


def get_top_words(cleaned_review_list):
    words = []

    for review in cleaned_review_list:
        words.extend(review.split())

    # Add stop-word filtering here if desired
    return Counter(words).most_common(3)


def perform_analysis(product_url):
    match = re.search(r"i(\d+)", product_url)

    if not match:
        return {"error": "Invalid Daraz URL"}

    product_id = match.group(1)

    reviews = fetch_all_reviews(product_id)

    if not reviews:
        return {"error": "No reviews found"}

    sentiments = analyze_sentiment_batch(reviews)

    counts = {
        "positive": 0,
        "negative": 0,
        "neutral": 0,
    }

    categorized_reviews = {
        "positive": [],
        "negative": [],
        "neutral": [],
    }

    for review, sentiment in zip(reviews, sentiments):
        label = sentiment["label"].lower()

        if label not in counts:
            label = "neutral"

        counts[label] += 1
        categorized_reviews[label].append(review)

    total = len(reviews)

    return {
        "total_reviews": total,
        "positive": counts["positive"],
        "negative": counts["negative"],
        "neutral": counts["neutral"],

        "positive_percentage": round(counts["positive"] / total * 100, 2),
        "negative_percentage": round(counts["negative"] / total * 100, 2),
        "neutral_percentage": round(counts["neutral"] / total * 100, 2),

        "overall": get_overall_sentiment(counts),

        "top_positive_words": get_top_words(
            [clean_text(r) for r in categorized_reviews["positive"]]
        ),

        "top_negative_words": get_top_words(
            [clean_text(r) for r in categorized_reviews["negative"]]
        ),

        "top_neutral_words": get_top_words(
            [clean_text(r) for r in categorized_reviews["neutral"]]
        ),
    }


def analyze_review(request):
    if request.method == "POST":

        url_a = request.POST.get("url_a")
        url_b = request.POST.get("url_b")

        results = {}

        if url_a:
            results["a"] = perform_analysis(url_a)

        if url_b:
            results["b"] = perform_analysis(url_b)

        request.session["results"] = results

        return redirect("chart_page")

    return render(request, "reviews_list.html")


def chart_page(request):
    results = request.session.get("results", {})

    return render(
        request,
        "chart.html",
        {
            "results": results,
        },
    )