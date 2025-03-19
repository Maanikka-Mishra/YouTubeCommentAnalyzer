from youtube_comments import get_comments  # Import comment fetching function
from sentiment import analyze_sentiment, visualize_sentiment, save_results_to_csv  # Import sentiment functions
import sys
sys.stdout.reconfigure(encoding='utf-8')  # Force UTF-8 encoding for print()
print("🎥 YouTube Comment Sentiment Analyzer 🎭")
video_id = input("\n🔹 Enter YouTube Video ID: ").strip()

if not video_id:
    print("\n⚠️ No Video ID provided. Exiting...")
else:
    comments = get_comments(video_id)

    if comments:
        sentiment_results, detailed_results = analyze_sentiment(comments)
        print("\n📊 Sentiment Analysis Results:", sentiment_results)

        # ✅ Save results to CSV
        save_results_to_csv(detailed_results)

        # ✅ Force Pie Chart to Display
        visualize_sentiment(sentiment_results)  # Ensure this runs after saving CSV
    else:
        print("\n⚠️ No comments available for analysis.")