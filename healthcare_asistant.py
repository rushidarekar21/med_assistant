import streamlit as st
import requests

# Set the title of the Streamlit app
st.title('Speech Therapy asistant')

# Create a text input widget for the user to enter a prompt
text_input = st.text_input('Share your problem')

# Define a function to get a response from the Llama model
def get_llama_response(input_text):
    try:
        # Send a POST request to the FastAPI server
        response = requests.post(
            "http://localhost:8000/prompt/invoke",
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