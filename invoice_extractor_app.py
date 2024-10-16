"""
README
End to End Multi Language Invoice Extractor Project using Gemini Pro LLM Model

Note:
    1. Currently im using the `gemini-1.5-flash` model but in feature it will be depricated
    please ensure you are the right model for your project.
"""

import os
from dotenv import load_dotenv
import streamlit as st
from PIL import Image
import google.generativeai as genai

load_dotenv()

genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

model = genai.GenerativeModel("gemini-1.5-flash")  # Note: gemini-pro-vision is deprecated


def get_gemini_response(input, image, prompt):
    """
    Parameters:
        - `input`: Kind of system message and extra information.
        - `image`: Our image
        - `prompt`: What message I want to display
    """
    prompt = prompt + "\n" + input
    # response = model.generate_content(image=image, prompt=prompt)
    response = model.generate_content([input, image[0], prompt])
    return response.text


def input_image_details(uploaded_file):
    """
    Convert the uploaded file into bytes and return
    """
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No File Uploaded")


st.set_page_config(page_title="MultiLanguage Invoice Extractor")
st.header("MultiLanguage Invoice Extractor")
input = st.text_input("Input Prompt: ", key="input")
uploaded_file = st.file_uploader("Choose an image of invoice...", type=["jpg", "jpeg", "png"])
image = ""

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded image", use_column_width=True)

submit = st.button("Tell me about the invoice")

input_prompt = """
You are an expert in understanding invoices. we will upload a image as invoice
and you will have to answer any questions based on the uploaded invoice image
"""

if submit:
    image_data = input_image_details(uploaded_file)
    response = get_gemini_response(input_prompt, image_data, input)
    st.subheader("The Response is")
    st.write(response)
