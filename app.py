import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from gtts import gTTS
import os

# Download NLTK dependencies
nltk.download("vader_lexicon")

# API Key for NewsAPI 
API_KEY = "5c41f82230c0433aa16229c857b261df"

# Function to fetch news articles
def get_news(company_name):
    url = f"https://newsapi.org/v2/everything?q={company_name}&language=en&sortBy=publishedAt&apiKey={API_KEY}"
    response = requests.get(url)

    if response.status_code != 200:
        st.error("⚠️ Failed to fetch news. Check your API key or try another company.")
        return []

    data = response.json()
    return [{"title": item["title"], "link": item["url"]} for item in data.get("articles", [])[:10]]

# Function to perform sentiment analysis
def analyze_sentiment(news_articles):
    sia = SentimentIntensityAnalyzer()
    sentiment_counts = {"Positive": 0, "Negative": 0, "Neutral": 0}
    sentiment_data = []

    for article in news_articles:
        sentiment_score = sia.polarity_scores(article["title"])["compound"]
        
        if sentiment_score >= 0.05:
            sentiment = "Positive"
        elif sentiment_score <= -0.05:
            sentiment = "Negative"
        else:
            sentiment = "Neutral"

        article["sentiment"] = sentiment
        sentiment_counts[sentiment] += 1  
        
        # Store sentiment score for analysis
        sentiment_data.append({"Title": article["title"], "Sentiment": sentiment, "Score": sentiment_score})

    return sentiment_counts, news_articles, pd.DataFrame(sentiment_data)

# Function to generate Hindi text-to-speech
def generate_hindi_tts(summary_text):
    tts = gTTS(text=summary_text, lang="hi")
    tts_file = "sentiment_summary.mp3"
    tts.save(tts_file)
    return tts_file

# Function to display comparative sentiment analysis
def display_sentiment_comparison(df):
    st.subheader("📊 Comparative Sentiment Analysis")

    # Grouping by sentiment to count occurrences
    sentiment_counts = df["Sentiment"].value_counts()

    # Display bar chart
    fig, ax = plt.subplots()
    ax.bar(sentiment_counts.index, sentiment_counts.values, color=["green", "red", "blue"])
    ax.set_xlabel("Sentiment")
    ax.set_ylabel("Number of Articles")
    ax.set_title("Sentiment Comparison Across Articles")
    st.pyplot(fig)

    # Display sentiment summary
    st.write(f"🔹 **Total Articles Analyzed**: {len(df)}")
    st.write(f"✅ **Positive Articles**: {sentiment_counts.get('Positive', 0)}")
    st.write(f"⚠️ **Negative Articles**: {sentiment_counts.get('Negative', 0)}")
    st.write(f"➖ **Neutral Articles**: {sentiment_counts.get('Neutral', 0)}")

# Streamlit UI
st.title("📰 News Sentiment Analyzer with Hindi TTS 🔊")
st.write("Enter a company name to analyze its recent news sentiment and generate a Hindi audio summary.")

# Input for company name
company = st.text_input("🔎 Enter Company Name", "")

# Analyze button
if st.button("Analyze"):
    if company:
        news_articles = get_news(company)

        if not news_articles:
            st.warning("⚠️ No news articles found. Try another company.")
        else:
            sentiment_counts, analyzed_articles, sentiment_df = analyze_sentiment(news_articles)

            # Display individual articles with sentiment
            st.subheader("📰 Latest News Articles & Sentiment")
            for article in analyzed_articles:
                st.write(f"**{article['title']}** - {article['sentiment']}")
                st.markdown(f"[Read more]({article['link']})")

            # Display Comparative Sentiment Analysis
            display_sentiment_comparison(sentiment_df)

            # Generate Hindi TTS Summary
            st.subheader("🔊 Hindi Audio Summary")
            summary_text = f"{company} के लिए समाचार विश्लेषण:\n" \
                        f"सकारात्मक समाचार: {sentiment_counts['Positive']}\n" \
                        f"नकारात्मक समाचार: {sentiment_counts['Negative']}\n" \
                        f"तटस्थ समाचार: {sentiment_counts['Neutral']}"

            tts_file = generate_hindi_tts(summary_text)
            st.audio(tts_file, format="audio/mp3")

    else:
        st.warning("⚠️ Please enter a company name.")
