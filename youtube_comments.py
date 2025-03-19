import sys
sys.stdout.reconfigure(encoding='utf-8')

from googleapiclient.discovery import build

API_KEY = ''  # Replace with a valid YouTube Data API key
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

def get_comments(video_id):
    """Fetch comments from a YouTube video."""
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=API_KEY)
    comments = []

    try:
        print("\n🔄 Fetching comments...")

        response = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=100
        ).execute()

        for item in response.get("items", []):  # Use .get() to avoid KeyError
            comment = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
            comments.append(comment)

    except Exception as e:
        print("\n❌ Error fetching comments:", e)

    return comments  # ✅ Now it can be used in another file

# ✅ Only run this when executing this file directly
if __name__ == "__main__":
    video_id = input("Enter YouTube Video ID: ")
    comments = get_comments(video_id)
    print("Fetched Comments:", comments)
