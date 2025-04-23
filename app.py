from flask import Flask, render_template, request
import os
import matplotlib.pyplot as plt
import nltk
from textblob import TextBlob
import googleapiclient.discovery

app = Flask(__name__)

# Ensure static/images directory exists
os.makedirs("static/images", exist_ok=True)

# Replace with your actual YouTube Data API Key
YOUTUBE_API_KEY = 'AIzaSyCZKb09ksAG3ODCOb4VaeJAnHFzT1g9S4I'

# Function to fetch YouTube comments
def fetch_comments(video_id):
    try:
        youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
        request = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=20  # Adjust as needed
        )
        response = request.execute()

        comments = [item["snippet"]["topLevelComment"]["snippet"]["textDisplay"] for item in response.get("items", [])]
        return comments
    except Exception as e:
        print("Error fetching comments:", e)
        return []

# Function to perform sentiment analysis
def analyze_sentiments(comments):
    results = []
    sentiment_count = {"Positive": 0, "Negative": 0, "Neutral": 0}
    negative_comments = []

    for comment in comments:
        sentiment_score = TextBlob(comment).sentiment.polarity
        if sentiment_score > 0:
            sentiment = "Positive"
            sentiment_count["Positive"] += 1
        elif sentiment_score < 0:
            sentiment = "Negative"
            sentiment_count["Negative"] += 1
            negative_comments.append(comment)
        else:
            sentiment = "Neutral"
            sentiment_count["Neutral"] += 1

        results.append({"comment": comment, "sentiment": sentiment})

    return results, sentiment_count, negative_comments

# Function to generate pie chart
def generate_pie_chart(sentiment_count, video_id):
    labels = sentiment_count.keys()
    sizes = sentiment_count.values()
    colors = ["#66b3ff", "#99ff99", "#ff9999"]
    
    plt.figure(figsize=(5, 5))
    plt.pie(sizes, labels=labels, autopct="%1.1f%%", colors=colors, startangle=90)
    plt.title("Sentiment Distribution")

    pie_chart_path = f"static/images/pie_chart_{video_id}.png"
    plt.savefig(pie_chart_path)
    plt.close()
    
    return pie_chart_path

# Function to generate bar chart
def generate_bar_chart(sentiment_count, video_id):
    labels = list(sentiment_count.keys())
    values = list(sentiment_count.values())
    colors = ["#66b3ff", "#99ff99", "#ff9999"]

    plt.figure(figsize=(6, 4))
    plt.bar(labels, values, color=colors)
    plt.xlabel("Sentiment")
    plt.ylabel("Count")
    plt.title("Sentiment Analysis Results")

    bar_chart_path = f"static/images/bar_chart_{video_id}.png"
    plt.savefig(bar_chart_path)
    plt.close()
    
    return bar_chart_path

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    video_id = request.form.get("video_id")  # Get video ID from form

    if not video_id:
        return "Error: No Video ID provided", 400  # Return error if no input

    comments = fetch_comments(video_id)
    
    if not comments:
        return "Error: No comments found or API quota exceeded", 400

    sentiment_results, sentiment_count, negative_comments = analyze_sentiments(comments)

    # Generate and save charts
    pie_chart_path = generate_pie_chart(sentiment_count, video_id)
    bar_chart_path = generate_bar_chart(sentiment_count, video_id)

    return render_template(
        'result.html',
        results=sentiment_results,
        video_id=video_id,
        sentiment_results=sentiment_count,
        negative_comments=negative_comments,
        pie_chart_path=pie_chart_path,
        bar_chart_path=bar_chart_path
    )

if __name__ == '__main__':
    app.run(debug=True)
