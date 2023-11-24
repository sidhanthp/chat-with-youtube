import streamlit as st

from youtube import get_transcript, extract_video_id
from search_video import (
    find_answer_in_transcript,
    find_relevant_segments,
    summarize_segment,
)

from llm import create_chat_completion

st.title("YouTube Q&A Chatbot")
url = st.text_input("Enter the YouTube URL:")

# Video Summary
if url:
    video_id = extract_video_id(url)
    transcript_with_timestamps = get_transcript(video_id)
    st.video(f"https://www.youtube.com/watch?v={video_id}")

    summary_prompt = f"Please summarize the following video. Here is the transcript: {transcript_with_timestamps}"
    summary_completion = create_chat_completion(summary_prompt)

    video_summary = summary_completion.choices[0].message.content.strip()

    st.subheader("Video Summary")
    st.write(video_summary)


question = st.text_input("Ask your question:")

# Question Answer
if question:
    answer = find_answer_in_transcript(question, transcript_with_timestamps)
    st.write(answer)  # Display the answer


# Source of Data to Answer Question
if question:
    relevant_segments_with_timestamps = find_relevant_segments(
        question, transcript_with_timestamps
    )

    st.write("Data used to Answer Question")
    for segment, timestamp in relevant_segments_with_timestamps:
        # Summarize the segment in the context of the question
        summary = summarize_segment(question, segment)

        # Convert timestamp to a format suitable for a YouTube URL (e.g., "1h2m3s")
        formatted_timestamp = f"{int(timestamp // 3600)}h{int((timestamp % 3600) // 60)}m{int(timestamp % 60)}s"

        # Create a clickable link to the timestamp in the video
        st.markdown(
            f"[Jump to {formatted_timestamp}](https://www.youtube.com/watch?v={video_id}&t={formatted_timestamp})"
        )
        # Display the summary instead of the full segment
        st.write(summary)
