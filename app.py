import streamlit as st

from youtube import get_transcript, extract_video_id, get_video_metadata
from search_video import (
    find_answer_in_transcript,
    find_relevant_segments,
    summarize_segment,
    generate_summary,
)

st.title("YouTube Q&A Chatbot")
url = st.text_input("Enter the YouTube URL:")
question = None

# Video Summary
if url:
    video_id = extract_video_id(url)
    st.video(f"https://www.youtube.com/watch?v={video_id}")

    video_metadata = get_video_metadata(url)
    transcript_with_timestamps = get_transcript(video_id)
    video_summary = generate_summary(video_id)

    st.write("## Video Summary")
    st.write(video_summary)

    question = st.text_input("## Ask your question:", key=url)


if question:
    answer = find_answer_in_transcript(
        question, transcript_with_timestamps, video_metadata
    )
    st.write(answer)

    relevant_segments_with_timestamps = find_relevant_segments(
        question, transcript_with_timestamps
    )

    st.write("### Data Sources (beta)")
    
    for segment, timestamp in relevant_segments_with_timestamps:
        # Summarize the segment in the context of the question
        summary = summarize_segment(question, segment)

        # Convert timestamp to a format suitable for a YouTube URL (e.g., "1h2m3s")
        formatted_timestamp = f"{int(timestamp // 3600)}h{int((timestamp % 3600) // 60)}m{int(timestamp % 60)}s"

        # Create a clickable link to the timestamp in the video
        st.markdown(
            f"[Jump to {formatted_timestamp}](https://www.youtube.com/watch?v={video_id}&t={formatted_timestamp})"
        )
        st.write(summary)
