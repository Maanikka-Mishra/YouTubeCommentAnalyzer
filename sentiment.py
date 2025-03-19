import os
import nltk
import pandas as pd
import matplotlib.pyplot as plt
from nltk.sentiment import SentimentIntensityAnalyzer

# Download VADER lexicon (only needed once)
nltk.download('vader_lexicon')

# Initialize Sentiment Analyzer
sia = SentimentIntensityAnalyzer()

def analyze_sentiment(comments):
    """Analyze sentiment of YouTube comments and return a summary and detailed results."""
    sentiment_results = {"Positive": 0, "Neutral": 0, "Negative": 0}
    detailed_results = []

    for comment in comments:
        score = sia.polarity_scores(comment)['compound']
        sentiment = "Neutral"

        if score >= 0.05:
            sentiment = "Positive"
            sentiment_results["Positive"] += 1
        elif score <= -0.05:
            sentiment = "Negative"
            sentiment_results["Negative"] += 1
        else:
            sentiment_results["Neutral"] += 1

        # Ensure proper dictionary format for CSV
        detailed_results.append({"Comment": comment, "Sentiment": sentiment, "Score": score})

    return sentiment_results, detailed_results

def save_results_to_csv(results, filename="static/sentiment_results.csv"):
    """Save sentiment analysis results to a CSV file inside 'static' for Flask access."""
    
    # Ensure 'static' directory exists
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    # Convert to DataFrame before saving
    df = pd.DataFrame(results)
    df.to_csv(filename, index=False)
    print(f"✅ Sentiment analysis results saved to {filename}")

def visualize_sentiment(sentiment_results):
    """Generate and save pie chart and bar chart for sentiment analysis."""
    labels = list(sentiment_results.keys())
    sizes = list(sentiment_results.values())
    colors = ['#66b3ff', '#99ff99', '#ff9999']  # Blue, Green, Red
    explode = (0.1, 0.1, 0.1)  # Slightly separate each section

    # Ensure 'static' directory exists
    os.makedirs("static", exist_ok=True)

    # Save Pie Chart
    plt.figure(figsize=(6, 6))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors, explode=explode, startangle=140)
    plt.title("YouTube Comments Sentiment Analysis")
    pie_chart_path = "static/sentiment_pie_chart.png"
    plt.savefig(pie_chart_path)
    plt.close()

    # Save Bar Chart
    plt.figure(figsize=(6, 4))
    plt.bar(labels, sizes, color=colors)
    plt.xlabel("Sentiment")
    plt.ylabel("Number of Comments")
    plt.title("Sentiment Analysis - Bar Chart")
    bar_chart_path = "static/sentiment_bar_chart.png"
    plt.savefig(bar_chart_path)
    plt.close()

    return pie_chart_path, bar_chart_path  # Return both chart paths
