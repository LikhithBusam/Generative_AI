import streamlit as st
from dotenv import load_dotenv
import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser

# Load environment variables
load_dotenv()

# Retrieve the Gemini API key
api_key = os.getenv("GEMINI_API_KEY")

st.title('💬 LangChain Demo with Gemini')

# Check if API key exists
if not api_key:
    st.error("❌ GOOGLE_API_KEY not found in environment variables.")
else:
    try:
        # Initialize the LLM
        llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",  # Correct model name
            temperature=0.3,
            max_tokens=1024,
            google_api_key=api_key
        )

        # Define the prompt template
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a helpful chatbot."),
            ("human", "Question: {question}")
        ])

        # Create the output parser and chain
        output_parser = StrOutputParser()
        chain = prompt | llm | output_parser

        # Get user input
        input_text = st.text_input("Enter your question here")

        if input_text:
            with st.spinner("Generating response..."):
                response = chain.invoke({'question': input_text})
                st.success("✅ Response:")
                st.write(response)

    except Exception as e:
        st.error(f"⚠️ Error occurred: {e}")
