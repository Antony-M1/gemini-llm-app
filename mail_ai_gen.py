"""
Generate Better Response based on the mail content
"""

import os
from dotenv import load_dotenv
import streamlit as st
import google.generativeai as genai


load_dotenv(override=True)

genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

model = genai.GenerativeModel("gemini-1.5-flash")  # Note: gemini-pro-vision is deprecated


def get_gemini_response(prompt):
    response = model.generate_content(prompt)
    return response.text


def get_prompt(context, tone):
    prompt = """
    You are an AI email replier. You need to generate a polite and respectful response based on the context of the email provided. If the tone of the email is not specified, always generate a calm and positive reply. Your reply should avoid any negative language or offensive terms. If the email content is in HTML markdown, string, or any other format, extract the context and craft a thoughtful response. Please use a calm, positive, and professional tone when replying.

    ### Here is the mail context:
    {context}

    ### Here is the mail tone:
    {tone}
    """.format(context=context, tone=tone)
    return prompt


st.set_page_config(page_title="MailAIgen - Intelligent Email Replies Powered by AI")
st.header("Transform Emails into Instant Smart Replies with MailAIgen")

st.subheader("Provide Email Content")
mail_input = st.text_area("Mail content in String or HTML format: ", key="input")
st.subheader("Transform Email Tone")
st.markdown("""
            Here are some short, calm, and positive response options for rejecting an offer:
1. Grateful and Hopeful
2. Polite Decline
3. Respectful and Positive
4. Friendly and Hopeful
5. Clear and Appreciative""")

mail_tone_input = st.text_input("Provide the Sentiment like Generate in positive and calm")

submit_btn = st.button("Generate Response", type='primary')

if submit_btn:
    if mail_input and mail_tone_input:
        prompt = get_prompt(mail_input, mail_tone_input)
        response = get_gemini_response(prompt)
        st.write(response)
    else:
        st.error("Please provide the Mail Input & Tone")
