import os
import streamlit as st
from dotenv import load_dotenv

# Load local .env if present
load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

def get_secret(key_name, default=""):
    """
    Safely retrieves configuration secrets.
    First checks Streamlit Cloud Secrets (st.secrets), then falls back to OS Environment variables (.env).
    """
    try:
        if hasattr(st, "secrets") and key_name in st.secrets:
            val = st.secrets[key_name]
            if val:
                return str(val).strip()
    except Exception:
        pass
    
    env_val = os.getenv(key_name)
    if env_val:
        return env_val.strip()
        
    return str(default)

BUILTWITH_API_KEY = get_secret("BUILTWITH_API_KEY", "")
GTMETRIX_API_KEY = get_secret("GTMETRIX_API_KEY", "")
RATE_LIMIT_DELAY = int(get_secret("RATE_LIMIT_DELAY", 2))