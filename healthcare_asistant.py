import streamlit as st
import requests
import threading
from fastapi import FastAPI
import uvicorn
from langchain_core.prompts import ChatPromptTemplate
from langserve import add_routes
from langchain_groq import ChatGroq

# API key and LLM setup
api_key = "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"

llm = ChatGroq(
    model="llama-3.1-70b-versatile",
    temperature=1,
    groq_api_key=api_key
)

app = FastAPI(
    title="Simple Server",
    version='1.0',
    description="My first API server"
)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant. Please respond to the user queries."),
        ("user", "Question:{question}")
    ]
)

add_routes(
    app,
    prompt | llm,
    path="/prompt"
)

# Function to run the FastAPI server in a thread
def run_fastapi():
    uvicorn.run(app, host='0.0.0.0', port=8000)

# Start the FastAPI server in a separate thread
threading.Thread(target=run_fastapi, daemon=True).start()

# Streamlit app
st.title('Speech Therapy Assistant')

# Create a text input widget for the user to enter a prompt
text_input = st.text_input('Share your problem')

# Define a function to get a response from the Llama model
def get_llama_response(input_text):
    try:
        # Send a POST request to the FastAPI server
        response = requests.post(
            "http://localhost:8000/prompt",  # Adjusted path to match the FastAPI route
            json={'input': {'question': input_text}}
        )
        response.raise_for_status()  # Raise an error for bad responses
        return response.json().get('output', 'No response available')  # Safely get the output
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"

# If the user has entered text, get and display the response
if text_input:
    response = get_llama_response(text_input)  # Pass the actual variable
    st.write(response)
