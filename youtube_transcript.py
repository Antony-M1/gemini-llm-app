"""
README
End To End Youtube Video Transcribe Summarizer LLM App With Google Gemini Pro
"""
import os
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
from youtube_transcript_api import YouTubeTranscriptApi 

load_dotenv()


genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

prompt = """You are youtube summarizer . You will be taking the transcript
text and summarize the entire video and produce the important summaries in points
with in 250 words

### Here the transcript text

"""


def generate_gemini_content(transcript_text: str, prompt: str) -> str:
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt + transcript_text)
    return response.text


def extract_transcript_details(youtube_video_url: str) -> str:
    """
    Example video url
    https://www.youtube.com/watch?v=k2P_pHQDlp0
    """
    try:
        video_id = youtube_video_url.split("=")[1]
        trascript_text = YouTubeTranscriptApi.get_transcript(video_id)
        text = " ".join([ts["text"] for ts in trascript_text])
        return text
    except Exception as e:
        raise e


st.title("Youtube Transcript to Detailed notes converter")
youtube_link = st.text_input("Enter youtube video link")

if youtube_link:
    video_id = youtube_link.split("=")[1]
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)


if st.button("Get Detailed Notes"):
    transcript_text = extract_transcript_details(youtube_link)

    if transcript_text:
        summary = generate_gemini_content(transcript_text, prompt)
        st.markdown("## Detailed Notes:")
        st.write(summary)
