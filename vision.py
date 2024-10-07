import os
import streamlit as st
import google.generativeai as genai
from PIL import Image
from dotenv import load_dotenv
load_dotenv()


genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))


# model = genai.GenerativeModel("gemini-pro-vision")
model = genai.GenerativeModel("gemini-1.5-flash")


def get_gemini_response(input, image):

    if input:
        response = model.generate_content([input, image])
    else:
        response = model.generate_content(image)
    return response.text


st.set_page_config(page_title="Gemini Image Demo")

st.header("Gemini Application")
input = st.text_input("Input Prompt:", key="input")

uploaded_file = st.file_uploader(
                    "Choose an image...",
                    type=["jpg", "jpeg", "png"]
                )
image = ""
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="uploaded Image", use_column_width=True)


submit = st.button("Tell me about the image")


if submit:
    response = get_gemini_response(input, image)
    st.subheader("the Response is")
    st.write(response)
