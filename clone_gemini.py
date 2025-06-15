import os
import streamlit as st
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage

# Load environment variables
load_dotenv()

# Set page title
st.title("Gemini-powered Chatbot Clone")

# Set Gemini API key
GOOGLE_API_KEY = "AIzaSyCdc0WBthBoU6EZewU35wfkOPW-8IyjYgk"

# Initialize Gemini model
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",  # lightweight, fast Gemini model
    temperature=0.3,
    max_tokens=1024,
    google_api_key=GOOGLE_API_KEY,
)

# Initialize chat history if not already in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Get user input
if prompt := st.chat_input("What do you want to ask?"):
    # Show user message
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Generate response using Gemini
    try:
        response = llm.invoke([
            HumanMessage(content=prompt)
        ])
        reply = response.content

    except Exception as e:
        reply = f"Error: {str(e)}"

    # Show assistant message
    st.chat_message("assistant").markdown(reply)
    st.session_state.messages.append({"role": "assistant", "content": reply})
