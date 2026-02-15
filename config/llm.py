import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

# Load local environment variables (development)
load_dotenv()

# Cache for LLM instance
_llm_cache = None

def get_llm():
    """
    Get LLM instance with API key from:
    1. Streamlit secrets (Streamlit Cloud) - checked at runtime
    2. Environment variables (local development)
    3. .env file (local development)
    """
    global _llm_cache
    
    # Return cached instance if available
    if _llm_cache is not None:
        return _llm_cache
    
    api_key = None
    
    # Try Streamlit secrets first (checked at runtime to support Streamlit Cloud)
    try:
        import streamlit as st
        if hasattr(st, 'secrets') and "GROQ_API_KEY" in st.secrets:
            api_key = st.secrets["GROQ_API_KEY"]
    except (ImportError, AttributeError, KeyError, Exception):
        pass
    
    # Fall back to environment variable
    if not api_key:
        api_key = os.getenv("GROQ_API_KEY")
    
    if not api_key:
        raise RuntimeError(
            "GROQ_API_KEY is not set. Please:\n"
            "- Local development: Add GROQ_API_KEY to .env or .streamlit/secrets.toml\n"
            "- Streamlit Cloud: Go to 'Manage app' > 'Secrets' and add GROQ_API_KEY\n"
            "Visit: https://console.groq.com/keys to get your API key"
        )

    _llm_cache = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0,
        groq_api_key=api_key
    )
    
    return _llm_cache
