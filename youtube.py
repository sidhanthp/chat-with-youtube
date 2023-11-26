from youtube_transcript_api import YouTubeTranscriptApi
import urllib.parse as urlparse

from pytube import YouTube
import streamlit as st


def extract_video_id(url):
    url_data = urlparse.urlparse(url)
    query = urlparse.parse_qs(url_data.query)
    video_id = query["v"][0]
    return video_id


def get_video_metadata(url):
    """
    Fetches and returns the metadata of a YouTube video using pytube.
    """
    try:
        yt = YouTube(url)

        # This is absolutely insane that the `description` is broken
        # This GH issue had a fix: https://github.com/pytube/pytube/issues/1626, but it randomly threw an exception
        # So I stuck with the broken description...
        video_metadata = {
            "title": yt.title,
            "description": yt.description,
            "author": yt.author,
            "publish_date": yt.publish_date,
        }

        return video_metadata
    except Exception as e:
        print(f"An error occurred when trying to fetch the video metadata: {e}")
        return None


def get_transcript(video_id):
    """
    Fetches and returns the transcript of a YouTube video along with timestamps.
    If the transcript is already stored in Streamlit's session state, it returns it directly.
    """
    # Check if the transcript is already in the session state
    if "transcript" in st.session_state and st.session_state.transcript.get(video_id):
        return st.session_state.transcript[video_id]

    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        transcript_with_timestamps = []
        for item in transcript_list:
            segment = item["text"]
            start_time = item["start"]  # Timestamp in seconds
            transcript_with_timestamps.append((segment, start_time))

        # Store the transcript in Streamlit's session state under the video_id key
        if "transcript" not in st.session_state:
            st.session_state.transcript = {}
        st.session_state.transcript[video_id] = transcript_with_timestamps

        return transcript_with_timestamps
    except Exception as e:
        print(f"An error occurred when trying to fetch the transcript: {e}")
        return None
