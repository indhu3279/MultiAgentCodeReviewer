import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

# Load local environment variables (development)
load_dotenv(".gitignore/.env")

def get_llm():
    """
    Get LLM instance with API key from:
    1. Streamlit secrets (Streamlit Cloud)
    2. Environment variables (local development)
    3. .env file (local development)
    """
    api_key = None
    
    # Try Streamlit secrets first
    try:
        import streamlit as st
        if "GROQ_API_KEY" in st.secrets:
            api_key = st.secrets["GROQ_API_KEY"]
    except (ImportError, AttributeError, KeyError):
        pass
    
    # Fall back to environment variable
    if not api_key:
        api_key = os.getenv("GROQ_API_KEY")
    
    if not api_key:
        raise RuntimeError(
            "GROQ_API_KEY is not set. Please:\n"
            "- Local development: Add GROQ_API_KEY to .env or .streamlit/secrets.toml\n"
            "- Streamlit Cloud: Go to 'Manage app' > 'Secrets' and add GROQ_API_KEY"
        )

    return ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0,
        groq_api_key=api_key
    )
