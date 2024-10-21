"""
README
Modified End To End Resume ATS Tracking LLM Project With Google Gemini Pro.

The approach we are going to follow

PDF --> Text --> API --> Response

"""
import os
import streamlit as st
import google.generativeai as genai
import PyPDF2 as pdf
from dotenv import load_dotenv

load_dotenv()

LLM_MODEL = 'gemini-pro'

genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))


def get_gemini_response(input: str) -> str:
    model = genai.GenerativeModel(LLM_MODEL)
    response = model.generate_content(input)
    return response.text


def input_pdf_text(uploaded_file) -> str:
    """
    Process the PDF file into a text file
    """
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in range(len(reader.pages)):
        page = reader.pages[page]
        text += str(page.extract_text())
    return text


# Prompt Templae
input_prompt = """
Hey Act Like a skilled or very experience ATS(Application Tracking System)
with a deep understanding of tech field,software engineering,data science ,data analyst
and big data engineer. Your task is to evaluate the resume based on the given job description.
You must consider the job market is very competitive and you should provide 
best assistance for improving the resumes. Assign the percentage Matching based 
on Jd and
the missing keywords with high accuracy
resume:{text}
description:{jd}

I want the response in one single string having the structure
{{"JD Match":"%","MissingKeywords:[]","Profile Summary":""}}
"""


st.title("Smart ATS")
st.text("Improve your resume ATS")
jd = st.text_area("Paste the Job Description")
uploaded_file = st.file_uploader("Upload your resume", type="pdf", help="Please upload")

submit = st.button("Submit")

if submit:
    if uploaded_file is not None:
        text = input_pdf_text(uploaded_file)
        input_prompt = input_prompt.format(text=text, jd=jd)
        response = get_gemini_response(input_prompt)
        st.subheader(response)