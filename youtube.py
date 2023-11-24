from youtube_transcript_api import YouTubeTranscriptApi
import urllib.parse as urlparse


def extract_video_id(url):
    """
    Extracts the video ID ffrom a YouTube URL.
    """
    url_data = urlparse.urlparse(url)
    query = urlparse.parse_qs(url_data.query)
    video_id = query["v"][0]
    return video_id


def get_transcript(video_id):
    """
    Fetches and returns the transcript of a YouTube video along with timestamps.
    """
    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        transcript_with_timestamps = []
        for item in transcript_list:
            segment = item["text"]
            start_time = item["start"]  # Timestamp in seconds
            transcript_with_timestamps.append((segment, start_time))
        return transcript_with_timestamps
    except Exception as e:
        print(f"An error occurred when trying to fetch the transcript: {e}")
        return None
