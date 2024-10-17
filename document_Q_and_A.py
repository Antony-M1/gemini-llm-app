"""
README

End To End Document Q&A Using Google Gemma,Groq API.

Note:
    1. I'm using the google "models/embedding-001" for a vector technique and FAISS for store and handle the vector data
    2. I'n this tutorial I'm using the GROQ Gemmma Model
    3. Ensure you have the GROQ_API_KEY in your .env file
"""
import os
import time
import streamlit as st
from langchain_groq import ChatGroq
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv

load_dotenv()


# Load the GROQ & Google API Key

# qroq_api_key = os.getenv("GROQ_API_KEY")
# google_api_key = os.getenv("Google_API_KEY")
llm_model_name = "gemma-7b-it"

st.title("Gemma Model Document Q&A")

llm = ChatGroq(model=llm_model_name)

prompt = ChatPromptTemplate.from_template("""
    Answer the questions based on the provided context only.
    Please provide the most accurate response based on the question
    <context>
    {context}
    <context>
    Questions:{input}

    """)


def vector_embedding():
    if "vectors" not in st.session_state:
        st.session_state.embeddings = GoogleGenerativeAIEmbeddings(model=os.getenv("EMBEDING_MODEL"))
        st.session_state.loader = PyPDFDirectoryLoader("./data/us_census")  # Data Ingestion
        st.session_state.docs = st.session_state.loader.load()  # Document Loading
        st.session_state.text_spliter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        st.session_state.final_documents = st.session_state.text_spliter.split_documents(st.session_state.docs)
        st.session_state.vectors = FAISS.from_documents(st.session_state.final_documents, st.session_state.embeddings)


prompt_1 = st.text_input("What you want ask from the documents")


if st.button("Creating Vectors Store"):
    vector_embedding()
    st.write("Vector DB is Ready")


if prompt_1:
    docuemnt_chain = create_stuff_documents_chain(llm, prompt)
    retriever = st.session_state.vectors.as_retriever()
    retrieval_chain = create_retrieval_chain(retriever, docuemnt_chain)

    start = time.process_time()
    response = retrieval_chain.invoke({'input': prompt_1})
    st.write(response['answer'])

    # With a streamlit expander
    with st.expander("Document Similarity Search"):
        # Find the relevant chunks
        for i, doc in enumerate(response['context']):
            st.write(doc.page_content)
            st.write("-------------------------------------")
