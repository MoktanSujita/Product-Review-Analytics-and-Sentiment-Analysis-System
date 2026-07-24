from django.shortcuts import render, redirect
import re
from collections import Counter

import plotly.graph_objects as go
from plotly.offline import plot
from .services.daraz_service import fetch_all_reviews
from .services.sentiment_service import analyze_sentiment_batch
from .utils.text_cleaner import clean_text
from .utils.helpers import get_overall_sentiment
from .utils.keyword_extractor import extract_key_phrases

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

        "top_positive_words": extract_key_phrases(
            [clean_text(r) for r in categorized_reviews["positive"]]
        ),

        "top_negative_words": extract_key_phrases   (
            [clean_text(r) for r in categorized_reviews["negative"]]
        ),

        "top_neutral_words": extract_key_phrases(
            [clean_text(r) for r in categorized_reviews["neutral"]]
        ),
        
        "recommendation": "Highly Recommended" if counts["positive"] >= 70 else "Recommended" if counts["positive"] >= 50 else "Buy with Caution",
    }

def compare_reviews(product_a, product_b):
    score_a = (
        (product_a["positive"]-product_a["negative"]/product_a["total_reviews"])*100
    )
    score_b = (
        (product_b["positive"]-product_b["negative"]/product_b["total_reviews"])*100
    )

    if score_a > score_b:
        winner = "Product A"
        verdict = "Product A is more positively reviewed."
        
    elif score_b > score_a:
        winner = "Product B"
        verdict = "Product B is more positively reviewed."
    else:
        winner = "Tie"
        verdict = "Both products have similar review sentiments."   

    return {
        "winner": winner,
        "verdict": verdict,
        "score_a": round(score_a, 2),
        "score_b": round(score_b, 2),
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

        if "a" in results and "b" in results:
            results["comparison"] = compare_reviews(
            results["a"],
            results["b"]
        )

        request.session["results"] = results

        return redirect("chart_page")

    return render(request, "index.html")


def chart_page(request):
    results = request.session.get("results", {})

    comparison_chart = None

    if "a" in results and "b" in results:
        fig = go.Figure()

        fig.add_trace(go.Bar(
            x=["Product A", "Product B"],
            y=[
                results["a"]["positive_percentage"],
                results["b"]["positive_percentage"]
            ],
            marker_color='green',
            width=0.1,
        ))

        fig.update_layout(
            height=420,
            margin=dict(l=20,r=20,t=20,b=20),

        paper_bgcolor='rgba(0,0,0,0)',

        plot_bgcolor='rgba(0,0,0,0)',

        xaxis_title="",

        yaxis_title="Positive Reviews (%)",

        font=dict(size=15),

        showlegend=False
    )

    comparison_chart = plot(
        fig,
        output_type="div",
        include_plotlyjs=False
    )
        

    return render(
        request,
        "dashboard.html",
        {
            "results": results,
            "comparison_chart": comparison_chart,
        }
    )