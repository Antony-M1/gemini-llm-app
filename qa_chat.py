"""
README

This app is going to be Q&A Chat application it will store the history and show provide the better
responses based on the chat history
"""

import os
from dotenv import load_dotenv

import streamlit as st
import google.generativeai as genai

load_dotenv()

genai.configure(
    api_key=os.getenv('GOOGLE_API_KEY')
)

model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])


def get_gemini_response(question):
    response = chat.send_message(question, stream=True)
    return response


st.set_page_config(page_title="Q&A Chat")

if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

input = st.text_input("Input: ", key='input')
submit = st.button("Ask The Question")

if submit and input:
    response = get_gemini_response(input)
    st.session_state['chat_history'].append(("You", input))
    st.subheader("The response is")

    for chunk in response:
        st.write(chunk.text)
        st.session_state['chat_history'].append(("Bot", chunk.text))
st.subheader("To chat history is")


for role, text in st.session_state['chat_history']:
    st.write(f"{role}:{text}")
