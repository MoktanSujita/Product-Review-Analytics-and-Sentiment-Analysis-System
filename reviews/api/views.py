from django.shortcuts import render, redirect
from transformers import pipeline
from collections import Counter
import re
from ..models import Review
from ..services.scraper_service import fetch_all_reviews


# MAIN VIEW
def analyze_sentiment(text):
    if not text or not text.strip():
        return{
            'label':'NETURAL'
        }
