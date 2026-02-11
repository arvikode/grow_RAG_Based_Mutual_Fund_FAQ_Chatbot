"""
Streamlit app entry point for Streamlit Cloud deployment.
This file must be in the root directory as streamlit_app.py.
"""
import sys
import os

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import the main app module
import app

import streamlit as st

# Streamlit will automatically run the app.py module
# Setup environment from Streamlit secrets if available
try:
    if "GEMINI_API_KEY" in st.secrets:
        os.environ["GEMINI_API_KEY"] = st.secrets["GEMINI_API_KEY"]
    if "GEMINI_MODEL" in st.secrets:
        os.environ["GEMINI_MODEL"] = st.secrets["GEMINI_MODEL"]
except Exception:
    pass # Secrets not available or not configured

# However, we need to call the main function explicitly
if __name__ == "__main__":
    app.main()
