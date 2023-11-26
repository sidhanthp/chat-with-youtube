from openai import OpenAI
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from llm import create_chat_completion
import tiktoken
import os
from dotenv import load_dotenv
from youtube import get_transcript, get_video_metadata, extract_video_id
import streamlit as st

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)


def find_relevant_segments(
    question,
    transcript_with_timestamps,
    top_n=5,
    max_tokens=500,
    similarity_threshold=0.1,
):
    """
    Retrieves the top_n most relevant segments from the transcript for the question along with their timestamps,
    ensuring that each segment is less than max_tokens.
    """
    enc = tiktoken.encoding_for_model("gpt-4")

    new_transcript_with_timestamps = []
    current_segment = []
    current_segment_token_count = 0
    current_segment_start_time = None

    # Iterate over the transcript and split into sentences
    for segment, start_time in transcript_with_timestamps:
        # Tokenize the segment
        tokens = enc.encode(segment)
        token_count = len(tokens)

        # Check if adding this segment would exceed the max token count
        if current_segment_token_count + token_count > max_tokens:
            # Save the current segment and reset the accumulator
            new_transcript_with_timestamps.append(
                (" ".join(current_segment), current_segment_start_time)
            )
            current_segment = []
            current_segment_token_count = 0
            current_segment_start_time = None

        # If the accumulator is empty, set the start time to the current sentence's start time
        if current_segment_start_time is None:
            current_segment_start_time = start_time

        # Add the segment to the accumulator
        current_segment.append(segment)
        current_segment_token_count += token_count

    # Add the last accumulated segment if it's not empty
    if current_segment:
        new_transcript_with_timestamps.append(
            (" ".join(current_segment), current_segment_start_time)
        )

    segments, timestamps = zip(*new_transcript_with_timestamps)
    segments = list(segments)
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(segments + [question])
    cosine_similarities = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])

    # I've removed everything that is less than a certain similarity search, so we're not giving the model
    # context of unnecessary information. I've defaulted to .1 here after playing around with it a little,
    # to make sure we get paragraphs that still have a little information about the topic
    filtered_indices = [
        i
        for i, similarity in enumerate(cosine_similarities[0])
        if similarity > similarity_threshold
    ]

    # Sort the remaining segments by similarity
    top_indices = sorted(
        filtered_indices, key=lambda i: cosine_similarities[0][i], reverse=True
    )[:top_n]

    return [(segments[i], timestamps[i]) for i in top_indices]


def find_answer_in_transcript(question, transcript, video_metadata):
    if video_metadata is not None:
        video_metadata_string = f"This video is titled '{video_metadata['title']}' with description: {video_metadata['description']}."
    else:
        video_metadata_string = ""

    prompt = f"I am going to give you a transcript of a video. {video_metadata_string} Below that, I will include a question for that video. Respond directly to the question. Refer to the transcript below as a video, not as text. If the queation isn't answered by the transcript, let me know that the question is not answered in the video.\n\n {transcript}\n\nQuestion: {question}"

    answer = create_chat_completion(prompt)
    return answer


def summarize_segment(question, segment):
    """
    Uses OpenAI's GPT-4 to summarize the segment of the transcript relevant to the question.
    """
    summary_prompt = f"Summarize the following segment in the context of the question asked.\n\nSegment: {segment}\n\nQuestion: {question}"

    summary = create_chat_completion(summary_prompt)
    return summary


def generate_summary(video_id):
    # Initialize the 'summary' key in session state if it doesn't exist
    if "summary" not in st.session_state:
        st.session_state.summary = {}

    # Check if the summary is already in the session state
    if video_id in st.session_state.summary:
        return st.session_state.summary[video_id]

    # If not, generate the summary
    transcript_with_timestamps = get_transcript(video_id)
    if transcript_with_timestamps is None:
        st.error("Unable to retrieve transcript.")
        return None

    summary_prompt = f"Please summarize the following video. Here is the transcript: {transcript_with_timestamps}"
    summary = create_chat_completion(summary_prompt)

    # Store the summary in the session state
    st.session_state.summary[video_id] = summary

    return summary
