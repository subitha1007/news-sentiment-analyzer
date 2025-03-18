import requests
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk
import matplotlib.pyplot as plt
from collections import Counter

nltk.download("vader_lexicon")

API_KEY = "5c41f82230c0433aa16229c857b261df"  # Replace with your valid API key

def get_news(company_name):
    url = f"https://newsapi.org/v2/everything?q={company_name}&language=en&sortBy=publishedAt&apiKey={API_KEY}"
    response = requests.get(url)

    if response.status_code != 200:
        print("Failed to fetch news")
        return []

    data = response.json()
    return [{"title": item["title"], "link": item["url"]} for item in data.get("articles", [])[:10]]

def analyze_sentiment(news_articles):
    sia = SentimentIntensityAnalyzer()
    sentiment_counts = {"Positive": 0, "Negative": 0, "Neutral": 0}

    for article in news_articles:
        sentiment_score = sia.polarity_scores(article["title"])["compound"]
        if sentiment_score >= 0.05:
            sentiment = "Positive"
        elif sentiment_score <= -0.05:
            sentiment = "Negative"
        else:
            sentiment = "Neutral"
        
        article["sentiment"] = sentiment
        sentiment_counts[sentiment] += 1  # Count sentiment types

    return sentiment_counts

def plot_sentiment_distribution(sentiment_counts, company_name):
    labels = sentiment_counts.keys()
    sizes = sentiment_counts.values()
    colors = ["green", "red", "blue"]

    plt.figure(figsize=(6, 4))
    plt.bar(labels, sizes, color=colors)
    plt.xlabel("Sentiment")
    plt.ylabel("Number of Articles")
    plt.title(f"Sentiment Analysis for {company_name}")
    plt.show()

from gtts import gTTS
import os

def generate_hindi_tts(summary_text):
    tts = gTTS(text=summary_text, lang="hi")
    tts.save("sentiment_summary.mp3")
    print("\n🎤 Hindi audio summary saved as 'sentiment_summary.mp3'. Playing now...\n")
    os.system("start sentiment_summary.mp3")  # Opens the audio file (Windows)


if __name__ == "__main__":
    company = input("Enter company name: ")
    news_articles = get_news(company)

    if not news_articles:
        print("No news articles found. Try another company.")
    else:
        sentiment_counts = analyze_sentiment(news_articles)
        
        # Print Sentiment Results
        for i, article in enumerate(news_articles, 1):
            print(f"{i}. {article['title']} ({article['link']}) - Sentiment: {article['sentiment']}")

        # Show Comparative Sentiment Analysis
        print("\nSentiment Distribution:")
        print(sentiment_counts)

        # Plot a bar chart for sentiment distribution
        plot_sentiment_distribution(sentiment_counts, company)

        summary_text = f"{company} के लिए समाचार विश्लेषण:\n" \
                       f"सकारात्मक समाचार: {sentiment_counts['Positive']}\n" \
                       f"नकारात्मक समाचार: {sentiment_counts['Negative']}\n" \
                       f"तटस्थ समाचार: {sentiment_counts['Neutral']}"
        
        generate_hindi_tts(summary_text)