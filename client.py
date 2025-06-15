import requests
import streamlit as st

def get_groq_response(input_text):
    json_body = {
        "language": "French",   # or make this dynamic
        "text": input_text     # use the text user entered
    }

    # Correct usage of requests.post with json= keyword argument
    response = requests.post("http://127.0.0.1:8000/translate", json=json_body)

    # Check if request was successful
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Request failed with status code {response.status_code}"}

# Streamlit app
st.title("LLM Application Using LCEL")

input_text = st.text_input("Enter the text you want to convert to French")

if input_text:
    result = get_groq_response(input_text)
    st.write(result)
