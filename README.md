# Product Review Sentiment Analyzer

## Overview
The **Product Review Sentiment Analyzer** is a Django-based web application that performs sentiment analysis on product reviews.

Users can:
- Enter a **manual review**, or
- Provide a **Daraz product URL** to analyze all available reviews

The system processes the input using NLP techniques and generates insights such as sentiment distribution, key terms, and overall product perception.

---

## Features

- Manual review sentiment analysis  
- Daraz product review scraping  
- Sentiment classification (Positive, Negative, Neutral)  
- Sentiment distribution with percentages  
- Top words extraction per sentiment  
- Sample review display  
- Data storage using Django models  
- Chart-ready output (Chart.js compatible)

---

## Tech Stack

**Backend**
- Django
- Python

**NLP & AI**
- Hugging Face `transformers` (DistilBERT)
- TensorFlow (Backend for Hugging Face Transformers)

**Frontend**
- HTML, CSS, JavaScript (Chart.js)
- **Bootstrap** (Grid & Components)
- **Custom CSS** (Styling & Theming)

**Other Tools**
- Requests

---

## Project Structure

```
product_analyzer/
├── reviews/
│   ├── services/           # Business logic layer
│   │   ├── analytics_service.py
│   │   ├── daraz_service.py
│   │   ├── scraper_service.py
│   │   └── sentiment_service.py
│   ├── utils/              # Helpers and text cleaning
│   │   ├── helpers.py
│   │   └── text_cleaner.py
│   └── views.py
├── templates/
├── manage.py
├── requirements.txt
```

---

## Installation

### 1. Clone Repository
```bash
git clone https://github.com/MoktanSujita/Product-Review-Analytics-and-Sentiment-Analysis-System.git
cd product_analyzer
```

### 2. Create Virtual Environment
```bash
python -m venv .venv
```

Activate environment:
```bash
# Linux / Mac
source .venv/bin/activate

# Windows
.venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Download NLP Resources
```bash
python -m textblob.download_corpora
```

### 5. Apply Migrations
```bash
python manage.py migrate
```

### 6. Run Server
```bash
python manage.py runserver
```

---

## Usage

### Manual Review
- Enter text in the input field
- Submit to get:
  - Sentiment label
  - Polarity score

---

### URL-Based Analysis
Paste a Daraz product URL:
```
https://www.daraz.com.np/products/...
```

The system will:
- Extract product ID
- Fetch reviews
- Analyze sentiments

---

## How It Works

### 1. Input Detection
- Text → Direct analysis  
- URL → Scraping + batch processing  

### 2. Review Extraction
- Extracts `itemId` using regex  
- Calls Daraz API:
```
/pdp/review/getReviewList
```

### 3. Sentiment Analysis
The system uses a pre-trained **DistilBERT** model from Hugging Face to perform pre-trained DistilBERT-based sentiment classifier (Hugging Face Transformers)

```python
from transformers import pipeline

# Initialize the pipeline
classifier = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

def analyze_sentiment(text):
    result = classifier(text)
    return result

```

## Example Output

```
Total Reviews: 120
Positive: 70 (58.3%)
Negative: 30 (25%)
Overall Sentiment: Positive

Neutral sentiment is derived using a confidence threshold on model output scores.
```

---


## Limitations

- **Scraping Reliability:** The project relies on direct requests to Daraz, which may be subject to rate-limiting or changes in their site structure.
- **Resource Intensity:** Transformer models (DistilBERT) are more resource-intensive than rule-based models and require sufficient RAM/CPU for real-time processing.
- **Language Support:** Currently optimized for English-based sentiments, with future plans for localized language models.
- **Noisy real-world data:** Daraz reviews often include mixed English and Romanized Nepali text, which affects sentiment consistency.

## Future Improvements

- **Caching:** Implement Redis or Django caching to store results for frequently searched products.
- **Async Scraping:** Use `Celery` or `asyncio` to handle scraping in the background to avoid blocking the user experience.
- **UI/UX:** Further visual enhancements for the dashboard.

## Model Evolution
-Started with TextBlob for baseline sentiment scoring
-Moved to transformer-based DistilBERT for improved contextual understanding
-Current focus is on improving robustness for real-world noisy review data
